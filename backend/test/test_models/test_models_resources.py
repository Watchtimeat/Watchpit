import io

from models.resources import create_resource, delete_resource, get_resource, get_resources, update_resource, get_resource_stream, has_resource, has_resource_stream
import unittest

resources = [
    {"id": "r" + str(i), "type": "resource", "attribute1": "value1"}
    for i in range(3)
]


class TestResources(unittest.TestCase):

    def test_crud(self):
        for resource in resources:
            create_resource(resource)
        try:
            self.assertEqual(resources[0], get_resource(resources[0]["id"]))
            self.assertEqual(resources, get_resources())
            for resource in resources:
                self.assertTrue(has_resource(resource["id"]))

            with self.assertRaises(Exception):
                create_resource({"id": "r1", "type": "resource"})
            resources[0]["attribute2"] = "value2"
            update_resource(resources[0])
            resource = get_resource(resources[0]["id"])
            self.assertEqual("value2", resource["attribute2"])

            update_resource({"id": resources[0]["id"], "attribute1": None})
            resource = get_resource(resources[0]["id"])
            self.assertNotIn("attribute1", resource)
        finally:
            for resource in get_resources():
                delete_resource(resource["id"])

    def test_crud_stream(self):
        binary = b'content'
        create_resource({
            "id": "r0",
            "type": "binary"
        }, stream=io.BytesIO(binary))
        try:
            self.assertTrue(has_resource_stream("r0"))
            resource = get_resource("r0")
            self.assertEqual("r0", resource["id"])
            self.assertEqual("binary", resource["type"])
            self.assertEqual(binary, io.BytesIO(get_resource_stream("r0")).read())
        finally:
            delete_resource("r0")
