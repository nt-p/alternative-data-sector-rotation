import pandas as pd

keyword_to_etf = {
    "mortgage rates": "XLF",
    "artificial intelligence": "XLK",
    "oil price": "XLE",
    "online shopping": "XLY"
}

momentum = pd.read_csv('data/trends_momentum.csv', index_col=0, parse_dates=True)
returns = pd.read_csv('data/etf_returns.csv', index_col=0, parse_dates=True)

momentum = momentum.reindex(returns.index)

top_n = 3
portfolio = []


for date in momentum.index[:-1]:
    top_keywords = momentum.loc[date].nlargest(top_n).index.tolist()
    picks = [keyword_to_etf[keyword] for keyword in top_keywords if keyword in keyword_to_etf]
    next_date = returns.index[returns.index.get_loc(date) + 1]

    ret = returns.loc[next_date, picks].mean()
    portfolio.append((next_date, ret))

pd.DataFrame(portfolio, columns=['Date', 'Return'])\
.set_index('Date')\
.to_csv('data/portfolio_returns.csv', index=True, index_label='Date')
    