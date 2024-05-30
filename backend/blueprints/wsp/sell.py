from flask import Blueprint, request, jsonify, abort

from blueprints.utils import get_current_user, multidict_to_dict
from models.sells import create_sell, get_sells, get_sell, update_sell, delete_sell, create_sells

blueprint = Blueprint("sells", __name__, url_prefix="/api/sells")


@blueprint.route("", methods=["POST"])
def create_sell_handler():
    """ create sell based on the given data

    POST /sells

    body: {
        attribute: value
    }

    :return: None
    """
    get_current_user()
    data = request.get_json()
    if isinstance(data, list):
        return jsonify(create_sells(data))
    elif isinstance(data, object):
        return jsonify(create_sell(data))
    abort(400)


@blueprint.route("<sell_id>", methods=["PATCH"])
def update_sell_handler(sell_id):
    """ update sell

    PUT /sells/<sell_id>

    :body: {
        attribute: value
    }

    :return: {
        id: sell id
        attribute: value
    }
    """
    get_current_user()
    return jsonify(update_sell({**request.get_json(), "id": sell_id}))


@blueprint.route("<sell_id>", methods=["DELETE"])
def delete_sell_handler(sell_id):
    """ delete sell

    DELETE /sells/<sell_id>

    :return: None
    """
    get_current_user()
    delete_sell(sell_id)
    return jsonify(), 204


@blueprint.route("", methods=["GET"])
def get_sells_handler():
    """ get sells

    GET /sells

    parameters:
        <field>: <value>

    :return: [
        {
            id: sell id
            attribute: value
        }
    ]
    """
    get_current_user()
    filters = multidict_to_dict(request.args)
    return jsonify(get_sells(filters))


@blueprint.route("<sell_id>", methods=["GET"])
def get_sell_handler(sell_id):
    """ get sell

    GET /sell/<sell_id>

    :return: {
        id: sell id
        attribute: value
    }
    """
    get_current_user()
    return jsonify(get_sell(sell_id))
