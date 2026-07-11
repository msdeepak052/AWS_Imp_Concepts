# 24 - How To Export S3 In DynamoDB? Part 2 Select Best Exported File Format

> Goal: cover the two export file formats and which analytics tools each pairs best with.

---

## 1. The two formats

| Format | Characteristics |
|---|---|
| **DynamoDB JSON** | Preserves DynamoDB's own attribute-type wrapper format (e.g. `{"S": "value"}`) — a direct, lossless representation of the original items |
| **Amazon Ion** (text or binary) | A richer, self-describing data format (superset of JSON) supporting additional types DynamoDB itself uses internally, without needing DynamoDB's type-wrapper syntax |

---

## 2. Choosing based on the downstream tool

- **Athena / Redshift Spectrum / Glue**: generally prefer **Ion** or plain **JSON**, depending on the specific SerDe (serializer/deserializer) configured for the table definition reading the exported data.
- If downstream tooling expects to see DynamoDB's **native attribute-type structure** preserved exactly (e.g. custom processing code written against that shape), **DynamoDB JSON** avoids any re-mapping step.
- If working with tools that already understand richer typing (dates, binary, etc.) and prefer a more compact/efficient encoding, **Ion binary** is typically the more efficient choice.

> 🎯 **Exam tip:** the exam is unlikely to demand byte-level format trivia — the testable takeaway is simply that **the export format is a deliberate choice**, made based on which downstream analytics tool will consume the data, not a fixed, one-size-fits-all default.

---

## 3. Recap

- DynamoDB Export to S3 supports **DynamoDB JSON** and **Amazon Ion** — the right choice depends on what the downstream analytics tooling (Athena, Redshift Spectrum, Glue, custom processing) expects to consume.
- Next: Note 25 — AWS DynamoDB Stream & Trigger, covering the change-data-capture mechanism underlying Global Tables (Note 20) and much more.

### Sources
- [Exporting DynamoDB table data to Amazon S3 — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/S3DataExport.html)
- [Data export formats — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/S3DataExport.Output.html)
