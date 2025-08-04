from django.shortcuts import get_object_or_404
from decks.models import Deck

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
