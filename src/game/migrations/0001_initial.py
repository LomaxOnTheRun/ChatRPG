# Generated by Django 4.1 on 2023-03-22 15:26

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Character",
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
                ("name", models.CharField(max_length=200)),
                ("race_name", models.CharField(max_length=100)),
                ("class_name", models.CharField(max_length=100)),
                ("visual_description", models.CharField(max_length=1000)),
                ("personality", models.CharField(max_length=1000)),
                ("backstory", models.CharField(max_length=1000)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
