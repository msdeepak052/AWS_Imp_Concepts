# 14 - AWS Secondary Indexes

> Goal: introduce the problem secondary indexes solve — efficiently querying by attributes other than the primary key — before Notes 15-17 go deep on the two specific index types.

---

## 1. The problem: the primary key isn't always what you want to query by

DynamoDB's `Query` operation is efficient specifically because it uses the **partition key** (Note 04) to go directly to the right partition (Note 06). But real applications often need to look items up by a **different attribute** — e.g. a table keyed by `OrderId`, but a common need is "find all orders for this `CustomerId`" or "find all orders with `Status = Shipped`."

Without an index, that second kind of lookup would require a **`Scan`** — reading the **entire table** and filtering — which is slow and expensive at any real scale.

---

## 2. Secondary indexes: an alternate view of the same data

A **secondary index** lets you query by a **different key** than the table's own primary key, without a full table scan — DynamoDB automatically maintains the index in sync with the base table.

| Index type | Covered in |
|---|---|
| **Local Secondary Index (LSI)** | Note 15 |
| **Global Secondary Index (GSI)** | Note 16 |

> 🧠 **Mental model:** this is the same underlying need as a relational database's secondary index (e.g. an index on `customer_id` in a table primary-keyed by `order_id`) — DynamoDB's version just comes in two distinct flavors with meaningfully different trade-offs (Note 17), rather than one general-purpose index type.

---

## 3. Recap

- Secondary indexes let you efficiently query DynamoDB tables by attributes other than the primary key, avoiding expensive full-table `Scan` operations.
- DynamoDB offers two distinct types — LSI and GSI — each with different capabilities and constraints, covered next.
- Next: Note 15 — AWS DynamoDB Local Secondary Index (LSI).

### Sources
- [Improving data access with secondary indexes — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SecondaryIndexes.html)
