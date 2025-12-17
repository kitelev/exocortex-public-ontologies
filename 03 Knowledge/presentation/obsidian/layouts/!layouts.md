---
type: owl:Ontology
label: Obsidian Layouts
uri: https://exocortex.my/ontology/presentation/obsidian/layouts#
prefix: layout
version: 1.0.0
imports:
  - presentation/obsidian
---

# Obsidian Layouts

Визуальные шаблоны для отображения заметок в Obsidian.

## Концепт Layout

Layout определяет как отображать заметку определённого типа:
- Какие секции показывать
- Какие поля в каждой секции
- Какие UI-компоненты использовать

## Структура

```
Layout
  └── Section[]
        └── FieldRenderer[]
```

## Стандартные layouts

- [[layout__TaskLayout]] — отображение задачи
- [[layout__ProjectLayout]] — отображение проекта
- [[layout__AreaLayout]] — отображение области

## Связь с Domain

```yaml
# Layout привязывается к типу
type: layout:Layout
layout:Layout_targetType: "[[ems__Task]]"
```
