from flask import Blueprint, request, jsonify, abort

from blueprints.utils import get_current_user, multidict_to_dict
from models.products import create_product, get_products, get_product, update_product, delete_product, create_products

blueprint = Blueprint("products", __name__, url_prefix="/api/products")


@blueprint.route("", methods=["POST"])
def create_product_handler():
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
        return jsonify(create_products(data))
    elif isinstance(data, object):
        return jsonify(create_product(data))
    abort(400)


@blueprint.route("<product_id>", methods=["PATCH"])
def update_product_handler(product_id):
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
    return jsonify(update_product({**request.get_json(), "id": product_id}))


@blueprint.route("<product_id>", methods=["DELETE"])
def delete_product_handler(product_id):
    """ delete product

    DELETE /products/<product_id>

    :return: None
    """
    get_current_user()
    delete_product(product_id)
    return jsonify(), 204


@blueprint.route("", methods=["GET"])
def get_products_handler():
    """ get products

    GET /products

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
    return jsonify(get_products(filters))


@blueprint.route("<product_id>", methods=["GET"])
def get_product_handler(product_id):
    """ get product

    GET /product/<product_id>

    :return: {
        id: product id
        attribute: value
    }
    """
    get_current_user()
    return jsonify(get_product(product_id))
