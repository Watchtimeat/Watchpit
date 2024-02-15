import unittest

from app import app
from models.auth import set_password
from models.users import create_user, delete_user


class TestFunctions(unittest.TestCase):

    def setUp(self):
        self.api = app.test_client()
        self.user = create_user({"email": "admin@test", "name": "Administrator", "roles": ["admin"]})
        set_password(self.user, "pass")
        response = self.api.post("/api/auth/login", json={"email": "admin@test", "password": "pass"})
        self.assertEqual(200, response.status_code)
        self.token = response.json["token"]
        self.headers = {"Authorization": "Bearer " + self.token}

    def tearDown(self):
        delete_user(self.user)

    def test_execution_loopback(self):
        response = self.api.post("/api/functions/execute", headers=self.headers, json={
            "name": "functions.loopback",
            "args": {
                "attr": "value"
            }
        })
        self.assertEqual(200, response.status_code)
        self.assertEqual("value", response.json.get("attr"))

    def test_execution_loopback_sleep(self):
        response = self.api.post("/api/functions/execute", headers=self.headers, json={
            "name": "functions.loopback",
            "args": {
                "sleep": 1
            }
        })
        self.assertEqual(200, response.status_code)

    def test_execution_loopback_exception(self):
        response = self.api.post("/api/functions/execute", headers=self.headers, json={
            "name": "functions.loopback",
            "args": {
                "exception": "message"
            }
        })
        self.assertEqual(500, response.status_code)
        self.assertEqual("message", response.json["message"])
        self.assertIn("stacktrace", response.json)
