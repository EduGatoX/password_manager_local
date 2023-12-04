import unittest
from db.models import User, Password
from db.types import SQLDataType, Integer, Text


class TestUser(unittest.TestCase):
    def setUp(self):
        DB_ENGINE = "sqlite3"
        user_id = Integer(DB_ENGINE, 1, primary_key=True)
        name = Text(DB_ENGINE, "Eduardo", nullable=False)
        email = Text(DB_ENGINE, "eduardo@mail.com", nullable=False)
        hashed_pw = Text(DB_ENGINE, "376basdrasbc098471ñlad", nullable=False)

        self.user = User(user_id, name, email, hashed_pw)
        self.data = {
            "name": name,
            "email": email,
            "hashed_pw": hashed_pw,
        }
        self.repr = f"User(id={user_id}, name={name}, email={email})"

    def tearDown(self):
        pass

    def test_name(self):
        self.assertEqual(self.user.name.value, "Eduardo")

    def test_email(self):
        self.assertEqual(self.user.email.value, "eduardo@mail.com")

    def test_hashed_pw(self):
        self.assertEqual(self.user.hashed_pw.value, "376basdrasbc098471ñlad")

    def test_dump_data(self):
        self.assertEqual(self.user.dump_data(), self.data)

    def test_repr(self):
        self.assertEqual(str(self.user), self.repr)


class TestPassword(unittest.TestCase):
    def setUp(self):
        DB_ENGINE = "sqlite3"
        password_id = Integer(DB_ENGINE, 1, primary_key=True)
        app_name = Text(DB_ENGINE, "my_app", nullable=False)
        app_url = Text(DB_ENGINE, "www.my_app.url", nullable=False)
        username = Text(DB_ENGINE, "enunez", nullable=False)
        password = Text(DB_ENGINE, "1234", nullable=False)
        user_id = Integer(DB_ENGINE, 1, nullable=False)

        self.password = Password(password_id, app_name, app_url, username, password, user_id)
        self.data = {
            "app_name": app_name,
            "app_url": app_url,
            "username": username,
            "password": password,
            "user_id": user_id,
        }
        self.repr = f"Password(name={app_url}, username={username}, password={password})"

    def tearDown(self):
        pass

    def test_app_name(self):
        self.assertEqual(self.password.app_name.value, "my_app")

    def test_app_url(self):
        self.assertEqual(self.password.app_url.value, "www.my_app.url")

    def test_username(self):
        self.assertEqual(self.password.username.value, "enunez")

    def test_password(self):
        self.assertEqual(self.password.password.value, "1234")

    def test_user_id(self):
        self.assertEqual(self.password.user_id.value, 1)

    def test_dump_data(self):
        self.assertEqual(self.password.dump_data(), self.data)

    def test_repr(self):
        self.assertEqual(str(self.password), self.repr)


if __name__ == "__main__":
    unittest.main()
