import pytest
from pydantic import ValidationError
from tests.models.cart_models import CartResponseModel, ItemModel, DataGenerator


def test_cart_available_total_calculation():
    raw_response = {
        "user": {"id": 5, "name": "Artur"},
        "items": [
            {"title": "Keyboard", "price": 3000, "in_stock": True},
            {"title": "Mouse", "price": 1500, "in_stock": False},
            {"title": "Monitor", "price": 20000, "in_stock": True}
        ]
    }
    cart = CartResponseModel(**raw_response)

    assert cart.user.name == "Artur"
    assert cart.get_available_items_total() == 23000

@pytest.mark.parametrize(
    "invalid_title, invalid_price",
    [
        ("Mouse", 0),        # Кейс 1: граничное значение цены 0
        ("Mouse", -500),     # Кейс 2: отрицательная цена
        ("", 1500),          # Кейс 3: пустое имя товара
        ("Mouse", "free"),   # Кейс 4: неверный тип данных
    ]
)
def test_item_invalid_data_validation(invalid_title, invalid_price):
    with pytest.raises(ValidationError):
        ItemModel(title=invalid_title, price=invalid_price, in_stock=True)

def test_cart_with_generated_data():
    raw_response = {
        "user": DataGenerator.random_user(),
        "items": [
            DataGenerator.random_item(in_stock=True, price=1000),
            DataGenerator.random_item(in_stock=False, price=5000),
            DataGenerator.random_item(in_stock=True, price=2500)
        ]
    }
    cart = CartResponseModel(**raw_response)

    assert cart.get_available_items_total() == 3500



