import json
import uuid
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from io import BytesIO

from models import execute, fetchall, fetchone, databasePool
from models.products import get_product, has_product
from models.purchase_orders import update_purchase_order, get_purchase_order, has_purchase_order
from models.sql import select_data, build_where, build_column
from models.resources import get_resource_stream,create_resource
from utils import required, clean_dict
from models.resources import create_resource
from typing import List
import logging,ast,tempfile,shutil,zipfile,os


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s', handlers=[logging.StreamHandler()])


INVOICE_FIELDS = ["id", "data"]
JSON = "data"


def create_purchase_invoice(purchase_invoice):
    """ Create purchase invoice based on the given data

    :param purchase_invoice: {
        id: purchase invoice id
        attribute: value
        orders: [
            id: order id
            items: [
                product_id: product id
                product_cost: product cost
                received_quantity: received quantity
                attribute: value
            ]
        ]
    }
    :return: {
        id: purchase invoice id
        attribute: value
        orders: [
            id: order id
            items: [
                product_id: product id
                product_cost: product cost
                product_name: product name
                received_quantity: received quantity
                attribute: value
            ]
        ]
    }
    """
    if "id" in purchase_invoice and has_purchase_invoice(purchase_invoice["id"]):
        raise Exception("Purchase invoice '{}' already exists".format(purchase_invoice["id"]))
    if "orders" in purchase_invoice:
        if not isinstance(purchase_invoice["order"], list):
            raise Exception("Purchase invoice orders must be a list")
        for invoice_order in purchase_invoice["order"]:
            if "id" not in invoice_order:
                raise Exception("Purchase invoice order must have an 'id'")
            if not has_purchase_order(invoice_order["id"]):
                raise Exception("Purchase order {} not found".format(invoice_order["id"]))
            if "items" in invoice_order:
                if not isinstance(invoice_order["items"], list):
                    raise Exception("Purchase invoice order items must be a list")
                for item in invoice_order["items"]:
                    if "product_id" not in item:
                        raise Exception("Purchase invoice order item must have a 'product_id'")
                    if not has_product(item["product_id"]):
                        raise Exception("Product {} not found".format(item["product_id"]))

    purchase_invoice_copy = purchase_invoice.copy()
    if "id" not in purchase_invoice_copy:
        purchase_invoice_copy["id"] = uuid.uuid4().hex
    _add_product_attributes(purchase_invoice_copy)
    _calculate_totals(purchase_invoice_copy)
    purchase_orders = _get_related_purchase_orders(purchase_invoice_copy)
    purchase_orders = _update_purchase_orders(purchase_orders, purchase_invoice_copy)
    file_id = send_excel_to_resource(purchase_invoice_copy)
    purchase_invoice_copy["importation_files"] = file_id
    zip_id = generate_all_files(purchase_invoice_copy)
    purchase_invoice_copy["invoice_files"] = zip_id
    purchase_invoice_id = purchase_invoice_copy.pop("id")
    connection = databasePool.get_connection()
    try:
        execute(f"insert into watchtime.purchase_invoices (id, data) values (%s, %s)", purchase_invoice_id, json.dumps(purchase_invoice_copy))
        for purchase_order in purchase_orders:
                  update_purchase_order(purchase_order, connection=connection)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        databasePool.put_connection(connection)
    
    return {"id": purchase_invoice_id, **purchase_invoice_copy}


def update_purchase_invoice(purchase_invoice):
    """ Update purchase invoice based on the given data

    :param purchase_invoice: {
        id: purchase invoice id
        attribute: value
        orders: [
            id: order id
            items: [
                product_id: product id
                product_cost: product cost
                received_quantity: received quantity
                attribute: value
            ]
        ]
    }
    :return: {
        id: purchase invoice id
        attribute: value
        orders: [
            id: order id
            items: [
                product_id: product id
                product_cost: product cost
                product_name: product name
                received_quantity: received quantity
                attribute: value
            ]
        ]
    }
    """
    required(purchase_invoice, ["id"])
    if "orders" in purchase_invoice:
        if not isinstance(purchase_invoice["order"], list):
            raise Exception("Purchase invoice orders must be a list")
        for invoice_order in purchase_invoice["order"]:
            if "id" not in invoice_order:
                raise Exception("Purchase invoice order must have an 'id'")
            if not has_purchase_order(invoice_order["id"]):
                raise Exception("Purchase order {} not found".format(invoice_order["id"]))
            if "items" in invoice_order:
                if not isinstance(invoice_order["items"], list):
                    raise Exception("Purchase invoice order items must be a list")
                for item in invoice_order["items"]:
                    if "product_id" not in item:
                        raise Exception("Purchase invoice order item must have an 'product_id'")
                    if not has_product(item["product_id"]):
                        raise Exception("Product {} not found".format(item["product_id"]))
                    

    stored_purchase_invoice = get_purchase_invoice(purchase_invoice["id"])
    if not stored_purchase_invoice:
        raise Exception("Purchase invoice not found")
    purchase_orders = _get_related_purchase_orders(stored_purchase_invoice)
    
    
    stored_purchase_invoice.update(purchase_invoice)
    clean_dict(stored_purchase_invoice)
    _add_product_attributes(stored_purchase_invoice)
    _calculate_totals(stored_purchase_invoice)
    purchase_orders = _update_purchase_orders(purchase_orders, stored_purchase_invoice)
    zip_id = generate_all_files(stored_purchase_invoice)
    stored_purchase_invoice["invoice_files"] = zip_id
    purchase_invoice_id = stored_purchase_invoice.pop("id")
    connection = databasePool.get_connection()
    
    
    try:
        execute(f"update watchtime.purchase_invoices set data = %s where id=%s", json.dumps(stored_purchase_invoice), purchase_invoice_id, connection=connection)
        for purchase_order in purchase_orders:
            update_purchase_order(purchase_order, connection=connection)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        databasePool.put_connection(connection)

    

    return {"id": purchase_invoice_id, **stored_purchase_invoice}


def delete_purchase_invoice(purchase_invoice_id):
    """ Delete purchase invoice based on the given purchase_invoice_id

    :param purchase_invoice_id:
    :return: None
    """
    stored_purchase_invoice = get_purchase_invoice(purchase_invoice_id)
    if stored_purchase_invoice:
        purchase_orders = _get_related_purchase_orders(stored_purchase_invoice)
        stored_purchase_invoice["order"] = list()
        purchase_orders = _update_purchase_orders(purchase_orders, stored_purchase_invoice)

        connection = databasePool.get_connection()
        try:
            for purchase_order in purchase_orders:
                update_purchase_order(purchase_order, connection=connection)
            execute(f"delete from watchtime.purchase_invoices where id=%s", purchase_invoice_id, connection=connection)
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            databasePool.put_connection(connection)


def has_purchase_invoice(purchase_invoice_id):
    """ Return True if purchase invoice exists

    :param purchase_invoice_id:
    :return: bool
    """
    return fetchone(f"select count(*) from watchtime.purchase_invoices where id=%s", purchase_invoice_id)[0] == 1


def get_purchase_invoices_summary(column, filters=None):
    """ Get a purchase invoices summary by the given column and filters

    :param column: column name
    :param filters: dict of filters and order
    :return: { <column>: number of purchase orders }
    """
    field = build_column(column, INVOICE_FIELDS)
    where = build_where(INVOICE_FIELDS, filters if filters else dict())
    sql = "select {}, count(*) from watchtime.purchase_invoices {} group by {}".format(field, where, field)
    return {row[0] if row[0] else "-": row[1] for row in fetchall(sql)}


def get_purchase_invoices(filters=None):
    """ Get all purchase invoices based on the given filters

    :param filters: dict of filters and order
    :return: {
        data: [
            {
                id: purchase order id
                attribute: value
            }
        ],
        rows: total number of rows
    """
    return select_data("watchtime.purchase_invoices", INVOICE_FIELDS, JSON, filters)


def get_purchase_invoice(purchase_invoice_id):
    """ Get purchase invoice base on the given purchase invoice id

    :param purchase_invoice_id:
    :return: {
        id: purchase order id
        attribute: value
    }
    """
    row = fetchone(f"select id, data from watchtime.purchase_invoices where id=%s", purchase_invoice_id)
    if not row:
        return None

 
    return {"id": row[0], **row[1]}

def get_purchase_invoice_items(purchase_invoice_id):
    products = []
    row = fetchone(f"select data from watchtime.purchase_invoices where id=%s", purchase_invoice_id)
    orders = row[0]["order"]
    for order in orders:
        items = order["items"]
        
        for item in items:
            products.append({
    "product_code": item["product_code"],
    "received_quantity": item["received_quantity"],
    "cost": item.get("product_cost", 0), 
    "os": item.get("os", '')
})

    

    return products

def _add_product_attributes(purchase_invoice):
    for order in purchase_invoice.get("order", []):
        for item in order.get("items", []):
            product = get_product(item["product_id"])
            if product and "name" in product:
                item["product_name"] = product["name"]
            if purchase_invoice["status"] == 'received':
                item["received_quantity"] = item.get("received_quantity",0) + item["invoiced_quantity"]
            if purchase_invoice["status"] == 'cancelled':
                item["received_quantity"] = item.get("received_quantity",0) - item.get("invoiced_quantity",0)
                item["receiving_quantity"] = item.get("receiving_quantity",0) - item.get("invoiced_quantity",0)
                item["invoiced_quantity"] = item.get("invoiced_quantity",0) - item.get("invoiced_quantity",0)
            if purchase_invoice["status"] == 'receiving':
                item["receiving_quantity"] = item.get("receiving_quantity",0) + item["invoiced_quantity"]
def _calculate_totals(purchase_invoice):
    purchase_invoice["total_orders"] = len(purchase_invoice.get("order", []))
    purchase_invoice["total_quantity"] = sum([item.get("invoiced_quantity", 0) for order in purchase_invoice.get("order", []) for item in order.get("items", [])])
    purchase_invoice["total_cost"] = sum([item.get("product_cost", 0) * item.get("invoiced_quantity", 0) for order in purchase_invoice.get("order", []) for item in order.get("items", [])])


def _get_related_purchase_orders(purchase_invoice):
    purchase_orders = list()
    for order_id in [order["id"] for order in purchase_invoice.get("order", [])]:
        purchase_orders.append(get_purchase_order(order_id))
    return purchase_orders


def _update_purchase_orders(purchase_orders, purchase_invoice):
    for purchase_order in purchase_orders:
        
        if purchase_invoice["status"] == 'cancelled':
                if purchase_order.get("received_quantity",0) >0:
                    purchase_order["received_quantity"] = purchase_order.get("received_quantity",0) - purchase_invoice.get("total_quantity",0)
                if purchase_order.get("receiving_quantity",0) >0:
                    purchase_order["receiving_quantity"] = purchase_order.get("receiving_quantity",0) - purchase_invoice.get("total_quantity",0)
                purchase_order["invoiced_quantity"] = purchase_order.get("invoiced_quantity",0) - purchase_invoice.get("total_quantity",0)
        if purchase_invoice["status"] == 'requested':
                purchase_order["invoiced_quantity"] = purchase_order.get("invoiced_quantity",0) + purchase_invoice.get("total_quantity",0)  
        if purchase_invoice["status"] == 'received':
                purchase_order["received_quantity"] = purchase_order.get("received_quantity",0) + purchase_invoice.get("total_quantity",0)   
        if purchase_invoice["status"] == 'receiving':
                purchase_order["receiving_quantity"] = purchase_order.get("receiving_quantity",0) + purchase_invoice.get("total_quantity",0) 

        for purchase_order_item in purchase_order.get("items", []):
            purchase_order_item["invoices"] = [invoice for invoice in purchase_order_item.get("invoices", [])]
            for invoice_order in purchase_invoice.get("order", []):
                if invoice_order["id"] == purchase_order["id"]:
                    for invoice_order_item in invoice_order.get("items", []):
                        if invoice_order_item["product_id"] == purchase_order_item["product_id"]:
                            
                            if purchase_invoice["status"] == 'cancelled':
                                purchase_order_item["invoiced_quantity"] =- invoice_order_item["invoiced_quantity"]
                            
                            if purchase_invoice["status"] == 'requested':
                                purchase_order_item["invoices"].append({"id":purchase_invoice["id"],"invoiced_quantity": invoice_order_item["invoiced_quantity"]}) 
                            
                            else:
                                for invoice in purchase_order_item["invoices"]:
                                    if invoice["id"] == purchase_invoice["id"]:

                                        if purchase_invoice["status"] == 'cancelled':
                                            
                                            if invoice.get("receiving_quantity",0) > 0:
                                                invoice["receiving_quantity"] = invoice.get("receiving_quantity",0) - invoice["invoiced_quantity"]
                                            if invoice.get("received_quantity",0) > 0:
                                                invoice["received_quantity"] = invoice.get("received_quantity",0) - invoice["invoiced_quantity"]
                                            invoice["invoiced_quantity"] = invoice.get("invoiced_quantity",0) - invoice["invoiced_quantity"]
                                            
                                        if purchase_invoice["status"] == 'receiving':
                                            invoice["receiving_quantity"] = invoice["invoiced_quantity"]
                                        elif purchase_invoice["status"] == 'received':
                                            invoice["received_quantity"] = invoice["invoiced_quantity"]
    
    return purchase_orders



def generate_excel_file(purchase_invoice):
    orders = purchase_invoice["order"]
    products = []
    for order in orders:
        items = order["items"]
        for item in items:
            if item["status"] == "active":
                products.append({
    "product_code": item["product_code"],
    "invoiced_quantity": item["invoiced_quantity"],
    "cost": item.get("product_cost", 0), 
    "os": item.get("os", '')})
    
    df = pd.DataFrame(products)

    # Criar um arquivo Excel e escrever os dados do DataFrame em uma planilha
    wb = Workbook()
    ws = wb.active
    df_subset = df[['product_code', 'invoiced_quantity','cost','os']]
    col_names = ['Reference', 'Invoice Qty','Unit Price','Obs']

    # Adicionar os cabeçalhos personalizados
    ws.append(col_names)
    for r in dataframe_to_rows(df_subset, index=False, header=False):
        ws.append(r)
    id =purchase_invoice["id"]
    # Salvar o arquivo Excel em um diretório especificado
    filename = f"/app/excel_files/{id}.xlsx"
    wb.save(filename)


def send_excel_to_resource(purchase_invoice):
    # Gerar o arquivo Excel
    purchase_invoice_id = purchase_invoice["id"]
    generate_excel_file(purchase_invoice)

    # Ler o arquivo Excel gerado
    filename = f"/app/excel_files/{purchase_invoice_id}.xlsx"
    with open(filename, "rb") as f:
        wb_bytes = BytesIO(f.read())

    # Criar o objeto resource com o arquivo Excel como stream
    resource = {
        "name":"Arquivos para importacao.xlsx",
        "purchase_invoice": purchase_invoice_id,
        "content_type": "application/vnd.ms-excel",
        "type": "excel"
    }
    id = create_resource(resource, stream=wb_bytes)
    return id["id"]

def has_excel_file(purchase_invoice_id):

    row = fetchone(f"select id,data from watchtime.resources where data->>'purchase_invoice' = '"+ purchase_invoice_id+"'", purchase_invoice_id, connection= None)

    if not row:
        return False
    return row[0]

def generate_all_files(purchase_invoice):
    resources_id = list()
    purchase_orders = list()
    
    
    resources_id.append(purchase_invoice.get("awb_file_id",[]))
    resources_id.append(purchase_invoice.get("invoice_file_id",[]))
    resources_id.append(purchase_invoice.get("importation_files",[]))
    resources_id.append(purchase_invoice.get("nota_fiscal_file_id",''))
    resources_id.append(purchase_invoice.get("fatura_file_id",''))
    for order_id in [order["id"] for order in purchase_invoice.get("order", [])]:
        purchase_orders.append(get_purchase_order(order_id))

    for purchase_order in purchase_orders:
        resources_id.append(purchase_order.get("proforma_url",''))
        resources_id.append(purchase_order.get("cambio_url",''))
    resources = get_resources_by_ids(resources_id)
    dir = baixar_arquivos(resources)
    zip = criar_zip(dir)
    zip_id = enviar_zip(zip)
    limpar_temp_dir(dir)

    return zip_id["id"]



def get_resources_by_ids(ids: List[str]) -> List[dict]:
    id_placeholders = ', '.join(['%s'] * len(ids))
    sql = f"SELECT id, data FROM watchtime.resources WHERE id IN ({id_placeholders})"
    rows = fetchall(sql, *ids)
    
    resources = []
    for row in rows:
        resource = {"id": row[0], **row[1]}
        resources.append(resource)

    return resources

# Baixar e armazenar arquivos temporariamente
def baixar_arquivos(recursos):
    temp_dir = tempfile.mkdtemp()
    for recurso in recursos:
        resource_id = recurso['id']
        nome = recurso.get('name', f"{resource_id}.bin")
        arquivo = get_resource_stream(resource_id)
        if arquivo:  # Certifique-se de que o arquivo existe
            file_path = os.path.join(temp_dir, nome)
            with open(file_path, "wb") as f:
                f.write(arquivo)
    return temp_dir

# Criar um arquivo ZIP
def criar_zip(temp_dir):
    zip_path = os.path.join(temp_dir, "arquivos.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file != "arquivos.zip":
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, temp_dir))
    return zip_path

# Enviar o arquivo ZIP como um novo recurso
def enviar_zip(zip_path):
    with open(zip_path, "rb") as f:
        arquivo_zip = f.read()
        stream = BytesIO(arquivo_zip)
    resource = {
        "nome": "arquivos.zip",
        "tipo": "zip",  # você pode ajustar o tipo de recurso conforme necessário
    }
    return create_resource(resource, stream=stream)
# Limpar os arquivos temporários
def limpar_temp_dir(temp_dir):
    shutil.rmtree(temp_dir)
