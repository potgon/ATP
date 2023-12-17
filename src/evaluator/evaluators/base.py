from abc import ABC, abstractmethod

class TradingAlgorithm(ABC):
    
    @abstractmethod
    def evaluate(self):
        pass
    
    @abstractmethod
    def preprocess_data(self, data):
        pass
    
    @abstractmethod
    def custom_metric_handler(self, val):
        pass