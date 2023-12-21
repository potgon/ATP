from django.db import models

class Asset(models.Model):
    name = models.CharField(max_length=15)
    
class Zone_Type(models.TextChoices):
    SUPPORT = "Support", "Support"
    RESISTANCE = "Resistance", "Resistance"

class ReversalZone(models.Model):
    asset_id = models.ForeignKey(Asset, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=18, decimal_places=5)
    zone_type = models.CharField(max_length=10, choices=Zone_Type.choices, default=Zone_Type.SUPPORT)
    price_range_max = DecimaField(max_digits=18, decimal_places=5)
    price_range_min = DecimalField(max_digits=18, decimal_places=5)
    