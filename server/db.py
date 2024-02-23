import sqlite3

db = sqlite3.connect("messages.db")
cursor = db.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                name TEXT NOT NULL,
                text TEXT)''')

