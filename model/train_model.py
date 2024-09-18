from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor

def create_features(data):
    """
    Create technical indicators (features) for stock price prediction.
    Features include moving averages (MA10, MA50) and volatility.
    """
    data['MA10'] = data['Adj Close'].rolling(window=10).mean()
    data['MA50'] = data['Adj Close'].rolling(window=50).mean()
    data['Volatility'] = data['Adj Close'].rolling(window=10).std()
    data.dropna(inplace=True)
    return data

def train_random_forest_model(data):
    """
    Train a Random Forest Regressor model on historical stock data.
    The features are technical indicators (MA10, MA50, Volatility), and the target is the adjusted closing price of the next day.
    """
    features = data[['MA10', 'MA50', 'Volatility']]
    target = data['Adj Close'].shift(-1)

    features = features[:-1]
    target = target.dropna()

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, shuffle=False)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    return model