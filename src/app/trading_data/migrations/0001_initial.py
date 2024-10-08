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
            name="Position",
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
                (
                    "status",
                    models.CharField(
                        choices=[("Open", "Open"), ("Closed", "Closed")],
                        default="Closed",
                        max_length=10,
                    ),
                ),
                ("entry_date", models.DateTimeField(auto_now_add=True)),
                ("exit_date", models.DateTimeField(blank=True, null=True)),
                ("entry_price", models.DecimalField(decimal_places=5, max_digits=18)),
                (
                    "exit_price",
                    models.DecimalField(
                        blank=True, decimal_places=5, max_digits=18, null=True
                    ),
                ),
                ("alpha", models.IntegerField()),
                (
                    "net_profit",
                    models.DecimalField(
                        blank=True, decimal_places=5, max_digits=18, null=True
                    ),
                ),
                ("sl", models.DecimalField(decimal_places=5, max_digits=18)),
                ("tp", models.DecimalField(decimal_places=5, max_digits=18)),
                (
                    "algorithm",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="evaluation_core.algorithm",
                    ),
                ),
                (
                    "asset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="evaluation_core.asset",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["user", "asset", "algorithm"],
                        name="trading_dat_user_id_8512bf_idx",
                    )
                ],
            },
        ),
    ]
