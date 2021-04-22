import numpy as np
import pandas as pd

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
