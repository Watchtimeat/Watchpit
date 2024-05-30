import json
import uuid,logging

from models import execute, fetchone, execute_values,fetchall
from models.sql import select_data
from utils import required, clean_dict



FIELDS = ["id", "data"]
JSON = "data"


def create_watch(watch):
    """ Create watch based on the given data

    :param watch: {
        id: watch id
        attribute: value
    }
    :return: {
        id: watch id
        attribute: value
    }
    """
    required(watch, ["name"])
    if "id" not in watch:
        watch["id"] = uuid.uuid4().hex
    if has_watch(watch["id"]):
        raise Exception("watch '{}' already exists".format(watch["id"]))
    watch_copy = watch.copy()
    watch_id = watch_copy.pop("id")
    execute(f"insert into watchtime.wsp_watches (id, data) values (%s, %s)", watch_id, json.dumps(watch_copy))
    return get_watch(watch_id=watch["id"])


def create_watches(watches):
    """ Create watches based on the given data

    :param watches: [
        {
            id: watch id
            attribute: value
        }
    ]
    :return: None
    """
    if not isinstance(watches, list):
        raise Exception("watches must be a list")
    watches_value = list()
    for watch in watches:
        required(watch, ["name"])
        watches_value.append([
            watch.pop("id") if "id" in watch else uuid.uuid4().hex,
            json.dumps(watch)
        ])
    execute_values(f"insert into watchtime.wsp_watches (id, data) values %s", watches_value)
    return None


def update_watch(watch):
    required(watch, ['id'])
    stored_watch = get_watch(watch["id"])
    if not stored_watch:
        raise Exception("watch not found")
    stored_watch.update(watch)
    watch_id = stored_watch.pop("id")
    clean_dict(stored_watch)
    execute(f"update watchtime.wsp_watches set data = %s where id=%s", json.dumps(stored_watch), watch_id)
    return get_watch(watch["id"])


def delete_watch(watch_id):
    execute(f"delete from watchtime.wsp_watches where id=%s", watch_id)


def get_watches(filters=None):
    """ Get all watches based on the given filters

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
    return select_data("watchtime.wsp_watches", FIELDS, JSON, filters)


def get_watch(watch_id):
    row = fetchone(f"select id, data from watchtime.wsp_watches where id=%s", watch_id)
    if not row:
        return None
    return {"id": row[0], **row[1]}


def has_watch(watch_id):
    return fetchone(f"select count(*) from watchtime.wsp_watches where id=%s", watch_id)[0] == 1

def get_watches_by_ids(ids):
    # Adicione aspas simples ao redor de cada ID para tratá-los como strings
    id_list = ','.join(f"'{id}'" for id in ids)
    query = f"SELECT id, data FROM watchtime.wsp_watches WHERE id IN ({id_list})"
    logging.info(query)
    rows = fetchall(query)
    return {row[0]: {"id": row[0], **row[1]} for row in rows}
