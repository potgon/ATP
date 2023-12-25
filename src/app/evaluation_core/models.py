from django.db import models

class Asset(models.Model):
    name = models.CharField(max_length=15)
    
class ZoneType(models.TextChoices):
    SUPPORT = "Support", "Support"
    RESISTANCE = "Resistance", "Resistance"

class ReversalZone(models.Model):
    asset_id = models.ForeignKey(Asset, on_delete=models.CASCADE)
    asset_type = models.CharField(max_length=20, null=True)
    price = models.DecimalField(max_digits=18, decimal_places=5)
    zone_type = models.CharField(max_length=10, choices=ZoneType.choices, default=ZoneType.SUPPORT)
    price_range_max = models.DecimalField(max_digits=18, decimal_places=5)
    price_range_min = models.DecimalField(max_digits=18, decimal_places=5)
    
class Algorithm(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True, null=True)
    success_rate = models.FloatField(default=0.0)
    average_return = models.FloatField(default=0.0)
    risk_level = models.CharField(max_length=50, blank=True, null=True)
    total_trades = models.IntegerField(default=0)
    active_users = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default='active')
    version = models.CharField(max_length=50, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)