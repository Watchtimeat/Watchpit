import traceback

from flask import Blueprint, request, jsonify

from blueprints.utils import get_current_user
from models.functions import execute_function

blueprint = Blueprint("functions", __name__, url_prefix="/api/functions")


@blueprint.route("execute", methods=["POST"])
def execute_function_handler():
    """ execute function

    POST /functions/execute

s    :body: {
        name: function name,
        args: args object (optional)
    }

    :return: function's response
    """
    get_current_user()
    data = request.get_json()
    try:
        return jsonify(execute_function(data["name"], args=data.get("args")))
    except Exception as e:
        return jsonify({
            "message": str(e),
            "stacktrace": traceback.format_exc()
        }), 500
    

    
