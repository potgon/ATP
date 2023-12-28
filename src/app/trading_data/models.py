from django.db import models
from django.conf import settings
from datetime import datetime

from app.evaluation_core.models import Asset, Algorithm

class StatusChoices(models.TextChoices):
    OPEN = "Open", "Open"
    CLOSED = "Closed", "Closed"

class Position(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.CLOSED)
    entry_date = models.DateTimeField(auto_now_add=True)
    exit_date = models.DateTimeField(null=True, blank=True)
    entry_price = models.DecimalField(max_digits=18, decimal_places=5)
    exit_price = models.DecimalField(max_digits=18, decimal_places=5, null=True, blank=True)
    alpha = models.IntegerField()
    net_profit = models.DecimalField(max_digits=18, decimal_places=5, null=True, blank=True)
    sl = models.DecimalField(max_digits=18, decimal_places=5)
    tp = models.DecimalField(max_digits=18, decimal_places=5)
    
    class Meta:
        indexes = [
            models.Index(fields=["user", "asset", "algorithm"])
        ]
    
    def __init__(self, *args, entry_price, atr, alpha, **kwargs):
        super(Position, self).__init__(*args, **kwargs)
        self.entry_price = entry_price
        self.alpha = alpha
        self.entry_date = datetime.now()
        self.sl = Position.calculate_sl(open_price, atr)
        self.tp = Position.calculate_tp(open_price, self.sl)
        self.save()
    
    def close_db(self, exit_price: float):
        self.exit_date = models.DateTimeField.now()
        self.exit_price = exit_price
        self.net_profit = self.calculate_net_profit()
        self.save()
        
    def calculate_net_profit(self) -> float:
        return self.exit_price - self.entry_price
    
    def should_close(self, low: float, high: float) -> bool:
        return low <= self.sl or high >= self.tp

    @staticmethod
    def calculate_sl(close: float, atr: float) -> float:
        return close - (atr * 2)
    
    @staticmethod
    def calculate_tp(close: float, sl: float) -> float:
        return (abs(close - sl) * 1.5) + close
    
 
    