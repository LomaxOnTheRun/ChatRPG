from django.db import models


class Character(models.Model):
    name = models.CharField(max_length=200)
    race_name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)
    visual_description = models.CharField(max_length=1000)
    personality = models.CharField(max_length=1000)
    backstory = models.CharField(max_length=1000)

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
