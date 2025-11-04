# ======================================================================
# market_data.py
# Optimized stock lookup and caching system using yFinance
# ======================================================================

import yfinance as yf
from datetime import datetime, timedelta
from pytz import timezone
from typing import Dict, Any, Optional

from .exchange_rates_api import EXCHANGES, get_exchange_rate


# ======================================================================
# GLOBAL CACHE STRUCTURE
# ======================================================================
# CACHE = {
#     "AAPL": {
#         "exchange": "NASDAQ",
#         "timestamp": datetime,
#         "data": {...}
#     }
# }
CACHE: Dict[str, Dict[str, Any]] = {}
CACHE_TTL = timedelta(hours=12)  # optional safety TTL


# ======================================================================
# MARKET STATUS
# ======================================================================
def check_market_status(exchange: str) -> Dict[str, Any]:
    """Return whether the given exchange is open, along with local time info."""
    tz = timezone(EXCHANGES[exchange]["timezone"])
    now = datetime.now(tz)
    open_t = datetime.strptime(EXCHANGES[exchange]["open"], "%H:%M").time()
    close_t = datetime.strptime(EXCHANGES[exchange]["close"], "%H:%M").time()

    # Handle markets that close after midnight (e.g., 23:00–05:00)
    if open_t < close_t:
        is_open = open_t <= now.time() <= close_t
    else:
        is_open = now.time() >= open_t or now.time() <= close_t

    return {
        "market_open": is_open,
        "time_now": now,
        "date_now": now.date(),
    }


# ======================================================================
# YFINANCE UTILITIES
# ======================================================================
def safe_info(ticker: str) -> Dict[str, Any]:
    """Safely fetch ticker info, suppressing yFinance exceptions."""
    try:
        return yf.Ticker(ticker).info or {}
    except Exception as e:
        print(f"[safe_info error] {ticker}: {e}")
        return {}


def compute_price(info: Dict[str, Any], rate: float) -> Dict[str, Optional[float]]:
    """Compute key price metrics and convert to USD if needed."""
    def _convert(val: Optional[float]) -> Optional[float]:
        return val / rate if (val and rate != 1.0) else val

    market_open = _convert(info.get("regularMarketOpen"))
    price = _convert(info.get("regularMarketPrice"))
    bid = _convert(info.get("bid"))
    ask = _convert(info.get("ask"))
    volume = info.get("volume")
    daily_return = (price / market_open - 1) if (price and market_open) else None

    return {
        "market_open": market_open,
        "price": price,
        "daily_return": daily_return,
        "bid": bid,
        "ask": ask,
        "volume": volume,
    }


# ======================================================================
# STOCK VALIDATION
# ======================================================================
def check_stock(ticker: str) -> bool:
    """Validate if the ticker exists and represents an equity."""
    try:
        info = yf.Ticker(ticker).info
        if info.get("quoteType") == "EQUITY":
            return True
        return False
    except Exception:
        return False


# ======================================================================
# LOOKUP (MAIN FUNCTION)
# ======================================================================
def lookup(ticker: str) -> Dict[str, Any]:
    """
    Retrieve current stock data. Uses cache when market is closed.
    Clears cache when market opens.
    """
    info = safe_info(ticker)
    if not info or info.get("quoteType") != "EQUITY":
        return {"ticker": ticker, "error": "Invalid or unsupported ticker."}

    exchange_code = info.get("exchange")
    if exchange_code not in EXCHANGES:
        return {"ticker": ticker, "error": f"Unknown exchange '{exchange_code}'"}

    status = check_market_status(exchange_code)
    rate = get_exchange_rate(exchange_code)
    market_open_now = status["market_open"]

    # ---------- MARKET OPEN: Always fetch fresh ----------
    if market_open_now:
        data = compute_price(info, rate)
        CACHE.pop(ticker, None)  # remove stale cache
        CACHE[ticker] = {"exchange": exchange_code, "timestamp": datetime.now(), "data": data}
        return {"ticker": ticker, "is_open": True, **data}

    # ---------- MARKET CLOSED: Return cached or create ----------
    cached = CACHE.get(ticker)
    if cached and cached["exchange"] == exchange_code:
        # optional TTL check to prevent stale overnight cache
        if datetime.now() - cached["timestamp"] < CACHE_TTL:
            return {"ticker": ticker, "is_open": False, **cached["data"], "cached": True}

    # fetch once, store for reuse during market close
    data = compute_price(info, rate)
    CACHE[ticker] = {"exchange": exchange_code, "timestamp": datetime.now(), "data": data}
    return {"ticker": ticker, "is_open": False, **data, "cached": False}


# ======================================================================
# HISTORIC DATA
# ======================================================================
def get_historic_data(
    asset: str,
    start_date: str,
    end_date: str,
    freq: str = "1d"
):
    """Fetch historical OHLCV data for an asset, converted to USD."""
    info = safe_info(asset)
    exchange_code = info.get("exchange")

    if exchange_code not in EXCHANGES:
        raise ValueError(f"Unknown exchange '{exchange_code}'")
    if freq not in ["1h", "1d", "5d", "1wk"]:
        raise ValueError("Unsupported frequency: choose from '1h', '1d', '5d', '1wk'.")

    try:
        # Faster than calling .history() on each Ticker object
        data = yf.download(asset, start=start_date, end=end_date, interval=freq, progress=False)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch data for {asset}: {e}")

    currency = info.get("currency")
    if currency != "USD":
        rate = get_exchange_rate(exchange_code)
        data.loc[:, ["Open", "High", "Low", "Close"]] /= rate

    return data


# ======================================================================
# TEST BLOCK
# ======================================================================
if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "^GSPC"]
    for t in tickers:
        print(t, "→", lookup(t))
    print("\nCACHE snapshot:", CACHE)