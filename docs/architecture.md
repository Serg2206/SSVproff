
# Архитектура проекта SSVproff

## Обзор

SSVproff — это монорепозиторий для управления файлами, автоматизации процессов, обеспечения безопасности и версионирования данных.

## Диаграмма C4: Контекст системы

```mermaid
C4Context
    title Контекст системы SSVproff

    Person(user, "Пользователь", "Администратор системы")
    
    System(ssvproff, "SSVproff", "Система управления файлами и автоматизации")
    
    System_Ext(b2, "Backblaze B2", "Облачное хранилище")
    System_Ext(github, "GitHub", "Версионирование кода")
    System_Ext(pages, "GitHub Pages", "Хостинг документации")
    
    Rel(user, ssvproff, "Использует", "HTTPS")
    Rel(ssvproff, b2, "Синхронизирует файлы", "rclone")
    Rel(ssvproff, github, "Хранит код", "git")
    Rel(pages, ssvproff, "Публикует документацию", "mkdocs")
```

## Диаграмма C4: Контейнеры

```mermaid
C4Container
    title Контейнеры SSVproff

    Person(user, "Пользователь")
    
    Container(web, "Web Frontend", "Next.js 14", "React интерфейс пользователя")
    Container(api, "API Backend", "FastAPI", "REST API для управления")
    Container(docs, "Documentation", "MkDocs", "Техническая документация")
    Container(flows, "Automation Flows", "Shell Scripts", "Скрипты автоматизации")
    
    ContainerDb(postgres, "Database", "PostgreSQL", "Хранение метаданных")
    ContainerDb(redis, "Cache", "Redis", "Кэширование")
    
    System_Ext(b2, "Backblaze B2", "Облачное хранилище")
    
    Rel(user, web, "Взаимодействует", "HTTPS")
    Rel(web, api, "Вызывает API", "JSON/HTTPS")
    Rel(api, postgres, "Читает/пишет", "SQL")
    Rel(api, redis, "Кэширует", "Redis Protocol")
    Rel(flows, b2, "Синхронизирует", "rclone")
    Rel(flows, api, "Триггерит", "HTTP")
```

## Компоненты

### 1. API Backend (`/api`)

**Технологии:**
- Python 3.11+
- FastAPI 0.115+
- SQLAlchemy 2.0 (ORM)
- PostgreSQL (база данных)
- Redis (кэширование)

**Ответственности:**
- REST API для управления файлами
- Аутентификация и авторизация
- Бизнес-логика
- Интеграция с внешними сервисами

**Структура:**
```
api/
├── app/
│   ├── main.py           # Точка входа
│   ├── api/              # API endpoints
│   ├── core/             # Конфигурация, безопасность
│   ├── models/           # SQLAlchemy модели
│   ├── schemas/          # Pydantic схемы
│   ├── services/         # Бизнес-логика
│   └── db/               # Database utilities
├── tests/                # Тесты
├── Dockerfile            # Production образ
└── requirements.txt      # Зависимости
```

### 2. Web Frontend (`/web`)

**Технологии:**
- Node.js 20+
- Next.js 14
- React 18
- TypeScript 5

**Ответственности:**
- Пользовательский интерфейс
- Server-side rendering
- API интеграция
- State management

**Структура:**
```
web/
├── src/
│   ├── app/              # Next.js App Router
│   ├── components/       # React компоненты
│   ├── lib/              # Утилиты
│   ├── hooks/            # Custom hooks
│   └── styles/           # CSS/Tailwind
├── public/               # Статические файлы
└── package.json          # Зависимости
```

### 3. Automation Flows (`/flows`)

**Технологии:**
- Shell scripts
- rclone
- DVC (Data Version Control)

**Ответственности:**
- Автоматическая синхронизация файлов
- Backup и restore
- Data versioning
- Scheduled tasks

### 4. Documentation (`/docs`)

**Технологии:**
- MkDocs
- Material for MkDocs
- mike (версионирование)

**Ответственности:**
- Техническая документация
- API документация
- Руководства пользователя
- ADR (Architecture Decision Records)

## Потоки данных

### Upload Flow

```mermaid
sequenceDiagram
    participant User
    participant Web
    participant API
    participant DB
    participant B2
    
    User->>Web: Загружает файл
    Web->>API: POST /api/files/upload
    API->>DB: Сохраняет метаданные
    API->>B2: Загружает файл (rclone)
    B2-->>API: Подтверждение
    API-->>Web: Успех
    Web-->>User: Отображает успех
```

### Sync Flow

```mermaid
sequenceDiagram
    participant Cron
    participant Flow
    participant B2
    participant API
    participant DB
    
    Cron->>Flow: Запуск по расписанию
    Flow->>B2: rclone sync
    B2-->>Flow: Список изменений
    Flow->>API: POST /api/sync/update
    API->>DB: Обновляет метаданные
    API-->>Flow: Подтверждение
```

## Безопасность

### Аутентификация и авторизация

- JWT токены для API
- OAuth 2.0 для сторонних интеграций
- Role-based access control (RBAC)

### Защита данных

- HTTPS everywhere
- Шифрование данных в покое (B2 encryption)
- Шифрование в transit (TLS 1.3)
- Secrets management через environment variables

### Security scanning

- Dependabot для обновления зависимостей
- CodeQL для статического анализа
- Trivy для сканирования уязвимостей
- pip-audit и npm audit

## Deployment

### Development

```bash
# Локальная разработка через Docker Compose
docker-compose up -d
```

### Production

- **API:** Контейнер на облачной платформе (Railway, Render, AWS)
- **Web:** Vercel или Netlify для Next.js
- **Docs:** GitHub Pages через GitHub Actions

## Мониторинг и логирование

### Логирование

- Структурированное логирование (structlog)
- Уровни: DEBUG, INFO, WARNING, ERROR
- Централизованный сбор логов

### Метрики

- Health checks для всех сервисов
- Performance metrics
- Error tracking

## Масштабирование

### Горизонтальное масштабирование

- API: stateless, легко масштабируется
- Web: edge functions и CDN
- Database: read replicas при необходимости

### Оптимизация производительности

- Redis кэширование
- Database indexing
- CDN для статических файлов
- Lazy loading для больших данных

## Связанные документы

- [ADR-0001: Выбор монорепо](adr/0001-monorepo-structure.md)
- [API Documentation](api/fastapi.md)
- [Deployment Guide](development/ci-cd.md)
