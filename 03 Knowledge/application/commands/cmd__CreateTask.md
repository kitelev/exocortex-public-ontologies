---
type: cmd:Command
cmd:Command_name: createTask
cmd:Command_label: Создать задачу
cmd:Command_description: Создание новой задачи в системе EMS
cmd:Command_category: create
cmd:Command_form: "[[cmd__CreateTaskForm]]"
cmd:Command_targetType: "[[ems__Task]]"
---

# CreateTask Command

Команда создания новой задачи.

## Input (Form)

| Поле | Тип | Обязательное |
|------|-----|--------------|
| label | text | да |
| project | link(ems:Project) | - |
| area | link(ems:Area) | - |
| priority | number(0-10) | - |
| prototype | link(ems:Prototype) | - |

## Preconditions

Нет обязательных preconditions.

## Outcome

- Создан файл `{label}.md` с type: ems:Task
- Заполнены указанные свойства
- Если указан prototype — скопированы дефолтные значения

## Пример использования

```
User: Cmd+Shift+N → "Написать тесты" → Project: Exocortex → Create
Result: Создан файл "Написать тесты.md"
```
