# 05 - AWS DynamoDB Table Class

> Goal: cover DynamoDB's two table classes — a simple, S3-storage-class-like cost/access trade-off for storage-heavy, infrequently-accessed tables.

---

## 1. The two classes

| Class | Best for |
|---|---|
| **DynamoDB Standard** | Default — the right choice for the vast majority of tables |
| **DynamoDB Standard-Infrequent Access (Standard-IA)** | Tables where **storage cost dominates the bill** relative to throughput cost — e.g. large tables holding infrequently-read historical data |

- **Standard-IA** offers **lower storage price**, but **higher throughput (read/write request) price** than Standard — the same fundamental trade-off as `S3-Simple_Storage_Services`'s Standard-IA storage class, just applied to DynamoDB's pricing model instead of S3's.

---

## 2. When switching actually saves money

Switching to Standard-IA only makes sense when a table's **storage cost** is a large fraction of its total DynamoDB bill (i.e. a large table, accessed relatively rarely) — for a small, frequently-accessed table, the higher per-request price on Standard-IA would outweigh the storage savings.

> 🎯 **Exam tip:** "large table, infrequently accessed, minimize storage cost" is the Standard-IA signal — directly parallel to the `S3-Simple_Storage_Services` Standard-IA reasoning, just for DynamoDB tables instead of S3 objects.

---

## 3. Recap

- **DynamoDB Standard-IA** trades lower storage cost for higher per-request cost — worth it only when storage, not throughput, dominates a table's cost profile.
- Switching table class doesn't change any other DynamoDB behavior (capacity mode, indexes, etc.) — it's purely a pricing-tier choice.
- Next: Note 06 — AWS DynamoDB Storage Architecture, covering partitions in depth.

### Sources
- [DynamoDB table classes — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/table-classes.html)
