import matplotlib.pyplot as plt

def log_performance(trading_service, current_day, days_interval=30):
    """
    Log performance data every specified interval.
    """
    if current_day % days_interval == 0:
        trading_service.performance_log.append({
            "day": current_day,
            "balance": round(trading_service.balance, 2),
            "trades": len(trading_service.trades)
        })
        print(f"Day {current_day}: Balance = {round(trading_service.balance, 2)}, Trades executed = {len(trading_service.trades)}")

def visualize_performance(ticker, actual_prices, predicted_prices, performance_log):
    """
    Visualize the actual vs predicted prices and the balance over time.
    """
    # Plot actual vs predicted prices
    plt.figure(figsize=(12, 6))
    plt.plot(actual_prices, label='Actual Prices', color='blue')
    plt.plot(predicted_prices, label='Predicted Prices', color='orange')
    plt.title(f'Actual vs Predicted Prices for {ticker}')
    plt.xlabel('Days')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

    # Plot balance over time
    days = [log['day'] for log in performance_log]
    balances = [log['balance'] for log in performance_log]
    plt.figure(figsize=(12, 6))
    plt.plot(days, balances, label='Balance', color='green')
    plt.title(f'Trading Balance Over Time for {ticker}')
    plt.xlabel('Days')
    plt.ylabel('Balance')
    plt.legend()
    plt.show()