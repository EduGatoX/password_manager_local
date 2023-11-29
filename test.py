import db
from dataclasses import dataclass


@dataclass
class MyClass:
    arg1: str
    arg2: str
    arg3: str


obj1 = MyClass("arg1", "arg2", "arg3")
data = obj1.__dict__

sql = f"start {', '.join(data.keys())} end"
print(sql)


# conn = db.DBConnectionFactory("sqlite", "")

user = db.models.User(1, "Eduardo", "eduardo@mail.com", "lñkjsdf98723")

# conn.insert_into_table("users", user)

data = user.dump_data()

print(data)

sql = f"{', '.join([f'{key} = {value}' for key, value in data.items()])}"
print(sql)
