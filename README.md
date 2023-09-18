# Stock Price Predictor

A web application that predicts stock prices using machine learning models and displays historical and predicted price trends in a graphical format.

## Table of Contents

- [About](#about)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)


## About

Stock Price Predictor is a web-based application that allows users to predict stock prices for a specified stock symbol using machine learning models. It provides both historical and predicted price data in the form of interactive graphs. Users can choose from different machine learning models for predictions.

## Features

- **Stock Price Prediction:** The application uses machine learning models, including Linear Regression and Random Forest, to predict future stock prices.

- **Graphical Visualization:** Historical stock prices and predicted prices are displayed in interactive graphs for better visualization.

- **Model Selection:** Users can choose between different machine learning models to see how each model predicts stock prices.

- **Easy-to-Use Interface:** The user interface is intuitive, making it easy for users to enter a stock symbol and select a prediction model.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- Matplotlib
- Pandas
- Scikit-Learn
- yfinance

### Installation

```bash
# Clone the repository:
git clone https://github.com/yourusername/stock-price-predictor.git

# Change to the project directory:
cd stock-price-predictor

# Install the required packages:
pip install -r requirements.txt
```

### Usage
```bash
#Start the Flask application:
python app.py
```
**1.** Open your web browser and go to http://localhost:8000 to access the application.

**2.** Enter the stock symbol of the company you want to predict, select a machine learning model (Linear Regression or Random Forest), and click "Submit."

**3.** The application will display a graph showing historical stock prices and predicted prices for the selected stock symbol.

**4.** You can also see the current price and the predicted price displayed above the graph

### Technologies Used
Python
Flask
Matplotlib
Pandas
Scikit-Learn
yfinance

### Contributing
Contributions are welcome! If you have any suggestions or find any issues, please open an issue or create a pull request.
