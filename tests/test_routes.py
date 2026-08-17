# Test for Flas routes in app.py 

import pytest
import app
import data

#Test client that resets inventory before each test
@pytest.fixture
def client():
    data.inventory.clear()
    data.next_id = 1
    app.app.config["TESTING"] = True
    with app.app.test_client() as client:
        yield client

#Add sample item that returns ID
def add_sample_item(client):
    payload = {"product_name": "Milk", "price": 2.5, "stock": 10}
    response = client.post("/inventory", json=payload)
    return response.get_json()["id"]

#Create item and retrieve it
def test_create_and_get_item(client):
    item_id = add_sample_item(client)
    response = client.get(f"/inventory/{item_id}")
    assert response.status_code == 200
    assert response.get_json()["product_name"] == "Milk"

#Test updating existing item
def test_update_item(client):
    item_id = add_sample_item(client)
    response = client.patch(f"/inventory/{item_id}", json={"price": 1.5})
    assert response.status_code == 200
    assert response.get_json()["price"] == 1.5
    assert response.get_json()["stock"] == 10

#Test deleting item
def test_delete_item(client):
    item_id = add_sample_item(client)
    assert client.delete(f"/inventory/{item_id}").status_code == 204
    assert client.get(f"/inventory/{item_id}").status_code == 404

#requesting a non existent item
def test_get_item_not_found(client):
    assert client.get("/inventory/999").status_code == 404

#test adding item using barcode
def test_add_item_by_barcode(client, mocker):
    mocker.patch("app.openfoodfacts.get_product_by_barcode", return_value={
        "code": "3017624010701", "product_name": "Nutella",
        "brands": "Ferrero", "ingredients_text": "Sugar, palm oil, hazelnuts",
    })
    response = client.post("/inventory/barcode/3017624010701")
    assert response.status_code == 201
    assert response.get_json()["product_name"] == "Nutella"
   