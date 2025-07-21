import pandas as pd

trends = pd.read_csv('data/trends.csv', index_col=0, parse_dates=True)
prices = pd.read_csv('data/etf_prices.csv', index_col=0, parse_dates=True)

trends = trends.resample('W-MON').mean()

returns = prices.pct_change().dropna()

momentum = (trends - trends.shift(4))/trends.shift(4)

returns.to_csv('data/etf_returns.csv', index=True)
momentum.to_csv('data/trends_momentum.csv', index=True)