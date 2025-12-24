# SIOC Ontology Diagram

UML-style class diagram for the **sioc** namespace.

*Generated automatically. Classes: 11, Properties: 84*

**Legend:**
- `<|--` Inheritance (rdfs:subClassOf)
- `-->` Object Property (owl:ObjectProperty)
- `..>` Datatype Property (owl:DatatypeProperty)

```mermaid
classDiagram
    class foaf_Agent
    class _3cbd7949
    class xsd_nonNegativeInteger
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
    sioc_Container ..> xsd_nonNegativeInteger : sioc:num_items
    sioc_Usergroup --> sioc_UserAccount : sioc:has_member
    sioc_Item --> sioc_Item : sioc:previous_version
    sioc_Item --> sioc_UserAccount : sioc:mentions
    sioc_Site --> sioc_Container : sioc:host_of
    sioc_Item --> sioc_Item : sioc:next_version
    sioc_Forum ..> xsd_nonNegativeInteger : sioc:num_threads
    sioc_Item --> sioc_Container : sioc:has_container
    sioc_Container --> sioc_UserAccount : sioc:has_subscriber
    sioc_UserAccount ..> rdfs_Literal : sioc:last_name
    sioc_Item --> sioc_Item : sioc:reply_of
    sioc_Item --> _3cbd7949 : sioc:embeds_knowledge
    sioc_Usergroup --> sioc_Space : sioc:usergroup_of
    sioc_Container --> sioc_Item : sioc:container_of
    sioc_Item --> sioc_Item : sioc:previous_by_date
    sioc_Post ..> rdfs_Literal : sioc:title
    sioc_Item ..> rdfs_Literal : sioc:content
    sioc_UserAccount ..> rdfs_Literal : sioc:email_sha1
    sioc_Post ..> rdfs_Literal : sioc:modified_at
    sioc_UserAccount --> sioc_UserAccount : sioc:follows
    sioc_Item --> sioc_Item : sioc:latest_version
    sioc_UserAccount --> sioc_Container : sioc:subscriber_of
    sioc_Container --> sioc_Container : sioc:parent_of
    sioc_Post ..> rdfs_Literal : sioc:description
    sioc_Post ..> rdfs_Literal : sioc:subject
    sioc_Item --> sioc_Item : sioc:has_reply
    sioc_Post ..> rdfs_Literal : sioc:content_encoded
    sioc_Container --> sioc_Site : sioc:has_host
    sioc_Site --> sioc_UserAccount : sioc:has_administrator
    sioc_Post ..> rdfs_Literal : sioc:created_at
    sioc_UserAccount --> foaf_Agent : sioc:account_of
    sioc_Item ..> rdfs_Literal : sioc:read_at
    sioc_Forum --> sioc_UserAccount : sioc:has_moderator
    sioc_UserAccount --> sioc_Usergroup : sioc:member_of
    sioc_Item --> sioc_UserAccount : sioc:shared_by
    sioc_UserAccount ..> rdfs_Literal : sioc:first_name
    sioc_Space --> sioc_Usergroup : sioc:has_usergroup
```

## Statistics

| Metric | Count |
|--------|-------|
| Classes | 11 |
| Properties | 84 |
| Inheritance relationships | 7 |
| Properties with domain | 58 |
| Properties with range | 59 |
