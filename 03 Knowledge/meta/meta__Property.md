---
type: owl:Class
label: Property
uri: https://exocortex.my/ontology/meta#Property
rdfs:comment: Определение свойства класса
---

# Property

Мета-класс для определения свойств классов.

## Определение

meta:Property описывает атрибут или связь класса с типом, кардинальностью и ограничениями.

## Свойства

| Свойство | Тип | Описание |
|----------|-----|----------|
| `meta:Property_name` | xsd:string | Имя свойства |
| `meta:Property_type` | meta:DataType / meta:Class | Тип значения |
| `meta:Property_cardinality` | meta:Cardinality | Кардинальность |
| `meta:Property_required` | xsd:boolean | Обязательное |
| `meta:Property_default` | any | Значение по умолчанию |

## Типы свойств

### DataProperty
Свойство с примитивным типом (string, number, date).

### ObjectProperty
Свойство-ссылка на другой Asset.

## Пример

```yaml
type: meta:Property
meta:Property_name: priority
meta:Property_type: xsd:integer
meta:Property_cardinality: "[[meta__Cardinality_Single]]"
meta:Property_required: false
meta:Property_default: 0
```
