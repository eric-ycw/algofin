from algofin.data import fetch_data
from algofin.backtest import Backtest, PortfolioBacktest
from algofin.strategies import EMACrossover

df = fetch_data('GM', '2015-01-01', '2021-01-01')
ema_crossover = EMACrossover(
    t1=5, t2=20, short=True,
    take_profit=1.15, stop_loss=0.95, size=0.25, cost=0.03
)
backtest = Backtest(ema_crossover, df, capital=100000)

backtest.run()
backtest.print_report()

backtest.plot_pl()
backtest.plot_capital()

labels = ['FB', 'AMZN', 'AAPL', 'NFLX', 'GOOGL']
portfolio = [fetch_data(i, '2015-01-01', '2021-01-01') for i in labels]
capital_allocation = [0.25, 0.25, 0.2, 0.15, 0.15]

backtest_2 = PortfolioBacktest(
    ema_crossover, portfolio, capital=1000000,
    capital_allocation=capital_allocation, labels=labels
)

backtest_2.run()

backtest_2.plot_pl()
backtest_2.plot_pl_breakdown()
backtest_2.plot_capital()
