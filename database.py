import sqlite3
import os

# Create database folder if it doesn't exist
DB_FOLDER = "database"
os.makedirs(DB_FOLDER, exist_ok=True)

# Database path
DB_PATH = os.path.join(DB_FOLDER, "ticket_system.db")


def get_connection():
    """Return a connection to the SQLite database."""

    conn = sqlite3.connect(DB_PATH)

    # Enable foreign key constraints
    conn.execute("PRAGMA foreign_keys = ON")

    return conn

def initialize_database():
    """Create all required tables."""

    conn = get_connection()
    cursor = conn.cursor()

    # ---------------- USERS TABLE ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'Employee',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ---------------- TICKETS TABLE ----------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT UNIQUE NOT NULL,
            employee_id TEXT NOT NULL,
            category TEXT NOT NULL,
            subject TEXT NOT NULL,
            description TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT DEFAULT 'Open',
            assigned_to TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(employee_id) REFERENCES users(employee_id)
        )
    """)

    # ---------------- ADD ASSIGNED TO COLUMN ----------------

    cursor.execute("""
        PRAGMA table_info(tickets)
    """)

    columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    if "assigned_to" not in columns:

        cursor.execute("""
            ALTER TABLE tickets
            ADD COLUMN assigned_to TEXT
        """)

    conn.commit()
    conn.close()


# Create database automatically when imported
initialize_database()