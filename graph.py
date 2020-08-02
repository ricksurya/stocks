import stock as st
import matplotlib.pyplot as plt

from typing import List

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
    else:
        raise ValueError("The graph type=" + graphType + " is not supported")

def graphLineChart(stock: st.Stock):
    prices = stock.stock.history(period=PERIOD, interval=INTERVAL)
    prices['Close'].plot(figsize=(16, 9))

    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.title(stock.getName() + " Price Chart", **{'fontname':'Comic Sans MS'})

    ax = plt.gca()
    ax.set_facecolor('xkcd:light blue')
    plt.show()