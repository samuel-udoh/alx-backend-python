import sqlite3
from functools import wraps
from datetime import datetime
#### decorator to lof SQL queries
def log_queries(func):
    @wraps(func)
    def wrappers(*args, **kwargs):
        query = args[0] if args else kwargs.get('query', '')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{now}] Executing query in {func.__name__}: {query}")
        return func(*args, **kwargs)
    return wrappers


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users LIMIT 5")
print(users)