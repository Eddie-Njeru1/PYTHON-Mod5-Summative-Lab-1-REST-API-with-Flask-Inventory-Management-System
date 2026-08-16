# This CLI allows users to interact with the Flask API

import argparse # Module for parsing command-line arguments and options.
import requests # Module for sending HTTP requests

BASE_URL = "http://127.0.0.1:5000/inventory" #For inventory API

# View all items in the inventory
def view_inventory():
    try:
        response = requests.get(BASE_URL)
    except requests.exceptions.RequestException:
        print("Error: could not reach the API. Ensure Flask server is running.")
        return 
    if response.status_code != 200:
        print(f"Error: unexpected response ({response.status_code})")
        return
    items = response.json()
    if not items:
        print("Inventory is empty.")
        return
    for item in items:
        print(item)

# Add new item to inventory manually
def add_item(args):
    payload = {
        "product_name": args.name,
        "brands": args.brand,
        "ingredients_text": args.ingredients,
        "code": args.code,
        "price": args.price,
        "stock": args.stock,
    }
    try:
        response = requests.post(BASE_URL, json=payload)
    except requests.exceptions.RequestException:
        print("Error: could not reach the API.")
        return
    if response.status_code == 201:
        print("Item added:", response.json())
    else:
        print(f"Error adding item ({response.status_code}):", response.json())

# Find and add item to inventory using barcode
def find_on_api(args):
    url = f"{BASE_URL}/barcode/{args.barcode}"
    try:
        response = requests.post(url)
    except requests.exceptions.RequestException:
        print("Error: could not reach API.")
        return
    if response.status_code == 201:
        print("Item found and added:", response.json())
    elif response.status_code == 404:
        print("Product not found on OpenFoodFacts.")
    else:
        print(f"Unexpected error ({response.status_code}):", response.json())

# Update price and stock of item in inventory
def update_item(args):
    changes = {}
    if args.price is not None:
        changes["price"] = args.price
    if args.stock is not None:
        changes["stock"] = args.stock
    if not changes:
        print("Nothing to update.")
        return
    url = f"{BASE_URL}/{args.id}"
    try:
        response = requests.patch(url, json=changes)
    except requests.exceptions.RequestException:
        print("Error: could not reach API.")
        return
    if response.status_code == 200:
        print("Item updated:", response.json())
    elif response.status_code == 404:
        print(f"No item found with id {args.id}.")
    else:
        print(f"Unexpected error ({response.status_code}):", response.json())

# Delete item from inventory by id
def delete_item(args):
    url = f"{BASE_URL}/{args.id}"
    try:
        response = requests.delete(url)
    except requests.exceptions.RequestException:
        print("Error: could not reach API.")
        return
    if response.status_code == 204:
        print(f"Item {args.id} deleted.")
    elif response.status_code == 404:
        print(f"No item found with id {args.id}.")
    else:
        print(f"Unexpected error ({response.status_code}):", response.json())

# Configure and run the CLI
def main():
    parser = argparse.ArgumentParser(
        description="Inventory Management CLI"
    )
    subparsers = parser.add_subparsers(dest="command") # Subcommand for different inventory operations
    subparsers.add_parser( #View command
        "view",
        help="view all inventory items"
    )
    add_parser = subparsers.add_parser( #Add command
        "add",
        help="Add a new item manually"
    )
    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--brand", required=True)
    add_parser.add_argument("--ingredients", required=True)
    add_parser.add_argument("--code", required=True)
    add_parser.add_argument("--price", type=float, required=True)
    add_parser.add_argument("--stock", type=int, required=True)

# Find command
    find_parser = subparsers.add_parser(
        "find",
        help="Find and add item by barcode through OpenFoodFacts"
    )
    find_parser.add_argument("barcode")

# Update command
    update_parser = subparsers.add_parser(
     "update",
     help="Update price/stock for an item"
    )
    update_parser.add_argument("id", type=int)
    update_parser.add_argument("--price", type=float, default=None)
    update_parser.add_argument("--stock", type=int, default=None)

# Delete command 
    delete_parser = subparsers.add_parser(
     "delete",
     help="Delete an item by id"
)
    delete_parser.add_argument("id", type=int)
    args = parser.parse_args()

# Run function for selected command 
    if args.command == "view":
        view_inventory()
    elif args.command == "add":
        add_item(args)
    elif args.command == "find":
        find_on_api(args)
    elif args.command == "update":
        update_item(args)
    elif args.command == "delete":
        delete_item(args)
    else:
        parser.print_help()

#Run CLI when file is executed directly
if __name__ == "__main__":
    main()