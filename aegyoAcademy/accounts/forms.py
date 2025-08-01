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
        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['image'].required = False


class ProfileEditForm(BaseProfileForm):
    clear_image = forms.BooleanField(
        required=False,
        label='Remove current image'
    )

    def save(self, commit=True):
        profile = super().save(commit=False)

        if self.cleaned_data.get('clear_image') and profile.image:
            profile.image = None  # Uses signal to handle file deletion

        if commit:
            profile.save()
        return profile
