from datamanagement.stock_data_access import StockDataService
from model.train_model import create_features
from service.trading_service import TradingService
from utils.logging_and_visualization import visualize_performance

def fetch_data(ticker, start_date, end_date):
    """
    Fetch historical stock data and create features.
    """
    stock_data_service = StockDataService(ticker)
    data = stock_data_service.fetch_historical_data(start_date, end_date)
    return create_features(data)

def run_trading_system(tickers, start_date, end_date, stop_loss, target_profit, window_size=100):
    """
    Orchestrate the trading system by fetching data, running the trading service,
    and visualizing performance.
    """
    for ticker in tickers:
        print(f"Starting trading for {ticker}")

        # Fetch historical stock data
        data = fetch_data(ticker, start_date, end_date)

        # Initialize the trading service with a sliding window
        model = None  # Model is trained within the sliding window simulation
        trading_service = TradingService(model, target_profit=target_profit, stop_loss=stop_loss)

        # Run the trading simulation
        actual_prices, predicted_prices, performance_log = trading_service.run_simulation(data, window_size)

        # Save trade log
        stock_data_service = StockDataService(ticker)
        stock_data_service.save_trade_log(trading_service.trades)

        # Visualize performance
        visualize_performance(ticker, actual_prices, predicted_prices, performance_log)

        print(f"Finished trading for {ticker}\n")

# Run the trading system
if __name__ == "__main__":
    tickers = input("Enter stock ticker(s), separated by commas (e.g., AAPL,GOOG): ").split(',')
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    stop_loss = float(input("Enter stop loss percentage (e.g., 0.02 for 2%): ") or 0.02)
    target_profit = float(input("Enter target profit percentage (e.g., 0.05 for 5%): ") or 0.05)
    window_size = int(input("Enter sliding window size (e.g., 100 for last 100 days of data): ") or 100)

    run_trading_system(tickers, start_date, end_date, stop_loss, target_profit, window_size)