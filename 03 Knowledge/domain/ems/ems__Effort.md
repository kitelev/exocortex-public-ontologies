---
type: meta:Class
label: Effort
uri: https://exocortex.my/ontology/domain/ems#Effort
meta:Class_abstract: true
rdfs:comment: Mixin для трекинга времени выполнения
---

# Effort

Effort — mixin (примесь) для трекинга времени выполнения.

## Определение

Effort не является самостоятельным классом, а добавляет свойства времени к другим классам (Task).

## Свойства

| Свойство | Тип | Описание |
|----------|-----|----------|
| `ems:Effort_startTimestamp` | xsd:dateTime | Время начала |
| `ems:Effort_endTimestamp` | xsd:dateTime | Время завершения |

## Вычисляемые значения

### Duration
Длительность вычисляется как разница между end и start:
```
duration = endTimestamp - startTimestamp
```

### Status
Статус определяется наличием timestamps:
- `notStarted`: нет startTimestamp
- `inProgress`: есть start, нет end
- `completed`: есть и start, и end

## Применение

Task включает свойства Effort:
```yaml
type: ems:Task
core:Asset_label: "My Task"
ems:Effort_startTimestamp: "2025-01-15T10:00:00Z"
ems:Effort_endTimestamp: "2025-01-15T11:30:00Z"
# duration = 1h 30m
```

## SPARQL для аналитики

```sparql
SELECT ?label (SUM(?duration) as ?total)
WHERE {
  ?s a ems:Task .
  ?s core:Asset_label ?label .
  ?s ems:Effort_startTimestamp ?start .
  ?s ems:Effort_endTimestamp ?end .
  BIND(?end - ?start AS ?duration)
}
GROUP BY ?label
```
