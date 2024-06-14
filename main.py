from fastapi import FastAPI
from pydantic import BaseModel
from tools import scraping, scrappingProduct, scrappingProducts

app = FastAPI()

@app.get("/my-first-api")
def hello():
  return {"Hello world!"}

@app.get("/v1/get-info-amazon")
def scraperItemsAmazon(term: str):
  if (len(term) == 0):
    return { "code": 500, "message": "You should send a search term", "items": [] }
  datosAmazon = []
  try:
    datosAmazon = scraping(True, term)
  except:
    return { "code": 404, "message": "Error: products could not be obtained", "items": [] } 
  if(len(datosAmazon) == 0): 
    return { "code": 404, "message": "Products could not be obtained", "items": [] }
  return { "code": 200, "message": "Success", "items": datosAmazon }

@app.get('/v1/get-info-item')
def scrapperItemAmazon(link: str):
  if (len(link) == 0):
    return { "code": 500, "message": "You should send a search link", "items": [] }
  try:
    dataProduct = scrappingProduct(link)
  except:
    return { "code": 404, "message": "Error: products could not be obtained", "items": [] } 
  return { "code": 200, "message": "Success", "items": dataProduct }

class URLProduct(BaseModel):
  links: list = []

@app.post('/v1/get-data-products-links')
def getDataProduct(data: URLProduct):
  try:
    dataProducts = scrappingProducts(data.links)
  except:
    return { "code": 404, "message": "Error: products could not be obtained", "items": [] } 
  return { "code": 200, "message": "Success", "items": dataProducts }
