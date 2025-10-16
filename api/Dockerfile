
# Multi-stage Dockerfile для FastAPI приложения
# Использует alpine для минимизации размера образа

# Стадия 1: Сборка зависимостей
FROM python:3.11-alpine AS builder

# Установка build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev

# Создание виртуального окружения
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Копирование файлов зависимостей
WORKDIR /app
COPY requirements.txt requirements-dev.txt* ./

# Установка зависимостей
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Стадия 2: Production образ
FROM python:3.11-alpine

# Метаданные
LABEL maintainer="SSVproff Team"
LABEL description="FastAPI backend for SSVproff"

# Установка runtime dependencies
RUN apk add --no-cache \
    tini \
    curl

# Создание non-root пользователя
RUN addgroup -g 10001 appuser && \
    adduser -D -u 10001 -G appuser appuser

# Копирование виртуального окружения из builder
COPY --from=builder /opt/venv /opt/venv

# Установка рабочей директории
WORKDIR /app

# Копирование кода приложения
COPY --chown=appuser:appuser . .

# Переключение на non-root пользователя
USER appuser

# Установка путей
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# Порт приложения
EXPOSE 8001

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Использование tini для корректной обработки сигналов
ENTRYPOINT ["/sbin/tini", "--"]

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
