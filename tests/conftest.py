import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.clients.order_client import OrderClient

from tests.models.cart_models import DataGenerator, UserModel


@pytest.fixture
def api_client() -> TestClient:
    """Фикстура HTTP-клиента для отправки запросов в наш FastAPI сервис."""
    return TestClient(app)

@pytest.fixture
def order_client(api_client: TestClient) -> OrderClient:
    """Фикстура нашего умного API-клиента."""
    return OrderClient(api_client)


@pytest.fixture
def created_user(order_client: OrderClient) -> UserModel:

    user = order_client.create_user(DataGenerator.random_user())

    yield user

    order_client.delete_user(user.id)