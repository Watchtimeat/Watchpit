import importlib


def execute_function(name, args=None):
    try:
        print("execute_function:", name, args)
        parts = name.split(".")
        if len(parts) < 2 or parts[0] != "functions":  # function name should be function.<function name> or functions.<package>.<function name>
            raise Exception("malformed function name '{}'".format(name))
        module = importlib.import_module(".".join(parts[:-1]))
        function_instance = getattr(module, parts[-1])
        if isinstance(args, dict):
            response = function_instance(**args)
        else:
            response = function_instance()
        return response
    except Exception as e:
        raise e
