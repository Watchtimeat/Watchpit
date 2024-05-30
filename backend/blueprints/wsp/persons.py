from flask import Blueprint, request, jsonify, abort

from blueprints.utils import get_current_user, multidict_to_dict
from models.persons import create_person, get_persons, get_person, update_person, delete_person, create_persons

blueprint = Blueprint("persons", __name__, url_prefix="/api/persons")


@blueprint.route("", methods=["POST"])
def create_person_handler():
    """ create person based on the given data

    POST /persons

    body: {
        attribute: value
    }

    :return: None
    """
    get_current_user()
    data = request.get_json()
    if isinstance(data, list):
        return jsonify(create_persons(data))
    elif isinstance(data, object):
        return jsonify(create_person(data))
    abort(400)


@blueprint.route("<person_id>", methods=["PATCH"])
def update_person_handler(person_id):
    """ update person

    PUT /persons/<person_id>

    :body: {
        attribute: value
    }

    :return: {
        id: person id
        attribute: value
    }
    """
    get_current_user()
    return jsonify(update_person({**request.get_json(), "id": person_id}))


@blueprint.route("<person_id>", methods=["DELETE"])
def delete_person_handler(person_id):
    """ delete person

    DELETE /persons/<person_id>

    :return: None
    """
    get_current_user()
    delete_person(person_id)
    return jsonify(), 204


@blueprint.route("", methods=["GET"])
def get_persons_handler():
    """ get persons

    GET /persons

    parameters:
        <field>: <value>

    :return: [
        {
            id: person id
            attribute: value
        }
    ]
    """
    get_current_user()
    filters = multidict_to_dict(request.args)
    return jsonify(get_persons(filters))


@blueprint.route("<person_id>", methods=["GET"])
def get_person_handler(person_id):
    """ get person

    GET /person/<person_id>

    :return: {
        id: person id
        attribute: value
    }
    """
    get_current_user()
    return jsonify(get_person(person_id))
