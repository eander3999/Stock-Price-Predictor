import pandas as pd
from model.train_model import train_random_forest_model

class TradingService:
    def __init__(self, model, target_profit=0.05, stop_loss=0.02):
        self.model = model
        self.target_profit = target_profit
        self.stop_loss = stop_loss
        self.balance = 10000
        self.position = 0  # 0 indicates no active position, 1 indicates a buy position
        self.buy_price = 0
        self.trades = []
        self.actual_prices = []
        self.predicted_prices = []
        self.performance_log = [] 

    def predict_price(self, features):
        """
        Predict the future price using the trained model.
        Ensure that the features have the correct column names.
        """
        feature_df = pd.DataFrame([features], columns=['MA10', 'MA50', 'Volatility'])
        return self.model.predict(feature_df)[0]

    def execute_trade(self, current_price, features):
        """
        Execute buy/sell decisions based on predictions and the current price.
        Buys if the predicted price is higher than the current price, sells if target profit or stop loss is hit.
        """
        predicted_price = self.predict_price(features)

        # Buy if there's no position and the predicted price is higher than the current price
        if self.position == 0 and predicted_price > current_price:
            self.buy_price = current_price
            self.position = 1
            self.trades.append(('Buy', current_price))

        # Sell if target profit or stop loss is triggered
        elif self.position == 1:
            if current_price >= self.buy_price * (1 + self.target_profit) or current_price <= self.buy_price * (1 - self.stop_loss):
                self.balance += (current_price - self.buy_price) * 100  # Assuming 100 shares
                self.trades.append(('Sell', current_price))
                self.position = 0
                self.buy_price = 0

    def run_simulation(self, data, window_size, days_interval=30):
        """
        Simulate real-time trading with a sliding window.
        This method encapsulates the entire trading simulation loop.
        """
        for current_day in range(window_size, len(data)):
            sliding_window_data = data.iloc[current_day-window_size:current_day]

            # Re-train model on sliding window
            self.model = train_random_forest_model(sliding_window_data)

            # Execute trades for the current day
            current_price = data['Adj Close'].iloc[current_day]
            features = data[['MA10', 'MA50', 'Volatility']].iloc[current_day]
            self.execute_trade(current_price, features)

            # Track prices for visualization
            self.actual_prices.append(current_price)
            self.predicted_prices.append(self.predict_price(features))

            # Log performance every 30 days
            if current_day % days_interval == 0:
                self.performance_log.append({
                    "day": current_day,
                    "balance": round(self.balance, 2),
                    "trades": len(self.trades)
                })
                print(f"Day {current_day}: Balance = {round(self.balance, 2)}, Trades executed = {len(self.trades)}")

        return self.actual_prices, self.predicted_prices, self.performance_log