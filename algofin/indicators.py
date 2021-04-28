import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from algofin.utils import mean_normalization, min_max_normalization

def SMA(close, t=15):
    return close.rolling(window=t, min_periods=t).mean()

def EMA(close, t=15):
    return close.ewm(span=t, min_periods=t).mean()

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

def RSI(close, t=14):
    diff = close.diff()
    u = diff.where(diff > 0, 0)
    d = -diff.where(diff < 0, 0)

    rs = u.ewm(span=t, min_periods=t).mean() / d.ewm(span=t, min_periods=t).mean()

    return 100 - 100 / (1 + rs)

def plot_RSI(rsi, overbought=70, oversold=30):
    rsi_copy = rsi.copy().dropna()
    plt.plot(rsi_copy, label='RSI')
    plt.axhline(y=70, color='r', linestyle='--', label='Overbought (70)')
    plt.axhline(y=30, color='g', linestyle='--', label='Oversold (30)')
    plt.legend()
    plt.show()

def ROC(close, t=21):
    return 100 * (close - close.shift(t)) / close.shift(t)

def WilliamsR(price, high, low, t=14):
    t_high = high.rolling(window=t, min_periods=t).apply(max)
    t_low = low.rolling(window=t, min_periods=t).apply(min)
    return -100 * (t_high - price) / (t_high - t_low)
