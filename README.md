# SSVproff

Минимальный старт: монорепо с документацией, автоматизацией и заготовками API/Web.

## Структура
- docs — MkDocs + Material, автодеплой на GitHub Pages
- api — FastAPI (заготовка)
- web — Next.js (заготовка, статический экспорт)
- data-meta — метаданные наборов
- flows — скрипты (rclone, dvc, ci)

## Быстрый старт
- Установить: Python 3.11+, Node LTS, rclone, dvc
- Документация локально: `make docs-serve`
- Загрузка медиа: `make upload-photos` / `make upload-videos`
- DVC push: `make push-data`

## Безопасность
- Включены Dependabot/CodeQL/Secret Scanning. Секреты хранить в GitHub Secrets.

## Локальный запуск

### API
```bash
cd api
uvicorn app.main:app --reload --port 8001
```

### Web
```bash
cd web
npm install
npm run dev
```

### Docs
```bash
make docs-serve  # http://localhost:8000
```
