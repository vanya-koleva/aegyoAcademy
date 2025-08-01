from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from accounts.forms import CustomUserCreationForm, ProfileEditForm
from accounts.models import Profile, AcademyUser
from decks.models import Deck, Flashcard


UserModel = get_user_model()


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

        context['deck_count'] = user.deck_set.count()
        context['card_count'] = Flashcard.objects.filter(deck__owner=user).count()

        return context


class EditProfile(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'registration/profile-edit.html'
    success_url = reverse_lazy('view-profile')

    def get_object(self, queryset=None):
        return self.request.user.profile


class DeleteAccountView(LoginRequiredMixin, DeleteView):
    model = UserModel
    template_name = 'registration/account_confirm_delete.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return super().delete(request, *args, **kwargs)