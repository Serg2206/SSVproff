
// Commitlint конфигурация для conventional commits
// Обеспечивает единообразный формат коммитов: type(scope): message
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    // Тип коммита должен быть одним из:
    'type-enum': [
      2,
      'always',
      [
        'feat',     // Новая функциональность
        'fix',      // Исправление бага
        'docs',     // Изменения в документации
        'style',    // Форматирование, отсутствие изменений кода
        'refactor', // Рефакторинг кода
        'perf',     // Улучшение производительности
        'test',     // Добавление тестов
        'chore',    // Обновление зависимостей, конфигурации
        'ci',       // Изменения CI/CD
        'build',    // Изменения системы сборки
        'revert',   // Откат предыдущего коммита
      ],
    ],
    // Scope может быть опциональным
    'scope-enum': [
      2,
      'always',
      [
        'api',
        'web',
        'docs',
        'flows',
        'data-meta',
        'ci',
        'deps',
        'config',
      ],
    ],
    'scope-empty': [1, 'never'], // Предупреждение, если scope пустой
    'subject-case': [
      2,
      'never',
      ['sentence-case', 'start-case', 'pascal-case', 'upper-case'],
    ],
    'subject-empty': [2, 'never'],
    'subject-full-stop': [2, 'never', '.'],
    'header-max-length': [2, 'always', 100],
    'body-leading-blank': [1, 'always'],
    'footer-leading-blank': [1, 'always'],
  },
};
