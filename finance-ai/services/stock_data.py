import yfinance as yf

tickers = {}

def get_stock_data(symbols):
    symbols_to_fetch = [symbol for symbol in symbols if symbol not in tickers]
    for symbol in symbols_to_fetch:
        tickers[symbol] = yf.Ticker(symbol)
    data = {}
    for symbol in symbols:
        stock = tickers[symbol]
        data[symbol] = stock.history(period="5y")
    return data