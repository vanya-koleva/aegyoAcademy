from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from accounts.forms import CustomUserCreationForm
from accounts.models import Profile
from decks.models import Deck, Flashcard


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('dashboard')
    # Uses signal to create the profile


class ViewProfile(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'registration/profile-details.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['deck_count'] = Deck.objects.filter(owner=user).count()
        context['card_count'] = Flashcard.objects.filter(deck__owner=user).count()

        return context
