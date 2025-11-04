import os
import pytz
from datetime import datetime, timedelta

import telebot
from celery import shared_task

from habits.models import Habit


@shared_task
def habit_reminder():
    bot = telebot.TeleBot(os.getenv('TG_TOKEN'))
    current_time = datetime.now(pytz.timezone('Europe/Moscow'))
    notify_delta = timedelta(minutes=20)

    upcoming_habits = Habit.objects.filter(
        lead_time__gte=current_time,
        lead_time__lte=current_time + notify_delta
    ).select_related('author')

    for habit in upcoming_habits:
        user_chat_id = habit.author.telegram_chat_id

        message = (f'Привет! Время для привычки {habit.title} приближается. \n'
                   f'Действие: {habit.action}\n'
                   f'Место: {habit.place}\n'
                   f'Время выполнения: {habit.lead_time.strftime('%Y-%m-%d %H:%M')}\n'
                   f'Время на выполнение: {habit.time_to_complete} секунд')

        try:
            bot.send_message(user_chat_id, message)
        except Exception as e:
            print(f'Ошибка отправки для habit {habit.id} пользователю с chat_id {user_chat_id}: {e}')

        habit.lead_time = habit.lead_time + timedelta(days=habit.period)
        habit.save()
