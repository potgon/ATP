from django.db import models

class Position:
    def __init__(models.Model):
        close = models.FloatField()
        atr = models.FloatField()
        sl = models.FloatField()
        tp = models.FloatField()
        timestamp = models.DateTimeField(auto_now_add=True)
        
    def open_position(cls, close, atr):
        return cls.objects.create(close=close, atr=atr, sl=calculated_sl, tp=calculated_tp)
    
    def close_position(self):
        self.delete()
        