import click
from typing import Optional

def validate_symbol(symbol: str) -> str:
    if not symbol or not str(symbol).strip():
        raise click.BadParameter("Symbol must not be empty.")
    return str(symbol).strip().upper()

def validate_side(side: str) -> str:
    valid_sides = ["BUY", "SELL"]
    side_upper = str(side).strip().upper()
    if side_upper not in valid_sides:
        raise click.BadParameter(f"Side must be one of {valid_sides}.")
    return side_upper

def validate_order_type(order_type: str) -> str:
    valid_types = ["MARKET", "LIMIT", "STOP_LIMIT"]
    type_upper = str(order_type).strip().upper()
    if type_upper not in valid_types:
        raise click.BadParameter(f"Order type must be one of {valid_types}.")
    return type_upper

def validate_quantity(quantity: float) -> float:
    try:
        qty = float(quantity)
    except (ValueError, TypeError):
        raise click.BadParameter("Quantity must be a valid number.")
    if qty <= 0:
        raise click.BadParameter("Quantity must be greater than 0.")
    return qty

def validate_price(price: float, required: bool) -> Optional[float]:
    if not required and price is None:
        return None
    if required and price is None:
        raise click.BadParameter("Price is required for this order type.")
    try:
        p = float(price)
    except (ValueError, TypeError):
        raise click.BadParameter("Price must be a valid number.")
    if p <= 0:
        raise click.BadParameter("Price must be greater than 0.")
    return p
