from fastapi import FastAPI, HTTPException
from tests.models.cart_models import UserModel, ItemModel, CartResponseModel

app = FastAPI(title="OrderFlow API")

# Временное хранилище в памяти (в Модуле 3 заменим на настоящую PostgreSQL в Docker!)
USERS_DB: dict[int, UserModel] = {}
CARTS_DB: dict[int, list[ItemModel]] = {}


@app.post("/users", response_model=UserModel, status_code=201)
def create_user(user: UserModel):
    if user.id in USERS_DB:
        raise HTTPException(status_code=400, detail="User already exists")
    USERS_DB[user.id] = user
    CARTS_DB[user.id] = []
    return user


@app.post("/users/{user_id}/items", response_model=CartResponseModel)
def add_item_to_cart(user_id: int, item: ItemModel):
    if user_id not in USERS_DB:
        raise HTTPException(status_code=404, detail="User not found")
    CARTS_DB[user_id].append(item)
    return CartResponseModel(user=USERS_DB[user_id], items=CARTS_DB[user_id])


@app.get("/users/{user_id}/cart", response_model=CartResponseModel)
def get_cart(user_id: int):
    if user_id not in USERS_DB:
        raise HTTPException(status_code=404, detail="User not found")
    return CartResponseModel(user=USERS_DB[user_id], items=CARTS_DB[user_id])


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    if user_id not in USERS_DB:
        raise HTTPException(status_code=404, detail="User not found")
    del USERS_DB[user_id]
    del CARTS_DB[user_id]