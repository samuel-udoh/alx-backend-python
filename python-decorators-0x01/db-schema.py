import sqlite3

create_user_table_query = '''
CREATE TABLE IF NOT EXISTS users (
    user_id char(36) PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    phone_number TEXT,
    role TEXT NOT NULL CHECK(role IN ('host', 'guest', 'admin')),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
'''

def create_user_table():
    connection = None
    try:
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        cursor.execute(create_user_table_query)
        connection.commit()
    except sqlite3.Error as e:
        print(f"Sqlite3 Error: {e}")
    finally:
        if connection is not None:
            connection.close()


create_user_table()