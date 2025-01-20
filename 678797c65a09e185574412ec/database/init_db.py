```python
import sqlite3

def init_db():
    # Connect to the database (or create it if it doesn't exist)
    conn = sqlite3.connect('event_photos.db')

    # Create a cursor to execute SQL commands
    cursor = conn.cursor()

    # Create tables for facial features, passwords, and matched results
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facial_features (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id TEXT NOT NULL,
            face_vector BLOB NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            event_id TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matched_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mobile_number TEXT NOT NULL,
            event_id TEXT NOT NULL,
            matched_image_path TEXT NOT NULL
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
```