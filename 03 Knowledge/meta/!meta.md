---
type: owl:Ontology
label: Meta Ontology
uri: https://exocortex.my/ontology/meta#
prefix: meta
version: 1.0.0
imports:
  - owl
  - rdfs
  - core
---

# Meta Ontology

Мета-онтология для описания структуры онтологий. Позволяет определять новые классы, свойства и ограничения.

## Назначение

Meta — это инструмент для создания новых онтологий:
- Определение новых классов
- Определение свойств классов
- Задание ограничений (constraints)
- Валидация данных

## Концепты

### Структурные
- [[meta__Class]] — определение класса
- [[meta__Property]] — определение свойства
- [[meta__Constraint]] — ограничение на свойство

### Типы данных
- [[meta__DataType]] — базовый тип данных
- [[meta__Cardinality]] — кардинальность свойства

## Зависимости

```
meta (этот модуль)
  └── core (Asset, Reference, Relation)
      └── owl, rdfs
```

## Использование

```yaml
# Определение нового класса
type: meta:Class
meta:Class_name: MyCustomClass
meta:Class_parent: core:Asset
meta:Class_properties:
  - "[[myProperty1]]"
  - "[[myProperty2]]"
```
