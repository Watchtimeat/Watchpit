from flask import Blueprint, request, jsonify, abort

from blueprints.utils import get_current_user, multidict_to_dict
from models.watches import create_watch, get_watches, get_watch, update_watch, delete_watch, create_watches

blueprint = Blueprint("watches", __name__, url_prefix="/api/watches")


@blueprint.route("", methods=["POST"])
def create_watch_handler():
    """ create watch based on the given data

    POST /watches

    body: {
        attribute: value
    }

    :return: None
    """
    get_current_user()
    data = request.get_json()
    if isinstance(data, list):
        return jsonify(create_watches(data))
    elif isinstance(data, object):
        return jsonify(create_watch(data))
    abort(400)


@blueprint.route("<watch_id>", methods=["PATCH"])
def update_watch_handler(watch_id):
    """ update watch

    PUT /watches/<watch_id>

    :body: {
        attribute: value
    }

    :return: {
        id: watch id
        attribute: value
    }
    """
    get_current_user()
    return jsonify(update_watch({**request.get_json(), "id": watch_id}))


@blueprint.route("<watch_id>", methods=["DELETE"])
def delete_watch_handler(watch_id):
    """ delete watch

    DELETE /watches/<watch_id>

    :return: None
    """
    get_current_user()
    delete_watch(watch_id)
    return jsonify(), 204


@blueprint.route("", methods=["GET"])
def get_watches_handler():
    """ get watches

    GET /watches

    parameters:
        <field>: <value>

    :return: [
        {
            id: watch id
            attribute: value
        }
    ]
    """
    get_current_user()
    filters = multidict_to_dict(request.args)
    return jsonify(get_watches(filters))


@blueprint.route("<watch_id>", methods=["GET"])
def get_watch_handler(watch_id):
    """ get watch

    GET /watch/<watch_id>

    :return: {
        id: watch id
        attribute: value
    }
    """
    get_current_user()
    return jsonify(get_watch(watch_id))
