import logging

logger = logging.getLogger(__name__)

def place_market_order(client, symbol: str, side: str, quantity: float) -> dict:
    logger.info(f"Placing MARKET {side} order: {symbol} qty={quantity}")
    params = {
        "symbol": symbol,
        "side": side,
        "type": "MARKET",
        "quantity": quantity
    }
    return client.place_order(**params)

def place_limit_order(client, symbol: str, side: str, quantity: float, price: float, time_in_force: str = "GTC") -> dict:
    logger.info(f"Placing LIMIT {side} order: {symbol} qty={quantity} price={price}")
    params = {
        "symbol": symbol,
        "side": side,
        "type": "LIMIT",
        "timeInForce": time_in_force,
        "quantity": quantity,
        "price": price
    }
    return client.place_order(**params)

def place_stop_limit_order(client, symbol: str, side: str, quantity: float, price: float, stop_price: float, time_in_force: str = "GTC") -> dict:
    logger.info(f"Placing STOP_LIMIT {side} order: {symbol} qty={quantity} price={price} stop_price={stop_price}")
    params = {
        "symbol": symbol,
        "side": side,
        "type": "STOP_LIMIT",
        "timeInForce": time_in_force,
        "quantity": quantity,
        "price": price,
        "stopPrice": stop_price
    }
    return client.place_order(**params)
