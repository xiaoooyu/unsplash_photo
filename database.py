import sqlite3
from model.photo import Photo

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

def insertOrUpdate(photo):
  conn = sqlite3.connect(DB_NAME)
  sql = 'INSERT INTO USER (id, name, age) values(?, ?, ?)'
  data = [
    (1, 'Alice', 21),
    (2, 'Bob', 22),
    (3, 'Chris', 23),
  ]

  with conn:
    conn.executemany(sql, data)

if __name__ == "__main__":
  createTable()
