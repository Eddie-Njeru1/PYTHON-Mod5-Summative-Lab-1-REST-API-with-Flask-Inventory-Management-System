# Test the CLI 

import cli

#Create a mock HTTP response for testing
def make_response(mocker, status_code, json_data=None):
    response = mocker.Mock()
    response.status_code = status_code
    response.json.return_value = json_data
    return response

#Test adding new item to inventoy
def test_add_item(mocker, capsys):
    mocker.patch( # simulate a successful API response
        "cli.requests.post",
        return_value=make_response(
            mocker, 201, {"id": 1, "product_name": "Bread"}
        )
    )

#Test adding new item to inventoy
def test_add_item(mocker, capsys):
    mocker.patch( # simulate a successful API response
        "cli.requests.post",
        return_value=make_response(
            mocker, 201, {"id": 1, "product_name": "Bread"}
        )
    )
    #sample item data 
    args = mocker.Mock(
        name="Bread",
        brand="Festive",
        ingredients="Flour",
        code="123",
        price=1.5,
        stock=5
    )
    #Run add item function
    cli.add_item(args)
    assert "added" in capsys.readouterr().out.lower()

#Test deleting item to inventoy
def test_delete_item(mocker, capsys):
    mocker.patch( # simulate a successful delete response
        "cli.requests.delete",
        return_value=make_response(
            mocker, 204)
    )
    #sample item data 
    args = mocker.Mock(id=1)
    #Run delete item function
    cli.delete_item(args)
    assert "deleted" in capsys.readouterr().out.lower()

#Test handling API connection error
def test_view_inventory_connection_error(mocker, capsys):
    mocker.patch( # simulate a successful API response
        "cli.requests.get",
        side_effect=cli.requests.exceptions.RequestException
    )
    
    #Run view inventory function
    cli.view_inventory()
    assert "could not reach the api" in capsys.readouterr().out.lower()
    