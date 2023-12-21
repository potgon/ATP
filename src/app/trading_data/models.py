from django.db import models
from datetime import datetime

class Position(models.Model): # Whole class might need a variable name refactor
    date_open = models.DateTimeField(auto_now_add=True)
    date_close = models.DateTimeField(null=True, blank=True)
    open_price = models.DecimalField(max_digits=18, decimal_places=5)
    close_price = models.DecimalField(max_digits=18, decimal_places=5, null=True, blank=True)
    alpha = models.IntegerField()
    net_profit = models.DecimalField(max_digits=18, decimal_places=5, null=True, blank=True)
    sl = models.DecimalField(max_digits=18, decimal_places=5)
    tp = models.DecimalField(max_digits=18, decimal_places=5)
    
    def __init__(self, *args, open_price, atr, alpha, **kwargs):
        super(Position, self).__init__(*args, **kwargs)
        self.open_price = open_price
        self.alpha = alpha
        self.date_open = datetime.now()
        self.sl = Position.calculate_sl(open_price, atr)
        self.tp = Position.calculate_tp(open_price, self.sl)
        self.save()
    
    def close_db(self, close_price: float):
        self.date_close = models.DateTimeField.now()
        self.close_price = close_price
        self.net_profit = self.calculate_net_profit(close_price)
        self.save()
        
    def calculate_net_profit(self, close_price: float) -> float:
        return close_price - self.open_price
    
    def should_close(self, low: float, high: float) -> bool:
        return low <= self.sl or high >= self.tp

    @staticmethod
    def calculate_sl(close: float, atr: float) -> float:
        return close - (atr * 2)
    
    @staticmethod
    def calculate_tp(close: float, sl: float) -> float:
        return (abs(close - sl) * 1.5) + close
    
 
    