---
exo__Asset_uid: 60000000-0000-0000-0000-000000000003
exo__Asset_label: Start Task Process
exo__Asset_description: Последовательность шагов для запуска задачи
exo__Asset_isDefinedBy: "[[!emscmd]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exocmd__Sequence]]"
exo__Sequence_steps:
  - "[[emscmd__StartTask_SetStatus]]"
  - "[[emscmd__StartTask_SetTimestamp]]"
  - "[[emscmd__StartTask_Save]]"
  - "[[emscmd__StartTask_Notify]]"
---
