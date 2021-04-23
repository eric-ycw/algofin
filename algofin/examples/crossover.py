from algofin.data import fetch_data
from algofin.backtest import Backtest
from algofin.strategies import EMACrossover

df = fetch_data('GM', '2015-01-01', '2021-01-01')
emac = EMACrossover(t1=5, t2=20, short=True, size=0.25, cost=0.03)
backtest = Backtest(emac, df, capital=100000)

backtest.run()
backtest.print_report()

backtest.plot_pl()
backtest.plot_capital()
