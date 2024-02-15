import io
import unittest

from app import app
from models.auth import set_password
from models.resources import get_resources, delete_resource
from models.users import create_user, delete_user

resources = [
    {"id": "r" + str(i), "type": "resource", "attribute1": "value1"}
    for i in range(3)
]


class TestResources(unittest.TestCase):
    def setUp(self):
        self.api = app.test_client()
        self.user = create_user({"email": "admin@test", "name": "Admin User", "roles": ["admin"]})
        set_password(self.user, "pass")
        response = self.api.post("/api/auth/login", json={"email": "admin@test", "password": "pass"})
        self.assertEqual(200, response.status_code)
        self.token = response.json["token"]
        self.headers = {"Authorization": "Bearer " + self.token}

    def tearDown(self):
        for resource in get_resources():
            delete_resource(resource["id"])
        delete_user(self.user)

    def test_crud(self):
        for i in range(len(resources)):
            response = self.api.post("/api/resources", headers=self.headers, json=resources[i])
            self.assertEqual(200, response.status_code)
            resources[i] = response.json

        response = self.api.get("/api/resources?type=resource", headers=self.headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual(resources, response.json)

        response = self.api.get("/api/resources/" + resources[0]["id"], headers=self.headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual(resources[0], response.json)

        response = self.api.post("/api/resources", headers=self.headers, json={"id": "r1", "type": "resource"})
        self.assertEqual(500, response.status_code)

        response = self.api.patch("/api/resources/" + resources[0]["id"], headers=self.headers, json={"attribute2": "value2"})
        self.assertEqual(200, response.status_code)

        response = self.api.get("/api/resources/" + resources[0]["id"], headers=self.headers)
        self.assertEqual(200, response.status_code)
        self.assertIn("attribute2", response.json)
        self.assertEqual("value2", response.json["attribute2"])

        response = self.api.patch("/api/resources/" + resources[0]["id"], headers=self.headers, json={"attribute1": None})
        self.assertEqual(200, response.status_code)
        response = self.api.get("/api/resources/" + resources[0]["id"], headers=self.headers)
        self.assertEqual(200, response.status_code)
        self.assertNotIn("attribute1", response.json)

        response = self.api.delete("/api/resources/" + resources[0]["id"], headers=self.headers)
        self.assertEqual(204, response.status_code)
        response = self.api.get("/api/resources", headers=self.headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.json))

    def test_stream(self):
        with open("test/files/products.xls", "rb") as file:
            binary = file.read()
        response = self.api.post("/api/resources", headers=self.headers, data={
            "file": (io.BytesIO(binary), "products.xls", "application/vnd.ms-excel"),
            "attr1": "value1",
            "attr2": ["value1", "value2"]
        })
        self.assertEqual(200, response.status_code)

        response = self.api.get("/api/resources/" + response.json["id"], headers=self.headers)
        self.assertEqual("value1", response.json["attr1"])
        self.assertEqual(["value1", "value2"], response.json["attr2"])

        response = self.api.get("/api/resources/" + response.json["id"] + "/stream", headers=self.headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/vnd.ms-excel", response.headers["content-type"])
        self.assertEqual(binary, response.get_data())
