from django.db import models

class Asset(models.Model):
    name = models.CharField(max_length=15)
    
class Zone_Type(models.TextChoices):
    SUPPORT = "Support", "Support"
    RESISTANCE = "Resistance", "Resistance"

class ReversalZone(models.Model):
    asset_id = models.ForeignKey(Asset, on_delete=models.CASCADE)
    asset_type = models.CharField(max_length=20, null=True)
    price = models.DecimalField(max_digits=18, decimal_places=5)
    zone_type = models.CharField(max_length=10, choices=Zone_Type.choices, default=Zone_Type.SUPPORT)
    price_range_max = models.DecimalField(max_digits=18, decimal_places=5)
    price_range_min = models.DecimalField(max_digits=18, decimal_places=5)
    