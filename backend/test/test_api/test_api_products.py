import json
import unittest

from app import app
from models.auth import set_password
from models.products import delete_product
from models.users import create_user, delete_user

PRODUCTS = [
    {"id": "p" + str(i), "mode": "test", "brand": "brand", "name": "Product " + str(i)}
    for i in range(10)
]


class TestProducts(unittest.TestCase):
    def setUp(self):
        self.api = app.test_client()
        self.user = create_user({"email": "admin@test", "name": "Admin User", "enabled": True, "administrator": True})
        set_password(self.user, "pass")
        response = self.api.post("/api/auth/login", json={"email": "admin@test", "password": "pass"})
        self.token = response.json["token"]
        self.headers = {"Authorization": "Bearer " + self.token}

    def tearDown(self):
        delete_user(self.user)

    def test_crud(self):
        for i in range(len(PRODUCTS)):
            response = self.api.post("/api/products", headers=self.headers, json=PRODUCTS[i])
            self.assertEqual(200, response.status_code)
            PRODUCTS[i] = response.json
        try:
            response = self.api.get("/api/products?id=p0&id=p1", headers=self.headers)
            self.assertEqual(200, response.status_code)
            print(json.dumps(response.json, indent=4))

            response = self.api.get("/api/products?mode=test&name=Product 0", headers=self.headers)
            self.assertEqual(200, response.status_code)
            self.assertEqual(1, int(response.json["rows"]))
            self.assertEqual(PRODUCTS[0], response.json["data"][0])

            response = self.api.get("/api/products?mode=test&name=Product 0&name=Product 1", headers=self.headers)
            self.assertEqual(200, response.status_code)
            self.assertEqual(2, int(response.json["rows"]))

            response = self.api.get("/api/products?mode=test&_order_d=name", headers=self.headers)
            self.assertEqual(200, response.status_code)
            self.assertEqual(10, int(response.json["rows"]))
            self.assertEqual(PRODUCTS[-1], response.json["data"][0])

            response = self.api.get("/api/products?mode=test&_limit=3", headers=self.headers)
            self.assertEqual(200, response.status_code)
            self.assertEqual(10, int(response.json["rows"]))
            self.assertEqual(3, len(response.json["data"]))
            self.assertEqual(PRODUCTS[0], response.json["data"][0])

            response = self.api.get("/api/products?mode=test&_limit=3&_offset=3", headers=self.headers)
            self.assertEqual(200, response.status_code)
            self.assertEqual(10, int(response.json["rows"]))
            self.assertEqual(3, len(response.json["data"]))
            self.assertEqual(PRODUCTS[3], response.json["data"][0])

            response = self.api.get("/api/products/" + PRODUCTS[0]["id"], headers=self.headers)
            self.assertEqual(200, response.status_code)
            self.assertEqual(PRODUCTS[0], response.json)

            response = self.api.post("/api/products", headers=self.headers, json={"id": "p1", "name": "Product"})
            self.assertEqual(500, response.status_code)

            response = self.api.patch("/api/products/" + PRODUCTS[0]["id"], headers=self.headers, json={"attribute1": "value1", "attribute2": "value2"})
            self.assertEqual(200, response.status_code)
            response = self.api.get("/api/products/" + PRODUCTS[0]["id"], headers=self.headers)
            self.assertEqual(200, response.status_code)
            self.assertIn("attribute1", response.json)
            self.assertIn("attribute2", response.json)
            self.assertEqual("value1", response.json["attribute1"])
            self.assertEqual("value2", response.json["attribute2"])

            response = self.api.patch("/api/products/" + PRODUCTS[0]["id"], headers=self.headers, json={"attribute1": None})
            self.assertEqual(200, response.status_code)
            response = self.api.get("/api/products/" + PRODUCTS[0]["id"], headers=self.headers)
            self.assertEqual(200, response.status_code)
            self.assertNotIn("attribute1", response.json)

            response = self.api.delete("/api/products/" + PRODUCTS[0]["id"], headers=self.headers)
            self.assertEqual(204, response.status_code)
        finally:
            for product in PRODUCTS:
                delete_product(product["id"])
