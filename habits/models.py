from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from config import settings


class Habit(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Author',
        related_name='Habit',
    )
    place = models.CharField(
        max_length=200,
        verbose_name='Место',
        help_text='Введите место, где необходимо выполнить привычку'
    )
    lead_time = models.DateTimeField()
    action = models.TextField(verbose_name='Действие')
    pleasant_habit = models.BooleanField(
        default=False,
        verbose_name='Признак приятной привычки',
        help_text='Выберете приятная ли это привычка'
    )
    related_habit = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Связанная привычка',
        help_text='Указывается только для полезных привычек',
        related_name='related_to'
    )
    period = models.PositiveSmallIntegerField(
        verbose_name='Периодичность (в днях)',
        help_text='Введите периодичность выполнения привычки в днях, но не более 7',
        validators=[
            MinValueValidator(1, message='Минимум 1 день'),
            MaxValueValidator(7, message='Максимум 7 дней')
        ]
    )
    time_to_complete = models.PositiveIntegerField(
        verbose_name='Время на выполнение привычки',
        help_text='Введите время за которое вы выполните привычку, но не более 120 секунд',
        validators=[
            MinValueValidator(1, message='Минимум 1 секунда'),
            MaxValueValidator(120, message='Максимум 120 секунд')
        ]
    )
    public = models.BooleanField(
        default=False,
        verbose_name='Признак публичности привычки',
        help_text='Публикация в общий доступ'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
        ordering = ['lead_time']

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.pleasant_habit and self.related_habit is not None:
            raise ValidationError('У приятных привычек не может быть связанной привычки')


class Award(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Author',
        related_name='Award',
    )
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        verbose_name='Habit',
        related_name='award_habit',
    )
    title = models.CharField(max_length=50)
    description = models.TextField(verbose_name='Описание вознаграждения')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'вознаграждение'
        verbose_name_plural = 'вознаграждения'