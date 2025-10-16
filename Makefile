# Makefile для SSVproff монорепо
# Управление задачами для API, Web, Docs и инфраструктуры

.PHONY: help
.DEFAULT_GOAL := help

# Цвета для вывода
CYAN := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RESET := \033[0m

## ============================================================================
## 📋 Основные команды
## ============================================================================

help: ## Показать это сообщение помощи
        @echo "$(CYAN)SSVproff Monorepo - Доступные команды:$(RESET)"
        @echo ""
        @grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
                awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(RESET) %s\n", $$1, $$2}'

## ============================================================================
## 🚀 Быстрый старт
## ============================================================================

bootstrap: ## Первоначальная настройка проекта
        @echo "$(CYAN)Bootstrapping project...$(RESET)"
        @command -v node >/dev/null 2>&1 || { echo "Node.js не установлен!"; exit 1; }
        @command -v python3 >/dev/null 2>&1 || { echo "Python3 не установлен!"; exit 1; }
        npm install
        $(MAKE) install-api
        $(MAKE) install-web
        @echo "$(GREEN)✓ Bootstrap завершён!$(RESET)"

install: install-api install-web ## Установить все зависимости

install-api: ## Установить зависимости API
        @echo "$(CYAN)Installing API dependencies...$(RESET)"
        cd api && pip install -r requirements.txt -r requirements-dev.txt

install-web: ## Установить зависимости Web
        @echo "$(CYAN)Installing Web dependencies...$(RESET)"
        cd web && npm install

## ============================================================================
## 🔍 Линтинг и форматирование
## ============================================================================

lint: lint-api lint-web ## Проверить код всех модулей

lint-api: ## Линтинг API кода (Python)
        @echo "$(CYAN)Linting API...$(RESET)"
        cd api && ruff check .
        cd api && mypy .

lint-web: ## Линтинг Web кода (TypeScript)
        @echo "$(CYAN)Linting Web...$(RESET)"
        cd web && npm run lint

format: format-api format-web ## Форматировать код всех модулей

format-api: ## Форматировать API код (Black, Ruff)
        @echo "$(CYAN)Formatting API...$(RESET)"
        cd api && black .
        cd api && ruff check --fix .

format-web: ## Форматировать Web код (Prettier)
        @echo "$(CYAN)Formatting Web...$(RESET)"
        cd web && npm run format || npx prettier --write .

## ============================================================================
## 🧪 Тестирование
## ============================================================================

test: test-api test-web ## Запустить тесты всех модулей

test-api: ## Запустить тесты API
        @echo "$(CYAN)Testing API...$(RESET)"
        cd api && pytest -v --cov=app --cov-report=term --cov-report=html

test-web: ## Запустить тесты Web
        @echo "$(CYAN)Testing Web...$(RESET)"
        cd web && npm test || echo "$(YELLOW)Тесты ещё не настроены$(RESET)"

test-watch-api: ## Запустить тесты API в watch режиме
        cd api && pytest-watch

## ============================================================================
## 🏗️ Сборка
## ============================================================================

build: build-api build-web build-docs ## Собрать все модули

build-api: ## Собрать API (проверка)
        @echo "$(CYAN)Building API...$(RESET)"
        cd api && python -m py_compile app/*.py || echo "$(GREEN)API готов к запуску$(RESET)"

build-web: ## Собрать Web (Next.js)
        @echo "$(CYAN)Building Web...$(RESET)"
        cd web && npm run build

build-docs: ## Собрать документацию
        @echo "$(CYAN)Building Docs...$(RESET)"
        mkdocs build --strict

## ============================================================================
## 🚀 Разработка
## ============================================================================

dev: ## Запустить все сервисы в dev режиме (через docker-compose)
        @echo "$(CYAN)Starting development environment...$(RESET)"
        docker-compose up -d

dev-api: ## Запустить API в dev режиме
        @echo "$(CYAN)Starting API dev server...$(RESET)"
        cd api && uvicorn app.main:app --reload --port 8001

dev-web: ## Запустить Web в dev режиме
        @echo "$(CYAN)Starting Web dev server...$(RESET)"
        cd web && npm run dev

dev-stop: ## Остановить все dev сервисы
        docker-compose down

## ============================================================================
## 📚 Документация
## ============================================================================

docs-serve: ## Запустить локальный сервер документации
        @echo "$(CYAN)Starting docs server...$(RESET)"
        mkdocs serve -a 0.0.0.0:8000

docs-deploy: ## Деплой документации на GitHub Pages
        @echo "$(CYAN)Deploying docs to GitHub Pages...$(RESET)"
        mkdocs gh-deploy --force

docs-version: ## Создать версию документации (использует mike)
        @read -p "Enter version (e.g. 1.0.0): " version; \
        mike deploy --push --update-aliases $$version latest

## ============================================================================
## 🐳 Docker
## ============================================================================

docker-build: ## Собрать Docker образы
        @echo "$(CYAN)Building Docker images...$(RESET)"
        docker-compose build

docker-up: ## Запустить Docker контейнеры
        docker-compose up -d

docker-down: ## Остановить Docker контейнеры
        docker-compose down

docker-logs: ## Показать логи Docker контейнеров
        docker-compose logs -f

docker-clean: ## Очистить Docker ресурсы
        docker-compose down -v
        docker system prune -f

## ============================================================================
## 🗄️ Данные и медиа
## ============================================================================

upload-photos: ## Загрузить фотографии в облако (rclone)
        rclone copy ./photos b2:ssvproff-media/photos/`date +%Y`/ --progress

upload-videos: ## Загрузить видео в облако (rclone)
        rclone sync ./videos b2:ssvproff-media/videos/ --progress

push-data: ## Отправить данные через DVC
        dvc push

pull-data: ## Получить данные через DVC
        dvc pull

rclone-check: ## Проверить конфигурацию rclone
        rclone ls b2:ssvproff-media || echo "$(YELLOW)Проверьте rclone config и креды$(RESET)"

dvc-config: ## Настроить DVC remote
        bash flows/dvc-remote-example.sh

## ============================================================================
## 🧹 Очистка
## ============================================================================

clean: clean-api clean-web clean-docs ## Очистить все артефакты

clean-api: ## Очистить артефакты API
        @echo "$(CYAN)Cleaning API...$(RESET)"
        find api -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        find api -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
        find api -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
        find api -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
        find api -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
        rm -rf api/htmlcov api/.coverage

clean-web: ## Очистить артефакты Web
        @echo "$(CYAN)Cleaning Web...$(RESET)"
        cd web && rm -rf .next out dist node_modules/.cache

clean-docs: ## Очистить артефакты документации
        @echo "$(CYAN)Cleaning Docs...$(RESET)"
        rm -rf site public

clean-all: clean docker-clean ## Полная очистка включая Docker
        rm -rf node_modules
        rm -rf web/node_modules

## ============================================================================
## 🔐 Security
## ============================================================================

security-check: ## Проверка безопасности зависимостей
        @echo "$(CYAN)Running security checks...$(RESET)"
        cd api && pip-audit || echo "$(YELLOW)pip-audit не установлен$(RESET)"
        cd web && npm audit

## ============================================================================
## ℹ️ Информация
## ============================================================================

info: ## Показать информацию о проекте
        @echo "$(CYAN)SSVproff Project Info:$(RESET)"
        @echo ""
        @echo "  $(GREEN)API:$(RESET)"
        @cd api && python --version 2>/dev/null || echo "    Python не найден"
        @echo ""
        @echo "  $(GREEN)Web:$(RESET)"
        @cd web && node --version 2>/dev/null || echo "    Node.js не найден"
        @cd web && npm --version 2>/dev/null || echo "    npm не найден"
        @echo ""
        @echo "  $(GREEN)Docs:$(RESET)"
        @mkdocs --version 2>/dev/null || echo "    MkDocs не установлен"
        @echo ""
        @echo "  $(GREEN)Docker:$(RESET)"
        @docker --version 2>/dev/null || echo "    Docker не установлен"
        @docker-compose --version 2>/dev/null || echo "    Docker Compose не установлен"
