from algofin.data import fetch_data
from algofin.backtest import Backtest
from algofin.strategies import EMACrossover

df = fetch_data('GM', '2015-01-01', '2021-01-01')
strategy = EMACrossover(t1=5, t2=20, short=True, volume=100, cost=0.03)
backtest = Backtest(strategy, df, capital=10000, cost=strategy.cost)

backtest.run()
backtest.plot_pl()
