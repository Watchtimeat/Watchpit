import json
import uuid,logging

from models import execute, fetchone, execute_values,fetchall
from models.sql import select_data
from utils import required, clean_dict



FIELDS = ["id", "data"]
JSON = "data"


def create_person(person):
    """ Create person based on the given data

    :param person: {
        id: person id
        attribute: value
    }
    :return: {
        id: person id
        attribute: value
    }
    """
    required(person, ["name"])
    if "id" not in person:
        person["id"] = uuid.uuid4().hex
    if has_person(person["id"]):
        raise Exception("person '{}' already exists".format(person["id"]))
    person_copy = person.copy()
    person_id = person_copy.pop("id")
    execute(f"insert into watchtime.wsp_persons (id, data) values (%s, %s)", person_id, json.dumps(person_copy))
    return get_person(person_id=person["id"])


def create_persons(persons):
    """ Create persons based on the given data

    :param persons: [
        {
            id: person id
            attribute: value
        }
    ]
    :return: None
    """
    if not isinstance(persons, list):
        raise Exception("persons must be a list")
    persons_value = list()
    for person in persons:
        required(person, ["name"])
        persons_value.append([
            person.pop("id") if "id" in person else uuid.uuid4().hex,
            json.dumps(person)
        ])
    execute_values(f"insert into watchtime.wsp_persons (id, data) values %s", persons_value)
    return None


def update_person(person):
    required(person, ['id'])
    stored_person = get_person(person["id"])
    if not stored_person:
        raise Exception("person not found")
    stored_person.update(person)
    person_id = stored_person.pop("id")
    clean_dict(stored_person)
    execute(f"update watchtime.wsp_persons set data = %s where id=%s", json.dumps(stored_person), person_id)
    return get_person(person["id"])


def delete_person(person_id):
    execute(f"delete from watchtime.wsp_persons where id=%s", person_id)


def get_persons(filters=None):
    """ Get all persons based on the given filters

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
    return select_data("watchtime.wsp_persons", FIELDS, JSON, filters)


def get_person(person_id):
    row = fetchone(f"select id, data from watchtime.wsp_persons where id=%s", person_id)
    if not row:
        return None
    return {"id": row[0], **row[1]}


def has_person(person_id):
    return fetchone(f"select count(*) from watchtime.wsp_persons where id=%s", person_id)[0] == 1

def get_persons_by_ids(ids):
    # Adicione aspas simples ao redor de cada ID para tratá-los como strings
    id_list = ','.join(f"'{id}'" for id in ids)
    query = f"SELECT id, data FROM watchtime.wsp_persons WHERE id IN ({id_list})"
    logging.info(query)
    rows = fetchall(query)
    return {row[0]: {"id": row[0], **row[1]} for row in rows}
