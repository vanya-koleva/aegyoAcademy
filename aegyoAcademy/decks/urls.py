from django.urls import path

from decks import views

urlpatterns = [
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),

    path('create/', views.DeckCreateView.as_view(), name='deck-create'),
    path('<int:pk>/', views.DeckDetailView.as_view(), name='deck-detail'),
    path('<int:pk>/edit/', views.DeckUpdateView.as_view(), name='deck-edit'),
    path('<int:pk>/delete/', views.DeckDeleteView.as_view(), name='deck-delete'),

    path('<int:deck_id>/flashcards/', views.FlashcardListView.as_view(), name='flashcards-list'),
    path('<int:deck_id>/add-flashcard/', views.FlashcardCreateView.as_view(), name='flashcard-add'),
    path('<int:deck_id>/flashcards/<int:pk>/edit/', views.FlashcardUpdateView.as_view(), name='flashcard-edit'),
    path('<int:deck_id>/flashcards/<int:pk>/delete/', views.FlashcardDeleteView.as_view(), name='flashcard-delete'),

    path('<int:deck_id>/study/', views.StudySessionStartView.as_view(), name='study-session-start'),
    path('<int:deck_id>/study/card/', views.StudySessionCardView.as_view(), name='study-session-card'),
    path('<int:deck_id>/study/answer/', views.StudySessionAnswerView.as_view(), name='study-session-answer'),
    path('study/<int:session_id>/results/', views.StudySessionResultsView.as_view(), name='study-session-results'),
]