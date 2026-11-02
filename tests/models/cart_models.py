from pydantic import BaseModel, Field
from faker import Faker

class UserModel(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1)

class ItemModel(BaseModel):
    title: str = Field(min_length=1)
    price: int = Field(gt=0)
    in_stock: bool

class CartResponseModel(BaseModel):
    user: UserModel
    items: list[ItemModel]

    def get_available_items_total(self) -> int:
        return sum(item.price for item in self.items if item.in_stock)

fake = Faker()

class DataGenerator:
    @staticmethod
    def random_user() -> dict:
        return {
            "id": fake.random_int(min=1, max=10000),
            "name": fake.first_name()
        }

    @staticmethod
    def random_item(in_stock: bool = True, price: int | None = None) -> dict:
        return {
            "title": fake.word().capitalize(),
            # Если цену не передали явно, генерируем случайную от 100 до 50000:
            "price": price if price is not None else fake.random_int(min=100, max=50000),
            "in_stock": in_stock
        }