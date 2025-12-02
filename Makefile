.PHONY: up down build logs test migrate createsuperuser collectstatic clean setup-env

setup-env:
	@echo "Создание .env файла из шаблона..."
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Файл .env создан. Отредактируйте его!"; \
	else \
		echo "Файл .env уже существует."; \
	fi

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose up -d --build

logs:
	docker-compose logs -f

logs-web:
	docker-compose logs -f web

logs-db:
	docker-compose logs -f db

logs-redis:
	docker-compose logs -f redis

logs-celery:
	docker-compose logs -f celery_worker celery_beat

logs-bot:
	docker-compose logs -f telegram_bot

test:
	docker-compose exec web python manage.py test

migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

shell:
	docker-compose exec web python manage.py shell

shell-plus:
	docker-compose exec web python manage.py shell_plus

clean:
	docker-compose down -v
	docker system prune -af