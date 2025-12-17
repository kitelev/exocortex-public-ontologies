---
type: owl:Class
label: Asset
uri: https://exocortex.my/ontology/core#Asset
rdfs:comment: Базовая единица знаний в системе Exocortex
---

# Asset

Фундаментальный класс, представляющий любую единицу знаний в системе.

## Определение

Asset — это любой идентифицируемый объект в базе знаний:
- Заметка (Note)
- Задача (Task)
- Проект (Project)
- Концепт (Concept)
- и т.д.

## Свойства

| Свойство | Тип | Описание |
|----------|-----|----------|
| `core:Asset_label` | xsd:string | Человекочитаемое название |
| `core:Asset_created` | xsd:dateTime | Дата создания |
| `core:Asset_modified` | xsd:dateTime | Дата последнего изменения |
| `core:Asset_uri` | xsd:anyURI | Уникальный идентификатор |

## Подклассы

Все доменные сущности наследуются от Asset:
- `ems:Task` — задача
- `ems:Project` — проект
- `ems:Area` — область ответственности
- `knowledge:Note` — заметка
- `knowledge:Concept` — концепт

## Пример

```yaml
type: core:Asset
core:Asset_label: "Моя заметка"
core:Asset_created: "2025-01-15T10:30:00Z"
```
