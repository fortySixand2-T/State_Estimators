import argparse
import stock_analysis as sa

def main():
    parser = argparse.ArgumentParser(description="Fetch and analyze stock data")
    parser.add_argument("tickers", nargs="+", help="Stock ticker symbols")
    parser.add_argument("--start-date","-s", default="2020-01-01", help="Start date (default: 2020-01-01)")
    parser.add_argument("--end-date", "-e", default="2023-05-18", help="End date (default: 2023-05-18)")
    parser.add_argument("--plot-type", "-p", choices=['plot_all', 'plot_ma', 'plot_rsi','plot_macd'], default='plot_all', help="Type of plot to display (default: plot_all)")
    parser.add_argument("--output_directory", "-o", required=True, help="Output directory to store plots")

    args = parser.parse_args()
    
    for ticker in args.tickers:
        play = sa.StockAnalysis(ticker, args.output_directory, args.start_date, args.end_date)
        # stock_data = sa.fetch_stock_data(ticker, args.start_date, args.end_date)
        play.plot_stock_data(args.plot_type)

if __name__ == "__main__":
    main()
