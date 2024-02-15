from flask import Blueprint, request, jsonify, abort

from blueprints.utils import get_current_user, multidict_to_dict
from datetime import datetime
from blueprints.utils import get_current_user
from models.service_orders import create_customer,create_customers,get_customer,get_customers,update_customer
from models.estoklus.service_orders import importar_clientes
from models.estoklus.services import get_customer_data


blueprint = Blueprint("customers", __name__, url_prefix="/api/customers")


@blueprint.route("estoklus", methods=["GET"])
def get_customers_estoklus_handler():
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    get_current_user()
    return jsonify(importar_clientes())

@blueprint.route("", methods=["GET"])
def get_customers_handler():
    """ get purchase orders

    GET /purchase_orders

    parameters:
        <field>: <value>

    :return: [
        {
            id: product id
            attribute: value
        }
    ]
    """
    get_current_user()
    filters = multidict_to_dict(request.args)
    return jsonify(get_customers(filters))


@blueprint.route("", methods=["POST"])
def create_customers_handler():
    """ create product based on the given data

    POST /products

    body: {
        attribute: value
    }

    :return: None
    """
    get_current_user()
    data = request.get_json()
    if isinstance(data, list):
        return jsonify(create_customers(data))
    elif isinstance(data, object):
        return jsonify(create_customer(data))
    abort(400)

@blueprint.route("<customer_id>", methods=["PATCH"])
def update_customer_handler(customer_id):
    """ update product

    PUT /products/<product_id>

    :body: {
        attribute: value
    }

    :return: {
        id: product id
        attribute: value
    }
    """
    get_current_user()
    return jsonify(update_customer({**request.get_json(), "id": customer_id}))


@blueprint.route("<customer_id>", methods=["GET"])
def get_customer_handler(customer_id):
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    get_current_user()
    return jsonify(get_customer(customer_id))



@blueprint.route("fetch_data", methods=["POST"])
def fetch_data_customer():


    data = request.get_json()
    return jsonify(get_customer_data(data["filter"],data["data"]))

