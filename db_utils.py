import mysql.connector

DB_NAME = "blg317_project"     
DB_USER = "root"               
DB_PASS = "PASSWORD" 
DB_HOST = "localhost"          

def get_db_connection():
    """MySQL veritabanına yeni bir bağlantı oluşturur."""

    conn = mysql.connector.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST
        )
    return conn


def execute_query(query, params=None, fetch=False):

    conn = get_db_connection()
    if conn is None:
        return None if fetch else False
        
    cursor = conn.cursor(dictionary=True) 
    try:
        cursor.execute(query, params)
        
        if fetch:
            results = cursor.fetchall() 
            return results
        else:
            conn.commit() 
            return True
            
    except mysql.connector.Error as e:
        print(f"HATA: Sorgu çalıştırılamadı: {e}")
        conn.rollback() 
        return None if fetch else False
    finally:
        cursor.close()
        conn.close()