from algofin.data import fetch_data
from algofin.backtest import Backtest
from algofin.strategies import EMACrossover

df = fetch_data('GM', '2015-01-01', '2021-01-01')
emac = EMACrossover(t1=5, t2=20, short=True, volume=100, cost=0.03)
backtest = Backtest(emac, df, capital=10000)

backtest.run()
backtest.plot_pl()
