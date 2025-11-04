from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email', help_text='Введите электронную почту')
    full_name = models.CharField(max_length=150, verbose_name='Full name', help_text='Введите свое Ф.И.О.')
    country = models.CharField(max_length=50, null=True, blank=True, verbose_name='Country', help_text='Введите страну')
    telegram_auth_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    telegram_chat_id = models.BigIntegerField(null=True, blank=True, verbose_name='Telegram chat ID')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def get_telegram_auth_link_bot(self):
        bot = 'habits_one_bot'
        return f'https://t.me/{bot}?start={self.telegram_auth_token}'