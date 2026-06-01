# Binance Futures Testnet Trading Bot

A production-quality CLI trading bot for Binance Futures Testnet (USDT-M) built in Python 3.x.
Supports MARKET, LIMIT, and STOP_MARKET orders on USDT-M futures pairs via direct REST calls
to the Binance Futures Testnet API. Features structured logging, full input validation, and a
clean CLI interface built with Click.

---

## Features

- **MARKET, LIMIT, and STOP_MARKET** order type support
- **BUY and SELL** direction support on any valid USDT-M futures symbol
- Full integration with the **Binance Futures Testnet REST API**
- **CLI interface** powered by Click with interactive prompts and confirmation flow
- Comprehensive **input validation** on all order parameters before submission
- **Rotating structured log files** for full request/response traceability
- Graceful **exception handling** for API, network, and validation errors
- **Environment variable** based credential management via `python-dotenv`
- Modular, layered **architecture** separating client, orders, validators, and logging concerns

---

## Tech Stack

- **Python 3.9+**
- **Click** — CLI framework
- **requests** — HTTP client for REST API communication
- **python-dotenv** — Environment variable loading from `.env`
- **logging** — Python standard library rotating file and stream logging

---

## Project Structure

```
trading_bot/
│
├── bot/
│   ├── __init__.py
│   ├── client.py          # BinanceFuturesClient — wraps all signed HTTP calls
│   ├── orders.py          # Order placement functions (MARKET, LIMIT, STOP_MARKET)
│   ├── validators.py      # Input validation for all CLI parameters
│   └── logging_config.py  # Rotating file + console logging setup
│
├── logs/
│   ├── trading_bot.log         # Live rotating log output
│   ├── market_order.log        # Sample trace of a successful MARKET BUY order
│   └── limit_order.log         # Sample trace of a successful LIMIT SELL order
│
├── cli.py            # Click CLI entry point — place-order command
├── requirements.txt  # Pinned dependencies
├── README.md
├── .env.example      # Template for environment variables
└── .gitignore
```

---

## Prerequisites

- Python 3.9+
- pip
- Binance Futures Testnet account

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/trading_bot.git
   cd trading_bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
   Open `.env` and populate your testnet credentials:
   ```
   BINANCE_TESTNET_API_KEY=your_api_key_here
   BINANCE_TESTNET_API_SECRET=your_api_secret_here
   ```
> ⚠️ Never commit your `.env` file. A `.gitignore` is included to prevent this automatically.

---

## Usage Examples

```bash
# View all available options
python cli.py place-order --help

# Market BUY
python cli.py place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# Limit SELL
python cli.py place-order --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 99000

# Stop-Market SELL (bonus)
python cli.py place-order --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 29000
```

---

## Example CLI Output

```
┌─────────────────────────────┐
│  Order Request Summary      │
│  Symbol   : BTCUSDT         │
│  Side     : BUY             │
│  Type     : MARKET          │
│  Quantity : 0.001           │
└─────────────────────────────┘

Place this order? [y/N]: y

✅ Order placed successfully
Order ID     : 13710044723
Status       : NEW
Executed Qty : 0.001
Avg Price    : 105432.50
```

---

## Input Validation

All CLI parameters are validated before any API request is dispatched:

| Parameter    | Rule                                             |
|--------------|--------------------------------------------------|
| `symbol`     | Non-empty string, normalized to uppercase        |
| `side`       | Must be `BUY` or `SELL` (case-insensitive)       |
| `type`       | Must be `MARKET`, `LIMIT`, or `STOP_MARKET`      |
| `quantity`   | Must be a numeric value greater than `0`         |
| `price`      | Required and `> 0` for `LIMIT` orders            |
| `stop-price` | Required and `> 0` for `STOP_MARKET` orders      |

Validation failures produce a clear, user-friendly error message and exit with code `1`, without exposing stack traces.

---

## Error Handling

The application handles all known failure modes gracefully:

| Error Type                  | Behaviour                                                        |
|-----------------------------|------------------------------------------------------------------|
| Invalid CLI input           | Prints fix hint, exits with code `1`                             |
| Binance API error (4xx/5xx) | Logs full response body at `ERROR`, prints API message to user   |
| Authentication failure      | Caught as `BinanceAPIError`, user-friendly message shown         |
| Invalid symbol              | API rejects; error message surfaced cleanly                      |
| Network connection failure  | Caught as `requests.ConnectionError`, prints network error hint  |
| Request timeout             | Caught as `requests.Timeout`, prints timeout hint                |
| Malformed API response      | Caught in JSON parsing; logs raw body for investigation          |

All errors are logged to the rotating log file with full context for post-mortem debugging.

---

## Log Files

All logs are written to `logs/trading_bot.log` using a `RotatingFileHandler` (max 5 MB, 3 backups).

- File handler captures logs at `DEBUG` level — includes raw API request params and response bodies.
- Console handler outputs at `INFO` level — surfaces order events and errors to the terminal.

**Log format:**
```
%(asctime)s | %(levelname)-8s | %(name)s | %(message)s
```

**Sample log entries:**
```
2026-06-01T10:20:11+0530 | INFO     | bot.orders | Placing MARKET BUY order: BTCUSDT qty=0.001
2026-06-01T10:20:11+0530 | DEBUG    | bot.client | Request: POST /fapi/v1/order params={'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET', 'quantity': 0.001, 'timestamp': 1717236011000}
2026-06-01T10:20:12+0530 | DEBUG    | bot.client | Response: 200 body={"orderId":13710044723,"status":"NEW","executedQty":"0.001","avgPrice":"105432.50"}
```

Two sample log files are included for review:
- `logs/market_order.log` — full trace of a confirmed MARKET BUY order
- `logs/limit_order.log`  — full trace of a confirmed LIMIT SELL order

To stream logs in real time:
```bash
tail -f logs/trading_bot.log
```

> The `logs/` directory is created automatically on first run — no manual setup needed.

---

## Security Notes

- API credentials are **never hardcoded** anywhere in the source code.
- Credentials are loaded exclusively from **environment variables** via a `.env` file using `python-dotenv`.
- The `.env` file is listed in `.gitignore` and is **never committed** to version control.
- The bot communicates exclusively with the **Binance Futures Testnet** — no real funds are at risk.
- Request signatures are generated using **HMAC-SHA256** and the secret key is never logged.

---

## Assumptions

- The bot exclusively targets Binance Futures Testnet (`https://testnet.binancefuture.com`).
- The bot assumes USDT-M futures pairs.
- It requires Python 3.9 or higher.
- The `python-dotenv` package is used for secure loading of API credentials.
- LIMIT orders use a default timeInForce of GTC (Good Till Cancelled).
- Minimum quantity and price precision are not validated by the bot; they depend on each symbol's exchange filters on the testnet.
- The Binance Futures Testnet resets periodically; placed orders will not persist indefinitely.
- Network connectivity to `https://testnet.binancefuture.com` is assumed to be available at runtime.
