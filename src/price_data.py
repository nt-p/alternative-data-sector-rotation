import yfinance as yf
import pandas as pd

etfs = ["XLF", "XLK", "XLE", "XLY"]

price = yf.download(etfs, start="2018-01-01", end="2025-07-20", interval = "1wk")["Close"]



price.to_csv('data/etf_prices.csv', index=True)