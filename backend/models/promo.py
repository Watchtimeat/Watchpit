import json
import uuid,logging

from models import execute, fetchone, execute_values,fetchall
from models.sql import select_data
from utils import required, clean_dict



FIELDS = ["id", "data"]
JSON = "data"


def create_promo(promo):
    """ Create promo based on the given data

    :param promo: {
        id: promo id
        attribute: value
    }
    :return: {
        id: promo id
        attribute: value
    }
    """
    required(promo, ["name"])
    if "id" not in promo:
        promo["id"] = uuid.uuid4().hex
    if has_promo(promo["id"]):
        raise Exception("promo '{}' already exists".format(promo["id"]))
    promo_copy = promo.copy()
    promo_id = promo_copy.pop("id")
    execute(f"insert into watchtime.promos (id, data) values (%s, %s)", promo_id, json.dumps(promo_copy))
    return get_promo(promo_id=promo["id"])


def create_promos(promos):
    """ Create promos based on the given data

    :param promos: [
        {
            id: promo id
            attribute: value
        }
    ]
    :return: None
    """
    if not isinstance(promos, list):
        raise Exception("promos must be a list")
    promos_value = list()
    for promo in promos:
        required(promo, ["name"])
        promos_value.append([
            promo.pop("id") if "id" in promo else uuid.uuid4().hex,
            json.dumps(promo)
        ])
    execute_values(f"insert into watchtime.promos (id, data) values %s", promos_value)
    return None


def update_promo(promo):
    required(promo, ['id'])
    stored_promo = get_promo(promo["id"])
    if not stored_promo:
        raise Exception("promo not found")
    stored_promo.update(promo)
    promo_id = stored_promo.pop("id")
    clean_dict(stored_promo)
    execute(f"update watchtime.promos set data = %s where id=%s", json.dumps(stored_promo), promo_id)
    return get_promo(promo["id"])


def delete_promo(promo_id):
    execute(f"delete from watchtime.promos where id=%s", promo_id)


def get_promos(filters=None):
    """ Get all promos based on the given filters

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
    return select_data("watchtime.promos", FIELDS, JSON, filters)


def get_promo(promo_id):
    row = fetchone(f"select id, data from watchtime.promos where id=%s", promo_id)
    if not row:
        return None
    return {"id": row[0], **row[1]}


def has_promo(promo_id):
    return fetchone(f"select count(*) from watchtime.promos where id=%s", promo_id)[0] == 1

def get_promos_by_ids(ids):
    # Adicione aspas simples ao redor de cada ID para tratá-los como strings
    id_list = ','.join(f"'{id}'" for id in ids)
    query = f"SELECT id, data FROM watchtime.promos WHERE id IN ({id_list})"
    logging.info(query)
    rows = fetchall(query)
    return {row[0]: {"id": row[0], **row[1]} for row in rows}



def select_customers(filters):
    select_clauses = ["data->>'nome'"]
    where_clauses = ["data->>'codigo_tipo_pessoa' = 'F'"]
    params = []

    for filter in filters:
        where_clauses.append(f"data->>'{filter['code']}' = %s")
        select_clauses.append(f"data->>'{filter['code']}'")
        params.append(filter['data'])

   # Monta a consulta SQL
    select_statement = "SELECT " + ", ".join(select_clauses)
    where_statement = " WHERE " + " AND ".join(where_clauses)
    sql_query = select_statement + " FROM watchtime.service_orders" + where_statement

    # Executa a consulta com os parâmetros desempacotados
    return fetchall(sql_query, *params)  # Use *params para desempacotar a lista

# Teste com os filtros
filtros = [
    {"code": "loja", "data": "SP"},
    {"code": "brand_id", "data": "AU"}
]





