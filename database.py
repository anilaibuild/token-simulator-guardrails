import sqlite3

def create_table():
    connection = sqlite3.connect("token_tracker.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usage_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT,
            question TEXT,
            provider TEXT,
            tokens_used INTEGER,
            cost REAL,
            timestamp TEXT
        )
    """)

    connection.commit()
    connection.close()
    print("Table created successfully!")


def add_thinking_columns():
    connection = sqlite3.connect("token_tracker.db")
    cursor = connection.cursor()

    try:
        cursor.execute("ALTER TABLE usage_log ADD COLUMN prompt_tokens INTEGER")
    except:
        pass

    try:
        cursor.execute("ALTER TABLE usage_log ADD COLUMN visible_tokens INTEGER")
    except:
        pass

    try:
        cursor.execute("ALTER TABLE usage_log ADD COLUMN thinking_tokens INTEGER")
    except:
        pass

    connection.commit()
    connection.close()
    print("Columns added (or already existed)!")


create_table()
add_thinking_columns()