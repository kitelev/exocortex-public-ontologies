---
type: meta:Class
label: Layout
uri: https://exocortex.my/ontology/presentation/obsidian/layouts#Layout
---

# Layout

Визуальный шаблон для отображения заметки.

## Определение

Layout описывает структуру визуального представления заметки определённого типа.

## Свойства

| Свойство | Тип | Описание |
|----------|-----|----------|
| `layout:Layout_name` | xsd:string | Имя layout |
| `layout:Layout_targetType` | meta:Class | Тип целевой сущности |
| `layout:Layout_sections` | layout:Section[] | Секции |

## Секции

| Секция | Описание |
|--------|----------|
| header | Заголовок с названием |
| metadata | Метаданные (проект, область, приоритет) |
| effort | Время выполнения |
| content | Основное содержимое |
| relations | Связанные сущности |

## Пример

```yaml
type: layout:Layout
layout:Layout_name: taskLayout
layout:Layout_targetType: "[[ems__Task]]"
layout:Layout_sections:
  - "[[layout__TaskHeader]]"
  - "[[layout__TaskMetadata]]"
  - "[[layout__TaskEffort]]"
  - "[[layout__TaskContent]]"
```
