import unittest
from models.models import User, Password
from models.typing import SQLDataType, Integer, Text


class TestUser(unittest.TestCase):
    def setUp(self):
        # Schema to be compared to the __schema__ property of the User model
        self.schema = dict(
            user_id=Integer(primary_key=True), name=Text(nullable=False),
            email=Text(nullable=False), hashed_pw=Text(nullable=False),
        )

        # This should be validated correctly
        self.data_correct = {
            "name": "Eduardo",
            "email": "eduardo@mail.com",
            "hashed_pw": "fsdkh913r1h139",
        }

        # This should not be be validated because the type of name is incorrect
        self.data_incorrect_1 = {
            "name": 1,
            "email": "eduardo@mail.com",
            "hashed_pw": "fsdkh913r1h139",
        }
        
        # This should not be be validated because one not nullable value is not provided
        self.data_incorrect_2 = {
            "email": "eduardo@mail.com",
            "hashed_pw": "fsdkh913r1h139",
        }

    def tearDown(self):
        pass

    def test_schema(self):
        self.assertEqual(User.__schema__, self.schema)

    def test_validate_data(self):
        self.assertTrue(User.validate_data(self.data_correct))
        self.assertFalse(User.validate_data(self.data_incorrect_1))
        self.assertFalse(User.validate_data(self.data_incorrect_2))


class TestPassword(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
