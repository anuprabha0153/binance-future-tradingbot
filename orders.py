"""
orders.py
---------
Sits between the CLI and the Binance client. It:
1. Validates input (using validators.py)
2. Calls client.py to actually place the order
3. Formats a clean summary for the user to read

Beginner note: this separation means if you ever swap python-binance
for raw REST calls, you'd only need to change client.py -- cli.py and
orders.py wouldn't need to change.
"""

from bot import validators
from bot.client import place_order
from bot.logging_config import setup_logger

logger = setup_logger()


def validate_inputs(symbol, side, order_type, quantity, price):
    """
    Runs all validators and returns the cleaned (uppercased, checked)
    values. Raises ValueError on the first bad input found.
    This is called BEFORE we ever try to connect to Binance, so bad
    input fails fast without wasting an API call.
    """
    symbol = validators.validate_symbol(symbol)
    side = validators.validate_side(side)
    order_type = validators.validate_order_type(order_type)
    quantity = validators.validate_quantity(quantity)
    price = validators.validate_price(price, order_type)
    return symbol, side, order_type, quantity, price


def build_and_place_order(client, symbol, side, order_type, quantity, price):
    """
    Validates all inputs, prints a request summary, places the order,
    then prints a response summary. Returns the Binance response dict.
    """
    # ---- 1. Validate everything first ----
    symbol, side, order_type, quantity, price = validate_inputs(
        symbol, side, order_type, quantity, price
    )

    # ---- 2. Show the user exactly what will be sent ----
    print("\n--- ORDER REQUEST SUMMARY ---")
    print(f"Symbol     : {symbol}")
    print(f"Side       : {side}")
    print(f"Order Type : {order_type}")
    print(f"Quantity   : {quantity}")
    if order_type == "LIMIT":
        print(f"Price      : {price}")
    print("-----------------------------\n")

    # ---- 3. Place the order (network call happens in client.py) ----
    response = place_order(client, symbol, side, order_type, quantity, price)

    # ---- 4. Show the response nicely ----
    print("--- ORDER RESPONSE ---")
    print(f"Order ID     : {response.get('orderId')}")
    print(f"Status       : {response.get('status')}")
    print(f"Executed Qty : {response.get('executedQty')}")
    # avgPrice only appears/matters once an order is filled
    print(f"Avg Price    : {response.get('avgPrice', 'N/A')}")
    print("----------------------\n")

    print(f"✅ Order placed successfully! (Order ID: {response.get('orderId')})")

    return response
