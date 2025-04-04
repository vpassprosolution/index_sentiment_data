# ✅ price_fetcher_index.py — fetch live index prices using yfinance
import yfinance as yf
import psycopg2
from datetime import datetime

# 🏦 Database config (Railway PostgreSQL)
DB_CONFIG = {
    'dbname': 'railway',
    'user': 'postgres',
    'password': 'vVMyqWjrqgVhEnwyFifTQxkDtPjQutGb',
    'host': 'interchange.proxy.rlwy.net',
    'port': '30451'
}

# 🌍 Index symbols from Yahoo Finance
INDEXES = {
    "DJI": "^DJI",       # Dow Jones
    "IXIC": "^IXIC",     # Nasdaq
    "GSPC": "^GSPC",     # S&P 500
    "FTSE": "^FTSE",     # FTSE 100
    "N225": "^N225",     # Nikkei 225
    "HSI": "^HSI",       # Hang Seng
    "DAX": "^GDAXI",     # DAX Germany
    "CAC40": "^FCHI",    # CAC 40 France
    "STOXX50": "^STOXX50E", # Euro Stoxx 50
    "AORD": "^AORD",     # ASX 200 Australia
    "BSESN": "^BSESN",   # BSE Sensex India
    "NSEI": "^NSEI",     # NSE Nifty 50 India
    "KS11": "^KS11",     # KOSPI South Korea
    "TWII": "^TWII",     # Taiwan Index
    "BVSP": "^BVSP",     # Bovespa Brazil
    "MXX": "^MXX",       # IPC Mexico
    "RUT": "^RUT",       # Russell 2000
    "VIX": "^VIX",       # Volatility Index
    "XU100": "XU100.IS", # BIST 100 Turkey
}

def update_price(symbol, price):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO index_sentiment (symbol, price, last_updated)
            VALUES (%s, %s, %s)
            ON CONFLICT (symbol) DO UPDATE
            SET price = EXCLUDED.price,
                last_updated = EXCLUDED.last_updated
        """, (symbol, price, datetime.utcnow()))

        conn.commit()
        cur.close()
        conn.close()
        print(f"✅ Saved → {symbol} = {price}")
    except Exception as e:
        print(f"❌ DB Error for {symbol}: {e}")

def fetch_prices():
    print("📡 Fetching Index Prices...\n")
    for symbol, yf_symbol in INDEXES.items():
        try:
            data = yf.Ticker(yf_symbol).history(period="1d")
            price = data["Close"].iloc[-1]
            update_price(symbol, float(price))
        except Exception as e:
            print(f"❌ Failed for {symbol}: {e}")

if __name__ == "__main__":
    fetch_prices()
