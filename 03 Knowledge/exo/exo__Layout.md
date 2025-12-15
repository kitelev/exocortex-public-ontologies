---
exo__Asset_uid: 10000000-0000-0000-0000-000000000020
exo__Asset_label: Layout
exo__Asset_description: Визуальное представление данных — определяет как рендерить ассеты определённого класса
exo__Asset_isDefinedBy: "[[!exo]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__Class]]"
exo__Class_subClassOf:
  - "[[exo__Asset]]"
---

# Layout

Layout определяет визуальное представление данных в Exocortex. Каждый Layout привязан к целевому классу (`Layout_targetClass`) и описывает, как отображать экземпляры этого класса.

## Архитектура

```
┌─────────────────────────────────────────┐
│               Layout                     │
├─────────────────────────────────────────┤
│ targetClass: Class      → что показываем │
│ columns: LayoutColumn[] → какие поля     │
│ filters: LayoutFilter[] → как фильтруем  │
│ sort: LayoutSort        → как сортируем  │
│ group: LayoutGroup      → как группируем │
└─────────────────────────────────────────┘
```

## Типы Layout

- [[exo__TableLayout]] — табличное представление
- [[exo__KanbanLayout]] — канбан-доска по статусам
- [[exo__GraphLayout]] — граф связей между ассетами
- [[exo__CalendarLayout]] — календарное представление
- [[exo__ListLayout]] — простой список

## Пример

```yaml
exo__Instance_class:
  - "[[exo__TableLayout]]"
exo__Layout_targetClass: "[[ems__Task]]"
exo__Layout_columns:
  - "[[MyLayout_LabelColumn]]"
  - "[[MyLayout_StatusColumn]]"
exo__Layout_defaultSort: "[[MyLayout_Sort]]"
```
