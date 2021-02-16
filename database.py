import sqlite3

DB_NAME = 'unsplash-photo.db'

def createTable():
  conn = sqlite3.connect(DB_NAME)
  with conn:
    conn.execute("""
      CREATE TABLE PHOTO(
        id TEXT NOT NULL PRIMARY KEY,
        raw TEXT,
        full TEXT,
        regular TEXT,
        small TEXT,
        thumb TEXT,
        created_at TIMESTAMP,
        updated_at TIMESTAMP,
        width INT,
        height INT,
        color TEXT,
        description TEXT,
        alt TEXT
      );
    """)

if __name__ == "__main__":
  createTable()
