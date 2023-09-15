from flask import Flask, render_template
import yfinance as yf
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend (non-interactive) for Matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

def generate_and_save_stock_graph():
    # Define the stock symbol (Apple Inc. is AAPL)
    stock_symbol = "GME"

    # Fetch stock data
    apple_stock = yf.Ticker(stock_symbol)
    stock_data = apple_stock.history(period="1y")

    # Extract the Date and Closing Price data
    dates = stock_data.index
    closing_prices = stock_data["Close"]

    # Create the stock graph
    plt.figure(figsize=(10, 6))
    plt.plot(dates, closing_prices, label=f'{stock_symbol} Closing Price', color='blue')
    plt.xlabel('Date')
    plt.ylabel('Closing Price (USD)')
    plt.title(f'Stock Price Graph for {stock_symbol}')
    plt.legend()
    plt.grid(True)

    # Save the plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    # Encode the image to base64 for HTML embedding
    img_base64 = base64.b64encode(img.read()).decode()

    return img_base64

@app.route('/')
def index():
    # Generate the stock graph and get the image data
    img_data = generate_and_save_stock_graph()
    
    return render_template('index.html', img_data=img_data)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
