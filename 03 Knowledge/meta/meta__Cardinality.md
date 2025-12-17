---
type: owl:Class
label: Cardinality
uri: https://exocortex.my/ontology/meta#Cardinality
rdfs:comment: Кардинальность свойства (сколько значений допустимо)
---

# Cardinality

Определяет количество допустимых значений свойства.

## Стандартные кардинальности

| Экземпляр | Min | Max | Описание |
|-----------|-----|-----|----------|
| `meta:Cardinality_Single` | 0 | 1 | Одно значение или пусто |
| `meta:Cardinality_Required` | 1 | 1 | Ровно одно значение |
| `meta:Cardinality_Multiple` | 0 | * | Любое количество |
| `meta:Cardinality_AtLeastOne` | 1 | * | Минимум одно |

## Свойства

| Свойство | Тип | Описание |
|----------|-----|----------|
| `meta:Cardinality_min` | xsd:integer | Минимум значений |
| `meta:Cardinality_max` | xsd:integer / "*" | Максимум значений |

## Пример использования

```yaml
type: meta:Property
meta:Property_name: tags
meta:Property_type: xsd:string
meta:Property_cardinality: "[[meta__Cardinality_Multiple]]"
```
