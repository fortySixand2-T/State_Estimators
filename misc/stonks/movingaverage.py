import matplotlib.pyplot as plt
import pandas as pd
import os

class MovingAverages:
    def __init__(self, data):
        self.data = data

    def calculate_sma(self, window):
        return self.data['Close'].rolling(window=window).mean()

    def calculate_ema(self, window):
        return self.data['Close'].ewm(span=window, adjust=False).mean()

    def calculate_wma(self, window):
        weights = pd.Series(range(1, window + 1))
        return self.data['Close'].rolling(window=window).apply(lambda prices: (prices * weights).sum() / weights.sum(), raw=True)

    def plot_moving_averages(self, ticker,output_folder):
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot the stock price
        ax.plot(self.data['Close'], label='Closing Price')
        
        # Plot the moving averages
        windows = [5, 10, 50, 200]
        for window in windows:
            sma = self.calculate_sma(window)
            ema = self.calculate_ema(window)
            wma = self.calculate_wma(window)
            
            ax.plot(sma, label=f'{window}-day SMA')
            ax.plot(ema, label=f'{window}-day EMA')
            ax.plot(wma, label=f'{window}-day WMA')
        
        # Plot year-to-date moving average
        ytd_sma = self.calculate_sma(self.data.index.dayofyear.max())
        ax.plot(ytd_sma, label='YTD SMA')
        
        # Plot 365-day moving average
        sma_365 = self.calculate_sma(365)
        ax.plot(sma_365, label='365-day SMA')
        
        ax.set_title(f"{ticker} Stock Price and Moving Averages")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.legend()
        ax.grid(True)
        plt.tight_layout()
        # plt.show()


        # Create the output folder if it doesn't exist
        output_folder = os.path.join(output_folder,"MA")
        if os.path.exists(output_folder) == False:
            os.makedirs(output_folder, exist_ok=True)
        
        # Save the plot to the output folder
        plt.savefig(os.path.join(output_folder, f"{ticker}_MA.png"))
        plt.close()
        