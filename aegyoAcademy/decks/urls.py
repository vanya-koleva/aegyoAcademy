from django.urls import path, include

from decks import views

urlpatterns = [
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('', include([
        path('<int:pk>/', views.DeckDetailView.as_view(), name='deck-detail'),
        path('<int:pk>/edit/', views.DeckUpdateView.as_view(), name='deck-edit'),
        path('<int:pk>/delete/', views.DeckDeleteView.as_view(), name='deck-delete'),
        path('<int:deck_id>/flashcards/', views.FlashcardListView.as_view(), name='flashcards-list'),
        path('<int:deck_id>/add-flashcard/', views.FlashcardCreateView.as_view(), name='flashcard-add'),
        path('<int:deck_id>/flashcards/<int:pk>/edit/', views.FlashcardUpdateView.as_view(), name='flashcard-edit'),
        path('<int:deck_id>/flashcards/<int:pk>/delete/', views.FlashcardDeleteView.as_view(), name='flashcard-delete'),
        path('create/', views.DeckCreateView.as_view(), name='deck-create'),
    ]))
]