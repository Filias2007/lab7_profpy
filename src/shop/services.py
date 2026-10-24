import sqlite3
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from shop.models import Product
from shop.exceptions import InsufficientStockError


class ShopService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_total_stock_value(self) -> float:
        statement = select(func.sum(Product.price * Product.quantity))
        result = self.session.scalar(statement)
        return float(result) if result is not None else 0.0

    def get_most_expensive_product(self) -> Product | None:
        statement = select(Product).order_by(Product.price.desc()).limit(1)
        return self.session.scalar(statement)

    def purchase_product(self, product_id: int, quantity_to_buy: int) -> Product:
        """Транзакційна покупка товару з перевіркою залишків та rollback при помилці."""
        try:
            product = self.session.get(Product, product_id)
            if product is None:
                raise ValueError(f"Product with ID {product_id} not found")

            if product.quantity < quantity_to_buy:
                raise InsufficientStockError(
                    f"Not enough stock: available {product.quantity}, requested {quantity_to_buy}"
                )

            product.quantity -= quantity_to_buy
            self.session.commit()
            self.session.refresh(product)
            return product
        except Exception:
            self.session.rollback()
            raise


def find_products_by_category_db_api(db_path: str, category_name: str) -> list[tuple]:
    """Демонстрація робочого DB-API з параметризованим SQL-запитом."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        query = """
            SELECT p.id, p.name, p.price, p.quantity
            FROM products p
            JOIN categories c ON p.category_id = c.id
            WHERE c.name = ?
        """
        cursor.execute(query, (category_name,))
        return cursor.fetchall()