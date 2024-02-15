import codecs
import datetime
import glob
import json
import uuid

from psycopg2 import Binary

from models import execute, fetchall, fetchone
from utils import required, clean_dict


def get_static_resources():
    resources = dict()
    base_dir = './resources'
    for file_name in glob.glob(base_dir + '/**/*.json', recursive=True):
        with codecs.open(file_name, "r", "utf-8") as f:
            resource = json.load(f)
            resource['static'] = True
        resource_id = file_name.replace('\\', '.').replace('/', '.').replace('resources.', '').replace('json', '').strip('.')
        resources[resource_id] = resource
    return resources


def get_static_resource(resource_id):
    try:
        with codecs.open('./resources/{}.json'.format(resource_id.replace('.', '/')), "r", "utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def create_resource(resource, stream=None):
    """ Create a resource

    :param resource: {
        "id": resource id (if not present, id will be created)
        "attribute": any attribute
    }
    :param stream: binary content
    :return:
    """
    if "id" in resource:
        if has_resource(resource["id"]):
            raise Exception("resource '{}' already exists".format(resource["id"]))
    else:
        resource["id"] = uuid.uuid4().hex
    resource_id = resource.pop("id")
    resource["created"] = datetime.datetime.utcnow().isoformat()
    execute("insert into watchtime.resources (id, data) values (%s, %s)", resource_id, json.dumps(resource))
    if stream:
        execute("insert into watchtime.files (id, file) values (%s, %s)", resource_id, Binary(stream.read()))
    resource["id"] = resource_id
    return resource


def update_resource(resource, exact=False):
    required(resource, ["id"])
    stored_resource = get_resource(resource["id"])
    if not stored_resource:
        return create_resource(resource)
    stored_resource.update(resource)
    resource_id = stored_resource.pop("id")
    stored_resource["updated"] = datetime.datetime.utcnow().isoformat()
    if not exact:
        clean_dict(stored_resource)
    execute("update watchtime.resources set data=%s where id=%s", json.dumps(stored_resource), resource_id)
    stored_resource["id"] = resource_id
    return stored_resource


def delete_resource(resource_id):
    execute("delete from watchtime.resources where id=%s", resource_id)
    execute("delete from watchtime.files where id=%s", resource_id)


def get_resources(static=False, resource_type=None):
    if static:
        resources = [{"id": resource_id, **resource} for resource_id, resource in get_static_resources().items()]
    else:
        resources = list()
    for row in fetchall("select id, data from watchtime.resources"):
        resources.append({"id": row[0], **row[1]})
    if resource_type:
        return [resource for resource in resources if resource.get("type") == resource_type]
    else:
        return resources


def get_resource(resource_id):
    resource = get_static_resource(resource_id)
    if resource:
        return resource
    row = fetchone("select id, data from watchtime.resources where id=%s", resource_id)
    if row:
        return {"id": row[0], **row[1]}
    return None


def get_resource_stream(resource_id):
    row = fetchone("select file from watchtime.files where id=%s", resource_id)
    if not row:
        return None
    return row[0]


def delete_resources():
    execute("delete from watchtime.resources")
    execute("delete from watchtime.files")


def has_resource(resource_id):
    return fetchone("select count(*) from watchtime.resources where id=%s", resource_id)[0] == 1


def has_resource_stream(resource_id):
    return fetchone("select count(*) from watchtime.files where id=%s", resource_id)[0] == 1
