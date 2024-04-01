# Generated by Django 4.2.8 on 2024-04-01 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("evaluation_core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ModelType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("model_name", models.CharField(max_length=50)),
                ("description", models.TextField()),
                ("default_hyperparameters", models.JSONField()),
                ("default_model_architecture", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="TrainedModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("model_name", models.CharField(max_length=50)),
                ("training_timestamp", models.DateTimeField(auto_now_add=True)),
                ("performance_metrics", models.JSONField()),
                ("hyperparameters", models.JSONField()),
                ("model_architecture", models.TextField()),
                ("serialized_model", models.BinaryField()),
                ("training_logs", models.TextField()),
                ("status", models.CharField(max_length=25)),
                (
                    "asset",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="evaluation_core.asset",
                    ),
                ),
                (
                    "model_type",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="model_core.modeltype",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TempModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("model_name", models.CharField(max_length=50)),
                ("training_timestamp", models.DateTimeField(auto_now_add=True)),
                ("performance_metrics", models.JSONField()),
                ("hyperparameters", models.JSONField()),
                ("model_architecture", models.TextField()),
                ("serialized_model", models.BinaryField()),
                ("training_logs", models.TextField()),
                ("status", models.CharField(default="Temporal", max_length=25)),
                (
                    "asset",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="evaluation_core.asset",
                    ),
                ),
                (
                    "model_type",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="model_core.modeltype",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
