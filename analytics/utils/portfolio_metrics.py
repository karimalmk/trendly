from .quotes_api import lookup

# ========================================================================
# Portfolio Retrieval
# ========================================================================
def get_portfolio(db, strategy_id):
    rows = db.execute(
        "SELECT ticker, shares FROM portfolio WHERE strategy_id = ?", (strategy_id,)
    ).fetchall()
    if not rows:
        raise ValueError("No stocks found in portfolio.")
    return {r["ticker"]: float(r["shares"]) for r in rows}


# ==========================================================================
# Transaction Handling
# ==========================================================================
def get_transactions(db, strategy_id):
    transactions = db.execute(
        "SELECT ticker, type, price, shares FROM transactions WHERE strategy_id = ?",
        (strategy_id,),
    ).fetchall()

    # Separate buys and sells
    buys, sells = {}, {}
    for t in transactions:
        d = buys if t["type"] == "buy" else sells
        d.setdefault(t["ticker"], []).append((t["price"], t["shares"]))
    return buys, sells

# ==========================================================================
# Portfolio Metrics Computation
# ==========================================================================
def compute_metrics(db, strategy_id):
    portfolio = get_portfolio(db, strategy_id)
    buys, sells = get_transactions(db, strategy_id)

    equity_value = 0.0
    results = []

    for ticker, shares in portfolio.items():
        if shares <= 0:
            continue

        quote = lookup(ticker)
        price = float(quote["price"]) if quote and "price" in quote else 0.0
        share_value = shares * price
        equity_value += share_value

        total_buys = sum(p * s for p, s in buys.get(ticker, []))
        total_sells = sum(p * s for p, s in sells.get(ticker, []))
        net_spend = total_buys - total_sells
        weighted_price = (net_spend / shares) if shares else 0.0
        stock_return = ((price - weighted_price) / weighted_price) if weighted_price else 0.0

        results.append({
            "ticker": ticker,
            "shares": shares,
            "price": price,
            "share_value": share_value,
            "weighted_price": weighted_price,
            "stock_return": stock_return,
        })

    # Compute contributions in one pass
    for r in results:
        r["portfolio_contribution"] = r["share_value"] / equity_value if equity_value else 0

    return {"portfolio": results, "equity_value": equity_value}


# ========== Test ==========
if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from ...helpers.setup import get_db, close_db
    db = get_db()
    strategy_id = 1
    portfolio = get_portfolio(db, strategy_id)
    close_db(db)
    print(portfolio)

# Add volatility, drawdown, max drawdown calculations here as needed.
# Add sharpe ratio, sortino ratio calculations here as needed.
# Add alpha, beta calculations here as needed.
# Add CAGR calculations here as needed.