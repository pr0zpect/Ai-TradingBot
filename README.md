# Binance Futures Testnet Trading Bot

A production-quality CLI trading bot for Binance Futures Testnet (USDT-M) built in Python.

## Prerequisites
- Python 3.9+
- pip
- Binance Futures Testnet account

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd trading_bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Setup environment variables:
   ```bash
   cp .env.example .env
   ```
   Open `.env` and fill in your `BINANCE_TESTNET_API_KEY` and `BINANCE_TESTNET_API_SECRET`.

## Usage Examples

Run the CLI bot to place orders on the testnet:

```bash
# Market BUY
python cli.py place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# Limit SELL
python cli.py place-order --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 99000

# Stop-Limit BUY (bonus)
python cli.py place-order --symbol BTCUSDT --side BUY --type STOP_LIMIT --quantity 0.001 --price 29500 --stop-price 29000
```

## Assumptions
- The bot exclusively targets Binance Futures Testnet (`https://testnet.binancefuture.com`).
- The bot assumes USDT-M futures pairs.
- It requires Python 3.9 or higher.
- The `python-dotenv` package is used for secure loading of API credentials.
- Stop-limit orders use a default time-in-force of `GTC`.

## Viewing Logs
The bot writes rotating logs to the `logs` directory. You can watch them in real-time:
```bash
tail -f logs/trading_bot.log
```
