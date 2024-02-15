import unittest

from models.products import create_product, get_product, get_products, has_product, update_product, delete_product

products = [
    {"id": "p" + str(i), "name": "product " + str(i), "type": "test"}
    for i in range(3)
]


class TestProducts(unittest.TestCase):

    def test_crud(self):
        for product in products:
            create_product(product)
        try:
            self.assertEqual(products[0], get_product(products[0]["id"]))
            self.assertEqual(products, get_products({"type": "test", "_order_a": "id"})["data"])
            for product in products:
                self.assertTrue(has_product(product["id"]))

            with self.assertRaises(Exception):
                create_product({"id": "p1", "name": "product"})
            products[0]["attribute2"] = "value2"
            update_product(products[0])
            product = get_product(products[0]["id"])
            self.assertEqual("value2", product["attribute2"])

            update_product({"id": products[0]["id"], "attribute1": None})
            product = get_product(products[0]["id"])
            self.assertNotIn("attribute1", product)
        finally:
            for product in products:
                delete_product(product["id"])
