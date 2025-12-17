---
type: meta:Class
label: Command
uri: https://exocortex.my/ontology/application/commands#Command
meta:Class_abstract: true
---

# Command

Базовый класс для всех команд системы.

## Определение

Command описывает Use Case — действие, которое пользователь может выполнить. Это декларативное описание, не реализация.

## Свойства

| Свойство | Тип | Обязательное | Описание |
|----------|-----|--------------|----------|
| `cmd:Command_name` | xsd:string | да | Уникальное имя команды |
| `cmd:Command_label` | xsd:string | да | Человекочитаемое название |
| `cmd:Command_description` | xsd:string | - | Описание |
| `cmd:Command_category` | cmd:Category | - | Категория команды |
| `cmd:Command_form` | app:Form | - | Форма ввода данных |
| `cmd:Command_preconditions` | cmd:Precondition[] | - | Условия выполнения |
| `cmd:Command_targetType` | meta:Class | - | Тип целевой сущности |

## Категории

| Category | Описание |
|----------|----------|
| `create` | Создание сущностей |
| `edit` | Редактирование |
| `action` | Действия |
| `navigate` | Навигация |
| `query` | Запросы |

## Жизненный цикл

```
[Define] → [Validate Preconditions] → [Show Form] → [Execute] → [Show Result]
```

## Пример

```yaml
type: cmd:Command
cmd:Command_name: createTask
cmd:Command_label: "Создать задачу"
cmd:Command_category: create
cmd:Command_form: "[[cmd__CreateTaskForm]]"
cmd:Command_targetType: "[[ems__Task]]"
```
