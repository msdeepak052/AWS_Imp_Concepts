# 07 - AWS DynamoDB Read Consistency

> Goal: cover DynamoDB's two read-consistency models — the direct consequence of Note 06's partitioned, replicated storage architecture.

---

## 1. Why this choice exists at all

Every item in DynamoDB is stored on **multiple replicas** (across multiple AZs) for durability. A write must propagate to those replicas — which takes a small amount of time — creating a choice: **read whichever replica answers fastest** (possibly slightly stale), or **guarantee you get the very latest write** (at a small latency/throughput cost).

---

## 2. Eventually consistent vs. strongly consistent reads

| | Eventually Consistent Reads (default) | Strongly Consistent Reads |
|---|---|---|
| Guarantee | May not reflect a write from the last split-second | Always reflects the most recent successful write |
| Latency | Lowest | Slightly higher |
| Throughput cost (RCU, Note 09) | **Half** the RCU cost of a strongly consistent read for the same data | Full RCU cost |
| Availability during network partition | Higher | Can be affected if the up-to-date replica is unreachable |

- You choose per-request (e.g. a `ConsistentRead: true` parameter on a `GetItem`/`Query` call) — it's not a fixed, table-wide setting.

> 🎯 **Exam tip:** "read-after-write consistency required" or "must always see the latest value" → **strongly consistent read**. "Can tolerate a brief delay before a write is visible, prioritize lowest cost/latency" → **eventually consistent read (the default)**.

---

## 3. Recap

- DynamoDB reads can be **eventually consistent** (default, cheaper, lowest latency) or **strongly consistent** (guarantees the latest write, costs more RCU) — chosen per request.
- This choice exists because of the underlying multi-replica storage architecture from Note 06.
- Next: Note 08 — AWS DynamoDB Write Consistency, covering the write side (and how transactions fit in).

### Sources
- [Read consistency — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html)
