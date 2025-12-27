# TIME Ontology Diagram

UML-style class diagram for the **time** namespace.

*Generated automatically. Classes: 23, Properties: 58*

**Legend:**
- `<|--` Inheritance (rdfs:subClassOf)
- `-->` Object Property
- `..>` Datatype Property

```mermaid
classDiagram
    class xsd_nonNegativeInteger
    class xsd_gYear
    class xsd_date
    class xsd_decimal
    class xsd_dateTime
    class xsd_duration
    class xsd_gYearMonth
    class owl_Thing
    class time_DateTimeDescription
    class time_DateTimeInterval
    class time_DayOfWeek
    class time_Duration
    class time_DurationDescription
    class time_GeneralDateTimeDescription
    class time_GeneralDurationDescription
    class time_Instant
    class time_Interval
    class time_January
    class time_MonthOfYear
    class time_ProperInterval
    class time_TemporalDuration
    class time_TemporalEntity
    class time_TemporalPosition
    class time_TemporalUnit
    class time_TimePosition
    class time_TimeZone
    class time_TRS
    class time_Year
    time_DateTimeDescription <|-- time_MonthOfYear
    time_DurationDescription <|-- time_Year
    time_GeneralDateTimeDescription <|-- time_DateTimeDescription
    time_Interval <|-- time_ProperInterval
    time_TemporalEntity <|-- time_Interval
    time_TemporalPosition <|-- time_TimePosition
    time_TemporalDuration <|-- time_GeneralDurationDescription
    time_GeneralDurationDescription <|-- time_DurationDescription
    time_ProperInterval <|-- time_DateTimeInterval
    owl_Thing <|-- time_TemporalEntity
    time_TemporalDuration <|-- time_Duration
    time_TemporalPosition <|-- time_GeneralDateTimeDescription
    time_DateTimeDescription <|-- time_January
    time_TemporalDuration <|-- time_TemporalUnit
    time_TemporalEntity <|-- time_Instant
    owl_Thing <|-- time_DayOfWeek
    time_ProperInterval --> time_ProperInterval : time:intervalAfter
    time_Instant ..> xsd_gYearMonth : time:inXSDgYearMonth
    time_Instant --> time_GeneralDateTimeDescription : time:inDateTime
    time_GeneralDateTimeDescription --> time_MonthOfYear : time:monthOfYear
    time_TemporalEntity ..> xsd_duration : time:hasXSDDuration
    time_Instant ..> xsd_dateTime : time:inXSDDateTime
    time_GeneralDurationDescription ..> xsd_decimal : time:weeks
    time_TimePosition ..> xsd_decimal : time:numericPosition
    time_ProperInterval --> time_ProperInterval : time:intervalOverlaps
    time_ProperInterval --> time_ProperInterval : time:intervalEquals
    time_TemporalEntity --> time_Instant : time:hasEnd
    time_Instant ..> xsd_date : time:inXSDDate
    time_ProperInterval --> time_ProperInterval : time:intervalFinishedBy
    time_Instant ..> xsd_gYear : time:inXSDgYear
    time_ProperInterval --> time_ProperInterval : time:intervalMeets
    time_TemporalEntity --> time_TemporalEntity : time:after
    time_GeneralDateTimeDescription ..> xsd_nonNegativeInteger : time:week
    time_GeneralDateTimeDescription ..> xsd_nonNegativeInteger : time:hour
    time_GeneralDateTimeDescription --> time_DayOfWeek : time:dayOfWeek
    time_Instant --> time_TemporalPosition : time:inTemporalPosition
```

## Statistics

| Metric | Count |
|--------|-------|
| Classes | 23 |
| Properties | 58 |
| Inheritance relationships | 69 |
| Properties with domain | 28 |
| Properties with range | 29 |
