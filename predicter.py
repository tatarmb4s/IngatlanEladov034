import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

def PredictNextPrice(prices: np.ndarray) -> float:
    """
    Predicts the next price based on the previous ones using an LSTM model.
    
    Args:
        prices (np.ndarray): An array of historical prices (integers).
        
    Returns:
        float: Predicted next price.
    """
    # Convert prices to a 2D array
    prices = prices.reshape(-1, 1)
    
    # Normalize the data
    scaler = MinMaxScaler()
    prices_scaled = scaler.fit_transform(prices)
    
    # Prepare data for LSTM
    X, y = [], []
    for i in range(len(prices_scaled) - 10):
        X.append(prices_scaled[i:i+10, 0])
        y.append(prices_scaled[i+10, 0])
    X, y = np.array(X), np.array(y)
    
    # Create and train the LSTM model
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(10, 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X, y, epochs=100, batch_size=32)
    
    # Predict the next price
    last_10_days = prices_scaled[-10:].reshape(1, 10, 1)
    next_price_scaled = model.predict(last_10_days)
    next_price = scaler.inverse_transform(next_price_scaled)[0][0]
    
    return next_price



# Example usage of the PredictNextPrice function
if __name__ == "__main__":
    # Replace this with your actual historical stock prices
    historical_prices = np.array([100, 110, 120, 130, 140, 150, 160, 170, 180, 190])
    
    # Call the function to predict the next price
    next_price = PredictNextPrice(historical_prices)
    
    print(f"Predicted next price: ${next_price:.2f}")
# © Copryright 2024 - Tatár Mátyás Bence, Kennedi Nadja