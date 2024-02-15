import unittest

from app import app
from models.auth import set_password
from models.users import create_user, delete_user, get_users


class TestAuth(unittest.TestCase):

    def setUp(self) -> None:
        self.api = app.test_client()

    def test_authentication_cycle(self):
        user = create_user({"email": "admin1@test", "name": "Administrator", "administrator": True, "roles": []})
        set_password(user, "pass")
        try:
            response = self.api.post("/api/auth/login", json={"email": "admin1@test", "password": "pass"})
            self.assertEqual(200, response.status_code)
            headers_admin1 = {"Authorization": "Bearer " + response.json["token"]}

            response = self.api.get("/api/auth/user", headers=headers_admin1)
            self.assertEqual(200, response.status_code)
            admin1 = response.json

            response = self.api.post("/api/auth/password", headers=headers_admin1, json={"current": "pass", "new": "newpass"})
            self.assertEqual(204, response.status_code)

            response = self.api.post("/api/auth/login", json={"email": admin1["email"], "password": "newpass"})
            self.assertEqual(200, response.status_code)
            headers_admin1 = {"Authorization": "Bearer " + response.json["token"]}

            response = self.api.post("/api/users", headers=headers_admin1, json={"email": "admin2@test", "name": "Administtrator 2", "administrator": True, "roles": [], "password": "pass"})
            self.assertEqual(200, response.status_code)
            admin2 = response.json

            response = self.api.post("/api/users", headers=headers_admin1, json={"email": "regular@test", "name": "Regular User", "roles": [], "password": "pass"})
            self.assertEqual(200, response.status_code)
            regular = response.json

            response = self.api.post("/api/auth/login", json={"email": "regular@test", "password": "pass"})
            self.assertEqual(200, response.status_code)
            headers_regular = {"Authorization": "Bearer " + response.json["token"]}

            response = self.api.get("/api/users", headers=headers_regular)
            self.assertEqual(403, response.status_code)

            response = self.api.get("/api/users/" + admin1["id"], headers=headers_regular)
            self.assertEqual(403, response.status_code)

            response = self.api.get("/api/users/" + regular["id"], headers=headers_regular)
            self.assertEqual(200, response.status_code)
            regular = response.json

            response = self.api.delete("/api/users/" + regular["id"], headers=headers_regular)
            self.assertEqual(403, response.status_code)

            response = self.api.delete("/api/users/" + admin2["id"], headers=headers_regular)
            self.assertEqual(403, response.status_code)

            response = self.api.get("/api/users", headers=headers_admin1)
            self.assertEqual(200, response.status_code)

            response = self.api.get("/api/users/" + admin1["id"], headers=headers_admin1)
            self.assertEqual(200, response.status_code)

            response = self.api.get("/api/users/" + regular["id"], headers=headers_admin1)
            self.assertEqual(200, response.status_code)

            response = self.api.delete("/api/users/" + admin2["id"], headers=headers_admin1)
            self.assertEqual(204, response.status_code)

            response = self.api.delete("/api/users/" + regular["id"], headers=headers_admin1)
            self.assertEqual(204, response.status_code)

        finally:
            for u in get_users():
                if u["email"] in ["admin1@test", "admin2@test", "regular@test"]:
                    delete_user(u)
