import numpy as np

def mean_normalization(x):
    return (x - x.mean()) / x.std()

def min_max_normalization(x):
    return (x - x.min()) / (x.max() - x.min())

def annual_return(start, end, period):
    if not period:
        return 0.0

    return (float(end) / start) ** (1 / float(period)) - 1

def sharpe(r, rfr, stdev):
    return (r - rfr) / stdev
