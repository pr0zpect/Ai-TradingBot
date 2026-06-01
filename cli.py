import os
import sys
import click
import requests
import json
from dotenv import load_dotenv

from bot.client import BinanceFuturesClient, BinanceAPIError
from bot.orders import place_market_order, place_limit_order, place_stop_limit_order
from bot.validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price
from bot.logging_config import setup_logging

load_dotenv()

# Setup logging
logger = setup_logging()

def print_summary(symbol, side, order_type, quantity, price, stop_price):
    click.echo("┌─────────────────────────────┐")
    click.echo("│  Order Request Summary      │")
    click.echo(f"│  Symbol   : {symbol:<15} │")
    click.echo(f"│  Side     : {side:<15} │")
    click.echo(f"│  Type     : {order_type:<15} │")
    click.echo(f"│  Quantity : {quantity:<15} │")
    if price:
        click.echo(f"│  Price    : {price:<15} │")
    if stop_price:
        click.echo(f"│  Stop Px  : {stop_price:<15} │")
    click.echo("└─────────────────────────────┘")

@click.group()
def cli():
    """Binance Futures Testnet Trading Bot CLI."""
    pass

@cli.command('place-order')
@click.option('--symbol', help='Trading symbol, e.g. BTCUSDT')
@click.option('--side', help='BUY or SELL')
@click.option('--type', 'order_type', help='MARKET, LIMIT, or STOP_LIMIT')
@click.option('--quantity', type=float, help='Order quantity')
@click.option('--price', type=float, help='Order price (required for LIMIT/STOP_LIMIT)')
@click.option('--stop-price', type=float, help='Stop price (required for STOP_LIMIT)')
@click.option('--yes', '-y', is_flag=True, help='Skip confirmation prompt')
def place_order(symbol, side, order_type, quantity, price, stop_price, yes):
    """Place an order on Binance Futures Testnet."""
    try:
        if not symbol:
            symbol = click.prompt("Enter symbol (e.g. BTCUSDT)")
        
        symbol = validate_symbol(symbol)

        if not side:
            side = click.prompt("Enter side (BUY/SELL)")
        side = validate_side(side)

        if not order_type:
            order_type = click.prompt("Enter order type (MARKET/LIMIT/STOP_LIMIT)")
        order_type = validate_order_type(order_type)

        if not quantity:
            quantity = click.prompt("Enter quantity", type=float)
        quantity = validate_quantity(quantity)

        # Handle price requirements
        price_required = order_type in ["LIMIT", "STOP_LIMIT"]
        if price_required and price is None:
            click.echo(f"⚠ Price is required for {order_type} orders. Add --price <value>.")
            price = click.prompt("Enter price", type=float)
            
        price = validate_price(price, price_required)

        # Handle stop price requirements
        stop_price_required = order_type == "STOP_LIMIT"
        if stop_price_required and stop_price is None:
            click.echo(f"⚠ Stop price is required for STOP_LIMIT orders. Add --stop-price <value>.")
            stop_price = click.prompt("Enter stop price", type=float)
            
        if stop_price is not None:
            stop_price = validate_price(stop_price, stop_price_required)

        print_summary(symbol, side, order_type, quantity, price, stop_price)

        if not yes:
            if not click.confirm("Place this order?"):
                click.echo("Order cancelled.")
                return

        api_key = os.environ.get("BINANCE_TESTNET_API_KEY")
        api_secret = os.environ.get("BINANCE_TESTNET_API_SECRET")

        if not api_key or not api_secret:
            click.echo("❌ Order failed: Missing API credentials in .env file.")
            sys.exit(1)

        client = BinanceFuturesClient(api_key=api_key, api_secret=api_secret)

        if order_type == "MARKET":
            res = place_market_order(client, symbol, side, quantity)
        elif order_type == "LIMIT":
            res = place_limit_order(client, symbol, side, quantity, price)
        elif order_type == "STOP_LIMIT":
            res = place_stop_limit_order(client, symbol, side, quantity, price, stop_price)

        click.echo("✅ Order placed successfully")
        click.echo(f"Order ID     : {res.get('orderId')}")
        click.echo(f"Status       : {res.get('status')}")
        click.echo(f"Executed Qty : {res.get('executedQty')}")
        click.echo(f"Avg Price    : {res.get('avgPrice', res.get('price', '0.0'))}")

    except click.BadParameter as e:
        click.echo(f"Validation error: {e}")
        sys.exit(1)
    except click.Abort:
        click.echo("\nCancelled by user.")
        sys.exit(1)
    except BinanceAPIError as e:
        logger.error(f"BinanceAPIError: {e} - Body: {e.response_body}")
        
        try:
            body = json.loads(e.response_body)
            msg = body.get('msg', e.response_body)
        except Exception:
            msg = e.response_body
            
        click.echo(f"❌ Order failed: {msg}")
        sys.exit(1)
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
        logger.error(f"Network error: {e}")
        click.echo(f"❌ Order failed: Network error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        click.echo(f"❌ Order failed: An unexpected error occurred.")
        sys.exit(1)

if __name__ == '__main__':
    cli()
