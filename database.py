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
  sql = """
    INSERT INTO PHOTO 
    (id, raw, full, regular, small, thumb, created_at, updated_at, width, height, color, description, alt) 
    values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  """
  data = (photo.id, photo.raw, photo.full, photo.regular, photo.small, photo.thumb,
  photo.createdAt, photo.updatedAt, photo.width, photo.height, photo.color, photo.description, photo.alt)

  with conn:
    conn.execute(sql, data)
    #conn.commit()
    #conn.executemany(sql, data)

def fetchOneById(id):
  conn = sqlite3.connect(DB_NAME)
  sql = "SELECT * FROM PHOTO WHERE id = ?"

  with conn:
    cursor = conn.cursor()
    cursor.execute(sql, (id,))
    return cursor.fetchone()

if __name__ == "__main__":
  createTable()
