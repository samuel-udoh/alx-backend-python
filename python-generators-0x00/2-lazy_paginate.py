from seed import connect_to_prodev
from mysql.connector import Error

def paginate_users(page_size, offset):
    """
    Fetches a single 'page' of users from the database.
    This is our "worker" function. It is stateless.
    """
    try:
        connection = connect_to_prodev()

        if not connection:
            return []
        
        get_page=f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}"

        with connection.cursor(buffered=True) as cursor:
            cursor.execute(get_page)
            rows = cursor.fetchall()
            return rows
    except Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if connection and connection.is_connected():
            connection.close()


def lazy_paginate(page_size):
    """
     A generator that lazily fetches pages of users from the database.
    This is our stateful "manager". It uses one loop.
    """
    offset=0

    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size