To perform CRUD operations on your FastAPI app using **Postman**, follow these steps. Your app has 5 routes for managing items, so we’ll walk through each one:

---

## 🧪 Setup in Postman

- **Base URL**: `http://127.0.0.1:8000`
- **Headers**: Add `Content-Type: application/json` for POST and PUT requests.

---

## 🔍 1. GET All Items

- **Method**: `GET`
- **URL**: `http://127.0.0.1:8000/items`
- **Body**: _None_
- **Response**: Returns all items in the in-memory store.

---

## 🔍 2. GET Item by ID

- **Method**: `GET`
- **URL**: `http://127.0.0.1:8000/items/1`
- **Body**: _None_
- **Response**: Returns item with ID `1` if it exists.

---

## 🆕 3. POST Create Item

- **Method**: `POST`
- **URL**: `http://127.0.0.1:8000/items/1`
- **Body**: Select **raw** → **JSON** and enter:

```json
{
  "name": "Laptop",
  "description": "A powerful machine"
}
```

- **Response**: Confirms item creation.

---

## ✏️ 4. PUT Update Item

- **Method**: `PUT`
- **URL**: `http://127.0.0.1:8000/items/1`
- **Body**: Select **raw** → **JSON** and enter:

```json
{
  "name": "Laptop Pro",
  "description": "Upgraded version"
}
```

- **Response**: Confirms item update.

---

## ❌ 5. DELETE Item

- **Method**: `DELETE`
- **URL**: `http://127.0.0.1:8000/items/1`
- **Body**: _None_
- **Response**: Confirms item deletion.

---

## ✅ Tips

- Use Postman's **Save** feature to store each request.
- Use the **Tests** tab to write simple assertions if needed.
- You can also explore the API via Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

