import json
import uuid,logging

from models import execute, fetchone, execute_values,fetchall
from models.sql import select_data
from utils import required, clean_dict



FIELDS = ["id", "data"]
JSON = "data"


def create_sell(sell):
    """ Create sell based on the given data

    :param sell: {
        id: sell id
        attribute: value
    }
    :return: {
        id: sell id
        attribute: value
    }
    """
    required(sell, ["name"])
    if "id" not in sell:
        sell["id"] = uuid.uuid4().hex
    if has_sell(sell["id"]):
        raise Exception("sell '{}' already exists".format(sell["id"]))
    sell_copy = sell.copy()
    sell_id = sell_copy.pop("id")
    execute(f"insert into watchtime.wsp_sells (id, data) values (%s, %s)", sell_id, json.dumps(sell_copy))
    return get_sell(sell_id=sell["id"])


def create_sells(sells):
    """ Create sells based on the given data

    :param sells: [
        {
            id: sell id
            attribute: value
        }
    ]
    :return: None
    """
    if not isinstance(sells, list):
        raise Exception("sells must be a list")
    sells_value = list()
    for sell in sells:
        required(sell, ["name"])
        sells_value.append([
            sell.pop("id") if "id" in sell else uuid.uuid4().hex,
            json.dumps(sell)
        ])
    execute_values(f"insert into watchtime.wsp_sells (id, data) values %s", sells_value)
    return None


def update_sell(sell):
    required(sell, ['id'])
    stored_sell = get_sell(sell["id"])
    if not stored_sell:
        raise Exception("sell not found")
    stored_sell.update(sell)
    sell_id = stored_sell.pop("id")
    clean_dict(stored_sell)
    execute(f"update watchtime.wsp_sells set data = %s where id=%s", json.dumps(stored_sell), sell_id)
    return get_sell(sell["id"])


def delete_sell(sell_id):
    execute(f"delete from watchtime.wsp_sells where id=%s", sell_id)


def get_sells(filters=None):
    """ Get all sells based on the given filters

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
    return select_data("watchtime.wsp_sells", FIELDS, JSON, filters)


def get_sell(sell_id):
    row = fetchone(f"select id, data from watchtime.wsp_sells where id=%s", sell_id)
    if not row:
        return None
    return {"id": row[0], **row[1]}


def has_sell(sell_id):
    return fetchone(f"select count(*) from watchtime.wsp_sells where id=%s", sell_id)[0] == 1

def get_sells_by_ids(ids):
    # Adicione aspas simples ao redor de cada ID para tratá-los como strings
    id_list = ','.join(f"'{id}'" for id in ids)
    query = f"SELECT id, data FROM watchtime.wsp_sells WHERE id IN ({id_list})"
    logging.info(query)
    rows = fetchall(query)
    return {row[0]: {"id": row[0], **row[1]} for row in rows}
