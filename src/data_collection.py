from pytrends.request import TrendReq
import pandas as pd

py = TrendReq()

keywords = [
    "mortgage rates",
    "artificial intelligence",
    "climate change",
    "oil price",
    "online shopping"
]

py.build_payload(keywords, timeframe='today 5-y', geo='US')
trends = py.interest_over_time()[keywords]

trends.to_csv('data/trends.csv', index=True)