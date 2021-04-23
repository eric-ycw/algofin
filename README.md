# algofin
A lightweight algorithmic trading and backtesting library. Currently in development.

## Examples
Running a backtest can be done in a few lines of code. Let's say we want to try out a crossover strategy on General Motors' stock using 5-day and 20-day exponential moving averages.
```
from algofin.data import fetch_data, risk_free_rate
from algofin.backtest import Backtest
from algofin.strategies import EMACrossover

df = fetch_data('GM', '2015-01-01', '2021-01-01')
emac = EMACrossover(t1=5, t2=20, short=True, size=0.25, cost=0.03)
backtest = Backtest(emac, df, capital=100000)

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

Algofin also comes with popular indicators for technical analysis. Let's say we want to take a look at the relative strength index of Bitcoin for the last 3 months. This can again be done in a few lines of code.

```
from algofin.data import fetch_data
from algofin.indicators import RSI, plot_RSI

df = fetch_data('BTC-USD', '2021-01-01', '2021-04-01')

df['RSI_14'] = RSI(df, df['Close'])
df.dropna(inplace=True)

plot_RSI(df['RSI_14'])
```
<img src="/images/bitcoin_rsi.png" alt="Bitcoin RSI" width="600"/>
