from django.db import models

from decks.choices import CardDifficultyChoices


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )

    created_by = models.ForeignKey(
        'accounts.AcademyUser',
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name


class Deck(models.Model):
    title = models.CharField(
        max_length=100
    )

    owner = models.ForeignKey(
        'accounts.AcademyUser',
        on_delete=models.CASCADE
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='decks',
    )

    is_public = models.BooleanField(
        default=False
    )


class Flashcard(models.Model):
    question = models.TextField()

    answer = models.TextField()

    deck = models.ForeignKey(
        Deck,
        on_delete=models.CASCADE,
        related_name='flashcards'
    )

    difficulty = models.CharField(
        choices=CardDifficultyChoices,
    )
