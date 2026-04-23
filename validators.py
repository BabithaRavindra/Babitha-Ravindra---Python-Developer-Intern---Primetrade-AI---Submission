"""Input validation helpers for the trading bot."""

from typing import Optional
import typer

VALID_SIDES = {"BUY", "SELL"}
VALID_TYPES = {"MARKET", "LIMIT"}


def validate_side(side: str) -> str:
    """Validate and normalise order side."""
    side = side.upper().strip()
    if side not in VALID_SIDES:
        raise typer.BadParameter(f"Side must be one of {VALID_SIDES}. Got: '{side}'")
    return side


def validate_order_type(order_type: str) -> str:
    """Validate and normalise order type."""
    order_type = order_type.upper().strip()
    if order_type not in VALID_TYPES:
        raise typer.BadParameter(
            f"Order type must be one of {VALID_TYPES}. Got: '{order_type}'"
        )
    return order_type


def validate_quantity(quantity: float) -> float:
    """Ensure quantity is a positive number."""
    if quantity <= 0:
        raise typer.BadParameter(f"Quantity must be greater than 0. Got: {quantity}")
    return quantity


def validate_price(price: Optional[float], order_type: str) -> Optional[float]:
    """Ensure price is supplied and positive for LIMIT orders."""
    if order_type == "LIMIT":
        if price is None:
            raise typer.BadParameter("Price is required for LIMIT orders.")
        if price <= 0:
            raise typer.BadParameter(
                f"Price must be greater than 0. Got: {price}"
            )
    return price


def validate_symbol(symbol: str) -> str:
    """Validate symbol is a non-empty string."""
    symbol = symbol.upper().strip()
    if not symbol:
        raise typer.BadParameter("Symbol cannot be empty.")
    return symbol
