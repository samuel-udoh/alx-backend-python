import sqlite3
import uuid
from faker import Faker
from enum import Enum

class UserRole(Enum):
    ADMIN="admin"
    GUEST="guest"
    HOST="host"

fake = Faker()

insert_query = '''
INSERT INTO users (user_id, first_name, last_name, age, email, password_hash,  phone_number, role)
VALUES (?, ?, ?, ?,  ?, ?, ?, ?)
'''

def generate_data(size):
    for _ in range(size):
        user_id = str(uuid.uuid4())
        first_name=fake.first_name()
        last_name=fake.last_name()
        age = fake.random_int(min=13, max=67)
        email=fake.email()
        password_hash = fake.sha256()
        phone_number=fake.phone_number()
        role = fake.random_element(UserRole).value

        yield (user_id, first_name, last_name, age, email, password_hash,  phone_number, role)

def seed_db():
    connection = None

    try:
        connection= sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.executemany(insert_query, generate_data(100))
        connection.commit()
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        if connection is not None:
            connection.close()

seed_db()