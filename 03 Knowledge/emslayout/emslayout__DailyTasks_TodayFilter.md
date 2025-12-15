---
exo__Asset_uid: 60000000-0000-0000-0000-000000000030
exo__Asset_label: Today Filter
exo__Asset_description: Фильтр — только задачи с Effort за сегодня
exo__Asset_isDefinedBy: "[[!emslayout]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__LayoutFilter]]"
exo__LayoutFilter_sparql: |
  ?asset ems:Task_currentEffort ?effort .
  ?effort ems:Effort_startTimestamp ?start .
  BIND(FLOOR(?start / 86400000) AS ?startDay)
  BIND(FLOOR(NOW() / 86400000) AS ?today)
  FILTER(?startDay = ?today)
---

# Today Filter

Показывает только задачи, у которых текущий Effort начат сегодня.

SPARQL-логика:
1. Получаем startTimestamp текущего Effort
2. Вычисляем день (timestamp / 86400000 = дни с эпохи)
3. Сравниваем с сегодняшним днём
