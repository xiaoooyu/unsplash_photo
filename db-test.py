import sqlite3 as sql
import database

conn = sql.connect("my-test.db")
with conn:
  conn.execute("""
    CREATE TABLE USER(
      id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
      name TEXT,
      age INTEGER
    );
  """)

sql = 'INSERT INTO USER (id, name, age) values(?, ?, ?)'
data = [
  (1, 'Alice', 21),
  (2, 'Bob', 22),
  (3, 'Chris', 23),
]

with conn:
  conn.executemany(sql, data)