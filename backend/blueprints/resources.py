from flask import Blueprint, request, jsonify, abort, make_response

from blueprints.utils import get_current_user
from models.resources import delete_resource, update_resource, get_resource, get_resource_stream, get_resources, create_resource

blueprint = Blueprint("resources", __name__, url_prefix="/api/resources")


@blueprint.route("", methods=["POST"])
def create_resource_handler():
    """ create resource based on the given card resource

    POST /resources

    body: {
        attribute: value
    }

    :return: None
    """
    get_current_user()
    if len(request.files) == 1:
        file = request.files[list(request.files.keys())[0]]
        resource = dict()
        resource["name"] = file.filename if file.filename != "" else "noname"
        resource["content_type"] = file.content_type
        for item in request.form:
            value = request.form.getlist(item)
            resource[item] = value[0] if len(value) == 1 else value
        return jsonify(create_resource(resource, stream=file.stream))
    else:
        resource = request.get_json()
        if resource:
            return jsonify(create_resource(resource))
    abort(403)


@blueprint.route("<resource_id>", methods=["PATCH"])
def update_resource_handler(resource_id):
    """ update resource

    PUT /resources/<resource_id>

    :body: {
        attribute: value
    }

    :return: {
        id: resource id
        attribute: value
    }
    """
    get_current_user(request)
    return jsonify(update_resource({**request.get_json(), "id": resource_id}))


@blueprint.route("<resource_id>", methods=["DELETE"])
def delete_resource_handler(resource_id):
    """ delete resource
    
    DELETE /resources/<resource_id>

    :return: None
    """
    get_current_user()
    delete_resource(resource_id)
    return jsonify(), 204


@blueprint.route("", methods=["GET"])
def get_resources_handler():
    """ get resources

    GET /resources

    parameters:
        type: type
        static: boolean (default is false)

    :return: [
        {
            id: resource id
            attribute: value
        }
    ]
    """
    get_current_user(request)
    return jsonify(
        get_resources(
            resource_type=request.args.get("type"),
            static=request.args.get("static", "false") == "true"
        )
    )


@blueprint.route("<resource_id>", methods=["GET"])
def get_resource_handler(resource_id):
    """ get resource

    GET /resources/<resource_id>

    :return: {
        id: resource id
        attribute: value
    }
    """
    get_current_user()
    return jsonify(get_resource(resource_id))


@blueprint.route("<resource_id>/stream", methods=["GET"])
def get_resource_stream_handler(resource_id):
    """ get resource stream

    GET /resources/<resource_id>/stream

    :return: stream
    """
    get_current_user()
    resource = get_resource(resource_id)
    stream = get_resource_stream(resource_id)
    if resource and stream:
        response = make_response(stream.tobytes())
        response.mimetype = resource.get("content_type", "application/octet-stream")
        response.headers["Content-disposition"] = "attachment; filename={}".format(resource.get("name", "noname"))
        return response
    abort(403)
