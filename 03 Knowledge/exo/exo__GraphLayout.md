---
exo__Asset_uid: 10000000-0000-0000-0000-000000000032
exo__Asset_label: Graph Layout
exo__Asset_description: Граф связей между ассетами — узлы и рёбра
exo__Asset_isDefinedBy: "[[!exo]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__Class]]"
exo__Class_subClassOf:
  - "[[exo__Layout]]"
---

# Graph Layout

Граф связей визуализирует отношения между ассетами. Узлы — ассеты, рёбра — связи между ними.

## Специфичные свойства

- `GraphLayout_nodeLabel` — какое свойство использовать для подписи узла
- `GraphLayout_edgeProperties` — какие связи отображать как рёбра
- `GraphLayout_depth` — глубина обхода графа

## Пример

```yaml
exo__Instance_class:
  - "[[exo__GraphLayout]]"
exo__Layout_targetClass: "[[ems__Task]]"
exo__GraphLayout_nodeLabel: "[[exo__Asset_label]]"
exo__GraphLayout_edgeProperties:
  - "[[ems__Task_project]]"
  - "[[ems__Task_blockedBy]]"
exo__GraphLayout_depth: 2
```
