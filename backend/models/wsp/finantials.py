import json
import uuid,logging

from models import execute, fetchone, execute_values,fetchall
from models.sql import select_data
from utils import required, clean_dict



FIELDS = ["id", "data"]
JSON = "data"


def create_finantial(finantial):
    """ Create finantial based on the given data

    :param finantial: {
        id: finantial id
        attribute: value
    }
    :return: {
        id: finantial id
        attribute: value
    }
    """
    required(finantial, ["name"])
    if "id" not in finantial:
        finantial["id"] = uuid.uuid4().hex
    if has_finantial(finantial["id"]):
        raise Exception("finantial '{}' already exists".format(finantial["id"]))
    finantial_copy = finantial.copy()
    finantial_id = finantial_copy.pop("id")
    execute(f"insert into watchtime.wsp_finantials (id, data) values (%s, %s)", finantial_id, json.dumps(finantial_copy))
    return get_finantial(finantial_id=finantial["id"])


def create_finantials(finantials):
    """ Create finantials based on the given data

    :param finantials: [
        {
            id: finantial id
            attribute: value
        }
    ]
    :return: None
    """
    if not isinstance(finantials, list):
        raise Exception("finantials must be a list")
    finantials_value = list()
    for finantial in finantials:
        required(finantial, ["name"])
        finantials_value.append([
            finantial.pop("id") if "id" in finantial else uuid.uuid4().hex,
            json.dumps(finantial)
        ])
    execute_values(f"insert into watchtime.wsp_finantials (id, data) values %s", finantials_value)
    return None


def update_finantial(finantial):
    required(finantial, ['id'])
    stored_finantial = get_finantial(finantial["id"])
    if not stored_finantial:
        raise Exception("finantial not found")
    stored_finantial.update(finantial)
    finantial_id = stored_finantial.pop("id")
    clean_dict(stored_finantial)
    execute(f"update watchtime.wsp_finantials set data = %s where id=%s", json.dumps(stored_finantial), finantial_id)
    return get_finantial(finantial["id"])


def delete_finantial(finantial_id):
    execute(f"delete from watchtime.wsp_finantials where id=%s", finantial_id)


def get_finantials(filters=None):
    """ Get all finantials based on the given filters

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
    return select_data("watchtime.wsp_finantials", FIELDS, JSON, filters)


def get_finantial(finantial_id):
    row = fetchone(f"select id, data from watchtime.wsp_finantials where id=%s", finantial_id)
    if not row:
        return None
    return {"id": row[0], **row[1]}


def has_finantial(finantial_id):
    return fetchone(f"select count(*) from watchtime.wsp_finantials where id=%s", finantial_id)[0] == 1

def get_finantials_by_ids(ids):
    # Adicione aspas simples ao redor de cada ID para tratá-los como strings
    id_list = ','.join(f"'{id}'" for id in ids)
    query = f"SELECT id, data FROM watchtime.wsp_finantials WHERE id IN ({id_list})"
    logging.info(query)
    rows = fetchall(query)
    return {row[0]: {"id": row[0], **row[1]} for row in rows}
