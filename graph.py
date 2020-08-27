import stock as st
import matplotlib.pyplot as plt
import pandas as pd

from typing import List
import mplfinance as mpf
import pandas_datareader.data as web
import datetime
import time

""" 
IMPORTANT VARIABLES
"""
PERIOD = "1mo"
INTERVAL = "1d"

def graphStocks(graphType: str, tickers: List[str]):
    for ticker in tickers:
        stock = st.Stock(ticker)
        graphStock(graphType, stock)

def graphStock(graphType: str, stock: st.Stock):
    if graphType == "line":
        graphLineChart(stock)
    elif graphType == 'candlestick':
        graphCandlestickChart(stock)
    elif graphType == 'rsi':
        graphRsi(stock)
    else:
        raise ValueError("The graph type=" + graphType + " is not supported")

def graphLineChart(stock: st.Stock):
    prices = stock.stock.history(period=PERIOD, interval=INTERVAL)
    prices['Close'].plot(figsize=(16, 9))

    plt.rc('figure', titlesize=48)
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.title(stock.getName() + " Price Chart")

    ax = plt.gca()
    ax.set_facecolor('xkcd:pale blue')
    plt.grid()
    plt.show()

def graphCandlestickChart(stock: st.Stock):
    prices = pd.DataFrame(stock.stock.history(period=PERIOD, interval=INTERVAL))
    
    mpf.plot(prices,type='candle')

def graphRsi(stock: st.Stock):
    n = 14
    end_time = datetime.datetime.now().date().isoformat()
    start_time = datetime.datetime.now() - datetime.timedelta(days=n)
    start_time = start_time.date().isoformat()
    df = web.get_data_yahoo(stock.symbol, start=start_time, end=end_time)
    
    delta = df['Adj Close'].diff().dropna()

    dUp, dDown = delta.copy(), delta.copy()
    dUp[dUp < 0] = 0
    dDown[dDown > 0] = 0

    RolUp = dUp.ewm(span=n).mean()
    RolDown = dDown.abs().ewm(span=n).mean()

    RS = RolUp / RolDown
    RSI = (100.0 - (100.0 / (1.0 + RS)))[1:]

    RSI.plot(figsize=(16, 9))

    plt.rc('figure', titlesize=48)
    plt.xlabel("Date")
    plt.ylabel("RSI")
    plt.title(stock.getName() + " RSI Chart")
    ax = plt.gca()
    ax.set_facecolor('xkcd:pale blue')
    plt.grid()
    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)

    plt.show()
