import datetime
import json
import re

NAME_PATTERN = re.compile('([a-z])([a-z0-9_])+')
PDATE_DICT_COMMANDS = {
    "$set": "$set",
    "$del": "$del",
    "$append": "$append",
    "$remove": "$remove"
}


def is_name_valid(name, min_len=3):
    return len(name) >= min_len and NAME_PATTERN.match(name.lower()) is not None


def jsonprint(*args):
    for arg in args:
        print(json.dumps(arg, indent=4))


def required(data, keys):
    for key in keys:
        if key not in data:
            raise Exception(f"'{key}' is required")


def not_allowed(data, keys):
    for key in data:
        if key in keys:
            raise Exception(f"'{key}' not allowed")


def isoformat(date: datetime.datetime) -> str:
    return date.isoformat() if date else None


def update_dict(dictionary, updates):
    """

    :param dictionary: dict
    :param updates: {
        "$add": dict,
        "$set": dict,
        "$del": key | [ key ]
        "$append": element
        "$remove": index | [ indexes ]
    }
    :return: dict
    """
    if isinstance(updates, dict):
        for key, value in updates.items():
            if key == "$add" and isinstance(dictionary, dict) and isinstance(value, dict):
                for k, v in value.items():
                    if k not in dictionary:
                        dictionary[k] = v
            elif key == "$set" and isinstance(value, dict):
                for k, v in value.items():
                    if k in dictionary:
                        dictionary[k] = v
            elif key == "$del":
                for k in value if isinstance(value, list) else [value]:
                    if k in dictionary:
                        del dictionary[k]
            elif key == '$append' and isinstance(dictionary, list):
                if isinstance(value, list):
                    dictionary.extend(value)
                else:
                    dictionary.append(value)
            elif isinstance(dictionary, dict) and key in dictionary:
                dictionary[key] = update_dict(dictionary[key], value)
    return dictionary


def merge_dicts(destination, source):
    """ merge dicts recursively

    :param destination: destination dict
    :param source: source dict
    :return: destination dict
    """
    if isinstance(source, dict) and isinstance(destination, dict):
        for key in source:
            if isinstance(source[key], dict) and key in source and key in destination:
                destination[key] = merge_dicts(destination[key], source[key])
            else:
                destination[key] = source[key]
    else:
        destination = source
    return destination


def clean_dict(data):
    """ Recursively remove keys if value is None

    :param data: dict
    :return: None
    """
    if isinstance(data, dict):
        copy = data.copy()
        for key, value in copy.items():
            if value is None:
                del data[key]
            elif isinstance(value, dict):
                clean_dict(data[key])
            elif isinstance(value, list):
                for e in value:
                    clean_dict(e)
