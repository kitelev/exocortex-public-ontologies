---
exo__Asset_uid: 50000000-0000-0000-0000-000000000010
exo__Asset_label: Остановить задачу
exo__Asset_description: Приостанавливает выполнение задачи, переводя её в статус Queued
exo__Asset_isDefinedBy: "[[!emscmd]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exocmd__Command]]"
exocmd__Command_icon: ⏹️
exocmd__Command_targetClass: "[[ems__Task]]"
exocmd__Command_process: "[[emscmd__StopTaskProcess]]"
exocmd__Command_grounding: "[[emscmd__StopTaskGrounding]]"
---

# Stop Task Command

Команда остановки задачи. Переводит текущий Effort в статус Queued.

## Когда доступна

Задача должна быть в статусе **Doing** (активно выполняется).

## Что делает

1. Меняет статус текущего Effort на Queued
2. Сохраняет время работы для последующего возобновления
