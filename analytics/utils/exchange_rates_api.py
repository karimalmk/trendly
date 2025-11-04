import csv
import yfinance as yf
from pathlib import Path

try:
    # If we're inside Django runtime
    from django.conf import settings
    csv_path = settings.BASE_DIR / 'data' / 'exchanges.csv'
except Exception:
    # If run directly (outside Django)
    BASE_DIR = Path(__file__).resolve().parent.parent.parent  
    # Goes from exchange_rates_api.py to utils/ to trendly/ to project root
    csv_path = BASE_DIR / 'data' / 'exchanges.csv'

with open(csv_path, 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    EXCHANGES = {row['code']: row for row in reader}

# ========== Get Live Exchange Rate ==========
def get_exchange_rate(exchange_code: str):
    exchange_info = EXCHANGES[exchange_code]
    if not exchange_info:
        return None

    currency = exchange_info["currency"]
    if currency == "USD":
        return 1.0

    pair = f"USD{currency}=X"
    try:
        data = yf.Ticker(pair).fast_info
        rate = data["last_price"] if data else None
        return float(rate) if rate is not None else None
    except Exception:
        return None
   
    
# ========== Get Historical Exchange Rates ==========
def get_historical_exchange_rate(exchange: str, start_date: str, end_date: str):
    exchange_info = EXCHANGES[exchange]
    if not exchange_info:
        return None

    currency = exchange_info["currency"]
    if currency == "USD":
        return 1.0

    pair = f"USD{currency}=X"
    try:
        historical_rates = {}
        data = yf.Ticker(pair).history(start=start_date, end=end_date)
        for i in range(len(data)):
            date = data.index[i].strftime("%Y-%m-%d")
            close_rate = float(data["Close"].iloc[i])
            historical_rates[date] = close_rate
        return historical_rates if historical_rates else None
    except Exception:
        return None

# ========== Test ==========    
if __name__ == "__main__":
    rate = get_exchange_rate("LSE")
    # historical_rates = get_historical_exchange_rate("LSE", "2023-01-01", "2023-01-31")
    print(rate)