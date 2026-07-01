"""
client.py
---------
This file's ONLY job is to talk to Binance. Nothing about CLI or
user input lives here. Keeping this separate is what the task means
by "separate client/API layer and command/CLI layer".

We use the python-binance library, which wraps Binance's REST API
for us so we don't have to build HTTP requests by hand.
"""

import os
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

from bot.logging_config import setup_logger

logger = setup_logger()

# Binance Futures Testnet base URL (given in the task)
FUTURES_TESTNET_URL = "https://testnet.binancefuture.com"


def get_client() -> Client:
    """
    Creates and returns a python-binance Client configured to talk
    to the FUTURES TESTNET (fake money, safe to experiment).

    API keys are read from environment variables so you never hard-code
    secrets into the source code (important for security + GitHub).
    """
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        raise EnvironmentError(
            "Missing API credentials. Please set BINANCE_API_KEY and "
            "BINANCE_API_SECRET as environment variables."
        )

    client = Client(api_key, api_secret, testnet=True)

    # Make sure it points at the FUTURES testnet specifically
    client.FUTURES_URL = FUTURES_TESTNET_URL + "/fapi"

    return client


def place_order(client: Client, symbol: str, side: str, order_type: str,
                 quantity: float, price: float = None):
    """
    Sends the actual order to Binance Futures Testnet.

    Returns the raw response dict from Binance on success.
    Raises an exception on failure (caught later in cli.py).
    """
    order_params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
    }

    if order_type == "LIMIT":
        # LIMIT orders on Binance require timeInForce + a price
        order_params["price"] = price
        order_params["timeInForce"] = "GTC"  # Good-Til-Cancelled

    logger.info(f"Sending order request: {order_params}")

    try:
        response = client.futures_create_order(**order_params)
        logger.info(f"Order response received: {response}")
        return response

    except (BinanceAPIException, BinanceRequestException) as e:
        # These are errors Binance itself returns (e.g. bad symbol, insufficient balance)
        logger.error(f"Binance API error: {e}")
        raise

    except Exception as e:
        # Anything else (e.g. no internet connection)
        logger.error(f"Unexpected/network error while placing order: {e}")
        raise
