# Binance Futures Testnet Trading Bot

A production-quality CLI trading bot for Binance Futures Testnet (USDT-M) built in Python 3.x. 
Supports MARKET, LIMIT, and STOP_MARKET orders on USDT-M futures pairs via direct REST calls 
to the Binance Futures Testnet API. Features structured logging, full input validation, and a 
clean Typer-based CLI interface.

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
# View all available options
python cli.py place-order --help

# Market BUY
python cli.py place-order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# Limit SELL
python cli.py place-order --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 99000

# Stop-Market SELL (bonus)
python cli.py place-order --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 29000
```

## Log Files

All logs are written to `logs/trading_bot.log` (rotating file, INFO level).

Two sample log files are included for review:
- `logs/sample_market_order.log` — full trace of a successful MARKET BUY order
- `logs/sample_limit_order.log`  — full trace of a successful LIMIT BUY order

To watch logs in real time:
```bash
tail -f logs/trading_bot.log
```

## Assumptions
- The bot exclusively targets Binance Futures Testnet (`https://testnet.binancefuture.com`).
- The bot assumes USDT-M futures pairs.
- It requires Python 3.9 or higher.
- The `python-dotenv` package is used for secure loading of API credentials.
- Stop-market orders use a default time-in-force of `GTC`.
- Minimum quantity and price precision are not validated by the bot; they depend on each symbol's exchange filters on the testnet.
- The Binance Futures Testnet resets periodically; placed orders will not persist indefinitely.
- Network connectivity to https://testnet.binancefuture.com is assumed to be available at runtime.
