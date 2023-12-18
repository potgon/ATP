from abc import ABC, abstractmethod

class TradingAlgorithm(ABC):
    
    @abstractmethod
    def __init__(self, fetcher):
        self.fetcher = fetcher
        self.fetch_error = False
    
    @abstractmethod
    def evaluate(self):
        """Evaluate the current data and send a trading signal"""
        pass
    
    @abstractmethod
    def preprocess_data(self, data):
        """Process the raw data and prepare for evaluation"""
        pass
    
    @abstractmethod
    def custom_metric_handler(self, val):
        """Handle custom metric based on specific algorithm logic"""
        pass