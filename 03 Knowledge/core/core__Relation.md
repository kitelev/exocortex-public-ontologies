---
type: owl:Class
label: Relation
uri: https://exocortex.my/ontology/core#Relation
rdfs:subClassOf: owl:ObjectProperty
rdfs:comment: Типизированная связь между Assets
---

# Relation

Класс для определения типов связей между Assets.

## Определение

Relation описывает семантику связи между двумя assets.
Это метакласс — его экземпляры являются типами связей.

## Стандартные типы связей

| Relation | Описание | Пример |
|----------|----------|--------|
| `core:partOf` | Часть целого | Task partOf Project |
| `core:relatedTo` | Общая связь | Note relatedTo Concept |
| `core:derivedFrom` | Производное | Task derivedFrom Prototype |
| `core:blockedBy` | Блокировка | Task blockedBy Task |

## Свойства

| Свойство | Тип | Описание |
|----------|-----|----------|
| `core:Relation_domain` | owl:Class | Допустимый тип источника |
| `core:Relation_range` | owl:Class | Допустимый тип цели |
| `core:Relation_inverse` | core:Relation | Обратная связь |

## Пример определения

```yaml
type: core:Relation
label: belongsToProject
core:Relation_domain: ems:Task
core:Relation_range: ems:Project
core:Relation_inverse: "[[hasTask]]"
```
