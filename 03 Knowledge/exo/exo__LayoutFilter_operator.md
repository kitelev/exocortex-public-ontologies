---
exo__Asset_uid: 10000000-0000-0000-0000-000000000052
exo__Asset_label: Filter Operator
exo__Asset_description: Оператор сравнения для фильтра
exo__Asset_isDefinedBy: "[[!exo]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__DatatypeProperty]]"
exo__Property_domain: "[[exo__LayoutFilter]]"
exo__Property_range: "[[xsd__string]]"
---

# Filter Operator

Оператор сравнения значения свойства с эталонным значением.

## Операторы

| Оператор | Описание | Пример |
|----------|----------|--------|
| `eq` | Равно | status = Done |
| `ne` | Не равно | status ≠ Done |
| `gt` | Больше | priority > 5 |
| `gte` | Больше или равно | priority ≥ 5 |
| `lt` | Меньше | priority < 5 |
| `lte` | Меньше или равно | priority ≤ 5 |
| `contains` | Содержит подстроку | label contains "urgent" |
| `startsWith` | Начинается с | label startsWith "🔥" |
| `endsWith` | Заканчивается на | label endsWith "!" |
| `in` | Входит в список | status in [Doing, Queued] |
| `notIn` | Не входит в список | status notIn [Done, Cancelled] |
| `isNull` | Значение пустое | project isNull |
| `isNotNull` | Значение не пустое | project isNotNull |

## Пример

```yaml
exo__LayoutFilter_operator: ne
```
