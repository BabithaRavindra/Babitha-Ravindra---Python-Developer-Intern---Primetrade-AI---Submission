"""CLI entry-point for the Binance Futures Testnet trading bot."""

from typing import Optional

import typer
from binance.exceptions import BinanceAPIException, BinanceOrderException
import requests

from bot.client import get_client
from bot.logging_config import logger
from bot.orders import place_limit_order, place_market_order
from bot.validators import (
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_symbol,
)

app = typer.Typer(
    name="trading-bot",
    help="Binance Futures Testnet CLI trading bot.",
    add_completion=False,
)


@app.command()
def place_order(
    symbol: str = typer.Option(
        ...,
        "--symbol",
        "-s",
        help="Trading pair symbol, e.g. BTCUSDT",
    ),
    side: str = typer.Option(
        ...,
        "--side",
        help="Order side: BUY or SELL",
    ),
    order_type: str = typer.Option(
        ...,
        "--type",
        "-t",
        help="Order type: MARKET or LIMIT",
    ),
    quantity: float = typer.Option(
        ...,
        "--quantity",
        "-q",
        help="Order quantity",
    ),
    price: Optional[float] = typer.Option(
        None,
        "--price",
        "-p",
        help="Limit price (required for LIMIT orders)",
    ),
) -> None:
    """Place a MARKET or LIMIT futures order on Binance Testnet."""

    # --- Validate inputs ---
    try:
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        order_type = validate_order_type(order_type)
        quantity = validate_quantity(quantity)
        price = validate_price(price, order_type)
    except typer.BadParameter as exc:
        logger.error("Validation error: %s", exc)
        typer.echo(f"[ERROR] {exc}", err=True)
        raise typer.Exit(code=1)

    logger.info(
        "Preparing order | symbol=%s side=%s type=%s qty=%s price=%s",
        symbol,
        side,
        order_type,
        quantity,
        price,
    )

    # --- Initialise client ---
    client = get_client()

    # --- Place order ---
    try:
        if order_type == "MARKET":
            result = place_market_order(client, symbol, side, quantity)
        else:
            result = place_limit_order(client, symbol, side, quantity, price)  # type: ignore[arg-type]

        typer.echo(
            f"\n✅  Order placed successfully!\n"
            f"   Order ID : {result.get('orderId')}\n"
            f"   Symbol   : {result.get('symbol')}\n"
            f"   Side     : {result.get('side')}\n"
            f"   Type     : {result.get('type')}\n"
            f"   Quantity : {result.get('origQty')}\n"
            f"   Price    : {result.get('price', 'N/A')}\n"
            f"   Status   : {result.get('status')}\n"
        )

    except BinanceOrderException as exc:
        typer.echo(f"[ORDER ERROR] {exc.message}", err=True)
        raise typer.Exit(code=2)
    except BinanceAPIException as exc:
        typer.echo(f"[API ERROR] {exc.message}", err=True)
        raise typer.Exit(code=2)
    except requests.exceptions.ConnectionError:
        typer.echo("[NETWORK ERROR] Could not connect to Binance Futures Testnet.", err=True)
        raise typer.Exit(code=3)
    except requests.exceptions.Timeout:
        typer.echo("[NETWORK ERROR] Request to Binance timed out.", err=True)
        raise typer.Exit(code=3)
    except requests.exceptions.RequestException as exc:
        typer.echo(f"[NETWORK ERROR] {exc}", err=True)
        raise typer.Exit(code=3)


if __name__ == "__main__":
    app()
