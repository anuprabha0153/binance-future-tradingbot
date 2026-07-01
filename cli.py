"""
cli.py
------
This is the file you actually RUN. It reads command-line arguments,
then hands off the real work to bot/orders.py and bot/client.py.

EXAMPLES (run these in your terminal):

  Market order:
    python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01

  Limit order:
    python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 65000
"""

import argparse
import sys

from bot.client import get_client
from bot.orders import build_and_place_order, validate_inputs
from bot.logging_config import setup_logger

logger = setup_logger()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Simplified Trading Bot for Binance Futures Testnet"
    )
    parser.add_argument("--symbol", required=True, help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL", "buy", "sell"],
                         help="Order side: BUY or SELL")
    parser.add_argument("--type", required=True, dest="order_type",
                         choices=["MARKET", "LIMIT", "market", "limit"],
                         help="Order type: MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, type=float,
                         help="Quantity to buy/sell")
    parser.add_argument("--price", required=False, type=float, default=None,
                         help="Price (required only for LIMIT orders)")
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        # Step 1: validate input FIRST — fail fast before touching the network
        validate_inputs(args.symbol, args.side, args.order_type, args.quantity, args.price)

        # Step 2: connect to Binance Futures Testnet
        client = get_client()

        # Step 3: place the order
        build_and_place_order(
            client=client,
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )

    except ValueError as e:
        # Bad user input (caught by validators.py)
        logger.error(f"Input validation error: {e}")
        print(f"❌ Input error: {e}")
        sys.exit(1)

    except EnvironmentError as e:
        # Missing API keys
        logger.error(f"Configuration error: {e}")
        print(f"❌ Configuration error: {e}")
        sys.exit(1)

    except Exception as e:
        # Anything from Binance itself or the network
        logger.error(f"Order failed: {e}")
        print(f"❌ Order failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
