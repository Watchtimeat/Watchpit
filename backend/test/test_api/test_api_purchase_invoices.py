import json
import unittest

from app import app
from models.auth import set_password
from models.purchase_invoices import get_purchase_invoices, delete_purchase_invoice, get_purchase_invoices_summary
from models.users import create_user, delete_user

PURCHASE_INVOICES = list()
for i in range(10):
    PURCHASE_INVOICES.append(
        {
            "id": "pi" + str(i),
            "brand": "test",
            "items": [{"product_id": "p" + str(i), "requested_quantity": i} for i in range(3)]
        })
PURCHASE_INVOICES.append({"id": "pix"})


class TestPurchaseInvoices(unittest.TestCase):
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
        for i in range(len(PURCHASE_INVOICES)):
            response = self.api.post("/api/purchase_invoices", headers=self.headers, json=PURCHASE_INVOICES[i])
            self.assertEqual(200, response.status_code)
            PURCHASE_INVOICES[i] = response.json
        try:

            response = self.api.get("/api/purchase_invoices/summary/brand", headers=self.headers)
            self.assertEqual(200, response.status_code)
            self.assertEqual(10, response.json["test"])
            self.assertEqual(1, response.json["-"])

            response = self.api.get("/api/purchase_invoices?brand=test", headers=self.headers)
            self.assertEqual(200, response.status_code)
            self.assertEqual(10, len(response.json.get("data", list())))

            response = self.api.get("/api/purchase_invoices?brand=test", headers=self.headers)
            self.assertEqual(200, response.status_code)
            self.assertEqual(10, int(response.json["rows"]))

            response = self.api.get("/api/purchase_invoices/" + PURCHASE_INVOICES[0]["id"], headers=self.headers)
            self.assertEqual(200, response.status_code)
            self.assertEqual(3, len(response.json["items"]))

            response = self.api.post("/api/purchase_invoices", headers=self.headers, json={"id": "pi1", "items": []})
            self.assertEqual(500, response.status_code)

            response = self.api.patch("/api/purchase_invoices/" + PURCHASE_INVOICES[0]["id"], headers=self.headers, json={"items": [{"product_id": "1", "requested_quantity": 1}]})
            self.assertEqual(200, response.status_code)
            response = self.api.get("/api/purchase_invoices/" + PURCHASE_INVOICES[0]["id"], headers=self.headers)
            self.assertEqual(200, response.status_code)
            self.assertEqual(1, len(response.json["items"]))

            response = self.api.delete("/api/purchase_invoices/" + PURCHASE_INVOICES[0]["id"], headers=self.headers)
            self.assertEqual(204, response.status_code)
            response = self.api.get("/api/purchase_invoices?brand=test", headers=self.headers)
            self.assertEqual(200, response.status_code)
            self.assertEqual(9, len(response.json["data"]))

        finally:
            for purchase_invoice in PURCHASE_INVOICES:
                delete_purchase_invoice(purchase_invoice["id"])
