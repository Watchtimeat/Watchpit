import datetime

import pytz
from flask import Blueprint, request, jsonify, abort

from blueprints.utils import jwt_encode, get_current_user
from models.auth import check_password, set_password
from models.users import get_user, update_user

blueprint = Blueprint("auth", __name__, url_prefix="/api/auth")


@blueprint.route('/login', methods=['POST'])
def login_handler():
    """ Login the given user

    POST /auth/login

    data: {
        email: user email,
        password: user password,
        remember: true/false
    }

    :return: {
        token: JWT token
    }
    """
    data = request.get_json()
    if data:
        email = data.get("email")
        password = data.get("password")
        if email and password:
            user = get_user(email=email)
            if user and user.get("enabled", False) and check_password(user, password):
                update_user({"id": user["id"], "last_login": pytz.utc.localize(datetime.datetime.utcnow()).isoformat()})
                return jsonify(token=jwt_encode(user["id"]))
            abort(401, "Usuário ou senha inválidos")
    abort(400)


@blueprint.route('/user', methods=['GET'])
def current_user_handler():
    """ Get the current user

    GET /auth/user

    :return: user object
    """
    return jsonify(get_current_user(required=False))


@blueprint.route('/password', methods=['POST'])
def update_password_handler():
    """ Update current user password

    POST /auth/password

    data: {
        current: current password
        new: new password
    }

    :return: None
    """
    current_user = get_current_user(required=True)
    data = request.get_json()
    if data:
        current_password = data.get("current")
        new_password = data.get("new")
        if current_password and new_password:
            user = get_user(current_user["id"])
            if user and check_password(user, current_password):
                set_password(user, new_password)
                return jsonify(), 204
            abort(401, description="Usuário ou senha inválidos")
    abort(400)
