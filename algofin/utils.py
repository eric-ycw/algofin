import numpy as np

def mean_normalization(x):
    return (x - x.mean()) / x.std()

def min_max_normalization(x):
    return (x - x.min()) / (x.max() - x.min())
