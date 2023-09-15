import yfinance as yf
import matplotlib.pyplot as plt

# Define the stock symbol (Apple Inc. is AAPL)
stock_symbol = "AAPL"

# Fetch stock data for Apple
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

# Save the plot as a static image
plt.savefig('static/graph.png', format='png')
plt.close()
