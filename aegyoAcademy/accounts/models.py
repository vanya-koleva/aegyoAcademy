from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from accounts.managers import AcademyUserManager


class AcademyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=25,
        unique=True,
    )

    email = models.EmailField(
        unique=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    objects = AcademyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Profile(models.Model):
    first_name = models.CharField(
        max_length=30,
        null=True,
        blank=True,
    )

    last_name = models.CharField(
        max_length=30,
        null=True,
        blank=True,
    )

    image = models.ImageField(
        upload_to='images',
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        AcademyUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    created_decks = models.IntegerField(
        default=0,
    )

    created_cards = models.IntegerField(
        default=0,
    )

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return 'user'
