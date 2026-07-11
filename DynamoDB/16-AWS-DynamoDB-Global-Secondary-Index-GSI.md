# 16 - AWS DynamoDB Global Secondary Index (GSI)

> Goal: cover GSI's exact semantics — a completely different partition key (and optional sort key), its own throughput, and its asynchronous relationship to the base table.

---

## 1. What it is

A **GSI** defines an **entirely different partition key** (and optionally a different sort key) than the base table — effectively a **second table-like view** over the same items, letting you query by whatever attribute the GSI is keyed on.

```
Base table: OrderId (PK)
GSI:        CustomerId (PK) + OrderDate (SK)   <-- totally different key structure
```

---

## 2. Key differences from LSI

| | LSI (Note 15) | GSI (this note) |
|---|---|---|
| Partition key | Same as base table | Can be **completely different** |
| Created | Only at table creation | **Anytime** — added to an existing table |
| Throughput | Shares the base table's | Has **its own** separate RCU/WCU (or On-Demand) |
| Max per table | 5 | **20** (default quota, increasable) |
| Consistency | Supports strongly consistent reads | **Eventually consistent only** — updates propagate asynchronously from the base table |
| Size constraint | 10GB per base partition key combined | No such per-partition-key cap |

---

## 3. Why GSI is the more commonly reached-for option

- Can be added **after the fact**, as query needs evolve — no upfront-only decision the way LSI requires.
- Supports genuinely different access patterns (different partition key entirely), not just an alternate sort order within the same partition.
- Its own independent throughput means a GSI's query load doesn't compete with the base table's own capacity.

> ⚠️ Because GSI updates are **asynchronous**, a GSI can briefly lag behind the base table — a write to the base table doesn't guarantee the GSI reflects it instantly, relevant to any workflow assuming the GSI is always perfectly current.

> 🎯 **Exam tip:** "need to query by a completely different attribute than the primary key," "need to add this query capability to an existing table," or "need independent throughput for this access pattern" → **GSI**. Only "must have strongly consistent reads on the index" pulls back toward **LSI**.

---

## 4. Recap

- GSI supports a fully independent partition/sort key, its own throughput, and can be added anytime — at the cost of only eventually-consistent reads.
- It's the more flexible and more commonly used of the two index types.
- Next: Note 17 — AWS DynamoDB LSI Vs GSI, consolidating the comparison.

### Sources
- [Global secondary indexes — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html)
