
# Contributing to SSVproff

Спасибо за интерес к проекту SSVproff! Это руководство поможет вам начать разработку.

## 📋 Оглавление

- [Code of Conduct](#code-of-conduct)
- [Начало работы](#начало-работы)
- [Структура проекта](#структура-проекта)
- [Стандарты разработки](#стандарты-разработки)
- [Процесс Pull Request](#процесс-pull-request)
- [Соглашения о коммитах](#соглашения-о-коммитах)
- [Тестирование](#тестирование)
- [Документация](#документация)

## Code of Conduct

Мы придерживаемся стандартного [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). Пожалуйста, будьте вежливы и уважительны ко всем участникам.

## 🚀 Начало работы

### Требования

- **Python**: 3.11+ (используйте pyenv для управления версиями)
- **Node.js**: 20.11+ (используйте nvm для управления версиями)
- **Git**: 2.30+
- **Make**: для запуска команд из Makefile

### Первоначальная настройка

1. **Форк и клонирование репозитория**
   ```bash
   git clone https://github.com/YOUR_USERNAME/SSVproff.git
   cd SSVproff
   ```

2. **Настройка окружения для API (Python/FastAPI)**
   ```bash
   cd api
   
   # Создайте виртуальное окружение
   python -m venv .venv
   source .venv/bin/activate  # На Windows: .venv\Scripts\activate
   
   # Установите зависимости
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   
   # Скопируйте .env.example и настройте переменные окружения
   cp .env.example .env
   
   cd ..
   ```

3. **Настройка окружения для Web (Next.js)**
   ```bash
   cd web
   
   # Установите зависимости
   npm ci
   
   # Скопируйте .env.example и настройте переменные окружения
   cp .env.example .env.local
   
   cd ..
   ```

4. **Установка pre-commit hooks**
   ```bash
   pip install pre-commit
   pre-commit install
   pre-commit install --hook-type commit-msg
   ```

5. **Проверка установки**
   ```bash
   # Запустите тесты
   make test
   
   # Запустите линтеры
   make lint
   
   # Запустите форматирование
   make format
   ```

### Использование Docker (альтернатива)

```bash
# Сборка и запуск всех сервисов
docker-compose up --build

# API будет доступен на http://localhost:8001
# Web будет доступен на http://localhost:3000
```

## 📁 Структура проекта

```
SSVproff/
├── api/                    # Backend (Python/FastAPI)
│   ├── app/                # Приложение
│   │   ├── api/v1/         # API endpoints v1
│   │   ├── core/           # Конфигурация, безопасность
│   │   ├── models/         # Модели данных
│   │   ├── schemas/        # Pydantic схемы
│   │   └── services/       # Бизнес-логика
│   ├── tests/              # Тесты
│   └── pyproject.toml      # Конфигурация проекта
├── web/                    # Frontend (Next.js/React)
│   ├── src/
│   │   ├── app/            # Next.js App Router
│   │   ├── components/     # React компоненты
│   │   ├── lib/            # Утилиты
│   │   └── types/          # TypeScript типы
│   └── __tests__/          # Тесты
├── docs/                   # MkDocs документация
├── flows/                  # Скрипты автоматизации
├── .github/                # GitHub Actions workflows
└── Makefile                # Команды для разработки
```

## 🎨 Стандарты разработки

### Python (API)

#### Стиль кода

- **Форматирование**: Black (длина строки: 100)
- **Линтинг**: Ruff
- **Сортировка импортов**: isort (профиль: black)
- **Проверка типов**: MyPy (basic mode)

#### Именование

```python
# Классы: PascalCase
class UserService:
    pass

# Функции и переменные: snake_case
def get_user_by_id(user_id: int) -> User:
    pass

# Константы: UPPER_SNAKE_CASE
MAX_RETRY_COUNT = 3

# Приватные методы: _leading_underscore
def _internal_method(self):
    pass
```

#### Type Hints

```python
from typing import Optional, List, Dict

# Всегда используйте type hints для функций
def process_data(items: List[Dict[str, str]], limit: Optional[int] = None) -> bool:
    """Process data with optional limit."""
    return True

# Используйте современный синтаксис (Python 3.11+)
def modern_types(items: list[dict[str, str]]) -> bool:
    return True
```

#### Docstrings

```python
def complex_function(param1: str, param2: int) -> dict:
    """
    Brief description of the function.

    Detailed description with multiple lines if needed.
    Explain what the function does, any side effects, etc.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When param2 is negative
        HTTPException: When API call fails

    Example:
        >>> result = complex_function("test", 42)
        >>> print(result)
        {'status': 'success'}
    """
    if param2 < 0:
        raise ValueError("param2 must be non-negative")
    return {"status": "success"}
```

### TypeScript/JavaScript (Web)

#### Стиль кода

- **Форматирование**: Prettier
- **Линтинг**: ESLint (Next.js config + TypeScript)
- **Проверка типов**: TypeScript (strict mode)

#### Именование

```typescript
// Интерфейсы и типы: PascalCase
interface UserData {
  id: number;
  name: string;
}

// Компоненты: PascalCase
function UserCard({ user }: { user: UserData }) {
  return <div>{user.name}</div>;
}

// Функции и переменные: camelCase
const getUserById = (userId: number): UserData | null => {
  return null;
};

// Константы: UPPER_SNAKE_CASE
const MAX_ITEMS_PER_PAGE = 20;

// Приватные свойства: #prefix (class) или _prefix (interfaces)
class Service {
  #privateField: string;
}
```

#### TypeScript Best Practices

```typescript
// Избегайте any - используйте unknown или конкретные типы
// ❌ Bad
function process(data: any) {
  return data.value;
}

// ✅ Good
function process(data: unknown) {
  if (typeof data === "object" && data !== null && "value" in data) {
    return data.value;
  }
  throw new Error("Invalid data");
}

// Используйте readonly где возможно
interface Config {
  readonly apiUrl: string;
  readonly timeout: number;
}

// Используйте discriminated unions для type-safe состояний
type Result<T> =
  | { status: "success"; data: T }
  | { status: "error"; error: string }
  | { status: "loading" };
```

#### React Best Practices

```typescript
// Используйте функциональные компоненты с hooks
import { useState, useEffect } from "react";

function DataFetcher() {
  const [data, setData] = useState<Data | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData().then((result) => {
      setData(result);
      setLoading(false);
    });
  }, []);

  if (loading) return <div>Loading...</div>;
  return <div>{data?.name}</div>;
}

// Извлекайте бизнес-логику в custom hooks
function useUserData(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  // ... логика
  return { user, loading, error };
}
```

### Общие правила

#### Комментарии

```python
# ❌ Плохо: очевидный комментарий
x = x + 1  # Increment x

# ✅ Хорошо: объясняет "почему", а не "что"
# User requested feature #123: reset counter after midnight
x = x + 1

# ✅ Хорошо: предупреждение о сложном коде
# HACK: Workaround for upstream bug in library v1.2.3
# TODO: Remove when upgrading to v1.3.0
```

#### Error Handling

```python
# Python
from fastapi import HTTPException

# Используйте специфичные исключения
try:
    user = get_user(user_id)
except UserNotFoundError:
    raise HTTPException(status_code=404, detail="User not found")
except DatabaseError as e:
    logger.error(f"Database error: {e}")
    raise HTTPException(status_code=500, detail="Internal server error")
```

```typescript
// TypeScript
// Используйте Result/Option типы вместо try-catch где возможно
function parseJson(text: string): Result<unknown, Error> {
  try {
    return { ok: true, value: JSON.parse(text) };
  } catch (error) {
    return { ok: false, error: error as Error };
  }
}
```

## 🔄 Процесс Pull Request

### Перед созданием PR

1. **Обновите вашу ветку**
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-feature-branch
   git rebase main
   ```

2. **Запустите проверки локально**
   ```bash
   make lint        # Проверка стиля кода
   make test        # Запуск тестов
   make format      # Форматирование кода
   ```

3. **Убедитесь, что тесты проходят**
   ```bash
   # API
   cd api && pytest --cov=app --cov-report=term
   
   # Web
   cd web && npm test -- --coverage
   ```

### Создание PR

1. **Создайте ветку с описательным именем**
   ```bash
   git checkout -b feature/add-user-authentication
   git checkout -b fix/resolve-login-error
   git checkout -b docs/update-api-guide
   ```

2. **Напишите качественное описание PR**

   ```markdown
   ## Описание
   Краткое описание изменений и их мотивация.

   ## Тип изменения
   - [ ] Bug fix (исправление ошибки)
   - [x] New feature (новая функциональность)
   - [ ] Breaking change (изменение, нарушающее обратную совместимость)
   - [ ] Documentation update (обновление документации)

   ## Как протестировано
   Описание того, как вы протестировали изменения.

   ## Чеклист
   - [x] Код следует стандартам стиля проекта
   - [x] Я провел самопроверку кода
   - [x] Я прокомментировал код в сложных местах
   - [x] Я обновил документацию
   - [x] Мои изменения не создают новых предупреждений
   - [x] Я добавил тесты, покрывающие мои изменения
   - [x] Все новые и существующие unit-тесты проходят
   ```

3. **Свяжите PR с issue**
   - Используйте keywords: `Closes #123`, `Fixes #456`, `Resolves #789`

### Code Review

- **Отвечайте на комментарии** конструктивно
- **Не принимайте критику лично** - это про код, не про вас
- **Задавайте вопросы** если что-то неясно
- **Обновляйте PR** на основе feedback

### После merge

```bash
git checkout main
git pull upstream main
git branch -d your-feature-branch  # Удалите локальную ветку
```

## 📝 Соглашения о коммитах

Мы используем [Conventional Commits](https://www.conventionalcommits.org/):

### Формат

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: Новая функциональность
- **fix**: Исправление ошибки
- **docs**: Изменения в документации
- **style**: Форматирование, пропущенные точки с запятой и т.д.
- **refactor**: Рефакторинг кода
- **perf**: Улучшение производительности
- **test**: Добавление или исправление тестов
- **chore**: Обновление зависимостей, конфигурации и т.д.
- **ci**: Изменения в CI/CD
- **build**: Изменения в системе сборки

### Scopes

- **api**: Изменения в API модуле
- **web**: Изменения в Web модуле
- **docs**: Изменения в документации
- **ci**: Изменения в CI/CD
- **deps**: Обновление зависимостей

### Примеры

```bash
# Новая функция
git commit -m "feat(api): add user authentication endpoint"

# Исправление ошибки
git commit -m "fix(web): resolve login form validation issue"

# Breaking change
git commit -m "feat(api)!: change API response format

BREAKING CHANGE: API now returns data in camelCase instead of snake_case"

# С телом и футером
git commit -m "fix(api): prevent race condition in user creation

Added mutex lock to prevent concurrent user creation with same email.

Fixes #123"
```

### Правила

- Используйте **imperative mood** в subject ("add" не "added" или "adds")
- Не заканчивайте subject точкой
- Subject ≤ 72 символов
- Разделяйте subject и body пустой строкой
- Body и footer опциональны для простых изменений

## 🧪 Тестирование

### Python (API)

#### Структура тестов

```
api/tests/
├── __init__.py
├── conftest.py              # Pytest fixtures
├── test_main.py             # Основные тесты
├── api/
│   └── v1/
│       ├── test_users.py    # Тесты users endpoint
│       └── test_auth.py     # Тесты auth endpoint
└── services/
    └── test_user_service.py # Тесты сервисов
```

#### Написание тестов

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_user():
    return {"email": "test@example.com", "password": "testpass123"}

def test_create_user(client, test_user):
    """Test user creation endpoint."""
    response = client.post("/api/v1/users", json=test_user)
    assert response.status_code == 201
    assert response.json()["email"] == test_user["email"]

@pytest.mark.asyncio
async def test_async_function():
    """Test async functions."""
    result = await some_async_function()
    assert result is not None
```

#### Запуск тестов

```bash
# Все тесты
pytest

# С покрытием
pytest --cov=app --cov-report=html

# Конкретный файл
pytest tests/api/v1/test_users.py

# С отладкой
pytest -v -s

# Только failed тесты
pytest --lf
```

### TypeScript (Web)

#### Структура тестов

```
web/__tests__/
├── components/
│   └── UserCard.test.tsx
├── lib/
│   └── utils.test.ts
└── integration/
    └── auth-flow.test.tsx
```

#### Unit тесты

```typescript
// __tests__/lib/utils.test.ts
import { formatDate } from "@/lib/utils";

describe("formatDate", () => {
  it("formats date correctly", () => {
    const date = new Date("2024-01-15");
    expect(formatDate(date)).toBe("Jan 15, 2024");
  });

  it("handles invalid dates", () => {
    expect(() => formatDate(null as any)).toThrow();
  });
});
```

#### Component тесты

```typescript
// __tests__/components/UserCard.test.tsx
import { render, screen } from "@testing-library/react";
import { UserCard } from "@/components/UserCard";

describe("UserCard", () => {
  const mockUser = { id: 1, name: "John Doe", email: "john@example.com" };

  it("renders user information", () => {
    render(<UserCard user={mockUser} />);
    expect(screen.getByText("John Doe")).toBeInTheDocument();
    expect(screen.getByText("john@example.com")).toBeInTheDocument();
  });

  it("handles click event", async () => {
    const handleClick = jest.fn();
    render(<UserCard user={mockUser} onClick={handleClick} />);

    const card = screen.getByRole("button");
    await userEvent.click(card);

    expect(handleClick).toHaveBeenCalledWith(mockUser);
  });
});
```

#### Запуск тестов

```bash
# Все тесты
npm test

# Watch mode
npm run test:watch

# С покрытием
npm run test:coverage

# Update snapshots
npm test -- -u
```

### Требования к покрытию

- **API**: минимум 80% coverage
- **Web**: минимум 70% coverage
- **Critical paths**: 100% coverage

## 📚 Документация

### API Documentation

- Используйте **docstrings** для всех публичных функций/классов
- FastAPI автоматически генерирует OpenAPI документацию
- Добавляйте примеры в schemas:

```python
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    email: str = Field(..., example="user@example.com")
    password: str = Field(..., min_length=8, example="securepass123")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepass123"
            }
        }
```

### MkDocs Documentation

- Документация в `docs/` директории
- Используйте Markdown
- Запуск локально: `mkdocs serve`
- Структурируйте документацию логически

### README Updates

- Обновляйте README при добавлении новых функций
- Держите примеры актуальными
- Добавляйте скриншоты для UI изменений

## 🐛 Reporting Bugs

### Перед созданием issue

1. Проверьте [существующие issues](https://github.com/Serg2206/SSVproff/issues)
2. Убедитесь, что вы используете последнюю версию
3. Соберите информацию о баге

### Создание Bug Report

Используйте [шаблон bug report](.github/ISSUE_TEMPLATE/bug_report.md):

```markdown
**Описание бага**
Краткое описание проблемы.

**Шаги для воспроизведения**
1. Перейти на '...'
2. Кликнуть на '...'
3. Увидеть ошибку

**Ожидаемое поведение**
Описание того, что должно было произойти.

**Скриншоты**
Если применимо, добавьте скриншоты.

**Окружение:**
 - OS: [e.g. Ubuntu 22.04]
 - Browser: [e.g. Chrome 120]
 - Python: [e.g. 3.11.7]
 - Node: [e.g. 20.11.0]

**Дополнительный контекст**
Любая другая полезная информация.
```

## 💡 Feature Requests

Используйте [шаблон feature request](.github/ISSUE_TEMPLATE/feature_request.md):

- Опишите проблему, которую решает ваша фича
- Предложите решение
- Рассмотрите альтернативы
- Добавьте mockups/примеры если возможно

## 🙏 Вопросы?

- **GitHub Discussions**: для общих вопросов
- **Issues**: для багов и feature requests
- **Email**: для security вопросов (см. SECURITY.md)

---

Спасибо за ваш вклад в SSVproff! 🎉
