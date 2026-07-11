# 10 - AWS DynamoDB - WCU Write Capacity Unit

> Goal: define the Write Capacity Unit (WCU) — the write-side equivalent of Note 09's RCU.

---

## 1. The definition

**1 WCU** = one **standard write** of an item **up to 1 KB** in size, per second.

- Items **larger than 1KB** round up proportionally — e.g. writing a 2.5KB item costs **3 WCUs** (ceiling of 2.5/1).
- **Transactional writes** (Note 08) cost **double** the standard rate.
- Unlike RCUs, there's no "eventually vs. strongly consistent" split on the write side — writes are always durably committed (Note 08) — the only multiplier is transactionality.

---

## 2. Worked example

Writing **5 items per second**, each **3KB**:

1. Round up: 3KB → 3 units of 1KB (ceiling of 3/1 = 3).
2. Each unit costs 1 WCU (standard, non-transactional), so each item costs **3 WCUs**.
3. 5 items/second × 3 WCUs = **15 WCUs** needed.

> 🎯 **Exam tip:** RCU rounds in **4KB** chunks; WCU rounds in **1KB** chunks — a common source of exam calculation mistakes is applying the wrong chunk size to the wrong unit.

---

## 3. Recap

- 1 WCU = one standard 1KB write per second; larger items round up in 1KB increments; transactional writes cost double — with no consistency-model discount the way RCUs have.
- Next: Note 11 — AWS DynamoDB On-Demand Capacity Mode, the first of the two capacity modes built on RCUs/WCUs.

### Sources
- [Read/write capacity mode — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html)
- [Provisioned throughput — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ProvisionedThroughput.html)
