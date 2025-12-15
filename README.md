# Exocortex Public Ontologies

Публичные онтологии для системы управления знаниями [Exocortex](https://github.com/kitelev/exocortex).

## Что это?

Этот репозиторий содержит RDF-онтологии, описывающие структуру данных Exocortex:
- **Классы** (Task, Effort, Command)
- **Свойства** (label, status, createdAt)
- **Экземпляры** (статусы задач, типы действий)

Онтологии хранятся в формате Obsidian-заметок с YAML frontmatter — это позволяет редактировать их как в IDE, так и в Obsidian.

## Структура

```
03 Knowledge/
├── rdf/      # RDF-примитивы (Property)
├── rdfs/     # RDFS-схема (Resource, Class, domain, range)
├── owl/      # OWL-конструкции (ObjectProperty, DatatypeProperty)
├── exo/      # Ядро Exocortex (Asset, Class, Property, Ontology)
├── ems/      # Effort Management System (Task, Effort, Status)
├── exocmd/   # Метаклассы команд (Command, Step, Grounding)
└── emscmd/   # Конкретные команды EMS (StartTaskCommand)
```

## Онтологии

### Граф импортов

```
rdf ← rdfs ← exo ← ems
      owl ←─┘  └← exocmd ← emscmd
                         ↑
                     ems ─┘
```

### Описание

| Онтология | URL | Описание |
|-----------|-----|----------|
| `rdf` | `http://www.w3.org/1999/02/22-rdf-syntax-ns#` | Базовые RDF-примитивы |
| `rdfs` | `http://www.w3.org/2000/01/rdf-schema#` | RDFS-схема для описания классов и свойств |
| `owl` | `http://www.w3.org/2002/07/owl#` | OWL-конструкции для выразительных онтологий |
| `exo` | `https://exocortex.my/ontology/exo#` | Ядро Exocortex — базовые классы Asset, Class, Property |
| `ems` | `https://exocortex.my/ontology/ems#` | Effort Management System — задачи, усилия, статусы |
| `exocmd` | `https://exocortex.my/ontology/exocmd#` | Метаклассы команд (OWL-S inspired) |
| `emscmd` | `https://exocortex.my/ontology/emscmd#` | Конкретные команды для управления задачами |

## Архитектура команд (OWL-S inspired)

Система команд вдохновлена [OWL-S](https://www.w3.org/Submission/OWL-S/) и состоит из трёх частей:

```
┌─────────────────────────────────────────────────────────────┐
│                      exocmd__Command                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Profile   │  │   Process   │  │     Grounding       │  │
│  │   (WHAT)    │  │   (HOW)     │  │   (EXECUTION)       │  │
│  ├─────────────┤  ├─────────────┤  ├─────────────────────┤  │
│  │ label       │  │ steps[]     │  │ sparqlUpdate        │  │
│  │ description │  │ precondition│  │ affectedProperties  │  │
│  │ icon        │  │             │  │                     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Пример: StartTaskCommand

**Profile** (что делает команда):
```yaml
exo__Asset_label: Начать задачу
exo__Asset_description: Переводит задачу в статус "Doing" и создаёт Effort
exocmd__Command_icon: ▶️
```

**Process** (как выполняется):
```yaml
exocmd__Process_steps:
  - "[[emscmd__StartTaskProcess]]"
exocmd__Process_precondition:
  - "[[emscmd__TaskNotDoingPrecondition]]"
```

**Precondition** (SPARQL ASK):
```sparql
PREFIX ems: <https://exocortex.my/ontology/ems#>
ASK {
  ?task ems:Task_currentEffort ?effort .
  ?effort ems:Effort_status ems:EffortStatus_Doing .
}
# Команда доступна, если ASK возвращает false (задача НЕ в статусе Doing)
```

**Grounding** (SPARQL UPDATE):
```sparql
PREFIX ems: <https://exocortex.my/ontology/ems#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

INSERT {
  ?task ems:Task_currentEffort ?newEffort .
  ?newEffort a ems:Effort ;
             ems:Effort_status ems:EffortStatus_Doing ;
             ems:Effort_startTimestamp ?now .
}
WHERE {
  BIND(?targetAsset AS ?task)
  BIND(UUID() AS ?newEffort)
  BIND(NOW() AS ?now)
}
```

## Формат файлов

Каждый ассет — это Markdown-файл с YAML frontmatter:

```markdown
---
exo__Asset_uid: 30000000-0000-0000-0000-000000000001
exo__Asset_label: Task
exo__Asset_description: Задача — единица работы с отслеживанием усилий
exo__Asset_isDefinedBy: "[[!ems]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__Class]]"
exo__Class_subClassOf:
  - "[[exo__Asset]]"
---

# Task

Задача (Task) — это единица работы в системе Exocortex...
```

### Соглашения

- **Имя файла** = имя ассета (например, `ems__Task.md`)
- **Онтология** обозначается `!` в начале (например, `!ems.md`)
- **Ссылки** используют Obsidian wikilinks: `[[ems__Task]]`
- **UID** — UUID v4 для глобальной идентификации

## Экспорт

Репозиторий содержит экспортированные данные:

| Файл | Формат | Описание |
|------|--------|----------|
| `ontologies.nt` | N-Triples | Машиночитаемый формат (728 триплетов) |
| `ontologies.ttl` | Turtle | Человекочитаемый формат (93 субъекта) |

### Генерация экспорта

```bash
# Требуется @kitelev/exocortex-cli
npx @kitelev/exocortex-cli sparql query \
  --vault /path/to/this/repo \
  --format ntriples \
  "CONSTRUCT { ?s ?p ?o } WHERE { ?s ?p ?o }" \
  > ontologies.nt
```

## Использование с Exocortex

### CLI

```bash
# Запрос к онтологиям
npx @kitelev/exocortex-cli sparql query \
  --vault /path/to/exocortex-public-ontologies \
  "SELECT ?class ?label WHERE {
    ?class exo:Instance_class exo:Class .
    ?class exo:Asset_label ?label .
  }"
```

### Obsidian Plugin

Онтологии используются плагином для:
- Валидации frontmatter-свойств
- Автодополнения при редактировании
- Рендеринга Layout'ов на основе классов

## Лицензия

MIT

## См. также

- [Exocortex](https://github.com/kitelev/exocortex) — основной репозиторий
- [OWL-S](https://www.w3.org/Submission/OWL-S/) — спецификация семантических веб-сервисов
