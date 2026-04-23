# Binance Futures Testnet CLI Trading Bot

## Setup

```bash
# 1. Clone / unzip the project
cd trading_bot

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API keys
cp .env.example .env
# Edit .env and paste your Futures Testnet keys
```

Get testnet keys from: https://testnet.binancefuture.com

## Usage

```bash
# MARKET BUY
python main.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# MARKET SELL
python main.py --symbol ETHUSDT --side SELL --type MARKET --quantity 0.01

# LIMIT BUY
python main.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 60000

# LIMIT SELL
python main.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 70000

# Help
python main.py --help
```

## Logs

All activity (requests, responses, errors) is written to `logs/trading_bot.log`.

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── cli.py            # Typer CLI entry-point
│   ├── client.py         # Binance client initialisation
│   ├── logging_config.py # File + console logging setup
│   ├── orders.py         # Order placement logic
│   └── validators.py     # Input validation
├── logs/                 # Auto-created at runtime
├── .env.example
├── main.py
├── README.md
└── requirements.txt
```
