from seed import connect_to_prodev
from mysql.connector import Error

def stream_users():
    """
    Connects to ALX_prodev database and yields user data one row at a time
    """
    connection = None
    try:
        connection = connect_to_prodev()

        if not connection :
            return
        
        get_query = "SELECT * FROM user_data;"
        
        with connection.cursor(buffered=True) as cursor:
            cursor.execute(get_query)
            for user in cursor:
                yield user
    except Error as e:
        print(f"Database Eror: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()
