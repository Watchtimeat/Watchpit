import jwt
from flask import request, abort
from werkzeug.datastructures import MultiDict

from models.users import get_user

SECRET = "8229b2ebfb77f494ce5ad1ab5c12d00e50074bf0dddf539b257e2238e95175da"


def get_current_user(required=True) -> [None, dict]:
    token = request.headers.get("authorization")
    if token:
        user_id = jwt_decode(token.split("Bearer ", 1)[-1])
        if user_id:
            return get_user(user_id=user_id)
    if required:
        abort(401)
    else:
        return None


def jwt_encode(payload: str) -> str:
    return jwt.encode({"payload": payload}, SECRET, algorithm="HS256")


def jwt_decode(token: str) -> dict:
    return jwt.decode(token, SECRET, algorithms=["HS256"]).get("payload")


def multidict_to_dict(multidict: MultiDict) -> dict:
    return {e[0]: e[1] if len(e[1]) > 1 else e[1][0] for e in [e for e in zip(multidict.keys(), multidict.listvalues())]}
