---
type: meta:Class
label: Project
uri: https://exocortex.my/ontology/domain/ems#Project
meta:Class_parent: "[[core__Asset]]"
meta:Class_abstract: false
---

# Project

Проект — контейнер для связанных задач с общей целью.

## Определение

Project группирует Tasks для достижения конкретной цели. Имеет временные рамки и статус.

## Свойства

| Свойство | Тип | Обязательное | Описание |
|----------|-----|--------------|----------|
| `ems:Project_area` | ems:Area | - | Область ответственности |
| `ems:Project_status` | xsd:string | - | Статус проекта |
| `ems:Project_dueDate` | xsd:date | - | Дедлайн проекта |
| `ems:Project_description` | xsd:string | - | Описание |

## Статусы

| Статус | Описание |
|--------|----------|
| `active` | Активный проект |
| `onHold` | Приостановлен |
| `completed` | Завершён |
| `archived` | Архивирован |

## Связи

- Содержит: множество `ems:Task` (через `ems:Task_project`)
- Принадлежит: одной `ems:Area` (через `ems:Project_area`)

## Пример

```yaml
type: ems:Project
core:Asset_label: "Exocortex v2.0"
ems:Project_area: "[[Development]]"
ems:Project_status: active
ems:Project_dueDate: "2025-03-01"
```
