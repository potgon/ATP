from django.contrib.auth.models import User
from django.db import models


class ModelType(models.Model):
    model_name = models.CharField(max_length=50)
    description = models.TextField()
    default_hyperparameters = models.JSONField()
    default_model_architecture = models.TextField()

    def __str__(self):
        return self.model_name


class TrainedModel(models.Model):
    model_type = models.ForeignKey(ModelType, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=50)
    training_timestamp = models.DateTimeField(auto_now_add=True)
    performance_metrics = models.JSONField()
    hyperparameters = models.JSONField()
    model_architecture = models.TextField()
    serialized_model = models.BinaryField()
    training_logs = models.TextField()
    status = models.CharField(max_length=25)

    def __str__(self):
        return self.model_name
