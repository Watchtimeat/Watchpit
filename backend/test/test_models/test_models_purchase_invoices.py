import json
import unittest

from models.products import create_product, delete_product
from models.purchase_invoices import create_purchase_invoice, get_purchase_invoices, get_purchase_invoice, \
    update_purchase_invoice, delete_purchase_invoice, get_purchase_invoices_summary
from models.purchase_orders import create_purchase_order, delete_purchase_order, get_purchase_order

PRODUCTS = [
    {"id": "product1", "name": "product 1", "brand": "test"},
    {"id": "product2", "name": "product 2", "brand": "test"}
]

PURCHASE_ORDERS = [
    {
        "id": "order1",
        "brand": "test",
        "status": "requested",
        "items": [
            {
                "product_id": "product1",
                "requested_quantity": 10,
                "product_cost": 1,
                "status": "active"
            },
            {
                "product_id": "product2",
                "requested_quantity": 10,
                "product_cost": 1,
                "status": "active"
            }
        ]
    },
    {
        "id": "order2",
        "brand": "test",
        "status": "requested",
        "items": [
            {
                "product_id": "product1",
                "requested_quantity": 10,
                "product_cost": 1,
                "status": "active"
            },
            {
                "product_id": "product2",
                "requested_quantity": 10,
                "product_cost": 1,
                "status": "active"
            }
        ]
    }
]

PURCHASE_INVOICES = [
    {
        "id": "invoice1",
        "brand": "test",
        "orders": [
            {
                "id": "order1",
                "items": [
                    {"product_id": "product1", "received_quantity": 10, "product_cost": 1},
                    {"product_id": "product2", "received_quantity": 10, "product_cost": 1}
                ]
            },
            {
                "id": "order2",
                "items": [
                    {"product_id": "product1", "received_quantity": 10, "product_cost": 1},
                    {"product_id": "product2", "received_quantity": 5, "product_cost": 1},
                ]
            }
        ]
    },
    {
        "id": "invoice2",
        "orders": [
            {
                "id": "order2",
                "items": [
                    {"product_id": "product2", "received_quantity": 10, "product_cost": 1},
                ]
            }
        ]
    }
]


class TestProducts(unittest.TestCase):

    def test_crud(self):
        for product in PRODUCTS:
            create_product(product)
        for order in PURCHASE_ORDERS:
            create_purchase_order(order)
        try:
            # create first invoice
            create_purchase_invoice(PURCHASE_INVOICES[0])
            order1 = get_purchase_order("order1")
            self.assertEqual("finished", order1["status"])
            self.assertEqual(20, order1["received_quantity"])
            order2 = get_purchase_order("order2")
            self.assertEqual("receiving", order2["status"])
            self.assertEqual(15, order2["received_quantity"])

            # create second invoice
            create_purchase_invoice(PURCHASE_INVOICES[1])
            order1 = get_purchase_order("order1")
            self.assertEqual("finished", order1["status"])
            self.assertEqual(20, order1["received_quantity"])
            order2 = get_purchase_order("order2")
            self.assertEqual("finished", order2["status"])
            self.assertEqual(25, order2["received_quantity"])

            # update first invoice removing order2
            invoice1 = get_purchase_invoice("invoice1")
            del invoice1["orders"][1]
            update_purchase_invoice(invoice1)
            order1 = get_purchase_order("order1")
            self.assertEqual("finished", order1["status"])
            self.assertEqual(20, order1["received_quantity"])
            order2 = get_purchase_order("order2")
            self.assertEqual("receiving", order2["status"])
            self.assertEqual(10, order2["received_quantity"])

            # delete second invoice
            delete_purchase_invoice("invoice2")
            order1 = get_purchase_order("order1")
            self.assertEqual("finished", order1["status"])
            self.assertEqual(20, order1["received_quantity"])
            order2 = get_purchase_order("order2")
            self.assertEqual("requested", order2["status"])
            self.assertEqual(0, order2["received_quantity"])

            # validate get_purchase_invoices
            purchase_invoices = get_purchase_invoices()["data"]
            self.assertEqual(1, len(purchase_invoices))

            # validate get_purchase_invoices_summary
            self.assertEqual(1, get_purchase_invoices_summary("brand", {"brand": "test"})["test"])

        finally:
            for invoice in PURCHASE_INVOICES:
                delete_purchase_invoice(invoice["id"])
            for order in PURCHASE_ORDERS:
                delete_purchase_order(order["id"], force=True)
            for product in PRODUCTS:
                delete_product(product["id"])
