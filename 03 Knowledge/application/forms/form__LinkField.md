---
type: meta:Class
label: LinkField
uri: https://exocortex.my/ontology/application/forms#LinkField
meta:Class_parent: "[[form__FormField]]"
---

# LinkField

Поле для выбора ссылки на другой Asset.

## Определение

LinkField показывает fuzzy-suggest для выбора связанной сущности определённого типа.

## Дополнительные свойства

| Свойство | Тип | Описание |
|----------|-----|----------|
| `form:LinkField_targetType` | meta:Class | Тип целевой сущности |
| `form:LinkField_allowCreate` | xsd:boolean | Разрешить создание новой |
| `form:LinkField_multiple` | xsd:boolean | Множественный выбор |

## Пример

```yaml
type: form:LinkField
form:FormField_name: project
form:FormField_label: "Проект"
form:FormField_required: false
form:LinkField_targetType: "[[ems__Project]]"
form:LinkField_allowCreate: false
```

## UI-реализация

В Obsidian реализуется через FuzzySuggestModal с фильтрацией по типу.
