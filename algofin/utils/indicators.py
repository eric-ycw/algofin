import numpy as np
import pandas as pd

from algofin.utils.tools import mean_normalization, min_max_normalization

def MACD(close, t1=12, t2=26):
    assert(t2 > t1)
    return close.ewm(span=t1, min_periods=t2).mean() - \
           close.ewm(span=t2, min_periods=t2).mean()

def StochasticK(price, high, low, t=5):
    t_high = high.rolling(window=t, min_periods=t).apply(max)
    t_low = low.rolling(window=t, min_periods=t).apply(min)
    return 100 * (price - t_low) / (t_high - t_low)

def StochasticD(sK, t=3):
    return sK.rolling(window=t, min_periods=t).mean()

def RSI(df, close, t=14):
    df_copy = df.copy()
    diff = close.diff()
    df_copy['u'] = np.where(diff > 0, diff, 0)
    df_copy['d'] = np.where(diff < 0, -diff, 0)

    rs = df_copy['u'].ewm(span=t, min_periods=t).mean() / df_copy['d'].ewm(span=t, min_periods=t).mean()

    return 100 - 100 / (1 + rs)

def WilliamsR(price, high, low, t=14):
    t_high = high.rolling(window=t, min_periods=t).apply(max)
    t_low = low.rolling(window=t, min_periods=t).apply(min)
    return -100 * (t_high - price) / (t_high - t_low)

def fill_indicators(df, normalization=None):
    indicators = ['EMA_15', 'MACD', 'StochasticK', 'StochasticD', 'RSI', 'WilliamsR']

    df['ClosePctChange'] = df['Close'].pct_change()
    df['EMA_15'] = df['Close'].ewm(span=15, min_periods=15).mean()
    df['MACD'] = MACD(df['Close'])
    df['StochasticK'] = StochasticK(df['Close'], df['High'], df['Low'])
    df['StochasticD'] = StochasticD(df['StochasticK'])
    df['RSI'] = RSI(df, df['Close'])
    df['WilliamsR'] = WilliamsR(df['Close'], df['High'], df['Low'])

    for i in indicators:
        if normalization == 'mean':
            df[i] = mean_normalization(df[i])
        elif normalization == 'minmax':
            df[i] = min_max_normalization(df[i])

    return df
