Here's the result of running `cat -n` on /home/ubuntu/github_repos/SSVproff/README.md:
     1	# 🚀 SSVproff
     2	
     3	[![CI](https://github.com/Serg2206/SSVproff/actions/workflows/ci.yml/badge.svg)](https://github.com/Serg2206/SSVproff/actions/workflows/ci.yml)
     4	[![Security](https://github.com/Serg2206/SSVproff/actions/workflows/security.yml/badge.svg)](https://github.com/Serg2206/SSVproff/actions/workflows/security.yml)
[![License: MIT](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/MIT_Logo_New.svg/1200px-MIT_Logo_New.svg.png)
[![Python](https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Blue_Python_3.7_Shield_Badge.svg/1200px-Blue_Python_3.7_Shield_Badge.svg.png)
[![Node](https://i.ytimg.com/vi/4cgpu9L2AE8/maxresdefault.jpg)
     8	[![Node](https://upload.wikimedia.org/wikipedia/commons/3/31/Intel-Xeon-Badge-2024.jpg)
     9	
    10	> Монорепозиторий для управления файлами, автоматизации процессов, обеспечения безопасности и версионирования данных.
    11	
    12	## 📚 Документация
    13	
    14	📖 **Полная документация доступна на:** [ssg2206.github.io/SSVproff](https://serg2206.github.io/SSVproff/)
    15	
    16	## ✨ Возможности
    17	
    18	- 🔥 **Монорепо архитектура** - все компоненты в одном месте
    19	- ⚡ **Современный стек** - FastAPI, Next.js 14, TypeScript
    20	- 🔒 **Безопасность** - CodeQL, Trivy, Dependabot, Security scanning
    21	- 🤖 **Автоматизация** - CI/CD с GitHub Actions, pre-commit hooks
    22	- 📊 **Качество кода** - Линтеры, форматтеры, type checking
    23	- 🐳 **Docker ready** - Production-ready контейнеры
    24	- 📝 **Документация** - MkDocs с автоматическим деплоем
    25	- 🔄 **Версионирование** - DVC для данных, mike для документации
    26	
    27	## 🗂️ Структура проекта
    28	
    29	```
    30	SSVproff/
    31	├── 📁 api/              # FastAPI Backend (Python 3.11+)
    32	│   ├── app/            # Код приложения
    33	│   ├── tests/          # Тесты
    34	│   └── Dockerfile      # Production образ
    35	├── 📁 web/              # Next.js Frontend (TypeScript)
    36	│   ├── src/            # Исходный код
    37	│   └── public/         # Статические файлы
    38	├── 📁 docs/             # MkDocs документация
    39	│   ├── adr/            # Architecture Decision Records
    40	│   └── architecture.md # Архитектура системы
    41	├── 📁 flows/            # Скрипты автоматизации
    42	│   ├── rclone          # Синхронизация с облаком
    43	│   └── dvc             # Версионирование данных
    44	├── 📁 data-meta/        # Метаданные и схемы
    45	├── 📁 .github/          # CI/CD конфигурации
    46	│   └── workflows/      # GitHub Actions
    47	├── 🐳 docker-compose.yml # Локальная разработка
    48	├── 📝 Makefile          # Команды для разработки
    49	└── 📦 package.json      # Monorepo конфигурация
    50	```
    51	
    52	### Карта модулей
    53	
    54	| Модуль | Технологии | Описание | Порт |
    55	|--------|-----------|----------|------|
    56	| **API** | Python 3.11, FastAPI, PostgreSQL, Redis | REST API backend для управления файлами | 8001 |
    57	| **Web** | Node 20, Next.js 14, React, TypeScript | Современный frontend интерфейс | 3000 |
    58	| **Docs** | MkDocs, Material, mike | Версионированная документация | 8000 |
    59	| **Flows** | Shell, rclone, DVC | Автоматизация и версионирование данных | - |
    60	| **Data-Meta** | JSON, YAML | Схемы данных и метаданные | - |
    61	
    62	## 🚀 Быстрый старт
    63	
    64	### Требования
    65	
    66	- **Python** 3.11+
    67	- **Node.js** 20+ 
    68	- **Docker** и Docker Compose (опционально)
    69	- **Make** (для удобства)
    70	
    71	### Установка
    72	
    73	```bash
    74	# 1. Клонировать репозиторий
    75	git clone https://github.com/Serg2206/SSVproff.git
    76	cd SSVproff
    77	
    78	# 2. Bootstrap проекта (установка всех зависимостей)
    79	make bootstrap
    80	
    81	# 3. Скопировать .env.example в .env и настроить
    82	cp .env.example .env
    83	```
    84	
    85	### Локальная разработка
    86	
    87	#### Вариант 1: С Docker Compose (рекомендуется)
    88	
    89	```bash
    90	# Запустить все сервисы
    91	make dev
    92	
    93	# Или напрямую
    94	docker-compose up -d
    95	```
    96	
    97	Сервисы будут доступны на:
    98	- API: http://localhost:8001
    99	- Web: http://localhost:3000
   100	- PostgreSQL: localhost:5432
   101	- Redis: localhost:6379
   102	
   103	#### Вариант 2: Без Docker
   104	
   105	```bash
   106	# Терминал 1: API
   107	make dev-api
   108	
   109	# Терминал 2: Web
   110	make dev-web
   111	
   112	# Терминал 3: Docs
   113	make docs-serve
   114	```
   115	
   116	## 🛠️ Основные команды
   117	
   118	```bash
   119	# Установка зависимостей
   120	make install              # Установить все зависимости
   121	make install-api          # Только API
   122	make install-web          # Только Web
   123	
   124	# Разработка
   125	make dev                  # Запустить все сервисы (Docker)
   126	make dev-api              # Запустить только API
   127	make dev-web              # Запустить только Web
   128	
   129	# Линтинг и форматирование
   130	make lint                 # Проверить весь код
   131	make format               # Отформатировать код
   132	make lint-api             # Линтинг API
   133	make lint-web             # Линтинг Web
   134	
   135	# Тестирование
   136	make test                 # Запустить все тесты
   137	make test-api             # Тесты API
   138	make test-web             # Тесты Web
   139	
   140	# Сборка
   141	make build                # Собрать все модули
   142	make build-api            # Собрать API
   143	make build-web            # Собрать Web
   144	
   145	# Документация
   146	make docs-serve           # Запустить локальный сервер
   147	make docs-build           # Собрать документацию
   148	make docs-deploy          # Деплой на GitHub Pages
   149	
   150	# Docker
   151	make docker-build         # Собрать образы
   152	make docker-up            # Запустить контейнеры
   153	make docker-down          # Остановить контейнеры
   154	make docker-logs          # Показать логи
   155	
   156	# Данные и медиа
   157	make upload-photos        # Загрузить фото в облако
   158	make upload-videos        # Загрузить видео в облако
   159	make push-data            # DVC push
   160	make pull-data            # DVC pull
   161	
   162	# Очистка
   163	make clean                # Очистить артефакты
   164	make clean-all            # Полная очистка
   165	
   166	# Информация
   167	make help                 # Показать все команды
   168	make info                 # Информация о проекте
   169	```
   170	
   171	## 🔐 Безопасность
   172	
   173	Проект включает множество мер безопасности:
   174	
   175	- ✅ **CodeQL** - статический анализ кода
   176	- ✅ **Trivy** - сканирование уязвимостей
   177	- ✅ **Dependabot** - автоматические обновления зависимостей
   178	- ✅ **Secret Scanning** - обнаружение секретов в коде
   179	- ✅ **pip-audit / npm audit** - проверка зависимостей
   180	- ✅ **CODEOWNERS** - обязательные code review
   181	
   182	Если вы обнаружили уязвимость, пожалуйста, следуйте нашей [Политике безопасности](SECURITY.md).
   183	
   184	## 🤝 Contributing
   185	
   186	Мы приветствуем вклад в проект! Пожалуйста:
   187	
   188	1. Fork репозитория
   189	2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
   190	3. Commit изменения (`git commit -m 'feat: add amazing feature'`)
   191	4. Push в branch (`git push origin feature/amazing-feature`)
   192	5. Откройте Pull Request
   193	
   194	Следуйте [Conventional Commits](https://www.conventionalcommits.org/) для commit messages.
   195	
   196	## 📄 Лицензия
   197	
   198	Этот проект лицензирован под [MIT License](LICENSE).
   199	
   200	## 🙏 Благодарности
   201	
   202	- [FastAPI](https://fastapi.tiangolo.com/) за потрясающий фреймворк
   203	- [Next.js](https://nextjs.org/) за React фреймворк
   204	- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) за красивую документацию
   205	
   206	---
   207	
   208	<div align="center">
   209	  Made with ❤️ by <a href="https://github.com/Serg2206">Serg2206</a>
   210	</div>
   211	