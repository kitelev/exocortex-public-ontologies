## As Predicate
```dataview
TABLE WITHOUT ID
	link(file.link, "_") AS "_",
	rdf__subject, 
	rdf__predicate,
	rdf__object
WHERE 
	rdf__predicate = this.file.link
	AND 
	!contains(file.name, "___")
```
