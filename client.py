"""Binance Futures Testnet client initialisation."""

import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

from bot.logging_config import logger

load_dotenv()

FUTURES_TESTNET_URL = "https://testnet.binancefuture.com"


def get_client() -> Client:
    """
    Build and return an authenticated Binance client pointed at the
    Futures Testnet.

    Raises:
        SystemExit: if API keys are missing or the connection fails.
    """
    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()

    if not api_key or not api_secret:
        logger.error(
            "BINANCE_API_KEY and BINANCE_API_SECRET must be set in the .env file."
        )
        raise SystemExit(1)

    try:
        client = Client(
            api_key=api_key,
            api_secret=api_secret,
            testnet=False,  # We override URLs manually below
        )
        # Override REST base URL to Futures Testnet
        client.FUTURES_URL = FUTURES_TESTNET_URL + "/fapi"
        client.futures_ping()  # Connectivity check
        logger.info("Connected to Binance Futures Testnet successfully.")
        return client
    except BinanceAPIException as exc:
        logger.error("Binance API error during client init: %s", exc)
        raise SystemExit(1) from exc
    except Exception as exc:
        logger.error("Unexpected error during client init: %s", exc)
        raise SystemExit(1) from exc
