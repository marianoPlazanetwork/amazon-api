from fastapi import FastAPI
from tools import scraping, scrappingProduct

app = FastAPI()

@app.get("/v1/get-info-amazon")
def scraperItemsAmazon(term: str):
  if (term.__len__() == 0):
    return { "code": 500, "message": "You should send a search term", "items": [] }
  datosAmazon = scraping(True, term)
  return { "code": 200, "message": "Success", "items": datosAmazon }

@app.get('/v1/get-info-item')
def scrapperItemAmazon(link: str):
  # if (link.__len__() == 0):
  #   return { "code": 500, "message": "You should send a search link", "items": [] }
  dataProduct = scrappingProduct(link)
  return { "code": 200, "message": "Success", "items": dataProduct }
