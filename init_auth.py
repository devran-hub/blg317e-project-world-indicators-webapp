from database.db_connect import get_db_connection
from werkzeug.security import generate_password_hash

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Users table
    with open('database/create_users_table.sql', 'r') as f:
        cursor.execute(f.read())
    
    # Check if admin exists
    cursor.execute("SELECT * FROM Users WHERE username = 'huseynov'")
    if not cursor.fetchone():
        # Create admin user
        password = "09052006"
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        cursor.execute(
            "INSERT INTO Users (username, password_hash, role) VALUES (%s, %s, %s)",
            ('huseynov', password_hash, 'admin')
        )
        print("Admin user 'huseynov' created.")
    else:
        print("Admin user already exists.")

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    init_db()
