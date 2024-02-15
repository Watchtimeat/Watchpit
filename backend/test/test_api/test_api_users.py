import unittest

from app import app
from models.auth import set_password
from models.users import create_user, delete_user, get_users


class TestUsers(unittest.TestCase):

    def setUp(self) -> None:
        self.api = app.test_client()

    def test_users(self):
        self.admin = create_user({"email": "admin@test", "name": "Admin User", "administrator": True})
        set_password(self.admin, "pass")
        try:
            response = self.api.post("/api/auth/login", json={"email": "admin@test", "password": "pass"})
            self.assertEqual(200, response.status_code)
            token = response.json["token"]
            headers = {"Authorization": "Bearer " + token}

            response = self.api.post("/api/users", headers=headers, json={"email": "user@test", "name": "User", "password": "pass"})
            self.assertEqual(200, response.status_code)
            if response.status_code == 200:
                user = response.json

                response = self.api.get("/api/users/" + user["id"], headers=headers)
                self.assertEqual(200, response.status_code)
                self.assertEqual(user["id"], response.json["id"])

                response = self.api.patch("/api/users/" + user["id"], headers=headers, json={"name": "User (updated)"})
                self.assertEqual(200, response.status_code)
                self.assertEqual("User (updated)", response.json["name"])

                self.api.delete("/api/users/" + user["id"], headers=headers)
                self.assertEqual(200, response.status_code)
        finally:
            for u in get_users():
                if u["email"] in ["admin@test", "user@test"]:
                    delete_user(u)
