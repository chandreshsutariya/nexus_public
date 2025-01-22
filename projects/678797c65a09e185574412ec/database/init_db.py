import sqlite3

def init_db():
    connection = sqlite3.connect('facial_features.db')
  
    # Create tables for storing facial features, passwords, and matched results
    with connection:
        connection.execute('''
            CREATE TABLE IF NOT EXISTS facial_features (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT NOT NULL,
                feature_vector BLOB NOT NULL
            )
        ''')

        connection.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                event_id TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL
            )
        ''')

        connection.execute('''
            CREATE TABLE IF NOT EXISTS matched_faces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mobile_number TEXT NOT NULL,
                matched_image_path TEXT NOT NULL,
                event_id TEXT NOT NULL
            )
        ''')

    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
