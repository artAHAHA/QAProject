from fastapi.testclient import TestClient

from tests.clients.order_client import OrderClient
from tests.models.cart_models import UserModel, CartResponseModel, DataGenerator


def test_add_items_and_check_cart_api(order_client: OrderClient, created_user: UserModel):
    item1 = DataGenerator.random_item(in_stock=True, price=4000)
    item2 = DataGenerator.random_item(in_stock=False, price=10000)

    order_client.add_item(created_user.id, item1)
    order_client.add_item(created_user.id, item2)

    cart =  order_client.get_cart_model(created_user.id)

    assert len(cart.items) == 2

    assert cart.get_available_items_total() == 4000


def test_get_non_existent_user_cart_returns_404(order_client: OrderClient):
    response = order_client.get_cart_raw(999999)

    assert response.status_code == 404
