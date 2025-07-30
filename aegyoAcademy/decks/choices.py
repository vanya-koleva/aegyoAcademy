from django.db import models


class CardDifficultyChoices(models.TextChoices):
    PERFECT = "P", "Perfect"
    EASY = "E", "Easy"
    MEDIUM = "M", "Medium"
    HARD = "H", "Hard"
