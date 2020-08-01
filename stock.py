import yfinance as yf

class Stock:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.stock = yf.Ticker(symbol)
        self.info = self.stock.info

    def getPrice(self):
        return self.info.get("previousClose")

    def getName(self):
        return self.info.get("shortName")