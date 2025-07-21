import pandas as pd
import vectorbt as vbt
import matplotlib.pyplot as plt
import numpy as np

pf_ret = pd.read_csv('data/portfolio_returns.csv', index_col=0)["Return"]
pf_ret.index = pd.to_datetime(pf_ret.index)

start_date = pf_ret.index[0].strftime("%Y-%m-%d")
spy = vbt.YFData.download("SPY", start=start_date, end="2025-07-20", interval="1wk")

spy_ret = spy.get("Close").pct_change().dropna()

pf_price  = (1 + pf_ret).cumprod()
bench_price = (1 + spy_ret).cumprod()

# 3. Create portfolios from prices
pf    = vbt.Portfolio.from_holding(pf_price,    freq="W")
bench = vbt.Portfolio.from_holding(bench_price, freq="W")

print("=== Strategy Performance ===")
print(pf.stats())
print("=== Benchmark Performance ===")
print(bench.stats())

# 4. Plot cumulative returns
plt.figure(figsize=(12, 6))
plt.plot(pf_price.index, pf_price, label='Strategy')
plt.plot(bench_price.index, bench_price, label='SPY Benchmark')
plt.title('Cumulative Returns')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Heatmap of 4-week momentum signals
momentum_window = 4
momentum = pf_ret.rolling(momentum_window).mean()
plt.figure(figsize=(12, 2))
plt.imshow(momentum.values[np.newaxis, :], aspect='auto', cmap='RdYlGn', interpolation='nearest')
plt.colorbar(label='4-Week Momentum')
plt.yticks([])
plt.xticks(range(0, len(momentum.index), max(1, len(momentum.index)//10)), 
           [momentum.index[i].strftime('%Y-%m-%d') for i in range(0, len(momentum.index), max(1, len(momentum.index)//10))], 
           rotation=45)
plt.title('4-Week Rolling Momentum Signal Heatmap')
plt.tight_layout()
plt.show()

# Sector weight over time (if sector weights data available)