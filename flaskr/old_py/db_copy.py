import sqlite3

DATABASE = 'database.db'

def create_samples_table():
    conn = sqlite3.connect(DATABASE)
    conn.execute("CREATE TABLE IF NOT EXISTS samples (title, number, create_day)")
    conn.close()