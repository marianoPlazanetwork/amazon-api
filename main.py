from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from tools import scraping, scrappingProduct, scrappingProducts, scrappingProductSKU

app = FastAPI()

# Mount static files (optional for CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 template directory
templates = Jinja2Templates(directory="templates")

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

@app.get('/v1/get-info-amazon-sku')
def scrapperItemAmazonSKU(sku: str):
  if (len(sku) == 0):
    return { "code": 500, "message": "You should send a search term", "items": [] }
  datosAmazon = []
  try:
    datosAmazon = scrappingProductSKU(sku)
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
  except  Exception as e:
    print(e)
    return { "code": 404, "message": "Error: products could not be obtained", "items": [] } 
  return { "code": 200, "message": "Success", "items": dataProducts }
