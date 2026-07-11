# 09 - AWS DynamoDB - RCU Read Capacity Unit

> Goal: define exactly what a Read Capacity Unit (RCU) measures — the core unit Provisioned Capacity Mode (Note 12) bills and throttles against.

---

## 1. The definition

**1 RCU** = one **strongly consistent** read of an item **up to 4 KB** in size, per second.

- **Eventually consistent reads** (the default, Note 07) cost **half** as much: 1 RCU covers **two** eventually-consistent reads of up to 4KB per second.
- **Transactional reads** (Note 08) cost **double**: 1 RCU covers half an item's worth of a transactional read.
- Items **larger than 4KB** consume **proportionally more RCUs** — e.g. a strongly consistent read of a 9KB item rounds up to 3 RCUs (ceiling of 9/4).

---

## 2. Worked example

Reading **10 items per second**, each **6KB**, eventually consistent:

1. Round each item up to the nearest 4KB multiple: 6KB → 2 units of 4KB (ceiling of 6/4 = 2).
2. Each eventually-consistent 4KB unit costs **0.5 RCU**, so each item costs 2 × 0.5 = **1 RCU**.
3. 10 items/second × 1 RCU = **10 RCUs** needed.

> 🧠 **Mental model:** RCUs measure **data read per second**, rounded up in 4KB chunks, with the consistency model (Note 07) and transactionality (Note 08) acting as multipliers on that base cost — not a measure of "number of requests" in isolation.

---

## 3. Recap

- 1 RCU = one strongly consistent 4KB read per second; eventually consistent reads cost half; transactional reads cost double; item size rounds up to the next 4KB boundary.
- Next: Note 10 — AWS DynamoDB WCU Write Capacity Unit, the equivalent unit for writes.

### Sources
- [Read/write capacity mode — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html)
- [Provisioned throughput — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ProvisionedThroughput.html)
