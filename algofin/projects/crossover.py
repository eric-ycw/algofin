import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

from algofin.orders import OrderFlag, MarketOrder, OrderBook
from algofin.backtest import Backtest
from algofin.strategies import EMACrossover
from algofin.indicators import SMA

tk = yf.Ticker('GM')
df = tk.history(start='2013-01-01', end='2021-04-01')
df.drop(['Dividends', 'Stock Splits'], axis=1, inplace=True)

capital = 100000
co = EMACrossover(t1=5, t2=20, short=True, volume=1, size=0.2, cost=0.03)
backtest = Backtest(co, df, capital, co.cost)

backtest.run()
backtest.plot_pl()
backtest.plot_capital()
