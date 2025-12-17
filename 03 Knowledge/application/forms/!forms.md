---
type: owl:Ontology
label: Forms Ontology
uri: https://exocortex.my/ontology/application/forms#
prefix: form
version: 1.0.0
imports:
  - application
---

# Forms Ontology

Определение форм ввода данных для команд.

## Концепт Form

Form — это декларативное описание UI для сбора данных:
- **Какие поля** (fields)
- **Какие типы** (field types)
- **Какая валидация** (constraints)

## Концепты

### Form
- [[form__Form]] — базовый класс формы

### FormField
- [[form__FormField]] — базовый класс поля
- [[form__TextField]] — текстовое поле
- [[form__NumberField]] — числовое поле
- [[form__DateField]] — выбор даты
- [[form__LinkField]] — ссылка на Asset
- [[form__SelectField]] — выпадающий список

## Принципы

1. **Declarative** — описание, не реализация
2. **Type-safe** — типизированные поля
3. **Validatable** — встроенная валидация

## Связь с Commands

```
Command --hasForm--> Form --hasFields--> FormField[]
```
