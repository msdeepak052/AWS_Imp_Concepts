# 02 - NoSQL And DynamoDB

> Goal: cover what "NoSQL" actually means as a category, and how DynamoDB specifically (a key-value/document store) fits within the broader NoSQL landscape.

---

## 1. NoSQL is a category, not one thing

"NoSQL" covers several genuinely different data models, unified only by **not** being the fixed-schema, table-and-joins relational model (`RDS/02-Introduction-to-Database`):

| NoSQL category | Example | Data shape |
|---|---|---|
| Key-value / document | **DynamoDB**, MongoDB | Item = a key + a flexible set of attributes (often JSON-like) |
| Wide-column | Cassandra | Rows with dynamic, per-row column sets |
| Graph | Neo4j | Nodes and relationships |
| In-memory | Redis (`RDS/33`) | Key-value, held in memory |

DynamoDB specifically is a **key-value and document** store — every item is retrieved by a **key**, and its value can be a rich, nested structure (numbers, strings, lists, maps).

---

## 2. The core trade-off versus relational databases

- **No fixed schema**: different items in the same table can have completely different sets of attributes — no `ALTER TABLE` needed to add a new field to some items.
- **No joins**: DynamoDB is not designed to combine data across tables at query time — data is typically **denormalized** (duplicated where needed) so that a single item read contains everything a query needs.
- **Horizontal, near-unlimited scaling**: DynamoDB scales by **partitioning** data across many physical nodes (Note 06) rather than by growing a single instance vertically.

> 🧠 **Mental model:** relational design asks "how do I normalize this data to avoid duplication, and join it back together at query time?" NoSQL/DynamoDB design instead asks "what will I query, and how do I shape each item so that single query never needs a join?" — this inversion of design philosophy is the single biggest adjustment moving from RDS-style thinking to DynamoDB.

---

## 3. Recap

- NoSQL spans several distinct data models; DynamoDB specifically is **key-value/document**.
- Its core trade-offs versus relational databases are: no fixed schema, no joins (design around denormalization instead), and horizontal partitioned scaling in place of vertical instance scaling.
- Next: Note 03 — UPI Case Study, a concrete relational-vs-non-relational design comparison.

### Sources
- [What is NoSQL? — AWS](https://aws.amazon.com/nosql/)
- [What is Amazon DynamoDB? — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)
