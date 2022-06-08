# Generated by Django 4.0.4 on 2022-06-08 03:30

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("transaction_id", models.IntegerField()),
                ("date", models.DateField()),
                ("kind", models.CharField(max_length=6)),
                (
                    "amount",
                    models.DecimalField(decimal_places=2, max_digits=19),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "unique_together": {("transaction_id", "date")},
            },
        ),
    ]