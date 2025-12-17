---
type: owl:Ontology
label: Obsidian UI Components
uri: https://exocortex.my/ontology/presentation/obsidian/ui#
prefix: ui
version: 1.0.0
imports:
  - presentation/obsidian
---

# Obsidian UI Components

UI-компоненты для реализации команд в Obsidian.

## Компоненты

### Модальные окна
- [[ui__Modal]] — базовый класс модального окна
- [[ui__FormModal]] — модальное окно с формой
- [[ui__FuzzySuggestModal]] — модальное окно с fuzzy-поиском
- [[ui__ConfirmModal]] — диалог подтверждения

### Уведомления
- [[ui__Notice]] — всплывающее уведомление

### Поля ввода
- [[ui__TextInput]] — текстовое поле
- [[ui__NumberInput]] — числовое поле
- [[ui__DatePicker]] — выбор даты
- [[ui__LinkSuggest]] — выбор ссылки

## Связь с Obsidian API

| UI Component | Obsidian API |
|--------------|--------------|
| Modal | `Modal` |
| FuzzySuggestModal | `FuzzySuggestModal<T>` |
| Notice | `Notice` |
| TextInput | `TextComponent` |
