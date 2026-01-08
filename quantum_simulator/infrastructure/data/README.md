# Stock Market Data

This directory contains historical stock market data used by the Quantum Finance module.

## Dataset

**File**: `15 Years Stock Data of NVDA AAPL MSFT GOOGL and AMZN.csv`

**Source**: [Kaggle - Stock Market Data](https://www.kaggle.com/datasets/marianadeem755/stock-market-data)

**Description**: 15 years of historical stock data for major tech companies

**Stocks Included**:
- AAPL (Apple Inc.)
- AMZN (Amazon.com Inc.)
- GOOGL (Alphabet Inc.)
- MSFT (Microsoft Corporation)
- NVDA (NVIDIA Corporation)

**Data Fields**:
- Date
- Close_[SYMBOL] - Closing price
- High_[SYMBOL] - Highest price
- Low_[SYMBOL] - Lowest price
- Open_[SYMBOL] - Opening price
- Volume_[SYMBOL] - Trading volume

## Usage

The data is automatically loaded by `StockDataProvider` in `data_provider.py` when the Quantum Finance tab is used in the GUI.
