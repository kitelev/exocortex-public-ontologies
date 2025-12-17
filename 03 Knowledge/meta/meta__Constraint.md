---
type: owl:Class
label: Constraint
uri: https://exocortex.my/ontology/meta#Constraint
rdfs:comment: Ограничение на значение свойства
---

# Constraint

Ограничение для валидации значений свойств.

## Типы ограничений

### ValueConstraint
Ограничение на значение:
- `minValue`, `maxValue` — для чисел
- `minLength`, `maxLength` — для строк
- `pattern` — regex для строк

### EnumConstraint
Ограничение на список допустимых значений.

### ReferenceConstraint
Ограничение на тип связанного Asset.

## Свойства

| Свойство | Тип | Описание |
|----------|-----|----------|
| `meta:Constraint_property` | meta:Property | Свойство |
| `meta:Constraint_type` | xsd:string | Тип ограничения |
| `meta:Constraint_value` | any | Значение ограничения |
| `meta:Constraint_message` | xsd:string | Сообщение об ошибке |

## Пример

```yaml
type: meta:Constraint
meta:Constraint_property: "[[ems__Task_priority]]"
meta:Constraint_type: range
meta:Constraint_value: { min: 0, max: 10 }
meta:Constraint_message: "Priority must be between 0 and 10"
```
