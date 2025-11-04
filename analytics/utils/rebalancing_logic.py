from trendly.analytics.utils.portfolio_metrics import get_portfolio

# fixed allocations is a dictionary which only contains information if rebalancing is selected

def rebalance(db, id, rebalancing_option, fixed_allocations, frequency, threshold, user_id):
    portfolio = get_portfolio(db, id) # returns dictionary of Stock objects
    if rebalancing_option == "none":
        return  # No rebalancing needed
    if rebalancing_option == "time-based":
        # Implement time-based rebalancing logic
        pass
    elif rebalancing_option == "drift-based":
        for stock in portfolio.values():
            min = fixed_allocations[stock.ticker] * (1 - threshold)
            max = fixed_allocations[stock.ticker] * (1 + threshold)
            if stock.portfolio_contribution > max or stock.portfolio_contribution < min:
                # Implement drift-based rebalancing logic
    else:
        raise ValueError("Invalid rebalancing option selected.")

# for t in time_span:
#     compute metrics
#     rebalance if needed