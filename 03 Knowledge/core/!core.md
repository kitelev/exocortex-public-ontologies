---
type: owl:Ontology
label: Core Ontology
uri: https://exocortex.my/ontology/core#
prefix: core
version: 1.0.0
imports:
  - owl
  - rdfs
---

# Core Ontology

Ядро онтологической системы Exocortex. Минимальный набор концептов, от которых зависят все остальные онтологии.

## Принципы

1. **Минимализм** — только essential concepts
2. **Стабильность** — изменения крайне редки
3. **Zero dependencies** — зависит только от OWL/RDFS

## Концепты

### Сущности
- [[core__Asset]] — базовая единица знаний (заметка, файл)
- [[core__Reference]] — ссылка на другой asset
- [[core__Relation]] — типизированная связь между assets

### Свойства
- `core:Asset_label` — человекочитаемое название
- `core:Asset_created` — дата создания
- `core:Asset_modified` — дата изменения

## Зависимости

```
core (этот модуль)
  └── owl, rdfs (стандартные)
```

Никакие другие модули НЕ должны зависеть от core напрямую, кроме:
- meta (мета-моделирование)
- domain/* (доменные модули)
