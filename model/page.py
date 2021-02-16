import requests
from model.photo import Photo

class Page:
  
  def __init__(self):
    super().__init__()

  def __init__(
    self,
    url,
    pageIndex,
    pageSize
  ):
    self.url = url
    self.pageIndex = pageIndex
    self.pageSize = pageSize

  def fetchPhotos(self):
    params = {'per_page':self.pageSize, 'page':self.pageIndex}
    r = requests.get(url = self.url, params = params)
    data = r.json()

    result = []
    for d in data:
      result.append(Photo(d))
    
    return result