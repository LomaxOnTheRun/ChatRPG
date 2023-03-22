from django.contrib import admin

from . import models


@admin.register(models.Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ("name", "race_name", "class_name")


@admin.register(models.OnePlayerGame)
class OnePlayerGameAdmin(admin.ModelAdmin):
    list_display = ("id", "character")


@admin.register(models.OnePlayerGameTurn)
class OnePlayerGameAdmin(admin.ModelAdmin):
    list_display = ("game", "character", "description")
