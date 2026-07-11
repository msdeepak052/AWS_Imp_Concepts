# 03 - UPI Case Study || Relational vs Non-Relational Databases

> Goal: use a concrete, real-world-shaped system — a UPI-style (Unified Payments Interface) instant payments platform — to make the relational-vs-non-relational decision tangible, rather than abstract.

---

## 1. The system: an instant payments platform

A UPI-style system needs to, at minimum:

1. Look up a user's linked bank account/profile by their UPI ID — extremely high volume, simple key-based lookup.
2. Process a money transfer between two accounts — needs a **strict, all-or-nothing** guarantee (money can't vanish or duplicate).
3. Store a transaction history/audit log — extremely high write volume, simple append-and-later-query pattern.
4. Support fraud-detection queries and reporting — complex, ad-hoc aggregations across many transactions.

These four needs pull in **different directions**, and a real system typically uses **more than one database**, matched to each need.

---

## 2. Mapping each need to a data model

| Need | Best fit | Why |
|---|---|---|
| 1. UPI ID → account profile lookup | **DynamoDB** | Simple key-based access, needs to handle enormous request volume with consistent low latency (Note 01) |
| 2. Money transfer (debit + credit, atomically) | **RDS/Aurora** | Needs ACID transactions (`RDS/02`) — a transfer must never partially apply |
| 3. Transaction history / audit log | **DynamoDB** (often paired with **DynamoDB Streams**, Note 25) | Extremely high write throughput, simple "append and look up by transaction ID / user+time" access pattern |
| 4. Fraud detection / reporting | **Amazon Redshift** (fed via Zero-ETL, `RDS/31`, or a similar pipeline) | Complex aggregation across huge historical datasets — a data warehouse workload, not a transactional one |

---

## 3. The exam-relevant lesson

The exam rarely asks "design a UPI system" directly, but it **regularly** asks a scenario matching one of these four shapes and expects you to pick the right database for **that specific need** — not to force one database to handle everything.

> 🎯 **Exam tip:** "needs ACID/strict consistency for a financial transaction" → **RDS/Aurora**. "Needs to handle massive, simple-key request volume with low, predictable latency" → **DynamoDB**. "Needs complex analytical queries over historical data" → **Redshift**. A single real-world system commonly uses **all three together**, each for the part of the workload it fits.

---

## 4. Recap

- A realistic payments-style system illustrates that "relational vs. non-relational" isn't a one-time architectural choice for the whole system — different sub-problems within the same system often want different data models.
- Matching each specific access pattern to the right database, rather than picking one database for everything, is the core skill the exam is testing.
- Next: Note 04 — AWS DynamoDB Core Components, starting the deep dive into DynamoDB's own architecture.

### Sources
- [What is Amazon DynamoDB? — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)
- [AWS databases overview](https://aws.amazon.com/products/databases/)
