import numpy as np
import pandas as pd
from typing import List, Tuple, Dict
from dataclasses import dataclass
import os

@dataclass
class StockData:
    """
    Represents historical stock price data.
    """
    symbol: str
    prices: List[float]
    dates: List[str]
    
    def normalize_to_angles(self) -> List[float]:
        """
        Normalize prices to [0, π] for quantum angle encoding.
        """
        prices_array = np.array(self.prices)
        min_price = prices_array.min()
        max_price = prices_array.max()
        
        # Avoid division by zero
        if max_price == min_price:
            return [np.pi / 2] * len(self.prices)
        
        # Normalize to [0, 1] then scale to [0, π]
        normalized = (prices_array - min_price) / (max_price - min_price)
        return (normalized * np.pi).tolist()

class StockDataProvider:
    """
    Provides real historical stock data from CSV file for quantum finance simulations.
    """
    
    CSV_FILENAME = "15 Years Stock Data of NVDA AAPL MSFT GOOGL and AMZN.csv"
    
    def __init__(self):
        """Initialize and load the CSV data."""
        try:
            # Get the path relative to this file (infrastructure/data_provider.py)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(current_dir, "data", self.CSV_FILENAME)
            
            self.df = pd.read_csv(csv_path)
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            self.df = self.df.sort_values('Date')  # Ensure chronological order
        except FileNotFoundError:
            raise FileNotFoundError(f"Stock data CSV not found at {csv_path}. Please ensure the file exists in quantum_simulator/infrastructure/data/")
    
    @staticmethod
    def get_available_stocks() -> List[str]:
        """Returns list of available stock symbols."""
        return ["AAPL", "AMZN", "GOOGL", "MSFT", "NVDA"]
    
    def fetch_stock_data(self, symbol: str, days: int = 10) -> StockData:
        """
        Fetches real historical stock data from CSV.
        
        Args:
            symbol: Stock ticker symbol
            days: Number of days of historical data
            
        Returns:
            StockData object with prices and dates
        """
        if symbol not in self.get_available_stocks():
            raise ValueError(f"Unknown stock symbol: {symbol}. Available: {self.get_available_stocks()}")
        
        # Get the most recent 'days' entries
        close_col = f"Close_{symbol}"
        
        if close_col not in self.df.columns:
            raise ValueError(f"Column {close_col} not found in CSV")
        
        # Get last N days
        recent_data = self.df.tail(days)
        
        prices = recent_data[close_col].tolist()
        dates = recent_data['Date'].dt.strftime('%Y-%m-%d').tolist()
        
        return StockData(symbol=symbol, prices=prices, dates=dates)
    
    def get_stock_summary(self, symbol: str, days: int = 30) -> Dict[str, float]:
        """
        Returns summary statistics for a stock.
        """
        data = self.fetch_stock_data(symbol, days=days)
        prices = np.array(data.prices)
        
        return {
            "mean": float(np.mean(prices)),
            "std": float(np.std(prices)),
            "min": float(np.min(prices)),
            "max": float(np.max(prices)),
            "volatility": float(np.std(np.diff(prices)))
        }
