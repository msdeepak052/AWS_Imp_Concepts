# 04 - AWS DynamoDB Core Components

> Goal: cover DynamoDB's core vocabulary — tables, items, attributes, and primary keys (partition key, and optional sort key) — the foundation every later note builds on.

---

## 1. Tables, items, attributes

| Term | Relational equivalent | DynamoDB meaning |
|---|---|---|
| **Table** | Table | A collection of items — but with **no fixed schema** across items |
| **Item** | Row | One record — a set of attributes, identified by a primary key |
| **Attribute** | Column | A named piece of data on an item — can be a scalar (string, number, boolean), or a nested list/map |

```
Table: Orders
{ "OrderId": "101", "CustomerId": "1", "Amount": 250.00, "Status": "Shipped" }
{ "OrderId": "102", "CustomerId": "2", "Amount": 75.50 }   <-- no "Status" attribute at all, and that's fine
```

---

## 2. Primary keys: the only thing every item must have in common

Every item **must** have a primary key, which is either:

- **Partition key only (simple primary key)**: the key alone must be unique across the whole table — e.g. `UserId`.
- **Partition key + sort key (composite primary key)**: the **combination** must be unique, but the same partition key can repeat across many items, each with a different sort key — e.g. `CustomerId` (partition key) + `OrderDate` (sort key), letting one customer have many orders, naturally sorted by date within that customer's partition.

> 🧠 **Mental model:** the **partition key** determines **which physical partition** (Note 06) an item lives on; the **sort key** determines **ordering within that partition** — this pairing is the single most important design decision in any DynamoDB table, since it directly shapes which queries are efficient later (Notes 14-17 on indexes exist specifically to add query flexibility beyond what the primary key alone provides).

---

## 3. Recap

- A DynamoDB **table** holds schema-less **items**, each with **attributes**, but every item shares one required structural element: a **primary key** — either a simple partition key, or a composite partition key + sort key.
- The choice of partition key drives physical data distribution; the sort key drives ordering within a partition.
- Next: Note 05 — AWS DynamoDB Table Class, covering the two storage-cost tiers.

### Sources
- [Core components of Amazon DynamoDB — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html)
- [Key concepts — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.NamingRulesDataTypes.html)
