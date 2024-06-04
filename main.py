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
  datosAmazon = scraping(True, term)
  if(len(datosAmazon) == 0): 
    return { "code": 404, "message": "Products could not be obtained", "items": [] }
  return { "code": 200, "message": "Success", "items": datosAmazon }
