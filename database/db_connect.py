import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='09052006Dreyk',
            database='wdi'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None