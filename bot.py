import os
import django

import telebot

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.services import save_chat_id_to_user


bot = telebot.TeleBot(os.getenv('TG_TOKEN'))

@bot.message_handler(commands=['start'])
def handle_start(message):
    args = message.text.split()
    if len(args) > 1:
        token = args[1]
    else:
        token = None

    chat_id = message.chat.id

    if token:
        save_chat_id_to_user(token, chat_id)
        bot.send_message(chat_id, "Здравствуйте! Ваш чат подключен.")
    else:
        bot.send_message(chat_id, "Здравствуйте! Отсутствует токен.")

bot.polling()