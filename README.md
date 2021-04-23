# algofin
A lightweight algorithmic trading and backtesting library. Currently in development.

## Examples
```
from algofin.data import fetch_data
from algofin.backtest import Backtest
from algofin.strategies import EMACrossover

df = fetch_data('GM', '2015-01-01', '2021-01-01')
emac = EMACrossover(t1=5, t2=20, short=True, volume=100, cost=0.03)
backtest = Backtest(emac, df, capital=10000)

backtest.run()
backtest.plot_pl()
```
<img src="/images/crossover_pl.png" alt="EMACrossover P&L" width="600"/>

```
from algofin.data import fetch_data
from algofin.indicators import RSI, plot_RSI

df = fetch_data('BTC-USD', '2021-01-01', '2021-04-01')

df['RSI_14'] = RSI(df, df['Close'])
df.dropna(inplace=True)

plot_RSI(df['RSI_14'])
```
<img src="/images/bitcoin_rsi.png" alt="Bitcoin RSI" width="600"/>
