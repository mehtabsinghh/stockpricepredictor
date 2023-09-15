from flask import Flask, render_template, request
import yfinance as yf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

def generate_and_save_stock_graph(stock_symbol):
    apple_stock = yf.Ticker(stock_symbol)
    stock_data = apple_stock.history(period="1y")

    dates = stock_data.index
    closing_prices = stock_data["Close"]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, closing_prices, label=f'{stock_symbol} Closing Price', color='blue')
    plt.xlabel('Date')
    plt.ylabel('Closing Price (USD)')
    plt.title(f'Stock Price Graph for {stock_symbol}')
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
