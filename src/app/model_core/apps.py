from django.apps import AppConfig


class ModelCoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.model_core"

    def ready(self):
        from .trainer import Trainer
        Trainer()