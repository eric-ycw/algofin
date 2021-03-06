import yfinance as yf
import pandas as pd

def fetch_data(ticker, start_date, end_date, actions=True):
    return yf.Ticker(ticker).history(start=start_date, end=end_date, actions=actions)

def risk_free_rate(start_date, end_date):
    # 13-week Treasury
    return yf.Ticker('^IRX').history(start=start_date, end=end_date, actions=False)
