# SIOC Ontology Diagram

UML-style class diagram for the **sioc** namespace.

*Generated automatically. Classes: 11, Properties: 84*

**Legend:**
- `<|--` Inheritance (rdfs:subClassOf)
- `-->` Object Property
- `..>` Datatype Property

```mermaid
classDiagram
    class _3cbd7949
    class rdfs_Literal
    class foaf_OnlineAccount
    class foaf_Document
    class sioc_Community
    class sioc_Container
    class sioc_Forum
    class sioc_Item
    class sioc_Post
    class sioc_Role
    class sioc_Site
    class sioc_Space
    class sioc_Thread
    class sioc_UserAccount
    class sioc_Usergroup
    sioc_Space <|-- sioc_Site
    foaf_Document <|-- sioc_Post
    sioc_Item <|-- sioc_Post
    sioc_Container <|-- sioc_Forum
    foaf_OnlineAccount <|-- sioc_UserAccount
    sioc_Container <|-- sioc_Thread
    sioc_UserAccount --> sioc_Forum : sioc:moderator_of
    sioc_Container ..> rdfs_Literal : sioc:last_item_date
    sioc_Container --> sioc_Container : sioc:has_parent
    sioc_Item --> sioc_Item : sioc:next_by_date
    sioc_UserAccount --> sioc_Site : sioc:administrator_of
    sioc_Item --> rdfs_Literal : sioc:delivered_at
    sioc_Item --> sioc_UserAccount : sioc:mentions
    sioc_Item --> sioc_Item : sioc:next_version
    sioc_Item --> sioc_Container : sioc:has_container
    sioc_Container --> sioc_UserAccount : sioc:has_subscriber
    sioc_Item --> sioc_Item : sioc:reply_of
    sioc_Item --> _3cbd7949 : sioc:embeds_knowledge
    sioc_Item --> sioc_Item : sioc:previous_by_date
    sioc_Post ..> rdfs_Literal : sioc:modified_at
```

## Statistics

| Metric | Count |
|--------|-------|
| Classes | 11 |
| Properties | 84 |
| Inheritance relationships | 7 |
| Properties with domain | 28 |
| Properties with range | 32 |
