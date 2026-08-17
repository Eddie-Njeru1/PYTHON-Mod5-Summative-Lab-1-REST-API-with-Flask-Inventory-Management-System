# test the OPenFoodfacts API 

import openfoodfacts

def test_get_product_by_barcode_success(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "code": "301624010701",
            "product_name": "Nutella",
            "brands": "Ferrero",
            "ingredients_text": "Sugar, palm oil, hazelnuts"
        },
    }
    
#Replace the real API  request with the mock respnse 
    mocker.patch(
        "openfoodfacts.requests.get",
        return_value=mock_response 
    )

#retrieve the product using barcode 
    result = openfoodfacts.get_product_by_barcode("3017624010701")

# veify the expected product data is returned
    assert result["product_name"] == "Nutella"
    assert result["brands"] == "Ferrero"

# test a barcode that is not found by the API
def test_get_product_by_barcode_not_found(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": 0},
        
    #Replace the real API  request with the mock respnse 
    mocker.patch(
        "openfoodfacts.requests.get",
        return_value=mock_response 
    )

#  search for non existent bar code
    result = openfoodfacts.get_product_by_barcode("1111111111111111")

#verify that None is returned when no product is found
    assert result is None 

# Test a failed request to the API
def test_get_product_by_barcode_request_failed(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mock_response.json.return_value = {"status": 0},
        
    #Replace the real API  request with the mock respnse 
    mocker.patch(
        "openfoodfacts.requests.get",
        return_value=mock_response 
    )

#attempt to retriev product
    result = openfoodfacts.get_product_by_barcode("3017624010701")

# verify that None is returned when the rerquest fails
    assert result is None 

