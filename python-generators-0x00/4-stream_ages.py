from decimal import Decimal
from seed import connect_to_prodev
from mysql.connector import Error

def stream_user_ages():
    """yield user ages one by one"""
    try:
        connection = connect_to_prodev()

        if not connection:
            return
        sql="SELECT age FROM user_data;"
        with connection.cursor() as cursor:
            cursor.execute(sql)

            for age_tuple in cursor:
                yield age_tuple[0]

    except Error as e:
        print(f"Database error: {e}")
    
    finally:
        if connection and connection.is_connected():
            connection.close()

def calculation_avg_age():
    """Calculate the average age from the stream of user ages"""
    total_age=Decimal('0.0')
    num_user=0
    
    for age in stream_user_ages():
        total_age += age
        num_user += 1
    if num_user > 0:
        average= total_age / num_user
        print(f" Average age of users: {average:.2f}")
    else:
        print("Database has no users")


if __name__ == "__main__":
    calculation_avg_age()

    