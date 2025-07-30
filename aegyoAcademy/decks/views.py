from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from .models import Tag, Deck, Flashcard
from decks.forms import SearchForm, DeckCreateForm, FlashcardCreateForm, DeckEditForm, FlashcardEditForm


class Dashboard(ListView, PermissionRequiredMixin):
    model = Deck
    template_name = 'decks/dashboard.html'
    query_param = "query"
    form_class = SearchForm
    permission_required = 'decks.view_deck'

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        query = self.request.GET.get(self.query_param, '').strip()

        if not user.is_authenticated:
            queryset = queryset.filter(is_public=True)
        elif not self.has_permission():
            queryset = queryset.filter(Q(is_public=True) | Q(owner=user))

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        combined_qs = context['object_list']
        user = self.request.user

        if user.is_authenticated:
            owned_decks = combined_qs.filter(owner=user)

            if self.has_permission():
                other_decks = combined_qs.exclude(owner=user)
            else:
                other_decks = combined_qs.filter(is_public=True).exclude(owner=user)
        else:
            owned_decks = Deck.objects.none()
            other_decks = combined_qs

        context.update({
            "owned_decks": owned_decks,
            "other_decks": other_decks,
            "search_form": self.form_class(),
            "query": self.request.GET.get(self.query_param, ''),
        })
        return context


class DeckDetailView(DetailView, PermissionRequiredMixin):
    model = Deck
    template_name = 'decks/deck-details.html'
    permission_required = 'decks.change_deck, decks.delete_deck'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deck = self.get_object()
        context['flashcards'] = deck.flashcards.all()
        return context


class DeckCreateView(LoginRequiredMixin, CreateView):
    model = Deck
    form_class = DeckCreateForm
    template_name = 'decks/create-deck.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_tags'] = Tag.objects.all()
        return context


class DeckUpdateView(LoginRequiredMixin, UpdateView):
    model = Deck
    form_class = DeckEditForm
    template_name = 'decks/deck-edit.html'
    success_url = reverse_lazy('dashboard')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_tags'] = Tag.objects.all()
        return context


class DeckDeleteView(LoginRequiredMixin, DeleteView):
    model = Deck
    success_url = reverse_lazy('dashboard')


class FlashcardListView(ListView):
    model = Flashcard
    context_object_name = 'flashcards'
    template_name = 'decks/flashcard-list.html'
    paginate_by = 20

    def dispatch(self, request, *args, **kwargs):
        self.deck = get_object_or_404(Deck, pk=self.kwargs['deck_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.deck.flashcards.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deck'] = self.deck
        return context


class FlashcardCreateView(CreateView):
    model = Flashcard
    form_class = FlashcardCreateForm
    template_name = 'decks/flashcard-create.html'

    def dispatch(self, request, *args, **kwargs):
        self.deck = get_object_or_404(Deck, pk=self.kwargs['deck_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['deck'] = self.deck
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deck'] = self.deck
        return context

    def form_valid(self, form):
        form.instance.deck = self.deck
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('flashcards-list', kwargs={'deck_id': self.object.deck.id})


class FlashcardUpdateView(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    model = Flashcard
    form_class = FlashcardEditForm
    permission_required = 'decks.change_flashcard'
    template_name = 'decks/flashcard-edit.html'

    def dispatch(self, request, *args, **kwargs):
        self.deck = get_object_or_404(Deck, pk=self.kwargs['deck_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['deck'] = self.deck
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deck'] = self.deck
        return context

    def form_valid(self, form):
        form.instance.deck = self.deck
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('flashcards-list', kwargs={'deck_id': self.object.deck.id})


class FlashcardDeleteView(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    model = Flashcard
    template_name = 'decks/flashcard_confirm_delete.html'
    permission_required = 'decks.delete_flashcard'

    def dispatch(self, request, *args, **kwargs):
        self.deck = get_object_or_404(Deck, pk=self.kwargs['deck_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deck'] = self.deck
        return context

    def get_success_url(self):
        return reverse_lazy('flashcards-list', kwargs={'deck_id': self.deck.id})
