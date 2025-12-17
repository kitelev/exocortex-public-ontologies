---
type: owl:Class
label: Class
uri: https://exocortex.my/ontology/meta#Class
rdfs:subClassOf: owl:Class
rdfs:comment: Определение пользовательского класса в онтологии
---

# Class

Мета-класс для определения новых классов в онтологии.

## Определение

meta:Class позволяет определять новые типы сущностей с их свойствами и ограничениями.

## Свойства

| Свойство | Тип | Описание |
|----------|-----|----------|
| `meta:Class_name` | xsd:string | Имя класса |
| `meta:Class_parent` | meta:Class | Родительский класс |
| `meta:Class_properties` | meta:Property[] | Список свойств |
| `meta:Class_abstract` | xsd:boolean | Абстрактный класс |

## Пример

```yaml
type: meta:Class
meta:Class_name: Task
meta:Class_parent: "[[core__Asset]]"
meta:Class_properties:
  - "[[ems__Task_project]]"
  - "[[ems__Task_priority]]"
meta:Class_abstract: false
```
