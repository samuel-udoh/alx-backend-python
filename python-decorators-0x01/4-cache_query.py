import sqlite3 
from functools import wraps


query_cache = {}

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



def cache_query(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        query = args[1] if len(args) > 1 else kwargs.get('query', '')
        if query in query_cache:
            return query_cache[query]

        print("Executing query and caching result")
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users LIMIT 5")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users LIMIT 5")