import pytest
from shop.value_objects import Money

def test_money_creation():
    m = Money(100.0, "UAH")
    assert m.amount == 100.0
    assert m.currency == "UAH"

def test_negative_money_raises_value_error():
    with pytest.raises(ValueError, match="cannot be negative"):
        Money(-10.0)

def test_money_addition():
    m1 = Money(100.0)
    m2 = Money(50.0)
    res = m1 + m2
    assert res.amount == 150.0