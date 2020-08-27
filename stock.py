import yfinance as yf
import pandas as pd
from bs4 import BeautifulSoup as bs
import pandas_datareader.data as web
import requests
import datetime
import time

class Stock:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.stock = yf.Ticker(symbol)
        self.info = self.stock.info

    def getPrice(self):
        return self.info.get("previousClose")

    def getName(self):
        return self.info.get("shortName")

    def getPeRatio(self):
        return get_fundamental_data("P/E", self.symbol)

    def getRsi(self, n=14):
        end_time = datetime.datetime.now().date().isoformat()
        start_time = datetime.datetime.now() - datetime.timedelta(days=n)
        start_time = start_time.date().isoformat()
        df = web.get_data_yahoo(self.symbol, start=start_time, end=end_time)
        df = df.reset_index()
        
        delta = df['Adj Close'].diff().dropna()

        dUp, dDown = delta.copy(), delta.copy()
        dUp[dUp < 0] = 0
        dDown[dDown > 0] = 0

        RolUp = dUp.ewm(span=n).mean()
        RolDown = dDown.abs().ewm(span=n).mean()

        RS = RolUp / RolDown

        return (100.0 - (100.0 / (1.0 + RS)))[len(RS)]
        

def fundamental_metric(soup, metric):
    return soup.find(text=metric).find_next(class_='snapshot-td2').text

def get_fundamental_data(metric, symbol):
    url = ("http://finviz.com/quote.ashx?t=" + symbol.lower())
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    soup = bs(requests.get(url, headers=headers).content, features="lxml") 
    return fundamental_metric(soup, metric)            
