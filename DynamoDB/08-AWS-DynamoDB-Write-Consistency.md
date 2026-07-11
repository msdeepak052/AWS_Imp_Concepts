# 08 - AWS DynamoDB Write Consistency

> Goal: cover how DynamoDB writes are always handled, plus DynamoDB Transactions for the rare case needing atomicity across multiple items — the NoSQL analogue to Note 07 finishing off the read side.

---

## 1. Writes are always strongly consistent — from a single-item view

Unlike reads, DynamoDB **writes don't have an "eventual" option to choose** — a successful write (`PutItem`, `UpdateItem`, `DeleteItem`) is durably committed across replicas before the API call returns success. The eventual-consistency behavior from Note 07 only affects **reads that might race a very recent write**, not the durability of the write itself.

---

## 2. Conditional writes

DynamoDB supports **conditional writes** — a write only succeeds if a specified condition on the item's current state is true (e.g. "only update this item if `Version` still equals 3") — implementing **optimistic concurrency control** without needing a separate locking mechanism.

```
UpdateItem ... ConditionExpression: "Version = :expectedVersion"
```

---

## 3. DynamoDB Transactions — atomicity across multiple items

For the rarer case of needing **all-or-nothing** behavior across **multiple items** (potentially across multiple tables) — e.g. "debit this item and credit that item, both or neither" — DynamoDB offers **Transactions** (`TransactWriteItems` / `TransactGetItems`), providing **ACID guarantees** across up to 100 items in a single call.

> ⚠️ Transactions cost **roughly double** the standard write/read capacity of the same operations done individually, since DynamoDB performs two underlying passes (prepare, then commit) to guarantee atomicity — use them specifically when true multi-item atomicity is required, not as a default habit.

> 🎯 **Exam tip:** "update multiple items atomically, all-or-nothing" is the DynamoDB Transactions signal — this is DynamoDB's answer to the ACID atomicity `RDS/02` covers for relational databases, scoped specifically to the items included in that one transactional call.

---

## 4. Recap

- Individual DynamoDB writes are always durably committed (no "eventual" write option); **conditional writes** enable optimistic concurrency control; **Transactions** provide ACID atomicity across multiple items, at roughly double the capacity cost.
- Next: Note 09 — AWS DynamoDB RCU (Read Capacity Unit), starting the capacity-and-cost model deep dive.

### Sources
- [Managing complex workflows with DynamoDB transactions — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transaction-apis.html)
- [Conditional writes — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithItems.html#WorkingWithItems.ConditionalUpdate)
