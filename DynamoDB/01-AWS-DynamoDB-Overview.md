# 01 - AWS DynamoDB

> Goal: set the stage for this folder — what DynamoDB is in one sentence, and the roadmap of notes that follow, before going deep on NoSQL fundamentals (Note 02) and DynamoDB's own architecture (Note 04 onward).

---

## 1. The one-sentence version

**Amazon DynamoDB** is a fully-managed, **serverless NoSQL key-value/document database**, designed for **massive horizontal scale** and **consistent single-digit-millisecond latency**, regardless of table size or request volume.

> 🧠 **Mental model:** where `RDS` (this repo's `RDS` folder) manages a **real relational engine** for you, DynamoDB **is** the engine — a purpose-built AWS service with no equivalent "engine choice" (Note 03's `RDS` engine list), because its data model and scaling architecture are unique to DynamoDB itself.

---

## 2. What this folder covers

- **Notes 02-03**: NoSQL fundamentals and a relational-vs-non-relational case study.
- **Notes 04-06**: core components, table classes, and storage architecture.
- **Notes 07-08**: read and write consistency models.
- **Notes 09-13**: capacity — RCUs, WCUs, On-Demand vs. Provisioned modes, and warm throughput.
- **Notes 14-17**: secondary indexes — LSI, GSI, and choosing between them.
- **Notes 18-19**: encryption at rest and resource-based policies.
- **Notes 20-22**: Global Tables and backup.
- **Notes 23-26**: exporting to S3, Streams, and Kinesis Data Streams integration.
- **Notes 27-28**: DynamoDB Accelerator (DAX).
- **Note 29**: a closing exam cheat sheet.

> ⚠️ This folder's pre-existing `DynamoDB-1.md` through `DynamoDB-6.md` files are earlier, unstructured notes kept only as background reference — they are **not** the template for these numbered notes, which follow this repo's standard structured convention instead (same pattern as `RDS`'s legacy files, and `IAM/Old`).

---

## 3. Recap

- DynamoDB is AWS's fully-managed, serverless NoSQL database, built for massive scale and consistent low-latency access.
- Next: Note 02 — NoSQL And DynamoDB, covering the NoSQL data model before DynamoDB specifics.

### Sources
- [What is Amazon DynamoDB? — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)
- [Amazon DynamoDB product page](https://aws.amazon.com/dynamodb/)
