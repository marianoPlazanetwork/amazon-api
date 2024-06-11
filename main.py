from fastapi import FastAPI
from tools import scraping

app = FastAPI()

@app.get("/my-first-api")
def hello():
  return {"Hello world!"}

@app.get("/v1/get-info-amazon")
def scraperItemsAmazon(term: str):
  if (term.__len__() == 0):
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
  if (link.__len__() == 0):
    return { "code": 500, "message": "You should send a search link", "items": [] }
  dataProduct = scrapperItemAmazon(link)
  return { "code": 200, "message": "Success", "items": dataProduct }
