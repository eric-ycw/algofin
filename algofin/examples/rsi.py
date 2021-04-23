from algofin.data import fetch_data
from algofin.indicators import RSI, plot_RSI

df = fetch_data('BTC-USD', '2020-11-20', '2021-04-20')

df['RSI_14'] = RSI(df, df['Close'])
df.dropna(inplace=True)

plot_RSI(df['RSI_14'])
