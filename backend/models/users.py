import json
import uuid

from models import execute, fetchall, fetchone
from models.sql import build_where, build_order
from utils import required, clean_dict

FIELDS = ["id", "email", "data"]


def create_user(user):
    """ Create user based on the given user data

    :param user: {
        id: user id
        name: username
        email: user email
        attribute: value
    }
    :return: {
        id: user id
        name: username
        email: user email
        attribute: value
    }
    """
    required(user, ["name", "email"])
    if "id" not in user:
        user["id"] = uuid.uuid4().hex
    if has_user_id(user["id"]):
        raise Exception("User '{}' already exists".format(user["id"]))
    if has_user_email(user["email"]):
        raise Exception("User email '{}' already in use".format(user["email"]))
    if "roles" in user:
        if not isinstance(user["roles"], list):
            raise Exception("roles should be a list")
    user_copy = user.copy()
    user_id = user_copy.pop("id")
    user_email = user_copy.pop("email")
    user_copy["enabled"] = user_copy.get("enabled", True)
    user_copy["roles"] = user_copy.get("roles", list())
    if "password" in user_copy:
        del user_copy["password"]
    execute(f"insert into watchtime.users (id, email, data) values (%s, %s, %s)", user_id, user_email, json.dumps(user_copy))
    return get_user(user_id=user["id"])


def get_users(with_password=False, filters=None):
    """ Get all users of the given domain id

    :param with_password: if True, return the password along with users (default is False)
    :param filters: dict of filters to be applied to users
    :return: [
        {
            id: user id
            name: user name
            email: user email
            attribute: value
        }
    ]
    """
    if not filters:
        filters = dict()
    users = list()
    for row in fetchall("select id, email, data from watchtime.users {} {}".format(build_where(FIELDS, filters), build_order(FIELDS, filters))):
        if not with_password and "password" in row[2]:
            del row[2]["password"]
        users.append({"id": row[0], "email": row[1], **row[2]})
    return users


def get_user(user_id=None, email=None, with_password=False):
    if user_id:
        row = fetchone(f"select id, email, data from watchtime.users where id=%s", user_id)
    elif email:
        row = fetchone(f"select id, email, data from watchtime.users where email=%s", email)
    else:
        raise Exception("id or email required")
    if not row:
        return None
    if not with_password and "password" in row[2]:
        del row[2]["password"]
    return {**{"id": row[0], "email": row[1]}, **row[2]}


def update_user(user):
    required(user, ['id'])
    stored_user = get_user(user["id"], with_password=True)
    if not stored_user:
        raise Exception("User not found")
    if "email" in user:
        user_by_email = get_user(email=user["email"])
        if user_by_email and user_by_email["id"] != user["id"]:
            raise Exception("Email '{}' already in use".format(user["email"]))
    if "password" in user:
        del user["password"]
    stored_user.update(user)
    user_id = stored_user.pop("id")
    email_id = stored_user.pop("email")
    clean_dict(stored_user)
    execute(f"update watchtime.users set email = %s, data = %s where id=%s", email_id, json.dumps(stored_user), user_id)
    return get_user(user["id"])


def delete_user(user):
    store_user = get_user(user["id"])
    if store_user:
        execute(f"delete from watchtime.users where id=%s", user["id"])


def has_user_id(user_id):
    return fetchone(f"select count(*) from watchtime.users where id=%s", user_id)[0] == 1


def has_user_email(user_email):
    return fetchone(f"select count(*) from watchtime.users where email=%s", user_email)[0] == 1
