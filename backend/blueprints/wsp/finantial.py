from flask import Blueprint, request, jsonify, abort

from blueprints.utils import get_current_user, multidict_to_dict
from models.finantials import create_finantial, get_finantials, get_finantial, update_finantial, delete_finantial, create_finantials

blueprint = Blueprint("finantials", __name__, url_prefix="/api/finantials")


@blueprint.route("", methods=["POST"])
def create_finantial_handler():
    """ create finantial based on the given data

    POST /finantials

    body: {
        attribute: value
    }

    :return: None
    """
    get_current_user()
    data = request.get_json()
    if isinstance(data, list):
        return jsonify(create_finantials(data))
    elif isinstance(data, object):
        return jsonify(create_finantial(data))
    abort(400)


@blueprint.route("<finantial_id>", methods=["PATCH"])
def update_finantial_handler(finantial_id):
    """ update finantial

    PUT /finantials/<finantial_id>

    :body: {
        attribute: value
    }

    :return: {
        id: finantial id
        attribute: value
    }
    """
    get_current_user()
    return jsonify(update_finantial({**request.get_json(), "id": finantial_id}))


@blueprint.route("<finantial_id>", methods=["DELETE"])
def delete_finantial_handler(finantial_id):
    """ delete finantial

    DELETE /finantials/<finantial_id>

    :return: None
    """
    get_current_user()
    delete_finantial(finantial_id)
    return jsonify(), 204


@blueprint.route("", methods=["GET"])
def get_finantials_handler():
    """ get finantials

    GET /finantials

    parameters:
        <field>: <value>

    :return: [
        {
            id: finantial id
            attribute: value
        }
    ]
    """
    get_current_user()
    filters = multidict_to_dict(request.args)
    return jsonify(get_finantials(filters))


@blueprint.route("<finantial_id>", methods=["GET"])
def get_finantial_handler(finantial_id):
    """ get finantial

    GET /finantial/<finantial_id>

    :return: {
        id: finantial id
        attribute: value
    }
    """
    get_current_user()
    return jsonify(get_finantial(finantial_id))
