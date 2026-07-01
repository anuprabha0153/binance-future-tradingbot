# Simplified Trading Bot — Binance Futures Testnet

A small Python CLI app that places MARKET and LIMIT orders on Binance
Futures Testnet (USDT-M), with input validation, structured code, and
logging of every request/response/error to a log file.

## Project Structure

```
trading_bot/
  bot/
    __init__.py
    client.py         # Talks to Binance (API layer)
    orders.py         # Validates input + places order (business logic layer)
    validators.py     # Input validation helpers
    logging_config.py # Sets up file + console logging
  cli.py               # CLI entry point (argparse)
  README.md
  requirements.txt
  logs/
    trading_bot.log    # Created automatically on first run
```

## 1. Setup Steps

### 1.1 Create a Binance Futures Testnet account
1. Go to https://testnet.binancefuture.com
2. Log in with a GitHub account (this is how the testnet works — no real KYC needed).
3. Once logged in, you'll see a fake USDT balance you can trade with.

### 1.2 Generate API credentials
1. On the testnet site, go to the **API Key** section.
2. Generate a new API Key + Secret Key.
3. Copy both — you'll need them below.

### 1.3 Install Python dependencies
```bash
python3 -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 1.4 Set your API credentials as environment variables
Never hard-code your keys into the source code. Instead:

**macOS/Linux:**
```bash
export BINANCE_API_KEY="your_api_key_here"
export BINANCE_API_SECRET="your_api_secret_here"
```

**Windows (PowerShell):**
```powershell
$env:BINANCE_API_KEY="your_api_key_here"
$env:BINANCE_API_SECRET="your_api_secret_here"
```

## 2. How to Run

### Place a MARKET order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### Place a LIMIT order
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 65000
```

Sample output:
```
--- ORDER REQUEST SUMMARY ---
Symbol     : BTCUSDT
Side       : BUY
Order Type : MARKET
Quantity   : 0.01
-----------------------------

--- ORDER RESPONSE ---
Order ID     : 3454312345
Status       : FILLED
Executed Qty : 0.01
Avg Price    : 65123.10
----------------------

✅ Order placed successfully! (Order ID: 3454312345)
```

Every request, response, and error is also written to `logs/trading_bot.log`
with a timestamp, so you have a full audit trail.

## 3. Assumptions

- The bot only supports USDT-M Futures (not Spot, not Coin-M Futures).
- API keys are provided via environment variables, not CLI flags or config
  files, for basic security hygiene.
- Quantity/price precision (e.g. BTCUSDT requires certain decimal steps)
  is enforced by Binance itself — if you pass an invalid precision, Binance
  will return an error, which the bot will catch, log, and display cleanly.
- `timeInForce=GTC` (Good-Til-Cancelled) is used by default for LIMIT orders.
- This is built for the **Testnet only**. Do not point `client.py` at the
  live Binance API without fully understanding the financial risk.

## 4. Error Handling Covered

- Invalid symbol / side / order type / quantity / missing price for LIMIT
  → caught by `validators.py`, shown as a clear `❌ Input error:` message.
- Missing API keys → clear `❌ Configuration error:` message.
- Binance API errors (bad symbol, insufficient testnet balance, etc.)
  → caught, logged, and shown to the user.
- Network failures (no internet, timeout) → caught, logged, and shown.

## 5. Bonus Ideas (not implemented, optional next steps)

- Add a STOP-LIMIT order type in `orders.py` + `client.py`.
- Add `rich` or `questionary` for a nicer interactive CLI menu.
- Add a simple Streamlit UI on top of the same `bot/` package.
