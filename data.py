#Database for managing inventory items using CRUD

inventory = [] #Stores inventory items
next_id = 1 #Assigns unique Id to new item in the inventory

def get_all_items(): #Will return a list with inventory items 
    return inventory

def get_item_by_id(item_id): #Find item by ID
    for item in inventory:
        if item["id"] == item_id:
            return item #Item is found
        return None #Item is not found

def add_item(data): #Create a new item into the inventory
    global next_id #Assigns the new item and ID
    new_item = { #Items information 
        "id": next_id,
        "product_name": data.get("product_name"),
        "brands": data.get("brands"),
        "ingredients_text": data.get("ingredients_text"),
        "code": data.get("code"),
        "price": data.get("price"),
        "stock": data.get("stock"),
    }
    inventory.append(new_item) #Add new item to inventory
    next_id += 1 #Id counter will add the next item
    return new_item

def update_item(item_id, changes):#Update an existing item in the inventory
    item = get_item_by_id(item_id) #Identify items that needs to be updated
    if item is None: 
        return None
    item.update(changes) #updates the changes 
    return item

def delete_item(item_id): #Delete item from inventory using its ID
    item = get_item_by_id(item_id) #Identify items that needs to be deleted
    if item is None: #
        return False
    inventory.remove(item) #removes item from inventory
    return True
