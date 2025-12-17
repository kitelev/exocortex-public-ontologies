---
type: owl:Ontology
label: EMS Domain Ontology
uri: https://exocortex.my/ontology/domain/ems#
prefix: ems
version: 1.0.0
imports:
  - core
  - meta
---

# EMS Domain Ontology

Effort Management System — домен управления задачами, проектами и областями ответственности.

## Bounded Context

EMS — это независимый домен со своим ubiquitous language:
- **Task** — единица работы с временными рамками
- **Project** — контейнер для связанных задач
- **Area** — область ответственности (бессрочная)
- **Effort** — факт выполнения работы (время)

## Aggregate Roots

1. **Task** — основной агрегат
   - Содержит Effort (время выполнения)
   - Принадлежит Project или Area
   - Может иметь Prototype

2. **Project** — агрегат проекта
   - Содержит множество Tasks
   - Принадлежит Area
   - Имеет статус и дедлайн

3. **Area** — агрегат области
   - Содержит Projects и Tasks
   - Иерархическая структура

## Концепты

### Сущности
- [[ems__Task]] — задача
- [[ems__Project]] — проект
- [[ems__Area]] — область ответственности
- [[ems__Prototype]] — шаблон задачи

### Value Objects
- [[ems__Effort]] — трекинг времени (mixin)
- [[ems__Priority]] — приоритет

## Зависимости

```
domain/ems (этот модуль)
  └── core (Asset, Reference)
      └── owl, rdfs
```

EMS НЕ зависит от:
- application (commands)
- presentation (layouts, UI)
