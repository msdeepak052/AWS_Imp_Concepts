# 15 - AWS DynamoDB Local Secondary Index (LSI)

> Goal: cover LSI's exact semantics — same partition key, alternate sort key — and the constraints that make it a "must plan at table creation" feature.

---

## 1. What it is

An **LSI** keeps the **same partition key** as the base table, but defines an **alternate sort key** — letting you query the same partition's items, ordered/filtered by a different attribute than the table's own sort key.

```
Base table: CustomerId (PK) + OrderDate (SK)
LSI:        CustomerId (PK) + OrderAmount (alternate SK)
```

Both let you query "all orders for this customer" — the base table sorted by date, the LSI sorted by amount.

---

## 2. The constraints that matter

- **Must be created at the same time as the table** — you cannot add an LSI to an existing table later.
- **Maximum of 5 LSIs per table.**
- **Shares the base table's provisioned throughput** (Notes 09-10) — it doesn't have its own separate RCU/WCU allocation the way a GSI does.
- A single partition's **combined size across the base table and all its LSIs is capped at 10GB** — a real constraint for very large, high-cardinality-per-partition-key datasets.

> ⚠️ Because an LSI can't be added after table creation, it's a decision that must be made **upfront**, during initial table design — a common practical reason teams default to GSIs (Note 16) instead, unless the same-partition-key requirement (needed for strongly consistent reads on the index, see below) specifically calls for an LSI.

---

## 3. The one thing only LSI can do: strongly consistent reads on the index

Because an LSI shares the base table's partition, it can support **strongly consistent reads** (Note 07) directly against the index — a **GSI cannot**, since a GSI's data lives on entirely separate partitions, updated asynchronously.

> 🎯 **Exam tip:** "need strongly consistent reads on a secondary index" is the one requirement that specifically points to **LSI** over GSI — every other secondary-indexing need is generally better served by a GSI's greater flexibility (Note 16).

---

## 4. Recap

- LSI shares the base table's partition key with an alternate sort key, must be defined at table creation, is capped at 5 per table and 10GB combined per partition key, and is the only index type supporting strongly consistent reads.
- Next: Note 16 — AWS DynamoDB Global Secondary Index (GSI), the more flexible, more commonly used alternative.

### Sources
- [Local secondary indexes — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/LSI.html)
