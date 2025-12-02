# Курсовая работа 5 - Приложение для отслеживания привычек

## Описание проекта

Django REST API приложение для управления привычками с системой уведомлений через Telegram. Приложение позволяет пользователям создавать, отслеживать и управлять своими привычками, получать напоминания и анализировать прогресс.

**Демо:** http://147.45.246.38

## Технологический стек

- **Backend:** Python 3.12, Django 5.2, Django REST Framework
- **База данных:** PostgreSQL 16
- **Кэширование и брокер:** Redis 7
- **Асинхронные задачи:** Celery 5.5 + Celery Beat
- **Уведомления:** Telegram Bot API
- **Веб-сервер:** Nginx + Gunicorn
- **Контейнеризация:** Docker + Docker Compose
- **CI/CD:** GitHub Actions
- **Документация API:** Swagger/OpenAPI

## Быстрый старт

### Предварительные требования

- Docker 20.10+
- Docker Compose 2.0+
- Git

### Локальная разработка

1. **Клонирование репозитория:**

```bash
git clone git@github.com:ExITPerson/Coursework_5.0.git
cd coursework_5
```

2. **Настройка переменных окружения:**

```bash
cp .env.example .env
```
Отредактируйте файл .env для локальной разработки:
```bash
SECRET_KEY=django-insecure-ваш-ключ-для-разработки
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
NAME=habits
USER=habits_user
PASSWORD=локальный-пароль
HOST=localhost
PORT=5432
TG_TOKEN=ваш-тестовый-токен-бота
```

3. **Запуск в режиме разработки:**

```bash
# Используйте Makefile для удобства
make setup-env  # Создает .env файл если его нет
make build      # Собирает и запускает контейнеры
```
Или напрямую через Docker Compose:
```bash
docker-compose -f docker-compose.yml -f docker-compose.override.yml up --build
```

4. **Доступ к приложению:**

После запуска приложение будет доступно по следующим адресам:
- Основное приложение: http://localhost:8000
- Swagger UI (документация API): http://localhost:8000/swagger/
- ReDoc (альтернативная документация): http://localhost:8000/redoc/
- Админ-панель Django: http://localhost:8000/admin/
- Статические файлы: http://localhost/static/

5. **Инициализация базы данных:**

```bash
# Создание суперпользователя
docker-compose exec web python manage.py createsuperuser

# Следовать инструкциям в терминале
```

### Продакшен-запуск

Для продакшен-окружения используйте:
```bash
# Используйте только основной docker-compose.yml
docker-compose up -d --build
```

### Управление проектом
#### Команды Docker Compose
```bash
# Запуск всех сервисов
docker-compose up -d

# Остановка всех сервисов
docker-compose down

# Пересборка и запуск
docker-compose up -d --build

# Просмотр логов
docker-compose logs -f              # Все сервисы
docker-compose logs -f web         # Только Django
docker-compose logs -f db          # Только PostgreSQL
docker-compose logs -f redis       # Только Redis
docker-compose logs -f celery_worker # Только Celery Worker
docker-compose logs -f celery_beat # Только Celery Beat
docker-compose logs -f telegram_bot # Только Telegram бот
docker-compose logs -f nginx       # Только Nginx

# Проверка состояния
docker-compose ps
docker-compose top
```

#### Команды Django

```bash
# Все команды выполняются внутри контейнера web
docker-compose exec web python manage.py <команда>

# Основные команды:
docker-compose exec web python manage.py migrate        # Применить миграции
docker-compose exec web python manage.py makemigrations # Создать миграции
docker-compose exec web python manage.py createsuperuser # Создать администратора
docker-compose exec web python manage.py collectstatic  # Собрать статику
docker-compose exec web python manage.py test           # Запустить тесты
docker-compose exec web python manage.py shell          # Django shell
```

#### Использование Makefile (рекомендуется)

Для удобства управления проектом используйте Makefile:
```bash
make up          # Запустить все контейнеры
make down        # Остановить все контейнеры
make build       # Пересобрать и запустить
make logs        # Показать логи всех сервисов
make logs-web    # Логи только Django
make logs-celery # Логи Celery
make test        # Запустить тесты
make migrate     # Выполнить миграции
make collectstatic # Собрать статику
make shell       # Открыть Django shell
make clean       # Полная очистка (контейнеры, образы, тома)
```

### Настройка CI/CD

#### Настройка GitHub Secrets

Для автоматического деплоя необходимо добавить секреты в репозитории GitHub:
1. Перейдите в настройки репозитория:
    - Settings → Secrets and variables → Actions → New repository secret
2. Добавьте следующие секреты:


3. Проверка работы CI/CD:
    - После добавления секретов создайте PR или запушите в main ветку
    - GitHub Actions автоматически запустит пайплайн
    - Проверьте статус в Actions → CI/CD Pipeline

#### Настройка сервера для деплоя

1. Подготовка сервера:
```bash
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Добавление пользователя в группу docker
sudo usermod -aG docker $USER
```

2. Настройка SSH доступа:
```bash
# На сервере сгенерируйте SSH ключ
ssh-keygen -t rsa -b 4096 -f ~/.ssh/github_actions -N ""

# Добавьте публичный ключ в authorized_keys
cat ~/.ssh/github_actions.pub >> ~/.ssh/authorized_keys

# Скопируйте приватный ключ (для GitHub Secrets)
cat ~/.ssh/github_actions
```

3. Развертывание проекта на сервере:
```bash
# Клонирование проекта
mkdir -p /root/coursework_5
cd /root/coursework_5
git clone <ваш-репозиторий> .

# Создание .env файла (значения будут подставлены GitHub Actions)
cp .env.example .env

# Первоначальный запуск
docker-compose up -d --build
```

### Структура проекта

```text
coursework_5/
├── .github/workflows/          # CI/CD конфигурация GitHub Actions
│   └── ci.yml                  # Пайплайн тестирования и деплоя
├── config/                     # Настройки Django проекта
│   ├── __init__.py
│   ├── settings.py            # Основные настройки
│   ├── urls.py                # Маршрутизация
│   ├── wsgi.py                # WSGI конфигурация
│   ├── asgi.py                # ASGI конфигурация
│   └── celery.py              # Конфигурация Celery
├── habits/                     # Приложение привычек
│   ├── migrations/            # Миграции базы данных
│   ├── __init__.py
│   ├── admin.py               # Админ-панель
│   ├── apps.py                # Конфигурация приложения
│   ├── models.py              # Модели данных
│   ├── views.py               # Представления API
│   ├── serializers.py         # Сериализаторы
│   ├── urls.py                # Маршруты API
│   ├── tasks.py               # Celery задачи
│   ├── tests.py               # Тесты
│   ├── permissions.py         # Права доступа
│   ├── paginators.py          # Пагинация
│   └── services.py            # Бизнес-логика
├── users/                      # Приложение пользователей
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── tests.py
│   └── services.py
├── static/                     # Статические файлы (CSS, JS, изображения)
├── media/                      # Медиафайлы (загружаемые пользователями)
├── docker-compose.yml          # Продакшен конфигурация Docker Compose
├── docker-compose.override.yml # Конфигурация для разработки
├── Dockerfile                  # Конфигурация Docker образа
├── nginx.conf                  # Конфигурация Nginx
├── requirements.txt            # Зависимости Python
├── .env.example                # Шаблон переменных окружения
├── .dockerignore               # Игнорируемые файлы для Docker
├── .gitignore                  # Игнорируемые файлы для Git
├── init.sql                    # Скрипт инициализации базы данных
├── bot.py                      # Telegram бот для уведомлений
├── Makefile                    # Утилита команд для разработки
├── manage.py                   # Утилита управления Django
└── README.md                   # Документация
```

## Переменные окружения

### Обязательные переменные
Создайте файл .env на основе .env.example:

```env
# Django
SECRET_KEY=ваш_уникальный_секретный_ключ
DEBUG=False                    # В продакшене всегда False
ALLOWED_HOSTS=localhost,127.0.0.1,147.45.246.38,ваш-домен.ru

# База данных PostgreSQL
NAME=habits                    # Имя базы данных
USER=habits_user              # Пользователь базы данных
PASSWORD=сильный_сложный_пароль # Пароль пользователя
HOST=db                       # Хост базы (db для Docker)
PORT=5432                     # Порт базы данных

# Telegram Bot
TG_TOKEN=ваш_токен_бота_от_BotFather

# Redis и Celery
CELERY_BROKER_URL=redis://redis:6379
CELERY_RESULT_BACKEND=redis://redis:6379
CACHE_LOCATION=redis://redis:6379/1
```

### Рекомендуемые значения для разработки
```env
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
TG_TOKEN=test_token_123  # Для разработки можно использовать заглушку
```

## Настройка Telegram бота

### Создание бота
1. Откройте Telegram и найдите @BotFather
2. Создайте нового бота:
    ```text
    /newbot
    → Укажите имя бота (например, Habits Tracker Bot)
    → Укажите username бота (например, habits_tracker_bot)
    → Получите токен
    ```
3. Добавьте токен в переменные окружения

### Подключение пользователей

Пользователи подключаются к боту через специальную ссылку, которая генерируется в их профиле. Бот использует вебхуки для получения обновлений и отправки уведомлений о привычках.

## Celery задачи

### Периодические задачи
- habit_reminder: Отправка уведомлений о приближающихся привычках (каждые 5 минут)
- Настройки в config/settings.py:
    ```python
    CELERY_BEAT_SCHEDULE = {
        'habit_reminder': {
            'task': 'habits.tasks.habit_reminder',
            'schedule': crontab(minute='*/5'),
        },
    }
    ```

