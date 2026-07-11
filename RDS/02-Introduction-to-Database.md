# 02 - Introduction Of Database

> Goal: cover database fundamentals — relational vs. non-relational, the vocabulary (tables, rows, schema, ACID, SQL) — needed before RDS-specific notes make sense.

---

## 1. What a database actually is

A **database** is organized, persistent storage for data, designed to be efficiently queried, updated, and managed — as opposed to flat files, which have no built-in query language, indexing, or integrity guarantees.

---

## 2. Relational databases

A **relational database** organizes data into **tables** (rows and columns), where:

- Each **table** has a fixed **schema** — defined columns with defined data types.
- Each **row** is one record; each **column** is one attribute of that record.
- Tables relate to each other via **foreign keys** — e.g. an `orders` table referencing a `customers` table by `customer_id`.
- Data is queried and manipulated using **SQL** (Structured Query Language).

```
customers                  orders
+----+--------+            +----+-------------+--------+
| id | name   |            | id | customer_id | amount |
+----+--------+            +----+-------------+--------+
| 1  | Alice  |    <------ | 101| 1           | 250.00 |
| 2  | Bob    |            | 102| 2           | 75.50  |
+----+--------+            +----+-------------+--------+
```

---

## 3. ACID properties

Relational databases are built around **ACID** guarantees:

| Property | Meaning |
|---|---|
| **Atomicity** | A transaction either fully completes or fully rolls back — no partial writes |
| **Consistency** | A transaction moves the database from one valid state to another, respecting all constraints |
| **Isolation** | Concurrent transactions don't interfere with each other's intermediate state |
| **Durability** | Once committed, a transaction's changes survive even a crash immediately after |

> 🧠 **Mental model:** ACID is *why* relational databases are the default choice for financial transactions, inventory systems, and anything where "the numbers must always add up" — the strict schema and transactional guarantees trade some flexibility/scale for strong correctness.

---

## 4. Relational vs. non-relational (a preview)

| | Relational (RDS) | Non-relational (DynamoDB) |
|---|---|---|
| Schema | Fixed, defined upfront | Flexible, per-item |
| Scaling model | Primarily vertical (bigger instance) + read replicas | Horizontal, virtually unlimited |
| Query language | SQL, supports joins across tables | Key-based access patterns, no joins |
| Best fit | Structured data, complex relationships, transactions | High-scale, simple access patterns, flexible schema |

> 🎯 **Exam tip:** this repo's `DynamoDB` folder covers the non-relational side in depth — this table is only meant as a preview so RDS's design choices throughout this folder make sense by contrast.

---

## 5. Recap

- A relational database organizes data into fixed-schema **tables** related via foreign keys, queried with **SQL**, and governed by **ACID** guarantees.
- ACID is the core reason relational databases remain the default choice for structured, transactional workloads.
- Next: Note 03 — What Is Relational Database Service, connecting these fundamentals to what RDS specifically manages for you.

### Sources
- [Relational database — AWS docs glossary](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/database-services.html)
- [What is a relational database? — AWS](https://aws.amazon.com/relational-database/)
