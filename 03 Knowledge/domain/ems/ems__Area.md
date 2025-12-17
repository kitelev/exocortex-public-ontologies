---
type: meta:Class
label: Area
uri: https://exocortex.my/ontology/domain/ems#Area
meta:Class_parent: "[[core__Asset]]"
meta:Class_abstract: false
---

# Area

Область ответственности — бессрочная категория для задач и проектов.

## Определение

Area представляет постоянную сферу деятельности или ответственности. В отличие от Project, Area не имеет дедлайна и продолжается неопределённо долго.

## Свойства

| Свойство | Тип | Обязательное | Описание |
|----------|-----|--------------|----------|
| `ems:Area_parent` | ems:Area | - | Родительская область |
| `ems:Area_description` | xsd:string | - | Описание |

## Иерархия

Areas могут образовывать дерево:

```
Life
├── Health
│   ├── Fitness
│   └── Nutrition
├── Work
│   ├── Development
│   └── Management
└── Personal
    └── Hobbies
```

## Связи

- Содержит: множество `ems:Project` (через `ems:Project_area`)
- Содержит: множество `ems:Task` (через `ems:Task_area`)
- Родитель: одна `ems:Area` (через `ems:Area_parent`)

## Пример

```yaml
type: ems:Area
core:Asset_label: "Development"
ems:Area_parent: "[[Work]]"
ems:Area_description: "Software development activities"
```
