---
type: meta:Class
label: Task
uri: https://exocortex.my/ontology/domain/ems#Task
meta:Class_parent: "[[core__Asset]]"
meta:Class_abstract: false
---

# Task

Задача — единица работы в системе EMS.

## Определение

Task представляет конкретную работу, которую нужно выполнить. Имеет временные рамки (Effort) и может принадлежать Project или Area.

## Свойства

### Основные
| Свойство | Тип | Обязательное | Описание |
|----------|-----|--------------|----------|
| `ems:Task_project` | ems:Project | - | Проект задачи |
| `ems:Task_area` | ems:Area | - | Область ответственности |
| `ems:Task_priority` | xsd:integer | - | Приоритет (0-10) |
| `ems:Task_dueDate` | xsd:date | - | Срок выполнения |

### Effort (время)
| Свойство | Тип | Описание |
|----------|-----|----------|
| `ems:Effort_startTimestamp` | xsd:dateTime | Время начала |
| `ems:Effort_endTimestamp` | xsd:dateTime | Время завершения |

### Prototype
| Свойство | Тип | Описание |
|----------|-----|----------|
| `ems:Task_prototype` | ems:Prototype | Шаблон задачи |

## Состояния

```
[Created] --start--> [In Progress] --complete--> [Completed]
                           |
                           +--pause--> [Paused] --resume--> [In Progress]
```

- **Created**: нет startTimestamp
- **In Progress**: есть startTimestamp, нет endTimestamp
- **Completed**: есть endTimestamp
- **Paused**: был startTimestamp, сброшен

## Пример

```yaml
type: ems:Task
core:Asset_label: "Написать документацию"
ems:Task_project: "[[Exocortex Development]]"
ems:Task_priority: 5
ems:Effort_startTimestamp: "2025-01-15T10:00:00Z"
```
