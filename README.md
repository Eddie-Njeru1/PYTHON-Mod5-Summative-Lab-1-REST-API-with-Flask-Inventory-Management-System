# Flask Inventory Management System
This is a REST API for managing retail inventory, built with Flask. It allows items to be added, viewed, updated, and deleted through the API, with data enriched using the OpenFoodFacts database. A CLI client is included for interacting with the API from the terminal.

# Features
* Create, view, update, and delete inventory items via REST API.
* Fetch product data automatically from OpenFoodFacts using a barcode.
* Update item price and stock levels independently.
* CLI tool to perform all of the above from the terminal.
* Automated tests covering API endpoints, CLI commands, and the OpenFoodFacts integration.

# Project Structure
Flask-Inventory-Management-System/
├── app.py # Flask REST API routes
├── data.py # In-memory inventory storage and CRUD logic
├── openfoodfacts.py # OpenFoodFacts API integration
├── cli.py # CLI client for the API
├── tests/
│ ├── test_routes.py
│ ├── test_openfoodfacts.py
│ └── test_cli.py
├── Pipfile
├── Pipfile.lock
└── README.md

# Data Model
* Each inventory item is a dictionary with an id, product_name, brands, ingredients_text, code, price, and stock.
* Items can be added manually through the API, or fetched automatically from OpenFoodFacts by supplying a barcode.
* All items live in a single in-memory list. Data resets each time the Flask server restarts.

# Prerequisites
Before running the project, ensure you have the following installed:
    * Python 3.x
    * Pipenv

# Installation and dependencies
* Clone the repository and create the virtual environment:
    * git clone <https://github.com/Eddie-Njeru1/PYTHON-Mod5-Summative-Lab-1-REST-API-with-Flask-Inventory-Management-System.git>
    * cd PYTHON-Mod5-Summative-Lab-1-REST-API-with-Flask-Inventory-Management-System
    * pipenv install - create project dependencies and virtual environment
    * pipenv shell - launch virtual environment
    * pipenv install flask requests - installs Flask
    * pipenv install pytest pytest-mock --dev - installs testing fields

The Pipfile defines the project's dependencies, while Pipfile.lock ensures consistent package versions across different development environments.
* flask — powers the REST API and routing.
* requests — used both to call the OpenFoodFacts API, and by the CLI to communicate with the Flask server.
* pytest, pytest-mock (dev only) — used for running the automated test suite and mocking external API calls during testing.

# Running the Application
* Start the Flask server first, from the project root:
    * python app.py
The API runs at http://127.0.0.1:5000. Leave this running, and use a separate terminal for CLI commands below.

* View All Items
    * python cli.py view
    * Add an Item Manually:
        python cli.py add
        --name "Milk"
        --brand "Brookside"
        --ingredients "Milk"
        --code "123456789"
        --price 2.5
        --stock 10

* Find and Add an Item by Barcode
    * python cli.py find 3017624010701

* Update Price or Stock
    * python cli.py update 1 --price 3.00 --stock 15

* Delete an Item
    * python cli.py delete 1

        * Note: Items must exist before they can be updated or deleted. If a requested id cannot be found, the API returns an error response instead of crashing.

* Running the Tests
Execute the test suite with:
    * pipenv run pytest -v

The tests verify:
* CRUD behaviour across all API endpoints.
* CLI commands and how they handle API responses.
* The OpenFoodFacts integration, using mocked responses so no real network calls are made during testing.

# Current Limitations
The current version intentionally keeps the feature set simple.
* Data is stored in memory only so inventory items are lost when the Flask server restarts.
* Items are identified by numeric id only.
* The API does not verify that submitted fields like price or stock are the correct type before storing them.
* Only one product can be looked up per barcode request. There is no bulk import from OpenFoodFacts.
