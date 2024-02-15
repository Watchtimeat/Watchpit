import json
import uuid
import pandas as pd
import os
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from io import BytesIO
from models.products import get_product
from models.resources import create_resource
from datetime import datetime
import pytz

from models import execute, fetchall, fetchone, databasePool
from models.sql import select_data, build_where, build_column
from utils import required, clean_dict
import logging


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s', handlers=[logging.StreamHandler()])
ORDERS_FIELDS = ["id", "data"]
ORDER_ITEMS_FIELDS = ["id", "purchase_order_id", "data"]
JSON = "data"


def create_purchase_order(purchase_order, connection=None):
    """ Create purchase order based on the given data

    :param purchase_order: {
        id: purchase order id (optional)
        attribute: value
        items: [
            id: purchase order item
            attribute: value
        ]
    }
    :param connection: connection for transation management (optional)
    :return: {
        id: purchase order id
        attribute: value
        items: [
            id: purchase order item
            attribute: value
        ]
    }
    """
    if not isinstance(purchase_order["items"], list):
        raise Exception("Purchase order items must be a list")
    if "id" not in purchase_order:
        purchase_order["id"] = uuid.uuid4().hex
    if has_purchase_order(purchase_order["id"]):
        raise Exception("Purchase order '{}' already exists".format(purchase_order["id"]))

    purchase_order_copy = purchase_order.copy()
    _calculate_totals(purchase_order_copy)
    purchase_order_id = purchase_order_copy.pop("id")
    purchase_order_items = purchase_order_copy.pop("items")

    execute(f"insert into watchtime.purchase_orders (id, data) values (%s, %s)", purchase_order_id, json.dumps(purchase_order_copy), connection=connection)
    for item in purchase_order_items:
        if "id" not in item:
            item["id"] = uuid.uuid4().hex
        item_id = item.pop("id")
        execute(f"insert into watchtime.purchase_order_items (id, purchase_order_id, data) values (%s, %s, %s)", item_id, purchase_order_id, json.dumps(item), connection=connection)
    return {"id": purchase_order_id, "items": purchase_order_items, **purchase_order}


def update_purchase_order(purchase_order, connection=None):
    """ Update purchase order based on the given data

    :param purchase_order: {
        id: purchase order id
        attribute: value
        items: [
            id: purchase order item
            attribute: value
        ]
    }
    :param connection: connection for transation management (optional)
    :return: {
        id: purchase order id
        attribute: value
        items: [
            id: purchase order item
            attribute: value
        ]
    }
    """
    required(purchase_order, ["id"])
    if "items" in purchase_order and not isinstance(purchase_order["items"], list):
        raise Exception("Purchase orders items must be a list")

    stored_purchase_order = get_purchase_order(purchase_order["id"], connection=connection)
    if not stored_purchase_order:
        raise Exception("Purchase order not found")

    stored_purchase_order.update(purchase_order)
    clean_dict(stored_purchase_order)
    _calculate_totals(stored_purchase_order)
    purchase_order_id = stored_purchase_order.pop("id")
    stored_purchase_order_items = stored_purchase_order.pop("items") if "items" in stored_purchase_order else list()

    if stored_purchase_order["status"] == 'draft':
        if stored_purchase_order.get('excel_url','N') != 'N':
            del stored_purchase_order['excel_url']
        execute(f"delete from watchtime.resources where data->>'purchase_order' = '"+ purchase_order_id+"'")

    execute(f"update watchtime.purchase_orders set data = %s where id=%s", json.dumps(stored_purchase_order), purchase_order_id, connection=connection)
    execute(f"delete from watchtime.purchase_order_items where purchase_order_id=%s", purchase_order_id, connection=connection)
    for item in stored_purchase_order_items:
        if "id" not in item:
            item["id"] = uuid.uuid4().hex
        item_id = item.pop("id")
        execute(f"insert into watchtime.purchase_order_items (id, purchase_order_id, data) values (%s, %s, %s)", item_id, purchase_order_id, json.dumps(item), connection=connection)
    return {"id": purchase_order_id, "items": stored_purchase_order_items, **stored_purchase_order}


def delete_purchase_order(purchase_order_id, force=False, connection=None):
    """ Delete purchase order

    :param purchase_order_id: purchase order id
    :param force: if force is True, the order is deleted even if there are invoices attached to it
    :param connection: connection for transation management (optional)
    :return: None
    """
    stored_purchase_order = get_purchase_order(purchase_order_id)
    if stored_purchase_order:
        if not force:
            if stored_purchase_order["status"] == "requested":
                raise Exception("Purchase order has been already requested")
            if stored_purchase_order["status"] == "receiving":
                raise Exception("Purchase order has been already requested e has invoices attached to it")
            if stored_purchase_order["status"] == "finished":
                raise Exception("Purchase order has been already requested and all producted received")
        conn = databasePool.get_connection() if not connection else connection
        try:
            execute(f"delete from watchtime.purchase_orders where id=%s", purchase_order_id, connection=conn)
            execute(f"delete from watchtime.purchase_order_items where purchase_order_id=%s", purchase_order_id, connection=conn)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            if not connection:
                databasePool.put_connection(conn)


def has_purchase_order(purchase_order_id, connection=None):
    """ Check if purchase order exists

    :param purchase_order_id: purchase order id
    :param connection: connection for transation management (optional)
    :return: true if purchase order exists
    """
    return fetchone(f"select count(*) from watchtime.purchase_orders where id=%s", purchase_order_id, connection=connection)[0] == 1


def get_purchase_orders_summary(column, filters=None, connection=None):
    """ Get a summary of purchase orders by the given column and filters

    :param column: column name
    :param filters: dict of filters and order
    :param connection: connection for transation management (optional)
    :return: { <column>: number of purchase orders }
    """
    field = build_column(column, ORDERS_FIELDS)
    where = build_where(ORDERS_FIELDS, filters if filters else dict())
    sql = "select {}, count(*) from watchtime.purchase_orders {} group by {}".format(field, where, field)
    return {row[0] if row[0] else "-": row[1] for row in fetchall(sql, connection=connection)}


def get_purchase_orders(filters=None, connection=None):
    """ Get all purchase orders based on the given filters

    :param filters: dict of filters
    :param connection: connection for transation management (optional)
    :return: {
        data: [
            {
                id: purchase order id
                attribute: value
            }
        ],
        rows: total number of rows
        sql: built sql
    }
    """
    return select_data("watchtime.purchase_orders", ORDERS_FIELDS, JSON, filters, connection=connection)


def get_purchase_order_items(filters=None, connection=None):
    """ Get all purchase order items based on the given filters

    :param filters: dict of filters
    :param connection: connection for transation management (optional)
    :return: {
        data: [
            {
                id: purchase order item id
                attribute: value
            }
        ],
        rows: total number of rows
        sql: built sql
    }
    """

    return select_data("watchtime.purchase_order_items", ORDER_ITEMS_FIELDS, JSON, filters, connection=connection)


def get_purchase_order(purchase_order_id, connection=None):
    """ Get a purchase order by id

    :param purchase_order_id: purchase order id
    :param connection: connection for transation management (optional)
    :return: {
        id: purchase order item id
        attribute: value
    }
    """
    row = fetchone(f"select id, data from watchtime.purchase_orders where id=%s", purchase_order_id, connection=connection)
    if not row:
        return None
    items = get_purchase_order_items({"purchase_order_id": purchase_order_id}, connection=connection)['data']
    if row[1]['status'] in ["confirmed","receiving", "finished"]:
        for item in items:
            if item["status"]== 'active':
                item["received_quantity"] = sum([invoice.get("received_quantity",0) for invoice in item["invoices"]])  
                item["invoiced_quantity"] = sum([invoice.get("invoiced_quantity",0) for invoice in item["invoices"]])
              



    excel_url = ''
    if 'status' in row[1] and row[1]['status'] == 'approved':
        if items:
            
            resource = has_excel_file(purchase_order_id)
            if not resource:
                resource =send_excel_to_resource(purchase_order_id)
                excel_url = resource["id"] 
            # Obter a URL do arquivo gerado
            else:
                excel_url = resource

            return {"id": row[0], "items": items, "excel_url": excel_url,  **row[1]}
    # return {"files":order_files}
    return {"id": row[0], "items": items,  **row[1]}


def _calculate_totals(purchase_order):
    """ Update purchase order with calculated totals

    :param purchase_order: purchase order
    :return: None
    """
    for item in purchase_order.get("items", []):
        item["total_cost"] = item.get("product_cost", 0) * item.get("requested_quantity", 0)
    active_items = [item for item in purchase_order["items"] if item.get("status") == "active"]
    purchase_order["requested_items"] = len(active_items)
    purchase_order["requested_quantity"] = sum([
        item.get("requested_quantity", 0)
        for item in active_items
    ])
    purchase_order["total_cost"] = sum([
        item.get("total_cost", 0)
        for item in active_items
    ])
    purchase_order['received_quantity'] = sum([
        invoice.get("received_quantity", 0)
        for item in purchase_order.get("items", [])
        for invoice in item.get("invoices", [])
        if item.get("status") == "active"
    ])
    purchase_order['invoiced_quantity'] = sum([
        invoice.get("invoiced_quantity", 0)
        for item in purchase_order.get("items", [])
        for invoice in item.get("invoices", [])
        if item.get("status") == "active"
    ])
    purchase_order['receiving_quantity'] = sum([
        invoice.get("receiving_quantity", 0)
        for item in purchase_order.get("items", [])
        for invoice in item.get("invoices", [])
        if item.get("status") == "active"
    ])

    if purchase_order.get("status") in ["requested","confirmed", "receiving", "finished"]:
        if purchase_order["invoiced_quantity"] == 0:
            purchase_order["status"] = "requested"

        elif purchase_order.get("received_quantity",0) >= purchase_order["requested_quantity"]:
            purchase_order["status"] = "finished"
            purchase_order["finished"] = datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat()          
        
        elif purchase_order.get("invoiced_quantity") > 0 and purchase_order.get("receiving_quantity") == 0:
            purchase_order["status"] = "confirmed"
            if purchase_order.get("confirmed",[]) == []:  
                purchase_order["confirmed"] = datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat() 
        
        
        elif purchase_order.get("receiving_quantity") > 0:
            purchase_order["status"] = "receiving"
            if purchase_order.get("receiving",[]) == []:
                purchase_order["received"] = datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat()

            



def generate_excel_file(purchase_order_id):
    filters = {"purchase_order_id": purchase_order_id}
    response = get_purchase_order_items(filters=filters)
    data = response["data"]

    for item in data:
        if isinstance(item.get("OS"), list):
            item["OS"] = ", ".join([os["code"] for os in item["OS"]])
        elif item.get("OS") is None:
            item["OS"] = ''

    df = pd.DataFrame(data)

    wb = Workbook()
    ws = wb.active

    row = fetchone(f"select data->> 'brand' from watchtime.purchase_orders where id=%s", purchase_order_id)
    if row:
        if row[0] in ('OMEGA','LONGINES','TISSOT','MIDO','RADO','HAMILTON'):            
            col_names = ['FullReferenceNumber', 'Quantity', 'Comment']
            df_subset = df[['product_code', 'requested_quantity', 'OS']]
            ws.append(col_names)
        elif row[0] == ('HUBLOT'):
            headers1 = ['Order No.']
            headers2 = ['Notes']
            headers3 = [None]
            headers4 = ['Qty', 'Reference', 'Notes']

            ws.append(headers1)
            ws.append(headers2)
            ws.append(headers3)
            ws.append(headers4)

            df_subset = df[['product_code', 'requested_quantity', 'OS']]
        else:
            col_names = ['CODIGO_PRODUTO', 'QTD', 'OS']
            df_subset = df[['product_code', 'requested_quantity', 'OS']]
    else:
        col_names = ['CODIGO_PRODUTO', 'QTD', 'OS']
        df_subset = df[['product_code', 'requested_quantity', 'OS']]
        ws.append(col_names)
    for r in dataframe_to_rows(df_subset, index=False, header=False):
        ws.append(r)

    filename = f"/app/excel_files/{purchase_order_id}.xlsx"
    wb.save(filename)


def send_excel_to_resource(purchase_order_id):
    # Gerar o arquivo Excel
    generate_excel_file(purchase_order_id)

    # Ler o arquivo Excel gerado
    filename = f"/app/excel_files/{purchase_order_id}.xlsx"
    with open(filename, "rb") as f:
        wb_bytes = BytesIO(f.read())

    # Criar o objeto resource com o arquivo Excel como stream
    resource = {
        "purchase_order": purchase_order_id,
        "content_type": "application/vnd.ms-excel",
        "type": "excel"
    }
    create_resource(resource, stream=wb_bytes)
    return resource    


def get_product_resquested_quantity(product_id):
    query = """SELECT 
    pi.data->>'product_code' as product_code, 
coalesce(SUM((pi.data->>'requested_quantity')::int),0) - coalesce(SUM((invoices->>'received_quantity')::int),0) as invoiced_quantity_total
FROM 
    watchtime.purchase_order_items pi 
LEFT JOIN 
    watchtime.purchase_orders p on  pi.purchase_order_id = p.id
LEFT JOIN LATERAL (
    SELECT jsonb_array_elements(pi.data->'invoices') as invoices
    UNION ALL
    SELECT '{}'::jsonb WHERE NOT EXISTS (SELECT 1 FROM jsonb_array_elements(pi.data->'invoices'))
) AS invoices ON TRUE
LEFT JOIN 
    watchtime.purchase_invoices inv ON inv.id = (invoices->>'id')
WHERE 
    pi.data->>'product_code' = '"""+product_id+"""'
    AND pi.data->>'status' != 'cancelled' AND p.data->>'status' in ('approved','requested','receiving','confirmed')
    AND (inv.data->>'status' IS NULL OR inv.data->>'status' != 'cancelled')
    group by pi.data->>'product_code'""".replace('\n\t', ' ')

    row = fetchone(query, product_id)
    if not row:
        return {"requested_quantity": 0}
    return {"requested_quantity": row[1]}



def has_excel_file(purchase_order_id):

    row = fetchone(f"select id,data from watchtime.resources where data->>'purchase_order' = '"+ purchase_order_id+"'", purchase_order_id, connection= None)

    if not row:
        return False
    return row[0]


def get_purchase_order_for_invoice(purchase_order_id,connection = None):
    
    row = fetchone(f"select id, data from watchtime.purchase_orders where id=%s", purchase_order_id, connection=connection)
    if not row:
        return None
    filters = {"status": "active","purchase_order_id": purchase_order_id}
    items = get_purchase_order_items(filters, connection=connection)['data']
    excel_url = ''
    if 'status' in row[1] and row[1]['status'] == 'approved':
        if items:
            
            resource = has_excel_file(purchase_order_id)
            if not resource:
                resource =send_excel_to_resource(purchase_order_id)
                excel_url = resource["id"] 
            # Obter a URL do arquivo gerado
            else:
                excel_url = resource

    new_items = []
    for item in items:
        if item["status"] == "cancelled":
            continue
        if not "invoices" in item:
            item["invoiced_quantity"] = item["requested_quantity"]
            new_items.append(item)
        else:
            total_received_quantity = 0
            if len(item["invoices"]) == 0:
                total_received_quantity = 0
            else:
                total_received_quantity = sum([invoice.get("invoiced_quantity",0) for invoice in item["invoices"]])
            
            if item["requested_quantity"] != '':
                item_requested_quantity = int(item["requested_quantity"])
            else:
                item_requested_quantity = 0
            if total_received_quantity >= int(item["requested_quantity"]):
                continue
            else:
                item["invoiced_quantity"] = int(item_requested_quantity) - total_received_quantity

            new_items.append(item)

    items = new_items        

    return {"id": row[0], "items": items, "excel_url": excel_url,  **row[1]}
    # return {"files":order_files}


def import_purchase_order_items(purchase_order_id,data):
    df = pd.read_excel(data, dtype={"referencia": str})
    items = []
    erros =[]
    tem_os = False
    # Check if the columns "referencia" and "quantidade" exist in the dataframe
    if "referencia" in df.columns.values and "quantidade" in df.columns.values:
        df['referencia'] = df['referencia'].str.strip().str.upper()
        # Check if the column "OS" exists in the dataframe
        if "OS" in df.columns.values:
            # If the column "OS" exists, select all three columns and return them as a list of dictionaries
            tem_os = True
            for _, row in df[["referencia", "quantidade", "OS"]].iterrows():
                product = get_product(str(row["referencia"]))
                if not product:
                    erros.append({"id": str(row["referencia"]),"problem": "Não cadastrado no Cockpit ou Estoklus"})
                else:
                    items.append({"product_id":product["id"],"product_category":product["category"],"product_code":product["code"],"product_cost":product["cost"],"product_name":product["name"],"requested_quantity": row["quantidade"],"status": "active","total_cost": float(product["cost"]) * float(row["quantidade"]),"OS":[{"code": str(row["OS"])}]})                           
        else:
            # If the column "OS" doesn't exist, select only the "referencia" and "quantidade" columns
            for _, row in df[["referencia", "quantidade"]].iterrows():
                product = get_product(str(row["referencia"]))
                if not product:
                    erros.append({"id": str(row["referencia"])})
                else:
                    items.append({"product_id":product["id"],"product_category":product["category"],"product_code":product["code"],"product_cost":product["cost"],"product_name":product["name"],"requested_quantity": row["quantidade"],"status": "active","total_cost": float(product["cost"])* float(row["quantidade"])})
                    

        if not erros:
            
            order = get_purchase_order(purchase_order_id)
            order["items"] = items
            if tem_os:
                order["mode"] = 'Importado'
            update_purchase_order(order)

            return [{"status": "success","message":"Produtos importados com sucesso"}]
        else:
            return [{"status": "warning","message":erros}]
    else:
        # If any of the columns don't exist, return None
        return [{"status": "error","message":"erro, verifique o layout  - as colunas devem se chamar (referencia,quantidade,OS)"}]

        #execute(f"insert into watchtime.purchase_order_items (id, purchase_order_id, data) values (%s, %s, %s)", item_id, purchase_order_id, json.dumps(item), connection=connection)

def consulta_pedidos_peca(referencia_produto):

        sql = f"""select p.data->> 'code',
    po.data->>'OS',
    p.data->>'status',
    p.data->>'mode',
    po.data->>'requested_quantity',
    po.data->>'product_name',
    coalesce(po.data->>'received_quantity','0')
    from 
     watchtime.watchtime.purchase_orders p
     left join watchtime.watchtime.purchase_order_items po 
     on p.id = po.purchase_order_id 
    where po.data->>'product_id'='{referencia_produto}'"""
        return [{'pedido_code':row[0],
                 'OS':row[1],
                 'status':row[2],
                 'mode':row[3],
                 'requested_quantity':row[4],
                 'product_name':row[5],
                 'received_quantity':row[6]
                 } for row in fetchall(sql)]