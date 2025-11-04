import yfinance as yf
from datetime import datetime
from pytz import timezone

from .exchange_rates_api import EXCHANGES, get_exchange_rate

CACHE = {}  # {"ticker": {"price": float, "time": datetime}}

# ==========================================================================
# Market Status
# ==========================================================================
def check_market_status(exchange: str):
    tz_name = EXCHANGES[exchange]["timezone"]
    tz = timezone(tz_name)
    now = datetime.now(tz)
    country_open = EXCHANGES[exchange]["open"]
    country_close = EXCHANGES[exchange]["close"]
    open_t = datetime.strptime(country_open, "%H:%M").time()
    close_t = datetime.strptime(country_close, "%H:%M").time()


    return {
        "market_open": (open_t <= now.time() <= close_t),
        "time_now": now,
        "date_now": now.date(),
    }


# ==========================================================================
# Lookup Stock Price
# ==========================================================================

def check_stock(ticker: str):
    try:
        info = yf.Ticker(ticker).info
        quote_type = info.get("quoteType", None)
        if quote_type != "EQUITY":
            return False
        if info is not None and info != {}:
            return True
        else:
            return False
    except Exception as e:
        print(f"[check_stock error] {ticker}: {e}")
        return False
    

def get_info(ticker: str):
    info = yf.Ticker(ticker).info
    if info:
        return info
    else: return None


def compute_price(info: dict, rate: float):
    market_open = info.get("regularMarketOpen")
    price = info.get("regularMarketPrice")
    bid = info.get("bid")
    ask = info.get("ask")
    volume = info.get("volume")

    # Converting values to USD
    if rate != 1.0:
        market_open = market_open / rate if market_open else None
        price = price / rate if price else None
        bid = bid / rate if bid else None
        ask = ask / rate if ask else None

    if market_open and price:
        daily_return = price / market_open - 1

    return market_open, price, daily_return, bid, ask, volume

## -------------------- MAIN LOOKUP FUNCTION --------------------
def lookup(ticker: str):
    if not check_stock(ticker):
        return {"error": "Stock ticker not found."}
    try:
        info = get_info(ticker)
        if not info:
            return {"error": "Stock ticker not found."}

        # Get exchange code
        exchange_code = info.get("exchange")
        if exchange_code not in EXCHANGES:
            raise ValueError(f"Unknown exchange '{exchange_code}'")

        status = check_market_status(exchange_code)
        rate = get_exchange_rate(exchange_code)

        # Fresh price
        if status["market_open"]:
            CACHE.pop(ticker, None)  # Clear cache if market is open
            market_open, price, daily_return, bid, ask, volume = compute_price(info, rate)
        
        # Cached price
        else:
            if ticker in CACHE:
                market_open = CACHE[ticker]["market_open"] if CACHE[ticker]["market_open"] else None
                price = CACHE[ticker]["price"] if CACHE[ticker]["price"] else None
                daily_return = CACHE[ticker]["daily_return"] if CACHE[ticker]["daily_return"] else None
                bid = CACHE[ticker]["bid"] if CACHE[ticker]["bid"] else None
                ask = CACHE[ticker]["ask"] if CACHE[ticker]["ask"] else None
                volume = CACHE[ticker]["volume"] if CACHE[ticker]["volume"] else None
            else:
                market_open, price, daily_return, bid, ask, volume = compute_price(info, rate)
                CACHE[ticker] = {"market_open": market_open, "price": price, "daily_return": daily_return, "bid": bid, "ask": ask, "volume": volume}

        return {
            "market_open": market_open,
            "ticker": ticker,
            "daily_return": daily_return,
            "price": price,
            "bid": bid,
            "ask": ask,
            "volume": volume,
        }

    except Exception as e:
        print(f"[lookup error] {ticker}: {e}")
        return {"ticker": ticker, "error": str(e)}


# ==========================================================================
# Get Historic Data
# ==========================================================================
def get_historic_data(asset: str, start_date: str, end_date: str, freq: str = '1d'):

    info = yf.Ticker(asset).info or {}
    exchange_code = info.get("exchange") if info else None

    if exchange_code not in EXCHANGES:
        raise ValueError(f"Unknown exchange '{exchange_code}'")
    
    if freq not in ['1h', '1d', '5d', '1wk']:
        raise ValueError("Frequency not supported. Use '1h', '1d', '5d', or '1wk'.")

    # Fetch asset data
    asset_data = yf.Ticker(asset).history(start=start_date, end=end_date, interval=freq)
    
    currency = info.get("currency")

    if currency == "USD":
        return asset_data
    else:
        rate = get_exchange_rate(exchange_code)
        asset_data.loc[:, ["Open", "High", "Low", "Close"]] /= rate # select all rows, specific columns
        return asset_data

# ========== Test ==========
if __name__ == "__main__":
    for symbol in ["AAPL", "MSFT", "^IXIC"]:
        print(symbol, "→", lookup(symbol))
    #     print(symbol, "→", lookup(symbol))
    # print("\nCACHE:", CACHE)
    # start_date = "2020-09-30"
    # end_date = "2023-01-01"
    # asset = "^GSPC"
    # freq = "1d"
    # index_data = get_historic_data(asset, start_date, end_date, freq)
    # print(index_data)    