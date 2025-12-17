---
type: owl:Ontology
label: Obsidian Presentation
uri: https://exocortex.my/ontology/presentation/obsidian#
prefix: obs
version: 1.0.0
imports:
  - presentation
---

# Obsidian Presentation

Реализация слоя представления для Obsidian.

## Подмодули

### layouts/
Визуальные шаблоны для отображения заметок:
- Как рендерить Task в режиме Preview
- Какие поля показывать в sidebar
- Стили и иконки

### groundings/
Привязка абстрактных команд к Obsidian API:
- Маппинг Command → plugin.addCommand()
- Реализация через Obsidian Modal API
- Работа с Vault и MetadataCache

### ui/
UI-компоненты:
- [[obs__Modal]] — модальные окна
- [[obs__Notification]] — уведомления
- [[obs__Sidebar]] — боковые панели

## Obsidian API

### Commands
```typescript
this.addCommand({
  id: 'create-task',
  name: 'Create Task',
  callback: () => { /* ... */ }
});
```

### Modals
```typescript
class MyModal extends Modal {
  onOpen() { /* ... */ }
}
```

### Frontmatter
```typescript
app.fileManager.processFrontMatter(file, (fm) => {
  fm['property'] = value;
});
```
