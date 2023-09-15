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
import numpy as np

app = Flask(__name__)

def generate_and_save_stock_graph(stock_symbol):
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

    # Create and train a Polynomial Regression model for historical data
    model = LinearRegression()
    model.fit(X_poly, closing_prices)

    # Generate dates for historical data and prediction (e.g., extending for 1 additional month)
    all_dates = stock_data.index
    future_dates = [all_dates[-1] + datetime.timedelta(days=i) for i in range(1, 32)]
    
    # Extend the polynomial regression line into the future
    future_days = np.arange(len(days), len(days) + 31).reshape(-1, 1)
    X_future_poly = poly.transform(future_days)
    y_pred = model.predict(X_future_poly)
    
    # Ensure all_dates has the correct length
    all_dates = np.concatenate((all_dates, future_dates[-31:]))

    # Plot historical and predicted stock prices
    plt.figure(figsize=(10, 6))
    plt.plot(all_dates[:len(closing_prices)], closing_prices, label=f'{stock_symbol} Closing Price', color='blue')
    plt.plot(all_dates[-31:], y_pred, label='Predicted Prices', color='red')
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
    return img_base64

@app.route('/', methods=['GET', 'POST'])
def index():
    stock_symbol = "AAPL"  # Default stock symbol
    img_data = None

    if request.method == 'POST':
        stock_symbol = request.form['stock_symbol']
    
    img_data = generate_and_save_stock_graph(stock_symbol)

    return render_template('index.html', img_data=img_data)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
