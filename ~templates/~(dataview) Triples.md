## As Subject
```dataview
TABLE WITHOUT ID
	link(file.link, "_") AS "_",
	subject.aliases[0] AS subject,
	predicate.aliases[0] AS predicate,
	object.aliases[0] AS object
WHERE subject = this.file.link
```
## As Predicate
```dataview
TABLE WITHOUT ID
	link(file.link, "_") AS "_",
	subject.aliases[0] AS subject,
	predicate.aliases[0] AS predicate,
	object.aliases[0] AS object
WHERE 
	predicate = this.file.link
```
## As Object
```dataview
TABLE WITHOUT ID
	link(file.link, "_") AS "_",
	subject.aliases[0] AS subject,
	predicate.aliases[0] AS predicate,
	object.aliases[0] AS object
WHERE object = this.file.link
```
