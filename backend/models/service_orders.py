import json
import uuid,logging,os,subprocess,tempfile


from models.estoklus.services import gerar_nf_entrada,criar_cliente_estoklus,criar_os_estoklus,atualizar_cliente_estoklus,inserir_orcamento
from models import execute, fetchone, execute_values,fetchall
from models.sql import select_data, build_where, build_column
from utils import required, clean_dict


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s', handlers=[logging.StreamHandler()])

FIELDS = ["id", "data"]
JSON = "data"

def create_service_order(service_order):
    """ Create service_order based on the given data

    :param service_order: {
        OS: service_order id
        attribute: value
    }
    :return: {
        OS: service_order id
        attribute: value
    }
    """
    retorno = criar_os_estoklus(service_order)
    if (retorno.get("error",'') != ''):
        return retorno   
    service_order["id"] = retorno["success"]
    service_order["codigo_estoklus"] = int(retorno["success"].lstrip(retorno["success"][0:2]))
    service_order["nf_estoklus"]=gerar_nf_entrada(service_order,'E')
    logging.info(f'OS {service_order["codigo_estoklus"]} criada ')
    logging.info(f'nf_entrada {service_order["nf_estoklus"]} ')


    if has_service_order(service_order["id"]):
        return {"service_order '{}' already exists".format(service_order["id"])}
    service_order_copy = service_order.copy()
    service_order_id = service_order_copy.pop("id")
    execute(f"insert into watchtime.service_orders (id, data) values (%s, %s)", service_order_id, json.dumps(service_order_copy))
    return {'success':str(service_order["id"])}


def create_service_orders(service_orders):
    """ Create service_orders based on the given data

    :param service_orders: [
        {
            id: service_order id
            attribute: value
        }
    ]
    :return: None
    """
    if not isinstance(service_orders, list):
        raise Exception("service_orders must be a list")
    service_orders_value = list()
    for service_order in service_orders:
        required(service_order, ["loja"])
        service_orders_value.append([
            service_order.pop("id") if "id" in service_order else uuid.uuid4().hex,
            json.dumps(service_order)
        ])

    execute_values(f"insert into watchtime.service_orders (id, data) values %s", service_orders_value)
    return None


def update_service_order(service_order):
    required(service_order, ['id'])
    stored_service_order = get_service_order(service_order["id"])
    if not stored_service_order:
        raise Exception("service_order not found")
    stored_service_order.update(service_order)
    service_order_id = stored_service_order.pop("id")
    clean_dict(stored_service_order)
    execute(f"update watchtime.service_orders set data = %s where id=%s", json.dumps(stored_service_order), service_order_id)
    return get_service_order(service_order["id"])


def delete_service_order(service_order_id):
    execute(f"delete from watchtime.service_orders where id=%s", service_order_id)


def get_service_orders(filters=None):
    """ Get all service_orders based on the given filters

    :param filters: dict of filters and order
    :return: {
        data: [
            {
                id: user id
                attribute: value
            }
        ],
        rows: total number of rows
    }
    """
    return select_data("watchtime.service_orders", FIELDS, JSON, filters)



def get_service_order(service_order_id):
    row = fetchone(f"select id, data from watchtime.service_orders where id=%s", service_order_id)
    if not row:
        return None
    return {"id": row[0], **row[1]}

def has_service_order(service_order_id):
    return fetchone(f"select count(*) from watchtime.service_orders where id=%s", service_order_id)[0] == 1

def get_service_orders_summary(column, filters=None, connection=None):
    """ Get a summary of purchase orders by the given column and filters

    :param column: column name
    :param filters: dict of filters and order
    :param connection: connection for transation management (optional)
    :return: { <column>: number of purchase orders }
    """
    field = build_column(column, FIELDS)
    where = build_where(FIELDS, filters if filters else dict())
    sql = "select {}, count(*) from watchtime.service_orders {} group by {}".format(field, where, field)
    return {row[0] if row[0] else "-": row[1] for row in fetchall(sql, connection=connection)}

def delete_customer(customer_id):
    execute(f"delete from watchtime.customers where id=%s", customer_id)

def create_customer(customer):
    """ Create service_order based on the given data

    :param customer: {
        OS: customer id
        attribute: value
    }
    :return: {
        OS: customer id
        attribute: value
    }
    """
    customer["id"] = criar_cliente_estoklus(customer)

    if not (customer["id"] ):
        return {"error":"Cliente já cadastrado"}

    required(customer, ["id"])

    if has_customer(customer["id"]):
        raise Exception("service_order '{}' already exists".format(customer["id"]))
    customer_copy = customer.copy()
    customer_id = customer_copy.pop("id")
    execute(f"insert into watchtime.customers (id, data) values (%s, %s)", customer_id, json.dumps(customer_copy))
    return {"success": customer["id"]}


def create_customers(customers):
    """ Create service_orders based on the given data

    :param service_orders: [
        {
            id: service_order id
            attribute: value
        }
    ]
    :return: None
    """
    if not isinstance(customers, list):
        raise Exception("customers must be a list")
    customers_value = list()
    for customer in customers:
        required(customer, ["id"])
        customers_value.append([
            customer.pop("id") if "id" in customer else uuid.uuid4().hex,
            json.dumps(customer)
        ])
    execute_values(f"insert into watchtime.customers (id, data) values %s", customers_value)



    return None


def update_customer(customer):
    required(customer, ['cliente_id'])
    atualizar_cliente_estoklus(customer)
    stored_customer = get_customer(customer["cliente_id"])
    if not stored_customer:
        raise Exception("service_order not found")
    stored_customer.update(customer)
    customer_id = stored_customer.pop("id")
    clean_dict(stored_customer)
    execute(f"update watchtime.customers set data = %s where id=%s", json.dumps(stored_customer), customer_id)
    return {"success":str(customer["cliente_id"])}


def get_customers(filters=None):
    """ Get all service_orders based on the given filters

    :param filters: dict of filters and order
    :return: {
        data: [
            {
                id: user id
                attribute: value
            }
        ],
        rows: total number of rows
    }
    """
    return select_data("watchtime.customers", FIELDS, JSON, filters)



def get_customer(customer_id):
    row = fetchone(f"select id, data from watchtime.customers where id=%s", customer_id)
    if not row:
        return None
    return {"id": row[0], **row[1]}

def has_customer(customer_id):
    return fetchone(f"select count(*) from watchtime.customers where id=%s", customer_id)[0] == 1

def create_service_order_items(items):
    for item in items:
        execute(f"insert into watchtime.service_order_items (id, referencia_produto, data) values (%s, %s, %s)", item["id"], item["referencia_produto"], json.dumps(item))
    return {'OK'}
    

def get_service_order_items(filters=None):
    """ Get all service_orders based on the given filters

    :param filters: dict of filters and order
    :return: {
        data: [
            {
                id: user id
                attribute: value
            }
        ],
        rows: total number of rows
    }
    """
    return select_data("watchtime.service_order_items", FIELDS, JSON, filters)


def calcula_orcamento(itens,desconto):

    valor_hora = 150
    total_obrigatorio = 0
    total_opcionais = 0
    custo_pecas_inclusas= 0
    custo_pecas_cobradas= 0
    custo_mao_obra = 0
    valor_liquido = 0
    margem = 0
    valor_servicos = 0
    valor_margem = 0
    total_bruto = 0
    valor_cliente = 0
    custo_total = 0
    desconto = 0.0 if desconto is None else (float(desconto) if isinstance(desconto, (int, float, str)) and (isinstance(desconto, (int, float)) or desconto.replace('.', '', 1).isdigit()) else 0.0)
    desconto_obrigatorios = 0
    desconto_todos = 0
    valor_margem_obrigatorios = 0
    custo_obrigatorio = 0
    for item in itens:
        if item["tipo"].strip()  == 'S':
            valor_servicos += float(item['preco_venda'])
            custo_mao_obra += float(item['quantidade']) * valor_hora
            total_bruto += float(item.get('preco_venda',0))
            total_obrigatorio += float(item.get('preco_venda',0))
            custo_obrigatorio += float(item['quantidade']) * valor_hora
        elif item["tipo"].strip()  == 'P':
            total_bruto += float(item['preco_venda']) * float(item['quantidade'])
            total_obrigatorio += float(item['preco_venda']) * float(item['quantidade'])
            custo_pecas_cobradas += float(item['quantidade']) * float(item['preco_custo'])
            custo_obrigatorio += float(item['quantidade']) *  float(item['preco_custo'])
          
        elif item["tipo"].strip()  == 'I':
            custo_pecas_inclusas += float(item['quantidade']) * float(item['preco_custo'])
            custo_obrigatorio += float(item['quantidade']) *  float(item['preco_custo'])
        
        elif item["tipo"].strip()  == 'OP':
            total_bruto += float(item.get('preco_venda',0)) * float(item['quantidade'])
            total_opcionais += float(item.get('preco_venda',0)) * float(item['quantidade'])
            custo_pecas_cobradas += float(item['quantidade']) * float(item['preco_custo'])
            
            
        elif item["tipo"].strip()  == 'SO':
            total_bruto += float(item.get('preco_venda',0)) * float(item['quantidade'])
            total_opcionais += float(item.get('preco_venda',0)) * float(item['quantidade'])
            custo_mao_obra += float(item['quantidade']) * valor_hora
    if desconto > 0:
        desconto_todos = total_bruto * (desconto / 100)
        desconto_obrigatorios = total_obrigatorio * (desconto / 100)
        
    total_obrigatorio_cliente = total_obrigatorio - desconto_obrigatorios
    valor_cliente = total_bruto - desconto_todos
    custo_total = custo_mao_obra + custo_pecas_cobradas + custo_pecas_inclusas
    valor_liquido = valor_cliente - (custo_total) -  (valor_cliente*0.18)
    valor_liquido_obrigatorios = total_obrigatorio_cliente - (custo_obrigatorio) -  (total_obrigatorio_cliente *0.18)
    if total_bruto > 0:
        valor_margem = valor_liquido / total_bruto * 100
        if valor_liquido_obrigatorios > 0:
            valor_margem_obrigatorios =  valor_liquido_obrigatorios / total_obrigatorio * 100
        else:
            valor_margem_obrigatorios = 0
    
    return {
        "valor_liquido":round(valor_liquido,2),
        "valor_cliente":round(valor_cliente,2),
        "valor_margem":round(valor_margem,2),
        "custo_total":round(custo_total,2),
        "total_bruto":round(total_bruto,2),
        "total_opcionais":round(total_opcionais,2),
        "valor_desconto_todos":round(desconto_todos,2),
        "valor_desconto_obrigatorios":round(desconto_obrigatorios,2),
        "total_obrigatorio":round(total_obrigatorio_cliente,2),
        "valor_margem_obrigatorios":round(valor_margem_obrigatorios,2),
        "valor_liquido_obrigatorios":round(valor_liquido_obrigatorios,2)}



def create_service_estimate(estimate):
    """ Create service_order based on the given data

    :param service_order: {
        OS: service_order id
        attribute: value
    }
    :return: {
        OS: service_order id
        attribute: value
    }
    """
    retorno = inserir_orcamento(estimate)
    if (retorno.get("error",'') != ''):
        return retorno   

    return {'success':str(estimate["id"])}



def copy_file_as_root(file_storage, destination_path):
    # Create a temporary file and save the uploaded file there
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    file_storage.save(temp_file.name)

    # Construct the copy command
    cmd = f'cp {temp_file.name} {destination_path}'

    # Execute the copy command as root
    try:
        os.system(f'{cmd}')
    finally:
        os.remove(temp_file.name)  # Cleanup the temporary file




def next_letter_for_os(os_number, directory):
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    for letter in letters:
        filename = f"F-{os_number:06}-{letter}.jpg"
        filepath = os.path.join(directory, filename)
        
        # Se o arquivo não existir, retorne a letra
        if not os.path.exists(filepath):
            return letter

    return None  # Todas as letras estão em uso

def format_date(date_str):
    # Verifica se a data está no formato dd/mm/yyyy
    if date_str and len(date_str) == 10 and date_str[2] == '/' and date_str[5] == '/':
        try:
            day, month, year = map(int, date_str.split('/'))
            return f"{year:04d}-{month:02d}-{day:02d}"
        except ValueError:
            # Retorna a data como está se ela for inválida
            return date_str
    else:
        # Retorna a data como está se ela não estiver no formato dd/mm/yyyy
        return date_str

def select_quickview(documento):
    select_clauses = ["data->>'marca'", "data->>'modelo'", "data->>'serie'", "data->>'data_entrega_produto'", "data->>'valor_cliente'", "data->>'loja'", "data->>'status_os',id"]
    where_clauses = [f"data->>'documento' = '{documento}'"]
    params = []

    # Monta a consulta SQL
    select_statement = "SELECT " + ", ".join(select_clauses)
    where_statement = " WHERE " + " AND ".join(where_clauses)
    sql_query = select_statement + " FROM watchtime.service_orders" + where_statement + "order by data->>'serie',data->>'data_entrega_produto' asc"

    # Executa a consulta com os parâmetros desempacotados
    return [{"marca": row[0],
             "modelo": row[1],
             "serie": row[2],
             "data_entrega": format_date(row[3]),
             "valor": row[4],
             "unidade": row[5],
             "tipo_servico": row[6],
             "id":row[7]} for row in fetchall(sql_query, *params)]  # Use *params para desempacotar a lista




