class ProductValidationError(Exception):
    """Помилка валідації даних товару."""
    pass

class InsufficientStockError(Exception):
    """Помилка недостатньої кількості товару на складі."""
    pass

class PaymentError(Exception):
    """Помилка обробки платежу."""
    pass