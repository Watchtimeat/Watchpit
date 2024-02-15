from models.auth import set_password, remove_password, check_password, has_password
from models.users import create_user, update_user, delete_user, get_user, get_users
import unittest

USERS = [
    {
        "id": "test" + str(i),
        "name": "User {}".format(i),
        "email": "user{}@test".format(i)
    }
    for i in range(3)
]


class TestUsers(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_crud(self):
        for user in USERS:
            create_user(user)
        try:
            users = get_users()
            emails = [user["email"] for user in users]
            for USER in USERS:
                self.assertIn(USER["email"], emails)

            with self.assertRaises(Exception):
                create_user({"email": "user0@test", "name": "new user"})

            user = get_user(email="user0@test")
            user["name"] = "new name"
            update_user(user)

            user["email"] = "new_email@test"
            update_user(user)

            with self.assertRaises(Exception):
                update_user({"id": user["id"], "email": "user1@test"})

            user["attribute"] = "value"
            update_user(user)
            update_user({"id": user["id"], "attribute": None})
            self.assertNotIn("attribute", get_user(user["id"]))
        finally:
            for USER in USERS:
                delete_user(get_user(user_id=USER["id"]))

    def test_password(self):
        user = create_user({"name": "Test User", "email": "user@test"})
        try:
            self.assertFalse(has_password(user))
            set_password(user, "pass")
            self.assertTrue(has_password(user))
            self.assertTrue(check_password(user, "pass"))
            self.assertFalse(check_password(user, "pass1"))
            remove_password(user)
            self.assertFalse(has_password(user))
        finally:
            delete_user(user)
