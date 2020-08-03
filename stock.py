import yfinance as yf
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests

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

def fundamental_metric(soup, metric):
    return soup.find(text=metric).find_next(class_='snapshot-td2').text

def get_fundamental_data(metric, symbol):
    url = ("http://finviz.com/quote.ashx?t=" + symbol.lower())
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    soup = bs(requests.get(url, headers=headers).content, features="lxml") 
    return fundamental_metric(soup, metric)            
