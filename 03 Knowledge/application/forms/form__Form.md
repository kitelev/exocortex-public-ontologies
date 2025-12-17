---
type: meta:Class
label: Form
uri: https://exocortex.my/ontology/application/forms#Form
meta:Class_abstract: false
---

# Form

Форма ввода данных для команды.

## Определение

Form описывает набор полей для сбора данных от пользователя.

## Свойства

| Свойство | Тип | Описание |
|----------|-----|----------|
| `form:Form_name` | xsd:string | Имя формы |
| `form:Form_fields` | form:FormField[] | Список полей |
| `form:Form_submitLabel` | xsd:string | Текст кнопки отправки |
| `form:Form_cancelLabel` | xsd:string | Текст кнопки отмены |

## Пример

```yaml
type: form:Form
form:Form_name: createTaskForm
form:Form_fields:
  - "[[form__LabelField]]"
  - "[[form__ProjectField]]"
  - "[[form__AreaField]]"
  - "[[form__PriorityField]]"
form:Form_submitLabel: "Создать"
form:Form_cancelLabel: "Отмена"
```
