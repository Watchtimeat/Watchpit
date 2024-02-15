import unittest

from app import app
from models.auth import set_password
from models.purchase_orders import get_purchase_orders, delete_purchase_order
from models.users import create_user, delete_user

PURCHASE_ORDERS = [
    {"id": "po" + str(i), "brand": "test", "status": "draft", "items": [{"product_id": "p" + str(i), "requested_quantity": i} for i in range(3)]}
    for i in range(10)
]


class TestPurchaseOrders(unittest.TestCase):

    def setUp(self):
        self.api = app.test_client()
        self.admin = create_user({"email": "admin@test", "name": "Admin User", "enabled": True, "Administrator": True})
        set_password(self.admin, "pass")
        response = self.api.post("/api/auth/login", json={"email": "admin@test", "password": "pass"})
        self.assertEqual(200, response.status_code)
        self.token = response.json["token"]
        self.headers = {"Authorization": "Bearer " + self.token}

    def tearDown(self):
        delete_user(self.admin)

    def test_crud(self):
        for i in range(len(PURCHASE_ORDERS)):
            response = self.api.post("/api/purchase_orders", headers=self.headers, json=PURCHASE_ORDERS[i])
            self.assertEqual(200, response.status_code)
            PURCHASE_ORDERS[i] = response.json
        try:
            response = self.api.get("/api/purchase_orders/summary/status?brand=test", headers=self.headers)
            self.assertEqual(200, response.status_code)
            self.assertEqual({"draft": 10}, response.json)

            response = self.api.get("/api/purchase_orders?brand=test", headers=self.headers)
            self.assertEqual(200, response.status_code)
            self.assertEqual(10, len(response.json.get("data", list())))

            response = self.api.get("/api/purchase_orders?brand=test&status=draft", headers=self.headers)
            self.assertEqual(200, response.status_code)
            self.assertEqual(10, int(response.json["rows"]))

            response = self.api.get("/api/purchase_orders/" + PURCHASE_ORDERS[0]["id"], headers=self.headers)
            self.assertEqual(200, response.status_code)
            self.assertEqual(3, len(response.json["items"]))

            response = self.api.post("/api/purchase_orders", headers=self.headers, json={"id": "po1", "items": []})
            self.assertEqual(500, response.status_code)

            response = self.api.patch("/api/purchase_orders/" + PURCHASE_ORDERS[0]["id"], headers=self.headers, json={"status": "confirmed"})
            self.assertEqual(200, response.status_code)
            response = self.api.patch("/api/purchase_orders/" + PURCHASE_ORDERS[0]["id"], headers=self.headers, json={"items": [{"product_id": "1", "requested_quantity": 1}]})
            self.assertEqual(200, response.status_code)
            response = self.api.get("/api/purchase_orders/" + PURCHASE_ORDERS[0]["id"], headers=self.headers)
            self.assertEqual(200, response.status_code)
            self.assertEqual("confirmed", response.json["status"])
            self.assertEqual(1, len(response.json["items"]))

            response = self.api.delete("/api/purchase_orders/" + PURCHASE_ORDERS[0]["id"], headers=self.headers)
            self.assertEqual(204, response.status_code)
            response = self.api.get("/api/purchase_orders?brand=test", headers=self.headers)
            self.assertEqual(200, response.status_code)
            self.assertEqual(9, len(response.json["data"]))

        finally:
            for purchase_order in get_purchase_orders({"brand": "test"})["data"]:
                delete_purchase_order(purchase_order["id"])
