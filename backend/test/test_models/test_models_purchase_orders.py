import unittest

from models.purchase_orders import create_purchase_order, delete_purchase_order, get_purchase_orders, get_purchase_order, update_purchase_order, get_purchase_orders_summary

PURCHASE_ORDER = {
    "id": "po1",
    "status": "draft",
    "items": [
        {"product": "p1", "status": "active", "requested_quantity": 1, "product_cost": 10},
        {"product": "p2", "status": "active", "requested_quantity": 1},
        {"product": "p3", "status": "active"}
    ]}

PURCHASE_ORDERS = [
    {"id": "po1", "brand": "test", "owner": "user1", "status": "draft", "items": []},
    {"id": "po2", "brand": "test", "owner": "user2", "status": "draft", "items": []},
    {"id": "po3", "brand": "test", "owner": "user1", "status": "confirmed", "items": []},
    {"id": "po4", "brand": "test", "owner": "user2", "status": "confirmed", "items": []}
]


class TestProducts(unittest.TestCase):

    def test_crud(self):
        create_purchase_order(PURCHASE_ORDER)
        try:
            orders = get_purchase_orders({"id": PURCHASE_ORDER["id"]})
            self.assertEqual(1, len(orders["data"]))

            order = get_purchase_order(PURCHASE_ORDER["id"])
            self.assertIsNotNone(order["id"])
            self.assertEqual("draft", order["status"])
            self.assertEqual(10, order["total_cost"])
            self.assertEqual(3, order["requested_items"])
            self.assertEqual(2, order["requested_quantity"])

            update_purchase_order({"id": PURCHASE_ORDER["id"], "items": [{"product": "p1", "quantity": 1}]})
            update_purchase_order({"id": PURCHASE_ORDER["id"], "status": "confirmed"})

            order = get_purchase_order(PURCHASE_ORDER["id"])
            self.assertIsNotNone(order["id"])
            self.assertEqual(1, len(order["items"]))
            self.assertEqual("confirmed", order["status"])

        finally:
            delete_purchase_order(PURCHASE_ORDER["id"])

    def test_summary(self):
        for purchase_order in PURCHASE_ORDERS:
            create_purchase_order(purchase_order)
            update_purchase_order({"id": purchase_order["id"], "status": purchase_order["status"]})
        try:
            self.assertEqual({'confirmed': 2, 'draft': 2}, get_purchase_orders_summary("status", {"brand": "test"}))
            self.assertEqual({'confirmed': 1, 'draft': 1}, get_purchase_orders_summary("status", {"brand": "test", "owner": "user1"}))
        finally:
            for purchase_order in PURCHASE_ORDERS:
                delete_purchase_order(purchase_order["id"])
