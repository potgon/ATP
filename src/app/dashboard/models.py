from django.db import models
from django.contrib.auth.models import User


class PriorityUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_priority = models.BooleanField(default=False)
