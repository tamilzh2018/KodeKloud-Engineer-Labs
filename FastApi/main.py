from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# In-memory "database"
items = {}

# Pydantic model for item
class Item(BaseModel):
    name: str
    description: str

# 1️⃣ GET all items
@app.get("/items")
def get_items():
    return items

# 2️⃣ GET item by ID
@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

# 3️⃣ POST a new item
@app.post("/items/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in items:
        raise HTTPException(status_code=400, detail="Item already exists")
    items[item_id] = item
    return {"message": "Item created", "item": item}

# 4️⃣ PUT to update an item
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = item
    return {"message": "Item updated", "item": item}

# 5️⃣ DELETE an item
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    return {"message": "Item deleted"}
