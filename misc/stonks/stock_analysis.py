import pandas as pd
import yfinance as yf
import rsi as r
import movingaverage as ma
import macd
import os

class StockAnalysis:
    def __init__(self, ticker, output_directory, start_date = "2022-05-01", end_date = "2024-05-01"):
        self.ticker = ticker
        self.output_folder = os.path.join(output_directory, ticker)
        self.stock_data = self.fetch_stock_data(start_date,end_date)

    def get_ticker(self):
        return self.ticker
    
    def get_stock_data(self):
        return self.stock_data
    
    def get_output_folder(self):
        return self.output_folder
    
    def fetch_stock_data(self, start_date, end_date):
        stock_data = yf.download(self.ticker, start=start_date, end=end_date)
        return stock_data

    def plot_stock_data(self, plot_type):
        if os.path.exists(self.output_folder) == False:
            os.makedirs(self.output_folder)
            
        if plot_type == 'plot_all' or plot_type == 'plot_ma':
            m = ma.MovingAverages(self.stock_data)
            m.plot_moving_averages(self.ticker, self.output_folder)
            # fig.show()

        if plot_type == 'plot_all' or plot_type == 'plot_rsi':
            p = r.RSI(self.stock_data)
            p.plot_rsi_data(self.ticker, self.output_folder)

        if plot_type == 'plot_all' or plot_type == 'plot_macd':
            mac = macd.MACD(self.stock_data)
            mac.plot_macd(self.ticker, self.output_folder)