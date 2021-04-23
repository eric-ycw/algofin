import yfinance as yf
import pandas as pd

def fetch_data(ticker, start_date, end_date):
    return yf.Ticker(ticker).history(start=start_date, end=end_date)
