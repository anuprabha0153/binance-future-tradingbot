"""
validators.py
--------------
Simple functions that check whether the user's CLI input makes sense
BEFORE we send anything to Binance. This prevents silly API errors.

Beginner note: each function either does nothing (input is fine) or
raises a ValueError with a clear message (input is bad).
"""

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def validate_symbol(symbol: str) -> str:
    """Symbol must be letters only, e.g. BTCUSDT. We uppercase it for safety."""
    symbol = symbol.strip().upper()
    if not symbol.isalpha():
        raise ValueError(f"Invalid symbol '{symbol}'. Example of a valid symbol: BTCUSDT")
    return symbol


def validate_side(side: str) -> str:
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValueError(f"Invalid side '{side}'. Must be one of {VALID_SIDES}")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(f"Invalid order type '{order_type}'. Must be one of {VALID_ORDER_TYPES}")
    return order_type


def validate_quantity(quantity: float) -> float:
    if quantity <= 0:
        raise ValueError(f"Quantity must be greater than 0. Got: {quantity}")
    return quantity


def validate_price(price, order_type: str):
    """
    Price is REQUIRED for LIMIT orders, and must be a positive number.
    Price is ignored for MARKET orders (Binance decides the price).
    """
    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders (use --price).")
        if price <= 0:
            raise ValueError(f"Price must be greater than 0. Got: {price}")
    return price
