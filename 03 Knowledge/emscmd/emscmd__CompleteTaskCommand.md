---
exo__Asset_uid: 50000000-0000-0000-0000-000000000020
exo__Asset_label: Завершить задачу
exo__Asset_description: Завершает выполнение задачи, переводя её в статус Done
exo__Asset_isDefinedBy: "[[!emscmd]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exocmd__Command]]"
exocmd__Command_icon: ✅
exocmd__Command_targetClass: "[[ems__Task]]"
exocmd__Command_process: "[[emscmd__CompleteTaskProcess]]"
exocmd__Command_grounding: "[[emscmd__CompleteTaskGrounding]]"
---

# Complete Task Command

Команда завершения задачи. Переводит текущий Effort в статус Done и фиксирует время окончания.

## Когда доступна

Задача должна быть в статусе **Doing** (активно выполняется).

## Что делает

1. Меняет статус текущего Effort на Done
2. Устанавливает endTimestamp = NOW()
