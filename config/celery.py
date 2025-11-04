from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установка переменной окружения для настроек проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создание экземпляра объекта Celery
app = Celery('config')

# Загрузка настроек из файла Django
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update({
    'broker_url': 'redis://localhost:6379/0',  # Замените на ваш брокер
    'result_backend': 'redis://localhost:6379/0',  # Замените на ваш backend
    'worker_concurrency': 4,  # Установите количество потоков или процессов
    'worker_pool': 'threads',  # Используйте потоки вместо процессов
})

# Автоматическое обнаружение и регистрация задач из файлов tasks.py в приложениях Django
app.autodiscover_tasks(['habits'])
