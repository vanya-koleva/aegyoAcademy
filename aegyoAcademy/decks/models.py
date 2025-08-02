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


class StudySession(models.Model):
    deck = models.ForeignKey(
        Deck,
        on_delete=models.CASCADE,
        related_name='study_sessions'
    )
    user = models.ForeignKey(
        'accounts.AcademyUser',
        on_delete=models.CASCADE,
        related_name='study_sessions'
    )
    started_at = models.DateTimeField(
        auto_now_add=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    total_cards = models.PositiveIntegerField(
        default=0
    )

    known_cards = models.PositiveIntegerField(
        default=0
    )

    unknown_cards = models.PositiveIntegerField(
        default=0
    )

    @property
    def known_percentage(self):
        if self.total_cards == 0:
            return 0
        return round((self.known_cards / self.total_cards) * 100)

    @property
    def unknown_percentage(self):
        if self.total_cards == 0:
            return 0
        return round((self.unknown_cards / self.total_cards) * 100)

class StudySessionCard(models.Model):
    session = models.ForeignKey(
        StudySession,
        on_delete=models.CASCADE,
        related_name='session_cards'
    )

    flashcard = models.ForeignKey(
        Flashcard,
        on_delete=models.CASCADE,
        related_name='study_sessions'
    )

    was_known = models.BooleanField()

    answered_at = models.DateTimeField(
        auto_now_add=True
    )
