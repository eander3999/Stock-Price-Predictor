import yfinance as yf
import pandas as pd

class StockDataService:
    def __init__(self, ticker):
        self.ticker = ticker

    def fetch_historical_data(self, start_date, end_date):
        """
        Fetch historical stock data from Yahoo Finance between the specified dates.
        Returns a DataFrame containing the stock data.
        """
        data = yf.download(self.ticker, start=start_date, end=end_date)
        data['Return'] = data['Adj Close'].pct_change()
        data.dropna(inplace=True)
        return data

    def save_trade_log(self, trades, filename="data/trade_log.csv"):
        """
        Save the list of trades to a CSV file.
        Each trade contains the action ('Buy' or 'Sell') and the price at which the trade was executed.
        """
        pd.DataFrame(trades, columns=['Action', 'Price']).to_csv(filename, index=False)