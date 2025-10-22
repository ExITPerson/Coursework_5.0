from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email', help_text='Введите электронную почту')
    full_name = models.CharField(max_length=150, verbose_name='Full name', help_text='Введите свое Ф.И.О.')
    country = models.CharField(max_length=50, null=True, blank=True, verbose_name='Country', help_text='Введите страну')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
