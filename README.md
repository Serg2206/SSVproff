Here's the result of running `cat -n` on /home/ubuntu/github_repos/SSVproff/README.md:
     1	Here's the result of running `cat -n` on /home/ubuntu/github_repos/SSVproff/README.md:
     2	     1  # 🚀 SSVproff
     3	     2  
     4	     3  [![CI](https://github.com/Serg2206/SSVproff/actions/workflows/ci.yml/badge.svg)](https://github.com/Serg2206/SSVproff/actions/workflows/ci.yml)
     5	     4  [![Security](https://github.com/Serg2206/SSVproff/actions/workflows/security.yml/badge.svg)](https://github.com/Serg2206/SSVproff/actions/workflows/security.yml)
     6	[![License: MIT](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/MIT_Logo_New.svg/1200px-MIT_Logo_New.svg.png)
     7	[![Python](https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Blue_Python_3.7_Shield_Badge.svg/1200px-Blue_Python_3.7_Shield_Badge.svg.png)
     8	[![Node](https://i.ytimg.com/vi/4cgpu9L2AE8/maxresdefault.jpg)
     9	     8  [![Node](https://upload.wikimedia.org/wikipedia/commons/3/31/Intel-Xeon-Badge-2024.jpg)
    10	     9  
    11	    10  > Монорепозиторий для управления файлами, автоматизации процессов, обеспечения безопасности и версионирования данных.
    12	    11  
    13	    12  ## 📚 Документация
    14	    13  
    15	    14  📖 **Полная документация доступна на:** [ssg2206.github.io/SSVproff](https://serg2206.github.io/SSVproff/)
    16	    15  
- 🔥 **Монорепо архитектура** - все компоненты в одном месте
- ⚡ **Современный стек** - FastAPI, Next.js 14, TypeScript
- 🔐 **Аутентификация** - JWT токены, защищённые роуты, управление пользователями
- 🔒 **Безопасность** - CodeQL, Trivy, Dependabot, Security scanning
- 🤖 **Автоматизация** - CI/CD с GitHub Actions, pre-commit hooks
- 📊 **Качество кода** - Линтеры, форматтеры, type checking
- 🐳 **Docker ready** - Production-ready контейнеры
- 📝 **Документация** - MkDocs с автоматическим деплоем
- 🔄 **Версионирование** - DVC для данных, mike для документации

## 🔐 Authentication System

Проект включает полнофункциональную систему аутентификации:

### Backend (FastAPI)
- ✅ JWT токены (access + refresh)
- ✅ Регистрация и авторизация пользователей
- ✅ Хеширование паролей (bcrypt)
- ✅ Защищённые endpoints
- ✅ Пример CRUD операций (Tasks)
- ✅ Полное тестовое покрытие

### Frontend (Next.js)
- ✅ React Context для состояния аутентификации
- ✅ Защищённые роуты
- ✅ Страницы Login/Register
- ✅ Dashboard с управлением задачами
- ✅ Профиль пользователя
- ✅ Типизированный API клиент

### Быстрый старт

```bash
# Backend
cd api
pip install -r requirements.txt
cp .env.example .env
python scripts/init_db.py  # Создаёт тестовых пользователей
uvicorn app.main:app --reload

# Frontend
cd web
npm install
cp .env.local.example .env.local
npm run dev
```

**Тестовые аккаунты:**
- Пользователь: `test@example.com` / `testpassword123`
- Админ: `admin@example.com` / `admin123`

📖 **Подробная документация:** [AUTHENTICATION_SETUP.md](AUTHENTICATION_SETUP.md)
    25	    24  - 📝 **Документация** - MkDocs с автоматическим деплоем
    26	    25  - 🔄 **Версионирование** - DVC для данных, mike для документации
    27	    26  
    28	    27  ## 🗂️ Структура проекта
    29	    28  
    30	    29  ```
    31	    30  SSVproff/
    32	    31  ├── 📁 api/              # FastAPI Backend (Python 3.11+)
    33	    32  │   ├── app/            # Код приложения
    34	    33  │   ├── tests/          # Тесты
    35	    34  │   └── Dockerfile      # Production образ
    36	    35  ├── 📁 web/              # Next.js Frontend (TypeScript)
    37	    36  │   ├── src/            # Исходный код
    38	    37  │   └── public/         # Статические файлы
    39	    38  ├── 📁 docs/             # MkDocs документация
    40	    39  │   ├── adr/            # Architecture Decision Records
    41	    40  │   └── architecture.md # Архитектура системы
    42	    41  ├── 📁 flows/            # Скрипты автоматизации
    43	    42  │   ├── rclone          # Синхронизация с облаком
    44	    43  │   └── dvc             # Версионирование данных
    45	    44  ├── 📁 data-meta/        # Метаданные и схемы
    46	    45  ├── 📁 .github/          # CI/CD конфигурации
    47	    46  │   └── workflows/      # GitHub Actions
    48	    47  ├── 🐳 docker-compose.yml # Локальная разработка
    49	    48  ├── 📝 Makefile          # Команды для разработки
    50	    49  └── 📦 package.json      # Monorepo конфигурация
    51	    50  ```
    52	    51  
    53	    52  ### Карта модулей
    54	    53  
    55	    54  | Модуль | Технологии | Описание | Порт |
    56	    55  |--------|-----------|----------|------|
    57	    56  | **API** | Python 3.11, FastAPI, PostgreSQL, Redis | REST API backend для управления файлами | 8001 |
    58	    57  | **Web** | Node 20, Next.js 14, React, TypeScript | Современный frontend интерфейс | 3000 |
    59	    58  | **Docs** | MkDocs, Material, mike | Версионированная документация | 8000 |
    60	    59  | **Flows** | Shell, rclone, DVC | Автоматизация и версионирование данных | - |
    61	    60  | **Data-Meta** | JSON, YAML | Схемы данных и метаданные | - |
    62	    61  
    63	    62  ## 🚀 Быстрый старт
    64	    63  
    65	    64  ### Требования
    66	    65  
    67	    66  - **Python** 3.11+
    68	    67  - **Node.js** 20+ 
    69	    68  - **Docker** и Docker Compose (опционально)
    70	    69  - **Make** (для удобства)
    71	    70  
    72	    71  ### Установка
    73	    72  
    74	    73  ```bash
    75	    74  # 1. Клонировать репозиторий
    76	    75  git clone https://github.com/Serg2206/SSVproff.git
    77	    76  cd SSVproff
    78	    77  
    79	    78  # 2. Bootstrap проекта (установка всех зависимостей)
    80	    79  make bootstrap
    81	    80  
    82	    81  # 3. Скопировать .env.example в .env и настроить
    83	    82  cp .env.example .env
    84	    83  ```
    85	    84  
    86	    85  ### Локальная разработка
    87	    86  
    88	    87  #### Вариант 1: С Docker Compose (рекомендуется)
    89	    88  
    90	    89  ```bash
    91	    90  # Запустить все сервисы
    92	    91  make dev
    93	    92  
    94	    93  # Или напрямую
    95	    94  docker-compose up -d
    96	    95  ```
    97	    96  
    98	    97  Сервисы будут доступны на:
    99	    98  - API: http://localhost:8001
   100	    99  - Web: http://localhost:3000
   101	   100  - PostgreSQL: localhost:5432
   102	   101  - Redis: localhost:6379
   103	   102  
   104	   103  #### Вариант 2: Без Docker
   105	   104  
   106	   105  ```bash
   107	   106  # Терминал 1: API
   108	   107  make dev-api
   109	   108  
   110	   109  # Терминал 2: Web
   111	   110  make dev-web
   112	   111  
   113	   112  # Терминал 3: Docs
   114	   113  make docs-serve
   115	   114  ```
   116	   115  
   117	   116  ## 🛠️ Основные команды
   118	   117  
   119	   118  ```bash
   120	   119  # Установка зависимостей
   121	   120  make install              # Установить все зависимости
   122	   121  make install-api          # Только API
   123	   122  make install-web          # Только Web
   124	   123  
   125	   124  # Разработка
   126	   125  make dev                  # Запустить все сервисы (Docker)
   127	   126  make dev-api              # Запустить только API
   128	   127  make dev-web              # Запустить только Web
   129	   128  
   130	   129  # Линтинг и форматирование
   131	   130  make lint                 # Проверить весь код
   132	   131  make format               # Отформатировать код
   133	   132  make lint-api             # Линтинг API
   134	   133  make lint-web             # Линтинг Web
   135	   134  
   136	   135  # Тестирование
   137	   136  make test                 # Запустить все тесты
   138	   137  make test-api             # Тесты API
   139	   138  make test-web             # Тесты Web
   140	   139  
   141	   140  # Сборка
   142	   141  make build                # Собрать все модули
   143	   142  make build-api            # Собрать API
   144	   143  make build-web            # Собрать Web
   145	   144  
   146	   145  # Документация
   147	   146  make docs-serve           # Запустить локальный сервер
   148	   147  make docs-build           # Собрать документацию
   149	   148  make docs-deploy          # Деплой на GitHub Pages
   150	   149  
   151	   150  # Docker
   152	   151  make docker-build         # Собрать образы
   153	   152  make docker-up            # Запустить контейнеры
   154	   153  make docker-down          # Остановить контейнеры
   155	   154  make docker-logs          # Показать логи
   156	   155  
   157	   156  # Данные и медиа
   158	   157  make upload-photos        # Загрузить фото в облако
   159	   158  make upload-videos        # Загрузить видео в облако
   160	   159  make push-data            # DVC push
   161	   160  make pull-data            # DVC pull
   162	   161  
   163	   162  # Очистка
   164	   163  make clean                # Очистить артефакты
   165	   164  make clean-all            # Полная очистка
   166	   165  
   167	   166  # Информация
   168	   167  make help                 # Показать все команды
   169	   168  make info                 # Информация о проекте
   170	   169  ```
   171	   170  
   172	   171  ## 🔐 Безопасность
   173	   172  
   174	   173  Проект включает множество мер безопасности:
   175	   174  
   176	   175  - ✅ **CodeQL** - статический анализ кода
   177	   176  - ✅ **Trivy** - сканирование уязвимостей
   178	   177  - ✅ **Dependabot** - автоматические обновления зависимостей
   179	   178  - ✅ **Secret Scanning** - обнаружение секретов в коде
   180	   179  - ✅ **pip-audit / npm audit** - проверка зависимостей
   181	   180  - ✅ **CODEOWNERS** - обязательные code review
   182	   181  
   183	   182  Если вы обнаружили уязвимость, пожалуйста, следуйте нашей [Политике безопасности](SECURITY.md).
   184	   183  
   185	   184  ## 🤝 Contributing
   186	   185  
   187	   186  Мы приветствуем вклад в проект! Пожалуйста:
   188	   187  
   189	   188  1. Fork репозитория
   190	   189  2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
   191	   190  3. Commit изменения (`git commit -m 'feat: add amazing feature'`)
   192	   191  4. Push в branch (`git push origin feature/amazing-feature`)
   193	   192  5. Откройте Pull Request
   194	   193  
   195	   194  Следуйте [Conventional Commits](https://www.conventionalcommits.org/) для commit messages.
   196	   195  
   197	   196  ## 📄 Лицензия
   198	   197  
   199	   198  Этот проект лицензирован под [MIT License](LICENSE).
   200	   199  
   201	   200  ## 🙏 Благодарности
   202	   201  
   203	   202  - [FastAPI](https://fastapi.tiangolo.com/) за потрясающий фреймворк
   204	   203  - [Next.js](https://nextjs.org/) за React фреймворк
   205	   204  - [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) за красивую документацию
   206	   205  
   207	   206  ---
   208	   207  
   209	   208  <div align="center">
   210	   209    Made with ❤️ by <a href="https://github.com/Serg2206">Serg2206</a>
   211	   210  </div>
   212	   211  