# --- Базовый образ Python ---
FROM python:3.12-slim AS base

# --- Устанавливаем рабочую директорию ---
WORKDIR /app

# --- Переменные окружения для Python ---
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# --- Устанавливаем зависимости системы ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# --- Устанавливаем зависимости Python ---
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# --- Копируем исходный код приложения ---
COPY ./src ./src

# --- Экспонируем порт ---
EXPOSE 8000

# --- Команда запуска приложения ---
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
