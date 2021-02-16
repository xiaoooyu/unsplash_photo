from dateutil import parser as dparser

import sqlite3
from database import DB_NAME

class Photo:
  
  def __init__(self):
    super().__init__()
  
  def __init__(
    self,
    id,
    raw,
    full,
    regular,
    small,
    thumb,
    createdAt,
    updatedAt,
    width,
    height,
    color,
    description,
    alt,
  ):
    self.id = id
    self.raw = raw
    self.full = full
    self.regular = regular
    self.small = small
    self.thumb = thumb
    self.createdAt = createdAt
    self.updatedAt = updatedAt
    self.width = width
    self.height = height
    self.color = color
    self.description = description
    self.alt = alt

  def __init__(self, dict):
    self.id = dict['id']
    self.raw = dict['urls']['raw']
    self.full =	dict['urls']['full']
    self.regular = dict['urls']['regular']
    self.small = dict['urls']['small']
    self.thumb = dict['urls']['thumb']
    self.createdAt = dparser.parse(dict['created_at'], fuzzy = True)
    self.updatedAt = dparser.parse(dict['updated_at'], fuzzy = True)
    self.width = dict['width']
    self.height = dict['height']
    self.color = dict['color']
    self.description = dict['description']
    self.alt = dict['alt_description']

  def insertOrUpdate(self):
    conn = sqlite3.connect(DB_NAME)
    photo = self
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

  