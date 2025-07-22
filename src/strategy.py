import pandas as pd

# keyword_to_etf = {
#     "mortgage rates": "XLF",
#     "artificial intelligence": "XLK",
#     "oil price": "XLE",
#     "online shopping": "XLY"
# }

# momentum = pd.read_csv('data/trends_momentum.csv', index_col=0, parse_dates=True)
# returns = pd.read_csv('data/etf_returns.csv', index_col=0, parse_dates=True)

# momentum = momentum.reindex(returns.index)

# top_n = 3
# portfolio = []


# for date in momentum.index[:-1]:
#     top_keywords = momentum.loc[date].nlargest(top_n).index.tolist()
#     picks = [keyword_to_etf[keyword] for keyword in top_keywords if keyword in keyword_to_etf]
#     next_date = returns.index[returns.index.get_loc(date) + 1]

#     ret = returns.loc[next_date, picks].mean()
#     portfolio.append((next_date, ret))

# pd.DataFrame(portfolio, columns=['Date', 'Return'])\
# .set_index('Date')\
# .to_csv('data/portfolio_returns.csv', index=True, index_label='Date')


def run_backtest(lookback_weeks=4, top_n=3):
    """
    Run the backtest for the Google Trends-driven sector rotation strategy.
    
    Parameters:
    - lookback_weeks: Number of weeks to look back for momentum calculation.
    - top_n: Number of top sectors to select based on momentum.
    
    Returns:
    - DataFrame with portfolio returns.
    """
    momentum = pd.read_csv('data/trends_momentum.csv', index_col=0, parse_dates=True)
    returns = pd.read_csv('data/etf_returns.csv', index_col=0, parse_dates=True)

    momentum = (momentum - momentum.shift(lookback_weeks)) / momentum.shift(lookback_weeks)
    momentum = momentum.reindex(returns.index)

    keyword_to_etf = {
    "mortgage rates": "XLF",
    "artificial intelligence": "XLK",
    "oil price": "XLE",
    "online shopping": "XLY"
    }
    
    portfolio = []

    for date in momentum.index[:-1]:
        top_keywords = momentum.loc[date].nlargest(top_n).index.tolist()
        picks = [keyword_to_etf[keyword] for keyword in top_keywords if keyword in keyword_to_etf]
        next_date = returns.index[returns.index.get_loc(date) + 1]

        ret = returns.loc[next_date, picks].mean()
        portfolio.append((next_date, ret))

    return pd.Series(
        [ret for _, ret in portfolio],
        index=[date for date, _ in portfolio],
        name=f"lookback_{lookback_weeks}_top_{top_n}"
    )

if __name__ == "__main__":
    # Example usage
    series = run_backtest()
    print(series.head())
    series.to_csv('data/portfolio_returns.csv')
    
    