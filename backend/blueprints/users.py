from flask import Blueprint, request, jsonify, abort

from blueprints.utils import get_current_user, multidict_to_dict
from models.auth import create_password, set_password
from models.functions import execute_function
from models.users import create_user, delete_user, get_user, get_users, update_user

blueprint = Blueprint("users", __name__, url_prefix="/api/users")


@blueprint.route("", methods=['POST'])
def create_user_handler():
    """ Add a new user
    POST /users
    data: {
        email: user email
        name: username
        password: user password (optional)
        attribute: value
    }
    :return: {
        id: user id
        email: user email
        name: username
        attribute: value
    }
    """
    current_user = get_current_user()
    user_data = request.get_json()
    password = user_data.get("password")
    if current_user.get("administrator", False):
        user = create_user(user_data)
        if password:
            set_password(user, password)
        else:
            password = create_password()
            set_password(user, password)
            execute_function(
                "functions.email.send_mail",
                args={
                    "to": user["email"],
                    "subject": "Watchtime: Bem-vindo {}".format(user["name"]),
                    "template": "signin",
                    "name": user["name"],
                    "password": password
                }
            )
        return jsonify(user)
    abort(403)


@blueprint.route("<user_id>", methods=['PATCH'])
def update_user_handler(user_id):
    """ update user based on given data
    PATCH /users/<user_id>
    data: {
        attribute: value
    }

    :return: {
        id: user id
        email: user email
        name: user name
        attribute: value
    }
    """
    current_user = get_current_user()
    data = request.get_json()
    if current_user.get("administrator", False):
        user = get_user(user_id)
        if user:
            if current_user["id"] == user["id"] and "administrator" in data:
                del data["administrator"]
                del data["enabled"]
            password = data.pop("password") if "password" in data else None
            if password:
                set_password(user, password)
            return jsonify(update_user({**user, **data}))
    elif user_id == current_user["id"]:
        if "roles" in data:
            del data["roles"]
        return jsonify(update_user({**current_user, **data}))
    abort(403)


@blueprint.route("<user_id>", methods=['DELETE'])
def delete_user_handler(user_id):
    """ Delete user based on the given user id
    DELETE /users/<user_id>

    :return: None
    """
    current_user = get_current_user()
    if user_id != current_user["id"] and current_user.get("administrator", False):
        user = get_user(user_id)
        if user:
            delete_user(user)
            return jsonify(), 204
    abort(403)


@blueprint.route("", methods=['GET'])
def get_users_handler():
    """ Get all users
    GET /users

    :return: [
        {
            id: user id
            email: user email
            name: user name
            attribute: value
        }
    ]
    """
    current_user = get_current_user()
    if current_user.get("administrator", False):
        filters = multidict_to_dict(request.args)
        return jsonify(get_users(filters=filters))
    abort(403)


@blueprint.route("<user_id_email>", methods=['GET'])
def get_user_handler(user_id_email):
    """ Get a user based on the given user id or email
    GET /users/<user_id_email>

    :return: {
        id: user id
        email: user email
        name: user name
        attribute: value
    }
    """
    current_user = get_current_user()
    user = get_user(user_id=user_id_email)
    if not user:
        user = get_user(email=user_id_email)
    if current_user.get("administrator", False):
        return jsonify(user)
    elif user["id"] == current_user["id"]:
        return jsonify(current_user)
    abort(403)
