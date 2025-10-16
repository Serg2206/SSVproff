
# Changelog

Все значимые изменения в проекте SSVproff будут документированы в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
и проект следует [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### ✨ Added
- GitHub Actions workflows: CI, docs-quality, security, pages-deploy
- Dependabot конфигурация для npm, pip, GitHub Actions
- Pre-commit hooks с husky и lint-staged
- Commitlint для conventional commits
- Линтеры и форматтеры: ESLint, Prettier, Ruff, Black, MyPy
- Docker конфигурация: Dockerfile для API, docker-compose.yml
- Улучшенный Makefile с множеством полезных команд
- Улучшенная конфигурация MkDocs с mike plugin
- ADR (Architecture Decision Records) шаблон и первая запись
- Документация архитектуры с Mermaid диаграммами
- GitHub templates: PR template, issue templates, CODEOWNERS
- SECURITY.md с процессом репортинга уязвимостей
- Requirements файлы для API: requirements.txt, requirements-dev.txt
- Обновлённый web/package.json с dev dependencies

### 🐛 Fixed
- Исправлены критические синтаксические ошибки в codeql.yml
- Исправлены синтаксические ошибки в release-drafter.yml

### 📝 Changed
- Полностью переработан Makefile для лучшей организации
- Улучшен mkdocs.yml с дополнительными плагинами и расширениями
- Обновлён api/pyproject.toml с полной конфигурацией линтеров

### 🔒 Security
- Добавлен security.yml workflow для Trivy и dependency review
- Добавлен .env.example для безопасного управления секретами

## [0.1.0] - 2025-10-16

### ✨ Added
- Начальная структура монорепозитория
- FastAPI backend (api/)
- Next.js frontend (web/)
- MkDocs документация (docs/)
- Скрипты автоматизации (flows/)
- Базовая конфигурация GitHub Actions

---

## Типы изменений

- `Added` для новой функциональности
- `Changed` для изменений существующей функциональности
- `Deprecated` для функциональности, которая скоро будет удалена
- `Removed` для удалённой функциональности
- `Fixed` для исправления багов
- `Security` для исправлений безопасности
