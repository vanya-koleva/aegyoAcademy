from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.models import Profile

UserModel = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')


class BaseProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'image']
