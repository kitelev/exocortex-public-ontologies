---
type: meta:Class
label: Grounding
uri: https://exocortex.my/ontology/presentation/obsidian/groundings#Grounding
---

# Grounding

Привязка команды к Obsidian API.

## Определение

Grounding описывает как абстрактная команда реализуется в Obsidian.

## Свойства

| Свойство | Тип | Описание |
|----------|-----|----------|
| `grnd:Grounding_command` | cmd:Command | Абстрактная команда |
| `grnd:Grounding_hotkey` | xsd:string | Горячая клавиша |
| `grnd:Grounding_modalClass` | xsd:string | Класс модального окна |
| `grnd:Grounding_capabilities` | xsd:string[] | Требуемые capabilities |
| `grnd:Grounding_status` | xsd:string | Статус реализации |

## Capabilities

| Capability | Описание |
|------------|----------|
| fileCreate | Создание файлов |
| fileDelete | Удаление файлов |
| frontmatterRead | Чтение frontmatter |
| frontmatterWrite | Запись frontmatter |
| modal | Модальные окна |
| notification | Уведомления |
| sparqlQuery | SPARQL-запросы |

## Статусы реализации

| Status | Описание |
|--------|----------|
| implemented | Реализовано |
| planned | Запланировано |
| partial | Частично реализовано |

## Пример

```yaml
type: grnd:Grounding
grnd:Grounding_command: "[[cmd__CreateTask]]"
grnd:Grounding_hotkey: "Cmd+Shift+N"
grnd:Grounding_modalClass: "CreateTaskModal"
grnd:Grounding_capabilities:
  - modal
  - fileCreate
  - frontmatterWrite
  - notification
grnd:Grounding_status: implemented
```
