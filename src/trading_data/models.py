from django.db import models

class Position(models.Model):
    date_open = models.DateTimeField(auto_now_add=True)
    date_close = models.DateTimeField(null=True, blank=True)
    open_price = models.DecimalFiled(max_digits=18, decimal_places=5)
    close_price = models.DecimalField(max_digits=18, decimal_places=5, null=True, blank=True)
    alpha = models.IntegerField()
    net_profit = models.DecimalField(max_digits=18, decimal_places=5, null=True, blank=True)
    
    def close_position(self, close_price):
        self.date_close = models.DateTimeField.now()
        self.close_price = close_price
        self.net_profit = self.calculate_net_profit()
        self.save()
        
    def calculate_net_profit(self):
        return self.close_price - self.open_price
    