import os
import matplotlib.pyplot as plt

class RSI:
    def __init__(self, data, window=14):
        self.data = data
        self.window = window
        self.rsi = self.calculate_rsi()

    def getWindowSize(self):
        return self.window
    def setWindowSize(self, window_size):
        self.window = window_size
    def getData(self):
        return self.data
    
    def calculate_rsi(self):
        delta = self.data['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=self.window).mean()
        avg_loss = loss.rolling(window=self.window).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def calculate_ema_rsi(self, alpha=1/14):
        delta = self.data['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.ewm(alpha=alpha, adjust=False).mean()
        avg_loss = loss.ewm(alpha=alpha, adjust=False).mean()
        rs = avg_gain / avg_loss
        ema_rsi = 100 - (100 / (1 + rs))
        return ema_rsi

    def calculate_cutlers_rsi(self):
        delta = self.data['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=self.window).sum() / self.window
        avg_loss = loss.rolling(window=self.window).sum() / self.window
        rs = avg_gain / avg_loss
        cutlers_rsi = 100 - (100 / (1 + rs))
        return cutlers_rsi

    def calculate_conners_rsi(self, streak_window=2, rank_window=100):
        rsi = self.calculate_rsi()
        streak = self.data['Close'].diff().apply(lambda x: 1 if x > 0 else -1 if x < 0 else 0)
        streak_rsi = streak.rolling(window=streak_window).sum() / streak_window
        percent_rank = self.data['Close'].diff().rolling(window=rank_window).apply(lambda x: x.rank(pct=True).iloc[-1])
        conners_rsi = (rsi + streak_rsi + percent_rank) / 3
        return conners_rsi
    
    def plot_rsi_data(self, ticker, output_folder):
        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, figsize=(12, 15))
        
        # Plot the stock price
        data = self.getData()
        ax1.plot(data['Close'])
        ax1.set_title(f"{ticker} Stock Price")
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Price")
        
        # Calculate and plot the RSI
        rsi = self.calculate_rsi()
        ax2.plot(rsi)
        ax2.set_title(f"{ticker} RSI")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("RSI")
        
        # Calculate and plot the EMA RSI
        ema_rsi = self.calculate_ema_rsi()
        ax3.plot(ema_rsi)
        ax3.set_title(f"{ticker} EMA RSI")
        ax3.set_xlabel("Date")
        ax3.set_ylabel("EMA RSI")
        
        # Calculate and plot Cutler's RSI
        cutlers_rsi = self.calculate_cutlers_rsi()
        ax4.plot(cutlers_rsi)
        ax4.set_title(f"{ticker} Cutler's RSI")
        ax4.set_xlabel("Date")
        ax4.set_ylabel("Cutler's RSI")
        
        # Calculate and plot Conner's RSI
        conners_rsi = self.calculate_conners_rsi()
        ax5.plot(conners_rsi)
        ax5.set_title(f"{ticker} Conner's RSI")
        ax5.set_xlabel("Date")
        ax5.set_ylabel("Conner's RSI")
        
        plt.tight_layout()
        # plt.show()

        # Create the output folder if it doesn't exist
        output_folder = os.path.join(output_folder,"RSI")

        if os.path.exists(output_folder) == False:
            os.makedirs(output_folder, exist_ok=True)
        
        # Save the plot to the output folder
        # Save the combined plot to the output folder
        plt.savefig(os.path.join(output_folder, f"{ticker}_RSI_combined.png"))
        
        # Save individual plots to separate files
        extent = ax1.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        fig.savefig(os.path.join(output_folder, f"{ticker}_stock_price.png"), bbox_inches=extent)
        
        extent = ax2.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        fig.savefig(os.path.join(output_folder, f"{ticker}_RSI.png"), bbox_inches=extent)
        
        extent = ax3.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        fig.savefig(os.path.join(output_folder, f"{ticker}_RSI_EMA.png"), bbox_inches=extent)
        
        extent = ax4.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        fig.savefig(os.path.join(output_folder, f"{ticker}_RSI_Cutlers.png"), bbox_inches=extent)

        extent = ax5.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        fig.savefig(os.path.join(output_folder, f"{ticker}_RSI_Conners.png"), bbox_inches=extent)
        
        plt.close()
        