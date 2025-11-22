import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="********",
        database="wdi",
        auth_plugin="mysql_native_password"  # macOS için gerekli
    )
