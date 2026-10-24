from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session
from shop.models import Category, Product


class CategoryRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, name: str) -> Category:
        category = Category(name=name)
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category

    def get_by_id(self, category_id: int) -> Category | None:
        return self.session.get(Category, category_id)

    def get_by_name(self, name: str) -> Category | None:
        statement = select(Category).where(Category.name == name)
        return self.session.scalar(statement)


class ProductRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, product: Product) -> Product:
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def get_by_id(self, product_id: int) -> Product | None:
        return self.session.get(Product, product_id)

    def get_all(self) -> Sequence[Product]:
        statement = select(Product)
        return self.session.scalars(statement).all()

    def filter_by_category(self, category_id: int) -> Sequence[Product]:
        statement = select(Product).where(Product.category_id == category_id)
        return self.session.scalars(statement).all()

    def update_price_and_quantity(self, product_id: int, price: float, quantity: int) -> Product | None:
        product = self.get_by_id(product_id)
        if product is None:
            return None
        product.price = price
        product.quantity = quantity
        self.session.commit()
        self.session.refresh(product)
        return product

    def delete(self, product_id: int) -> bool:
        product = self.get_by_id(product_id)
        if product is None:
            return False
        self.session.delete(product)
        self.session.commit()
        return True