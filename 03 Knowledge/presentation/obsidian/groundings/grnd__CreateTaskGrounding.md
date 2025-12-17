---
type: grnd:Grounding
grnd:Grounding_command: "[[cmd__CreateTask]]"
grnd:Grounding_hotkey: "Cmd+Shift+N"
grnd:Grounding_modalClass: CreateTaskModal
grnd:Grounding_capabilities:
  - modal
  - fileCreate
  - frontmatterWrite
  - notification
grnd:Grounding_status: implemented
---

# CreateTask Grounding

Реализация команды создания задачи в Obsidian.

## Obsidian API

### Регистрация команды

```typescript
this.addCommand({
  id: 'create-task',
  name: 'Create Task',
  hotkeys: [{ modifiers: ['Mod', 'Shift'], key: 'n' }],
  callback: () => new CreateTaskModal(this.app, this).open()
});
```

### Модальное окно

```typescript
class CreateTaskModal extends Modal {
  onOpen() {
    // Рендер формы из cmd:CreateTaskForm
  }

  async onSubmit(data: TaskFormData) {
    const path = `Tasks/${data.label}.md`;
    const content = this.generateFrontmatter(data);
    await this.app.vault.create(path, content);
    new Notice('Задача создана');
  }
}
```

## Маппинг формы

| Form Field | UI Component |
|------------|--------------|
| label | TextInput |
| project | FuzzySuggest(Project) |
| area | FuzzySuggest(Area) |
| priority | NumberInput(0-10) |
