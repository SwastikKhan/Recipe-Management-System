import sqlite3

def create_connection():
    conn = sqlite3.connect('recipes.db')
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        instructions TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY,
        recipe_id INTEGER,
        name TEXT NOT NULL,
        quantity TEXT NOT NULL,
        FOREIGN KEY (recipe_id) REFERENCES recipes (id)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print()