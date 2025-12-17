---
type: meta:Class
label: Prototype
uri: https://exocortex.my/ontology/domain/ems#Prototype
meta:Class_parent: "[[core__Asset]]"
meta:Class_abstract: false
---

# Prototype

Прототип (шаблон) задачи — переиспользуемый паттерн для создания однотипных задач.

## Определение

Prototype определяет стандартные значения для повторяющихся задач. При создании Task из Prototype копируются дефолтные значения.

## Свойства

| Свойство | Тип | Описание |
|----------|-----|----------|
| `ems:Prototype_defaultProject` | ems:Project | Проект по умолчанию |
| `ems:Prototype_defaultArea` | ems:Area | Область по умолчанию |
| `ems:Prototype_defaultPriority` | xsd:integer | Приоритет по умолчанию |
| `ems:Prototype_expectedDuration` | xsd:duration | Ожидаемая длительность |

## Применение

1. **Рутинные задачи**: "Утренний душ", "Еженедельный обзор"
2. **Рабочие шаблоны**: "Code Review", "Sprint Planning"
3. **Чеклисты**: "Deployment Checklist"

## Связь с Task

```yaml
# Task создан из Prototype
type: ems:Task
core:Asset_label: "Утренний душ 2025-01-15"
ems:Task_prototype: "[[Утренний душ (прототип)]]"
```

## Пример

```yaml
type: ems:Prototype
core:Asset_label: "Утренний душ"
ems:Prototype_defaultArea: "[[Health]]"
ems:Prototype_expectedDuration: "PT15M"
```
