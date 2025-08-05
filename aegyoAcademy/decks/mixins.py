from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from decks.models import Deck, Tag


class DeckAccessMixin:
    deck_url_kwarg = 'deck_id'

    def get_deck(self):
        if not hasattr(self, 'deck'):
            deck_id = self.kwargs.get(self.deck_url_kwarg) or self.kwargs.get('pk')
            if not deck_id and hasattr(self, 'get_object'):
                obj = self.get_object()
                if hasattr(obj, 'deck'):
                    self.deck = obj.deck
                    return self.deck
                raise AttributeError("Object has no related deck")
            self.deck = get_object_or_404(Deck, pk=deck_id)
        return self.deck

    def has_view_permission(self, user, deck):
        return (
            user.is_authenticated and (
                user.is_superuser or
                deck.owner == user or
                user.has_perm('decks.view_deck')
            )
        )

    def has_change_permission(self, user, deck):
        return (
            user.is_authenticated and (
                user.is_superuser or
                deck.owner == user or
                user.has_perm('decks.change_deck')
            )
        )

    def has_delete_permission(self, user, deck):
        return (
            user.is_authenticated and (
                user.is_superuser or
                deck.owner == user
            )
        )

    def has_add_permission(self, user, deck):
        return (
            user.is_authenticated and (
                user.is_superuser or
                deck.owner == user or
                user.has_perm('decks.add_deck')
            )
        )

    def test_func(self):
        return False


class TagContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_tags'] = Tag.objects.all()
        return context

class DeckContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deck'] = self.get_deck()
        return context


class FlashcardFormMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['deck'] = self.get_deck()
        return kwargs

    def form_valid(self, form):
        form.instance.deck = self.get_deck()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('flashcards-list', kwargs={'deck_id': self.object.deck.id})


class StudySessionBaseMixin(LoginRequiredMixin, DeckAccessMixin, UserPassesTestMixin):
    def test_func(self):
        deck = self.get_deck()
        return self.has_delete_permission(self.request.user, deck)

    def get_session_data(self):
        return self.request.session.get('current_study_session')