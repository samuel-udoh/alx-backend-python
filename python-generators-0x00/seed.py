import uuid
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import csv
load_dotenv()
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}
DB_NAME="ALX_prodev"

def connect_db():
    """function connect to mysql database"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        print("Successfully connected to MYSQL db")
        return connection
    except Error as e:
        print(f"The Error {e} occured")
        return None
    



def create_database(connection):
    """Function creates database" ALX_prodev if not exist"""
    if not connection:
        return
    
    create_db_ALX_prodev = f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"
    try:
        with connection.cursor() as cursor:
            cursor.execute(create_db_ALX_prodev)
        connection.commit()
        print(f"Database {DB_NAME} created")
    except Error as e:
        print(f"Error: {e} occured")
    


def connect_to_prodev():
    """Connects to the ALX_prodev"""
    connection = None
    config = DB_CONFIG.copy()
    config["database"] = DB_NAME
    try:
        connection = mysql.connector.connect(**config)
        # print(f"Connected to {DB_NAME}")
    except Error as e:
        print(f"Error: {e} occured")
    
    return connection

def create_table(connection):
    """Create **user_data** table"""
    if not connection:
        return False
    create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data(
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            age DECIMAL(10,1) NOT NULL
        );
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute(create_table_query);
        connection.commit()
        print("user_data Table created")
    except Error as e:
        print(f"Error: {e} occured")

def insert_data(connection, data):
    if not connection or not data:
        return False
    
    insert_query="""
        INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)
    """
    rows_to_insert= []
    try:
        with open(data, newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                rows_to_insert.append(
                    (
                        str(uuid.uuid4()),
                        row.get('name', '').strip(),
                        row.get('email', '').strip().lower(),
                        float(row.get('age'))
                    ))
    except FileNotFoundError:
        print("File not found")
        return False
    except (KeyError, ValueError) as e:
        print(f"Error: CSV file is missing a column or has invalid data. Details: {e}")
        return False
    if not rows_to_insert:
        print("No data to insert.")
        return True
    try:
        with connection.cursor() as cursor:
            cursor.executemany(insert_query, rows_to_insert)
        connection.commit()
        print(f"successfully inserted data from {data}")
        print(f"Successfully inserted {cursor.rowcount} rows.")
        return True
    except Error as e:
        print(f"Error: {e}")
        connection.rollback()
        return False

    