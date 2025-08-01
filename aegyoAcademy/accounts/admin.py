from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from decks.models import Flashcard, Deck
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Profile

CustomUser = get_user_model()


class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active', 'groups', 'user_permissions')}
         ),
    )
    search_fields = ('username',)
    ordering = ('username',)


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'deck_count', 'card_count')

    def deck_count(self, obj):
        return Deck.objects.filter(owner=obj.user).count()

    deck_count.short_description = 'Decks'

    def card_count(self, obj):
        return Flashcard.objects.filter(deck__owner=obj.user).count()

    card_count.short_description = 'Cards'
