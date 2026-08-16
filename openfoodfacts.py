#Queries the OpenFoodFacts API for item by barcode and wires results into app.py

import requests

BASE_URL = "https://world.openfoodfacts.org/api/v2/product" #This is the product-by-barcode endpoint
HEADERS = {"User-Agent": "InventoryManagementSystem/1.0 (email@example.com)"} #Unique user agent used to identify the app when making requests

#Rerieve product info from API using bar code
def get_product_by_barcode(barcode):
    url = f"{BASE_URL}/{barcode}.json" #Request URL created using barcode 
    params = {"fields": "code,product_name, brands, ingredients_text"} #Request only the product fileds required by the inventory system
    response = requests.get(url, headers=HEADERS, params=params) #Sends GET request to the API

    if response.status_code != 200:
        return None #If the API request is unsuccessful
    result = response.json() #Converts JSON response into python dictionary
    if result.get("status") != 1:
        return None
    product = result["product"] #Extract product info from API response
    return { #Return product data 
        "code": product.get("code"),
        "product_name": product.get("product_name"),
        "brands": product.get("brands"),
        "ingredients_text": product.get("ingredients_text"),
    }
