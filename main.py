import stock as st

""" 
IMPORTANT VARIABLES
"""

TICKERS = ["ABBV", "OKTA", "ENPH", "CVS"]

"""
METHODS
"""

def main(): 
    for ticker in TICKERS:
        try:
            stock = st.Stock(ticker)
            print(stock.getName() + ": " + str(stock.getPrice()))
        except IndexError:
            print("ERROR: the ticker " + ticker + " does not exist ¯\_(ツ)_/¯")
    
if __name__=="__main__": 
    main() 