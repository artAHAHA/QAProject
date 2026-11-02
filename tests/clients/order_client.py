from fastapi.testclient import TestClient
from httpx import Response
from tests.models.cart_models import UserModel, CartResponseModel


class OrderClient:
    def __init__(self, client: TestClient):
        self.client = client

    def create_user(self, user_data: dict) -> UserModel:
        response = self.client.post("/users", json=user_data)
        assert response.status_code == 201, f"Ошибка создания пользователя: {response.text}"
        return UserModel(**response.json())

    def add_item(self, user_id: int, item_data: dict) -> Response:
        response = self.client.post(f"/users/{user_id}/items", json=item_data)
        assert response.status_code == 200, f"Ошибка добавления товара: {response.text}"
        return response

    def get_cart_raw(self, user_id: int) -> Response:
        """Возвращает сырой Response (нужно для негативных тестов, например проверки 404)."""
        return self.client.get(f"/users/{user_id}/cart")

    def get_cart_model(self, user_id: int) -> CartResponseModel:
        response = self.get_cart_raw(user_id)
        assert response.status_code == 200
        return CartResponseModel(**response.json())

    def delete_user(self, user_id: int) -> Response:
        return self.client.delete(f"/users/{user_id}")