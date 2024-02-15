from flask import Blueprint, request, jsonify, abort

from blueprints.utils import get_current_user, multidict_to_dict
from models.purchase_invoices import create_purchase_invoice, update_purchase_invoice, delete_purchase_invoice, get_purchase_invoices_summary, get_purchase_invoices, get_purchase_invoice

blueprint = Blueprint("purchase_invoices", __name__, url_prefix="/api/purchase_invoices")


@blueprint.route("", methods=["POST"])
def create_purchase_invoice_handler():
    """ create purchase invoice based on the given data

    POST /purchase_invoices

    body: {
        attribute: value
        items: [
            attribute: value
        ]
    }

    :return: None
    """
    current_user = get_current_user()
    purchase_invoice = request.get_json()
    if purchase_invoice:
        purchase_invoice["owner"] = current_user["name"]
        return jsonify(create_purchase_invoice(purchase_invoice))
    abort(403)


@blueprint.route("<purchase_invoice_id>", methods=["PATCH"])
def update_purchase_invoice_handler(purchase_invoice_id):
    """ update purchase invoice

    PUT /purchase_invoices/<purchase_invoice_id>

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
    purchase_invoice = request.get_json()
    if purchase_invoice:
        return jsonify(update_purchase_invoice({"id": purchase_invoice_id, **request.get_json()}))
    abort(403)


@blueprint.route("<purchase_invoice_id>", methods=["DELETE"])
def delete_purchase_invoice_handler(purchase_invoice_id):
    """ delete purchase invoice

    DELETE /purchase_invoices/<purchase_invoice_id>

    :return: None
    """
    get_current_user()
    delete_purchase_invoice(purchase_invoice_id)
    return jsonify(), 204


@blueprint.route("summary/<column>", methods=["GET"])
def get_purchase_invoices_summary_handler(column):
    """ get purchase invoices summary

    GET /purchase_orders/summary/<column>

    parameters:
        <field>: <value>

    :return: { <column>: number of purchase invoices }
    """
    get_current_user()
    filters = multidict_to_dict(request.args)
    return jsonify(get_purchase_invoices_summary(column, filters))


@blueprint.route("", methods=["GET"])
def get_purchase_invoices_handler():
    """ get purchase invoices

    GET /purchase_invoices

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
    return jsonify(get_purchase_invoices(filters))


@blueprint.route("<purchase_invoice_id>", methods=["GET"])
def get_purchase_invoice_handler(purchase_invoice_id):
    """ get purchase invoice

    GET /purchase_invoices/<purchase_invoice_id>

    :return: {
        id: purchase invoice id
        attribute: value
        items: [
            attribute: value
        ]
    }
    """
    get_current_user()
    return jsonify(get_purchase_invoice(purchase_invoice_id))
