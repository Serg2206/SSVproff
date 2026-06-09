# Известные ограничения и риски

Снимок на момент обновления ветки `feat/comprehensive-config-no-workflows`.

## Публичная витрина (GitHub Pages / MkDocs)
- Основной публичный контент обслуживается через MkDocs.
- Сборка Next.js в публичный Pages выключена сознательно, чтобы не затронуть нерабочий фронтенд-артефакт.
- Public exposure для Next.js в этом репо минимален/нулевой.

## Блокер локальной сборки Next (`web/`)
- `web/src/pages/_app.tsx` импортирует `../styles/globals.css`, но файл отсутствует:
  - Локальный `next build` в `web/` не проходит до добавления файла или удаления импорта.
  - Это не ломает документацию MkDocs и GitHub Pages.

## Next.js — остаток рисков (показ без `--force` upgrade)
- Information exposure / origin verification в dev-сервере — неактуально, пока dev-сервер не слушается публично.
- HTTP request smuggling / rewrites / SSRF в advanced use-cases — не эксплуатируется текущей демо-конфигурацией.
- XSS в `beforeInteractive`-скриптах — риск только при недоверенном пользовательском вводе.
- DoS / unbounded Image Optimizer disk cache — снижен тем, что в `web/next.config.js` стоит `images: { unoptimized: true }`.

## PostCSS advisory
- Moderate‑уровень: XSS через неэкранированный `</style>` при рендере пользовательского CSS.
- В текущем репо CSS статичен, пользовательский CSS не загружается.

## Follow-up
- Вернуться к `web/` после того, как будет наполнен контент/стили для Serg2206.
- Следующий обзор зависимостей проводить через Dependabot/осознанный scoped upgrade Next.js, без перепрыгивания в preview-релизы.
