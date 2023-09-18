from flask import Flask, render_template, request
import yfinance as yf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import datetime
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor  
import numpy as np


app = Flask(__name__)

# Create a dictionary to map model names to their corresponding model objects
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),  # Example model
}

def generate_and_save_stock_graph(stock_symbol, selected_ml_model):
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=365)

    # Fetch historical stock data
    apple_stock = yf.Ticker(stock_symbol)
    stock_data = apple_stock.history(period="1y", start=start_date, end=end_date)

    # Extract features (days) and target variable (closing price)
    days = np.arange(len(stock_data)).reshape(-1, 1)
    closing_prices = stock_data["Close"]

    # Create polynomial features
    poly = PolynomialFeatures(degree=3)
    X_poly = poly.fit_transform(days)

    # Create and train the selected machine learning model for historical data
    model = selected_ml_model
    model.fit(X_poly, closing_prices)

    # Generate dates for historical data and prediction (e.g., extending for 15 days ahead)
    all_dates = stock_data.index
    future_dates = [all_dates[-1] + datetime.timedelta(days=i) for i in range(1, 6)]  # Extend for 15 days ahead
    
    # Create a continuous range of days for the entire graph, including future dates
    all_days = np.arange(0, len(days) + 5).reshape(-1, 1)
    all_X_poly = poly.transform(all_days)
    all_y_pred = model.predict(all_X_poly)

    # Calculate the predicted prices for the future dates
    future_y_pred = all_y_pred[len(days):]

    # Plot historical stock prices
    plt.figure(figsize=(10, 6))
    plt.plot(all_dates, closing_prices, label=f'{stock_symbol} Closing Price', color='blue')

    # Plot the polynomial regression model line throughout the entire graph
    plt.plot(np.concatenate((all_dates, future_dates)), np.concatenate((all_y_pred[:len(days)], future_y_pred)), label='Predicted Prices', color='red')

    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.title(f'Stock Price Prediction for {stock_symbol}')
    plt.legend()
    plt.grid(True)

    img = BytesIO()
    plt.savefig('static/graph.png', format='png')
    img.seek(0)
    plt.close()

    img_base64 = base64.b64encode(img.read()).decode()
    
    # Get the current price and round it to 2 decimal places
    current_price = round(stock_data["Close"].iloc[-1], 2)

    # Get the predicted price and round it to 2 decimal places
    predicted_price = round(all_y_pred[-1], 2)

    return img_base64, current_price, predicted_price

@app.route('/', methods=['GET', 'POST'])
def index():
    stock_symbol = "AAPL"  # Default stock symbol
    img_data = None
    current_price = None
    predicted_price = None

    if request.method == 'POST':
        stock_symbol = request.form['stock_symbol']
        selected_model = request.form['model']  # Retrieve the selected model
        
        # Get the selected machine learning model from the dictionary
        selected_ml_model = models[selected_model]

        # Generate the graph and update predicted prices using the selected model
        img_data, current_price, predicted_price = generate_and_save_stock_graph(stock_symbol, selected_ml_model)

    return render_template('index.html', img_data=img_data, current_price=current_price, predicted_price=predicted_price)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
