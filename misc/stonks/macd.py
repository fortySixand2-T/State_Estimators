import matplotlib.pyplot as plt
import pandas as pd
import os

class MACD:
    def __init__(self, data, fast=12, slow=26, signal=9):
        self.data = data
        self.fast = fast
        self.slow = slow
        self.signal = signal
        self.macd_line = self.calculate_macd_line()
        self.signal_line = self.calculate_signal_line()
        self.histogram = self.calculate_histogram()
        self.zero_lag_macd = self.calculate_zero_lag_macd()
        self.impulse_lag_macd = self.calculate_impulse_macd()

    def calculate_macd_line(self):
        fast_ema = self.data['Close'].ewm(span=self.fast, adjust=False).mean()
        slow_ema = self.data['Close'].ewm(span=self.slow, adjust=False).mean()
        macd_line = fast_ema - slow_ema
        return macd_line

    def calculate_signal_line(self):
        signal_line = self.macd_line.ewm(span=self.signal, adjust=False).mean()
        return signal_line

    def calculate_histogram(self):
        histogram = self.macd_line - self.signal_line
        return histogram

    def calculate_zero_lag_macd(self):
        fast_zlema = self.calculate_zlema(self.data['Close'], self.fast)
        slow_zlema = self.calculate_zlema(self.data['Close'], self.slow)
        zero_lag_macd = fast_zlema - slow_zlema
        return zero_lag_macd

    def calculate_zlema(self, series, period):
        ema1 = series.ewm(span=period, adjust=False).mean()
        ema2 = ema1.ewm(span=period, adjust=False).mean()
        d = ema1 - ema2
        zlema = ema1 + d
        return zlema

    def calculate_impulse_macd(self, length_ma=34, length_signal=9):
        src = self.data['Close']
        hi = src.rolling(window=length_ma).apply(lambda x: x.max(), raw=True)
        lo = src.rolling(window=length_ma).apply(lambda x: x.min(), raw=True)
        mi = self.calculate_zlema(src, length_ma)
        md = (mi - lo) * (mi > hi) + (mi - hi) * (mi < lo)
        sb = md.rolling(window=length_signal).mean()
        impulse_macd = md - sb
        return impulse_macd

    def plot_macd(self, ticker, output_folder):
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 12))
        
        ax1.plot(self.data['Close'])
        ax1.set_title(f"{ticker} Stock Price")
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Price")
        
        ax2.plot(self.macd_line, label="MACD Line")
        ax2.plot(self.signal_line, label="Signal Line")
        ax2.bar(self.histogram.index, self.histogram, label="Histogram")
        ax2.set_title(f"{ticker} MACD")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("MACD")
        ax2.legend()
        
        zero_lag_macd = self.calculate_zero_lag_macd()
        ax3.plot(zero_lag_macd, label="Zero-Lag MACD")
        ax3.set_title(f"{ticker} Zero-Lag MACD")
        ax3.set_xlabel("Date")
        ax3.set_ylabel("Zero-Lag MACD")
        ax3.legend()
        
        impulse_macd = self.calculate_impulse_macd()
        ax4.plot(impulse_macd, label="Impulse MACD")
        ax4.set_title(f"{ticker} Impulse MACD")
        ax4.set_xlabel("Date")
        ax4.set_ylabel("Impulse MACD")
        ax4.legend()
        
        plt.tight_layout()
        # plt.show()

        # Create the output folder if it doesn't exist
        output_folder = os.path.join(output_folder,"MACD")
        if os.path.exists(output_folder) == False:
            os.makedirs(output_folder, exist_ok=True)
        
        # Save the combined plot to the output folder
        plt.savefig(os.path.join(output_folder, f"{ticker}_macd_combined.png"))
        
        # Save individual plots to separate files
        extent = ax1.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        fig.savefig(os.path.join(output_folder, f"{ticker}_stock_price.png"), bbox_inches=extent)
        
        extent = ax2.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        fig.savefig(os.path.join(output_folder, f"{ticker}_macd.png"), bbox_inches=extent)
        
        extent = ax3.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        fig.savefig(os.path.join(output_folder, f"{ticker}_zero_lag_macd.png"), bbox_inches=extent)
        
        extent = ax4.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        fig.savefig(os.path.join(output_folder, f"{ticker}_impulse_macd.png"), bbox_inches=extent)
        
        plt.close()
        