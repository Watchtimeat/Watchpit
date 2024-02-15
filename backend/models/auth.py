import hashlib
import hmac
import json
import string
import random
import typing as t

from models import execute, fetchone

SALT_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
DEFAULT_PBKDF2_ITERATIONS = 260000


def hash_internal(salt: str, password: str) -> t.Tuple[str, str]:
    iterations = DEFAULT_PBKDF2_ITERATIONS
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), iterations).hex(), f"pbkdf2:sha256:{iterations}"


def generate_password_hash(password: str, salt_length: int = 16) -> str:
    salt = "".join(random.SystemRandom().choice(SALT_CHARS) for _ in range(salt_length))
    h, method = hash_internal(salt, password)
    return f"{method}${salt}${h}"


def check_password_hash(pwhash: str, password: str) -> bool:
    if pwhash.count("$") < 2:
        return False
    method, salt, hashval = pwhash.split("$", 2)
    return hmac.compare_digest(hash_internal(salt, password)[0], hashval)


def create_password():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))


def set_password(user, password):
    password_hash = generate_password_hash(password)
    execute("update watchtime.users set data=data||%s where id=%s", json.dumps({"password": password_hash}), user["id"])


def check_password(user, password):
    row = fetchone("select data->>'password' from watchtime.users where id=%s", user["id"])
    if row and row[0] and check_password_hash(row[0], password):
        return True
    else:
        return False


def remove_password(user):
    execute("update watchtime.users set data=data-'password' where id=%s", user["id"])


def has_password(user):
    row = fetchone("select data->>'password' from watchtime.users where id=%s", user["id"])
    if row and row[0]:
        return True
    else:
        return False
