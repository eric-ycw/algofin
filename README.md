# algofin
A lightweight algorithmic trading and backtesting library. Currently in development.

## Examples
### Backtesting
Running a backtest can be done in a few lines of code. Let's say we want to try out a crossover strategy on General Motors' stock using 5-day and 20-day exponential moving averages.
```
from algofin.data import fetch_data
from algofin.backtest import Backtest
from algofin.strategies import EMACrossover

df = fetch_data('GM', '2015-01-01', '2021-01-01')
ema_crossover = EMACrossover(
    t1=5, t2=20, short=True,
    take_profit=1.15, stop_loss=0.95, size=0.25, cost=0.03
)
backtest = Backtest(ema_crossover, df, capital=100000)

backtest.run()
backtest.print_report()
```
```
----------BACKTEST REPORT----------
Start Date       2015-01-29 00:00:00
End Date         2020-12-31 00:00:00
Realized P&L                 52821.2
Total P&L                    52779.9
Annual Return               0.074192
Sharpe Ratio                 2.31421
No. of Trades                     88
Win Rate                    0.571429
Max Drawdown               -0.147667
```

We can also easily visualise our strategy's P&L and capital management throughout the backtest.

```
backtest.plot_pl()
```
<img src="/images/backtest_pl.png" alt="Backtest P&L" width="600"/>

```
backtest.plot_capital()
```
<img src="/images/backtest_capital.png" alt="Backtest Capital" width="600"/>

We can also run a backtest on a portfolio of instruments using the PortfolioBacktest class.

```
from algofin.backtest import PortfolioBacktest

labels = ['FB', 'AMZN', 'AAPL', 'NFLX', 'GOOGL']
portfolio = [fetch_data(i, '2015-01-01', '2021-01-01') for i in labels]
capital_allocation = [0.25, 0.25, 0.2, 0.15, 0.15]

backtest_2 = PortfolioBacktest(
    ema_crossover, portfolio, capital=1000000,
    capital_allocation=capital_allocation, labels=labels
)

backtest_2.run()
backtest_2.plot_pl_breakdown()
```

<img src="/images/backtest_pl_breakdown.png" alt="Backtest P&L Breakdown" width="600"/>

### Indicators
Algofin comes with popular indicators for technical analysis. For example, we can quickly take a look at the relative strength index of Bitcoin for the last 5 months.

```
from algofin.data import fetch_data
from algofin.indicators import RSI, plot_RSI

df = fetch_data('BTC-USD', '2020-11-20', '2021-04-20')

df['RSI_14'] = RSI(df['Close'])
plot_RSI(df['RSI_14'])
```
<img src="/images/bitcoin_rsi.png" alt="Bitcoin RSI" width="600"/>
