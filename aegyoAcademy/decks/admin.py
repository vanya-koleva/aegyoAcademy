from django.contrib import admin
from .models import StudySession, StudySessionCard, Deck, Flashcard, Tag


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'is_public')
    list_filter = ('owner', 'is_public')


@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'deck', 'difficulty')
    list_filter = ('deck', 'difficulty')


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'deck', 'started_at', 'completed_at')
    list_filter = ('user', 'deck')


@admin.register(StudySessionCard)
class StudySessionCardAdmin(admin.ModelAdmin):
    list_display = ('session', 'flashcard', 'was_known', 'answered_at')
    list_filter = ('session', 'was_known')
