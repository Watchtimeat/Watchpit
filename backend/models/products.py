import json
import uuid,logging

from models import execute, fetchone, execute_values,fetchall
from models.sql import select_data
from utils import required, clean_dict



FIELDS = ["id", "data"]
JSON = "data"


def create_product(product):
    """ Create product based on the given data

    :param product: {
        id: product id
        attribute: value
    }
    :return: {
        id: product id
        attribute: value
    }
    """
    required(product, ["name"])
    if "id" not in product:
        product["id"] = uuid.uuid4().hex
    if has_product(product["id"]):
        raise Exception("Product '{}' already exists".format(product["id"]))
    product_copy = product.copy()
    product_id = product_copy.pop("id")
    execute(f"insert into watchtime.products (id, data) values (%s, %s)", product_id, json.dumps(product_copy))
    return get_product(product_id=product["id"])


def create_products(products):
    """ Create products based on the given data

    :param products: [
        {
            id: product id
            attribute: value
        }
    ]
    :return: None
    """
    if not isinstance(products, list):
        raise Exception("Products must be a list")
    products_value = list()
    for product in products:
        required(product, ["name"])
        products_value.append([
            product.pop("id") if "id" in product else uuid.uuid4().hex,
            json.dumps(product)
        ])
    execute_values(f"insert into watchtime.products (id, data) values %s", products_value)
    return None


def update_product(product):
    required(product, ['id'])
    stored_product = get_product(product["id"])
    if not stored_product:
        raise Exception("Product not found")
    stored_product.update(product)
    product_id = stored_product.pop("id")
    clean_dict(stored_product)
    execute(f"update watchtime.products set data = %s where id=%s", json.dumps(stored_product), product_id)
    return get_product(product["id"])


def delete_product(product_id):
    execute(f"delete from watchtime.products where id=%s", product_id)


def get_products(filters=None):
    """ Get all products based on the given filters

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
    return select_data("watchtime.products", FIELDS, JSON, filters)


def get_product(product_id):
    row = fetchone(f"select id, data from watchtime.products where id=%s", product_id)
    if not row:
        return None
    return {"id": row[0], **row[1]}


def has_product(product_id):
    return fetchone(f"select count(*) from watchtime.products where id=%s", product_id)[0] == 1

def get_products_by_ids(ids):
    # Adicione aspas simples ao redor de cada ID para tratá-los como strings
    id_list = ','.join(f"'{id}'" for id in ids)
    query = f"SELECT id, data FROM watchtime.products WHERE id IN ({id_list})"
    logging.info(query)
    rows = fetchall(query)
    return {row[0]: {"id": row[0], **row[1]} for row in rows}
