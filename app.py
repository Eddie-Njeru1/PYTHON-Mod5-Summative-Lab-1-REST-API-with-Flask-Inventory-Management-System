#Flask routes REST API to manage the inventory in-memory

from flask import Flask, jsonify, request #import dependencies 
import data #import form data.py
import openfoodfacts #from openfoodfacts.py

app = Flask(__name__) #Flask application instance

#Retrieve all inventory items
@app.route('/inventory', methods=['GET']) 
def get_inventory():
    return jsonify(data.get_all_items()), 200 #JSON response with inventory items and a HTTP status code 200 OK

#Retieve one item in inventory using its Id
@app.route('/inventory/<int:item_id>', methods=['GET']) 
def get_inventory_item(item_id):
    item = data.get_item_by_id(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404  
    return jsonify(item), 200 #JSON response with inventory item and a HTTP status code 200 OK

#Create new item in inventory manually
@app.route('/inventory', methods=['POST']) 
def create_inventory_item():
    new_data = request.get_json() #Extract JSON data from request body
    if not new_data:
        return jsonify({"error": "Request body must be JSON"}), 400 #JSON response if request body is invalid and a HTTP status code 400
    new_item = data.add_item(new_data) #Pass data to data module to create new item
    return jsonify(new_item), 201 #JSON response with new inventory item and a HTTP status code 201

#Add item in inventory using barcode (from openfoodfacts.py)
@app.route('/inventory/barcode/<barcode>', methods=['POST'])
def add_item_by_barcode(barcode): 
    product_data = openfoodfacts.get_product_by_barcode(barcode) #Retrieve product info from API using barcode
    if product_data is None:
        return jsonify({"error": "Product not found in OpenFoodFacts"}), 404 #Return HTTP status code 404 if not found
    new_item = data.add_item(product_data) #Add product info into inventory
    return jsonify(new_item), 201 #response with newly created item and HTTP status code 201

#Update existing item in inventory
@app.route('/inventory/<int:item_id>', methods=['PATCH']) 
def update_inventory_item(item_id):
    changes = request.get_json() #Extract fields to be updated from JSON request body
    if not changes:
        return jsonify({"error": "Request body must be JSON"}), 400 #JSON response if request body is invalid and a HTTP status code 400
    updated_item = data.update_item(item_id, changes) #Pass requested changes to data module
    if updated_item is None:
        return jsonify({"error": "Item not found"}), 404 #JSON response with error and a HTTP status code 404
    return jsonify(updated_item), 200 #JSON response with updated inventory item and a HTTP status code 200 OK

#Delete existing item in inventory using its ID
@app.route('/inventory/<int:item_id>', methods=['DELETE']) 
def delete_inventory_item(item_id):
    deleted = data.delete_item(item_id) #Delete item using data module
    if not deleted:
        return jsonify({"error": "Item not found"}), 404
    return '', 204 #Indicates successful deletion and a HTTP status code

if __name__ == '__main__': #Start Flask development server when file is run directly
    app.run(debug=True)

