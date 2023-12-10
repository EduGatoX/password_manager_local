import unittest
from db.db import SQLiteDBConnection
from models.models import User


class TestSQLiteDBConnection(unittest.TestCase):
    def setUp(self):
        self.conn = SQLiteDBConnection("test.db")
        self.user = dict(name="Eduardo", email="eduardo@mail.com",
                         hashed_pw="asflkh13098fhk130f")
        self.conditions = dict(name="Eduardo", email="eduardo@mail.com")

    def tearDown(self):
        pass

    def test_create_table(self):
        sql = self.conn.create_table(User)
        required_sql = "CREATE TABLE IF NOT EXISTS users (\n\t"
        required_sql += "user_id INTEGER PRIMARY KEY, \n\t"
        required_sql += "name TEXT NOT NULL, \n\t"
        required_sql += "email TEXT NOT NULL UNIQUE, \n\t"
        required_sql += "hashed_pw TEXT NOT NULL);"
        self.assertEqual(sql, required_sql)

    def test_insert_into_table(self):
        sql = self.conn.insert_into_table(User)

        required_sql = "INSERT INTO users \n"
        required_sql += "(name, email, hashed_pw) \n"
        required_sql += "VALUES (?, ?, ?);"

        self.assertEqual(sql, required_sql)

    def test_select_all_from_table(self):
        sql = self.conn.select_all_from_table(User)
        required_sql = "SELECT * FROM users;"

        self.assertEqual(sql, required_sql)

    def test_select_from_table_where(self):
        sql = self.conn.select_from_table_where(User, self.conditions)
        required_sql = "SELECT * FROM users \n\t"
        required_sql += "WHERE name = ?, \n\t"
        required_sql += "email = ?;"

        self.assertEqual(sql, required_sql)

    def test_update_from_table_where(self):
        sql = self.conn.\
            update_from_table_where(User, self.conditions, self.user)
        required_sql = "UPDATE users \n"
        required_sql += "SET name = ?, \n\t"
        required_sql += "email = ?, \n\t"
        required_sql += "hashed_pw = ? \n"
        required_sql += "WHERE name = ?, \n\t"
        required_sql += "email = ?;"

        self.assertEqual(sql, required_sql)

    def test_delete_from_table_where(self):
        sql = self.conn.delete_from_table_where(User, self.conditions)
        required_sql = "DELETE FROM users \n"
        required_sql += "WHERE name = ?, \n\t"
        required_sql += "email = ?;"

        self.assertEqual(sql, required_sql)


if __name__ == "__main__":
    unittest.main()
