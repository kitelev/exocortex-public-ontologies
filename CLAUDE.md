# CLAUDE.md — Инструкции для работы с exocortex-public-ontologies

## Обязательные правила

### После КАЖДОГО изменения онтологий

1. **Сразу создай PR и влей в main**:
   ```bash
   git checkout -b feat/описание-изменения
   git add -A
   git commit -m "тип: описание изменения"
   git push origin feat/описание-изменения
   gh pr create --title "тип: описание" --body "Краткое описание"
   gh pr merge --squash --delete-branch
   ```

2. **Типы коммитов**:
   - `feat:` — новый класс, свойство, команда
   - `fix:` — исправление ошибки в онтологии
   - `refactor:` — реструктуризация без изменения семантики
   - `docs:` — обновление README/CLAUDE.md

### Формат файлов

**Классы** — только frontmatter, без markdown body:
```yaml
---
exo__Asset_uid: uuid-v4
exo__Asset_isDefinedBy: "[[!ontology]]"
exo__Instance_class:
  - "[[meta__Class]]"
exo__Class_superClass:
  - "[[parent__Class]]"
exo__Class_description: Краткое описание
---
```

**Свойства** — отдельный файл для каждого:
```yaml
---
exo__Asset_uid: uuid-v4
exo__Asset_isDefinedBy: "[[!ontology]]"
exo__Instance_class:
  - "[[exo__StringProperty]]"  # или ObjectProperty, DateTimeProperty
exo__Property_domain: "[[TargetClass]]"
exo__Property_range: "[[RangeClass]]"  # для ObjectProperty
exo__Asset_description: Описание свойства
---
```

### Архитектура (Clean Architecture + DDD)

```
03 Knowledge/
├── core/           # НЕ зависит ни от чего
├── meta/           # Зависит от core
├── domain/         # Зависит от core, meta
├── application/    # Зависит от core, meta, domain
└── presentation/   # Зависит от всех
```

**Правила зависимостей:**
- Внутренние слои НЕ знают о внешних
- `core` → `meta` → `domain` → `application` → `presentation`
- Bounded Contexts в domain/ независимы друг от друга

### Naming Conventions

| Тип | Префикс | Пример |
|-----|---------|--------|
| Core | `core__` | `core__Asset.md` |
| Meta | `meta__` | `meta__Class.md` |
| EMS Domain | `ems__` | `ems__Task.md` |
| Commands | `cmd__` | `cmd__CreateTask.md` |
| Forms | `form__` | `form__FormField.md` |
| Layouts | `layout__` | `layout__TaskLayout.md` |
| Groundings | `grnd__` | `grnd__CreateTaskGrounding.md` |

## Запреты

- **НЕ** добавляй verbose markdown описания в файлы классов
- **НЕ** дублируй описания свойств в файлах классов (они в property-файлах)
- **НЕ** создавай циклические зависимости между слоями
- **НЕ** смешивай platform-specific код с domain logic

## Чеклист перед коммитом

- [ ] Все файлы имеют `exo__Asset_uid`
- [ ] Все файлы имеют `exo__Asset_isDefinedBy`
- [ ] Новые классы имеют property-файлы для каждого свойства
- [ ] Зависимости идут только от внешних слоёв к внутренним
- [ ] README.md обновлён если изменилась структура
