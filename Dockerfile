FROM python:3.12-slim

ARG SECRET_KEY
ARG TG_TOKEN

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/static /app/media

RUN if [ -n "$SECRET_KEY" ] && [ -n "$TG_TOKEN" ]; then \
    echo "SECRET_KEY=$SECRET_KEY" > .env && \
    echo "TG_TOKEN=$TG_TOKEN" >> .env; \
    fi

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]