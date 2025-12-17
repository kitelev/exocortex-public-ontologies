---
type: cmd:Command
cmd:Command_name: search
cmd:Command_label: Поиск
cmd:Command_description: Универсальный поиск по базе знаний
cmd:Command_category: navigate
cmd:Command_form: "[[cmd__SearchForm]]"
---

# Search Command

Команда универсального поиска по базе знаний.

## Input (Form)

| Поле | Тип | Обязательное |
|------|-----|--------------|
| query | text | да |
| typeFilter | multiselect | - |
| areaFilter | link(ems:Area) | - |
| projectFilter | link(ems:Project) | - |

## Preconditions

Нет.

## Outcome

- Выполнен SPARQL-запрос с фильтрами
- Показан список результатов
- При выборе — открыт соответствующий файл

## SPARQL

```sparql
PREFIX core: <https://exocortex.my/ontology/core#>
PREFIX ems: <https://exocortex.my/ontology/domain/ems#>

SELECT ?s ?label ?type
WHERE {
  ?s core:Asset_label ?label .
  ?s a ?type .
  FILTER(CONTAINS(LCASE(?label), LCASE("$query")))
}
ORDER BY ?label
LIMIT 50
```
