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
    class _4a4ea3e0
    class dfa4b23c
    class _54d176e7
    class _85395f0f
    class _3e1876d3
    class _5dcd4d6a
    class _0e812e2d
    class _8e4f0b81
    class a83f3b04
    class _4e31180f
    class _46aed95b
    class aaec4952
    class _0a03e5b1
    class e7015c0d
    class _89a07249
    class _463837a8
    class _260013df
    class owl_Thing
    class _31149b0b
    class _9ce08244
    class _0f481e29
    class _2a0f20aa
    class _73d74fd7
    class _7560d4d3
    class _52083215
    class _938ba17a
    class _2f3962d8
    class _91464865
    class _3799be63
    class _2faec320
    class _6be63cc0
    class _7bb41048
    class _86d89c72
    class a282e3cf
    class _03f5f412
    class _08532a6a
    class _7339538e
    class c68cd41d
    class _05ba1f9c
    class _3cbaaafd
    class _8b254840
    class _410601fb
    class _3e55892d
    class ccbb342d
    class _15fef9c5
    class ac4bb8c5
    class _35c893e9
    class fefe1a1c
    class _37dbb4e2
    class _297d4447
    class _33f2fd9d
    class f1e646f2
    class b22c6e01
    class a308e1b7
    class dec3c87c
    class ec3bf17f
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
    b22c6e01 <|-- time_MonthOfYear
    f1e646f2 <|-- time_MonthOfYear
    time_DateTimeDescription <|-- time_MonthOfYear
    _33f2fd9d <|-- time_MonthOfYear
    _297d4447 <|-- time_MonthOfYear
    _37dbb4e2 <|-- time_MonthOfYear
    fefe1a1c <|-- time_MonthOfYear
    _35c893e9 <|-- time_MonthOfYear
    ac4bb8c5 <|-- time_MonthOfYear
    time_DurationDescription <|-- time_Year
    _15fef9c5 <|-- time_Year
    ccbb342d <|-- time_Year
    _3e55892d <|-- time_Year
    _410601fb <|-- time_Year
    _8b254840 <|-- time_Year
    _3cbaaafd <|-- time_Year
    _05ba1f9c <|-- time_Year
    c68cd41d <|-- time_DateTimeDescription
    _7339538e <|-- time_DateTimeDescription
    _08532a6a <|-- time_DateTimeDescription
    time_GeneralDateTimeDescription <|-- time_DateTimeDescription
    _03f5f412 <|-- time_DateTimeDescription
    time_Interval <|-- time_ProperInterval
    time_TemporalEntity <|-- time_Interval
    time_TemporalPosition <|-- time_TimePosition
    dec3c87c <|-- time_TimePosition
    a282e3cf <|-- time_GeneralDurationDescription
    _86d89c72 <|-- time_GeneralDurationDescription
    _7bb41048 <|-- time_GeneralDurationDescription
    _6be63cc0 <|-- time_GeneralDurationDescription
    _2faec320 <|-- time_GeneralDurationDescription
    _3799be63 <|-- time_GeneralDurationDescription
    _91464865 <|-- time_GeneralDurationDescription
    time_TemporalDuration <|-- time_GeneralDurationDescription
    _2f3962d8 <|-- time_GeneralDurationDescription
    _938ba17a <|-- time_DurationDescription
    _52083215 <|-- time_DurationDescription
    _7560d4d3 <|-- time_DurationDescription
    _73d74fd7 <|-- time_DurationDescription
    time_GeneralDurationDescription <|-- time_DurationDescription
    _2a0f20aa <|-- time_DurationDescription
    _0f481e29 <|-- time_DurationDescription
    _9ce08244 <|-- time_DurationDescription
    _31149b0b <|-- time_DurationDescription
    time_ProperInterval <|-- time_DateTimeInterval
    owl_Thing <|-- time_TemporalEntity
    time_TemporalDuration <|-- time_Duration
    _260013df <|-- time_Duration
    _463837a8 <|-- time_Duration
    _89a07249 <|-- time_GeneralDateTimeDescription
    e7015c0d <|-- time_GeneralDateTimeDescription
    _0a03e5b1 <|-- time_GeneralDateTimeDescription
    aaec4952 <|-- time_GeneralDateTimeDescription
    _46aed95b <|-- time_GeneralDateTimeDescription
    time_TemporalPosition <|-- time_GeneralDateTimeDescription
    _4e31180f <|-- time_GeneralDateTimeDescription
    a83f3b04 <|-- time_GeneralDateTimeDescription
    _8e4f0b81 <|-- time_GeneralDateTimeDescription
    _0e812e2d <|-- time_GeneralDateTimeDescription
    _5dcd4d6a <|-- time_GeneralDateTimeDescription
    _3e1876d3 <|-- time_GeneralDateTimeDescription
    _85395f0f <|-- time_GeneralDateTimeDescription
    _54d176e7 <|-- time_January
    dfa4b23c <|-- time_January
    time_DateTimeDescription <|-- time_January
    time_TemporalDuration <|-- time_TemporalUnit
    time_TemporalEntity <|-- time_Instant
    owl_Thing <|-- time_DayOfWeek
    _4a4ea3e0 <|-- time_TemporalPosition
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
