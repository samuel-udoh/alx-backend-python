import sqlite3


class DatabaseConnection:
    def __init__(self, file_name: str):
        """Initialize with database file name."""
        self.file_name = file_name
    def __enter__(self):
        """Establish and return DB cursor."""
        self.connection = sqlite3.connect(self.file_name)
        self.cursor =  self.connection.cursor()
        return self.cursor, self.connection
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Close DB connection and optionally handle exceptions."""
        if exc_type:
            self.connection.rollback()
            print(f"An error occured: {exc_value}")
        self.connection.close()
        return False


with DatabaseConnection('users.db') as (cursor, connection):
    cursor.execute("SELECT * FROM users")
    for user in cursor.fetchmany(20):
        print(f"{user[0]} {user[1]}")