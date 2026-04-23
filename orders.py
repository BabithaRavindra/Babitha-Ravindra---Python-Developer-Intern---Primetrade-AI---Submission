"""Order placement logic for Binance Futures Testnet."""

import json
from typing import Any, Dict, Optional

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
import requests

from bot.logging_config import logger


def _log_request(symbol: str, side: str, order_type: str, quantity: float, price: Optional[float]) -> None:
    """Log outgoing order request details."""
    payload: Dict[str, Any] = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
    }
    if price is not None:
        payload["price"] = price
    logger.debug("ORDER REQUEST: %s", json.dumps(payload))


def _log_response(response: Dict[str, Any]) -> None:
    """Log raw API response."""
    logger.debug("ORDER RESPONSE: %s", json.dumps(response, default=str))


def place_market_order(
    client: Client,
    symbol: str,
    side: str,
    quantity: float,
) -> Dict[str, Any]:
    """
    Place a MARKET order on Binance Futures Testnet.

    Args:
        client:   Authenticated Binance client.
        symbol:   Trading pair, e.g. 'BTCUSDT'.
        side:     'BUY' or 'SELL'.
        quantity: Order quantity.

    Returns:
        API response dictionary.

    Raises:
        BinanceAPIException: On API-level errors.
        BinanceOrderException: On order validation errors.
        requests.exceptions.RequestException: On network failures.
    """
    _log_request(symbol, side, "MARKET", quantity, None)
    try:
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity,
        )
        _log_response(response)
        logger.info(
            "MARKET %s order placed | symbol=%s qty=%s | orderId=%s status=%s",
            side,
            symbol,
            quantity,
            response.get("orderId"),
            response.get("status"),
        )
        return response
    except BinanceOrderException as exc:
        logger.error("Order validation error (MARKET): %s", exc)
        raise
    except BinanceAPIException as exc:
        logger.error("Binance API error (MARKET order): %s", exc)
        raise
    except requests.exceptions.RequestException as exc:
        logger.error("Network error (MARKET order): %s", exc)
        raise


def place_limit_order(
    client: Client,
    symbol: str,
    side: str,
    quantity: float,
    price: float,
) -> Dict[str, Any]:
    """
    Place a LIMIT order on Binance Futures Testnet.

    Args:
        client:   Authenticated Binance client.
        symbol:   Trading pair, e.g. 'BTCUSDT'.
        side:     'BUY' or 'SELL'.
        quantity: Order quantity.
        price:    Limit price.

    Returns:
        API response dictionary.

    Raises:
        BinanceAPIException: On API-level errors.
        BinanceOrderException: On order validation errors.
        requests.exceptions.RequestException: On network failures.
    """
    _log_request(symbol, side, "LIMIT", quantity, price)
    try:
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            quantity=quantity,
            price=price,
            timeInForce="GTC",
        )
        _log_response(response)
        logger.info(
            "LIMIT %s order placed | symbol=%s qty=%s price=%s | orderId=%s status=%s",
            side,
            symbol,
            quantity,
            price,
            response.get("orderId"),
            response.get("status"),
        )
        return response
    except BinanceOrderException as exc:
        logger.error("Order validation error (LIMIT): %s", exc)
        raise
    except BinanceAPIException as exc:
        logger.error("Binance API error (LIMIT order): %s", exc)
        raise
    except requests.exceptions.RequestException as exc:
        logger.error("Network error (LIMIT order): %s", exc)
        raise
