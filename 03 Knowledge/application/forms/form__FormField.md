---
type: meta:Class
label: FormField
uri: https://exocortex.my/ontology/application/forms#FormField
meta:Class_abstract: true
---

# FormField

Базовый класс поля формы.

## Определение

FormField описывает одно поле ввода в форме с типом, валидацией и метаданными.

## Свойства

| Свойство | Тип | Описание |
|----------|-----|----------|
| `form:FormField_name` | xsd:string | Имя поля (ключ) |
| `form:FormField_label` | xsd:string | Отображаемая метка |
| `form:FormField_type` | xsd:string | Тип поля |
| `form:FormField_required` | xsd:boolean | Обязательное поле |
| `form:FormField_default` | any | Значение по умолчанию |
| `form:FormField_placeholder` | xsd:string | Подсказка |
| `form:FormField_hint` | xsd:string | Пояснение |

## Типы полей

| Тип | Класс | Описание |
|-----|-------|----------|
| text | form:TextField | Текстовое поле |
| textarea | form:TextAreaField | Многострочный текст |
| number | form:NumberField | Число |
| date | form:DateField | Дата |
| datetime | form:DateTimeField | Дата и время |
| select | form:SelectField | Выпадающий список |
| link | form:LinkField | Ссылка на Asset |
| checkbox | form:CheckboxField | Чекбокс |

## Пример

```yaml
type: form:FormField
form:FormField_name: label
form:FormField_label: "Название"
form:FormField_type: text
form:FormField_required: true
form:FormField_placeholder: "Введите название..."
```
