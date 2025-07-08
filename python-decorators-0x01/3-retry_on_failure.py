import time
import sqlite3 
from  functools import wraps

def with_db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect('users.db')
            result = func(conn, *args, **kwargs)
            return result
        except sqlite3.Error as e:
            print(f"Error: {e}")
        finally:
            if conn is not None:
                conn.close()
    return wrapper



def retry_on_failure(retries, delay):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            num_attempts = 0
            while (num_attempts < retries):
                try:
                    num_attempts += 1
                    return func(*args, **kwargs)
                except sqlite3.Error as e:
                    print(f"[Attempt {attempt}] Error: {e}")
                    if attempt < retries:
                        time.sleep(delay)
                    else:
                        print("Max retry attempts exceeded.")
                        raise
        return wrapper
    return decorator





@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)