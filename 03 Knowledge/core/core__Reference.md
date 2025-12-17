---
type: owl:Class
label: Reference
uri: https://exocortex.my/ontology/core#Reference
rdfs:comment: Ссылка на другой Asset
---

# Reference

Класс для представления ссылок между Assets.

## Определение

Reference — это типизированная ссылка от одного Asset к другому.
В Obsidian реализуется через wiki-links: `[[Target]]`.

## Свойства

| Свойство | Тип | Описание |
|----------|-----|----------|
| `core:Reference_source` | core:Asset | Исходный asset (откуда ссылка) |
| `core:Reference_target` | core:Asset | Целевой asset (куда ссылка) |
| `core:Reference_type` | core:Relation | Тип связи (опционально) |

## Связь с Relation

Reference — это конкретная ссылка между двумя assets.
Relation — это тип/категория таких ссылок.

```
Reference (instance) --hasType--> Relation (class)
```

## Пример

```yaml
# В frontmatter
ems:Task_project: "[[My Project]]"  # Reference к Project
```
