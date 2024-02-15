from flask import Blueprint, request, jsonify, abort

from blueprints.utils import get_current_user, multidict_to_dict
from models.purchase_orders import create_purchase_order, update_purchase_order, delete_purchase_order, get_purchase_order, get_purchase_orders, get_purchase_orders_summary, get_product_resquested_quantity,get_purchase_order_for_invoice,import_purchase_order_items
from models.purchase_orders import consulta_pedidos_peca
from models.forecast import gera_algoritimo
blueprint = Blueprint("purchase_orders", __name__, url_prefix="/api/purchase_orders")


@blueprint.route("", methods=["POST"])
def create_purchase_order_handler():
    """ create purchase order based on the given data

    POST /purchase_orders

    body: {
        attribute: value
        items: [
            attribute: value
        ]
    }

    :return: None
    """
    current_user = get_current_user()
    data = request.get_json()
    data["owner"] = current_user["name"]
    if data:
        return jsonify(create_purchase_order(data))
    abort(403)

@blueprint.route("order_by_planner", methods=["POST"])
def create_purchase_order_planner_handler():
    """ create purchase order based on the given data

    POST /purchase_orders

    body: {
        attribute: value
        items: [
            attribute: value
        ]
    }

    :return: None
    """
    data = request.get_json()
    if data:
        return jsonify(gera_algoritimo(data["brand"],data["first_period"],data["last_period"],data["month_forecast"],data["owner"]))
    abort(403)

@blueprint.route("<purchase_order_id>", methods=["PATCH"])
def update_purchase_order_handler(purchase_order_id):
    """ update purchase order

    PUT /purchase_orders/<purchase_order_id>

    :body: {
        attribute: value
    }

    :return: {
        id: product id
        attribute: value
        items: [
            attribute: value
        ]
    }
    """
    get_current_user()
    return jsonify(update_purchase_order({**request.get_json(), "id": purchase_order_id}))


@blueprint.route("<purchase_order_id>", methods=["DELETE"])
def delete_purchase_order_handler(purchase_order_id):
    """ delete purchase order

    DELETE /purchase_orders/<purchase_order_id>

    :return: None
    """
    get_current_user()
    delete_purchase_order(purchase_order_id)
    return jsonify(), 204


@blueprint.route("summary/<column>", methods=["GET"])
def get_purchase_orders_summary_handler(column):
    """ get purchase orders summary

    GET /purchase_orders/summary/<column>

    parameters:
        <field>: <value>

    :return: { <column>: number of puchase orders }
    """
    get_current_user()
    filters = multidict_to_dict(request.args)
    return jsonify(get_purchase_orders_summary(column, filters))


@blueprint.route("", methods=["GET"])
def get_purchase_orders_handler():
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
    return jsonify(get_purchase_orders(filters))


@blueprint.route("<purchase_order_id>", methods=["GET"])
def get_purchase_order_handler(purchase_order_id):
    """ get purchase order

    GET /purchase_orders/<purchase_order_id>

    :return: {
        id: purchase order id
        attribute: value
        items: [
            attribute: value
        ]
    }
    """
    get_current_user()
    return jsonify(get_purchase_order(purchase_order_id))


@blueprint.route("requested_quantity/", methods=["GET"])
def get_product_resquested_quantity_handler():
    """ get purchase order

    GET /purchase_orders/<purchase_order_id>

    :return: {
        id: purchase order id
        attribute: value
        items: [
            attribute: value
        ]
    }
    """
    data = request.get_json()
    get_current_user()
    return jsonify(get_product_resquested_quantity(data["product_code"]))


@blueprint.route("<purchase_order_id>/invoice", methods=["GET"])
def get_purchase_order_handler_invoice(purchase_order_id):
    """ get purchase order

    GET /purchase_orders/<purchase_order_id>/invoice

    :return: {
        id: purchase order id
        attribute: value
        items: [
            attribute: value
        ]
    }
    """
    get_current_user()
    return jsonify(get_purchase_order_for_invoice(purchase_order_id))


@blueprint.route("<purchase_order_id>/import_excel", methods=["POST"])
def import_purchase_order_items_handler(purchase_order_id):
    """ get purchase order

    GET /purchase_orders/<purchase_order_id>/invoice

    :return: {
        id: purchase order id
        attribute: value
        items: [
            attribute: value
        ]
    }
    """
    file = request.files['file']
    return jsonify(import_purchase_order_items(purchase_order_id,file))


@blueprint.route("consulta_pedidos", methods=["POST"])
def consulta_pedidos_handler():
    """ get purchase order

    GET /purchase_orders/<purchase_order_id>/invoice

    :return: {
        id: purchase order id
        attribute: value
        items: [
            attribute: value
        ]
    }
    """
    data = request.get_json()
    return jsonify(consulta_pedidos_peca(data["code"]))