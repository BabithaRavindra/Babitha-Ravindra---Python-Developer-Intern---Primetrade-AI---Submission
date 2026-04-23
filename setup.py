"""Package setup for the trading bot."""

from setuptools import setup, find_packages

setup(
    name="binance-futures-testnet-bot",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "python-binance==1.0.19",
        "typer==0.12.3",
        "python-dotenv==1.0.1",
        "requests==2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "trading-bot=bot.cli:main",
        ],
    },
    python_requires=">=3.8",
)
