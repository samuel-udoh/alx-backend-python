from seed import connect_to_prodev
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """yield user in batches of batch_size"""
    try:
        connection = connect_to_prodev()

        if not connection:
            return
        get_query = "SELECT * FROM user_data;"
        with connection.cursor(buffered=True) as cursor:
            cursor.execute(get_query)
            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                
                yield batch
    except Error as e:
        print(f"Database error: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()


def batch_processing(batch_size):
    """Process users in batches and yield those over 25 years old"""
    for batch in stream_users_in_batches(batch_size):
        filter_user = [user for user in batch if user[3] > 25]
        if filter_user:
            yield filter_user
