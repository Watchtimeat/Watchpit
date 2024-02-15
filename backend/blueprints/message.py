from models.functions import execute_function


def message_handler(message) -> None:
    if "name" not in message:
        raise Exception("function name required in '{}'".format(message))
    execute_function(message["name"], message.get("args"))
