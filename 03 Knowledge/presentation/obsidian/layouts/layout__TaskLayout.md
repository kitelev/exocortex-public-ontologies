---
type: layout:Layout
layout:Layout_name: taskLayout
layout:Layout_targetType: "[[ems__Task]]"
layout:Layout_sections:
  - "[[layout__TaskHeader]]"
  - "[[layout__TaskMetadata]]"
  - "[[layout__TaskEffort]]"
  - "[[layout__TaskContent]]"
---

# Task Layout

Визуальный шаблон для отображения задачи.

## Секции

### Header
- Название задачи (core:Asset_label)
- Иконка статуса (не начата / в процессе / завершена)

### Metadata
- Проект (ems:Task_project)
- Область (ems:Task_area)
- Приоритет (ems:Task_priority)
- Прототип (ems:Task_prototype)

### Effort
- Время начала (ems:Effort_startTimestamp)
- Время завершения (ems:Effort_endTimestamp)
- Длительность (вычисляемое)

### Content
- Основное содержимое заметки (markdown body)

## Рендеринг

```html
<div class="exo-task-layout">
  <div class="exo-header">
    <span class="exo-status-icon">●</span>
    <h1>{label}</h1>
  </div>
  <div class="exo-metadata">
    <span class="exo-project">{project}</span>
    <span class="exo-priority">{priority}</span>
  </div>
  <div class="exo-effort">
    Started: {startTimestamp}
    Duration: {duration}
  </div>
  <div class="exo-content">
    {content}
  </div>
</div>
```
