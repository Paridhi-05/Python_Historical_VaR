import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf
import matplotlib.pyplot as plt
from scipy.stats import norm

years = 15

endDate = dt.datetime.now()
startDate = endDate - dt.timedelta(days = 365*years)

tickers = ['SPY','BND','GLD','QQQ','VTI']

adj_close_df = pd.DataFrame()
for ticker in tickers:
    data = yf.download(ticker, start = startDate, end = endDate)
    adj_close_df[ticker] = data['Adj Close']

print(adj_close_df)

log_returns = np.log(adj_close_df/adj_close_df.shift(1))
log_returns = log_returns.dropna()

print(log_returns)

portfolio_value = 1000000
weights = np.array([1/len(tickers)]*len(tickers))
print(weights)

historical_returns = (log_returns*weights).sum(axis = 1)
print(historical_returns)

days = 5
range_returns = historical_returns.rolling(window = days).sum()
range_returns = range_returns.dropna()

print(range_returns)

confidence_interval = 0.95

VaR = -np.percentile(range_returns, 100-(confidence_interval*100))*portfolio_value
print (VaR)

return_windows = days
range_returns = historical_returns.rolling(window = days).sum()
range_returns = range_returns.dropna()

range_returns_dollar = range_returns*portfolio_value

plt.hist(range_returns_dollar.dropna(), bins=50,density=True)
plt.xlabel(f'(return_windows)- Day Portfolio return (Dollar values)')
plt.ylabel('frequency')
plt.title('Distribution of Portfolio(return_window)- Day Returns (Dollar Values)')
plt.axvline(-VaR, color = 'r', linestyle = 'dashed', linewidth= 2, label = f'VaR at {confidence_interval:.0%}confidence level')
plt.legend()
plt.show()

