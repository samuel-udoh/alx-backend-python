import sqlite3
class ExecuteQuery:
    def __init__(self, query, params):
        self.query = query
        self.params = params
    def __enter__(self):
        self.connection = sqlite3.connect("users.db")
        self.cursor = self.connection.cursor()
        result = self.cursor.execute(self.query, self.params)
        self.connection.commit()
        return result
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type:
            self.connection.rollback()
            print(f"An error occured: {exc_value}")
        self.connection.close()
        return False

with ExecuteQuery("SELECT * FROM users WHERE user_id = ?", ("1727c05c-1b63-456c-8a02-6078d4749c79",)) as result:
    print(result.fetchone())