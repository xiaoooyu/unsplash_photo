from dateutil import parser as dparser

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
    self.createAt = dparser.parse(dict['created_at'], fuzzy = True)
    self.updateAt = dparser.parse(dict['updated_at'], fuzzy = True)
    self.width = dict['width']
    self.height = dict['height']
    self.color = dict['color']
    self.description = dict['description']
    self.alt = dict['alt_description']
  