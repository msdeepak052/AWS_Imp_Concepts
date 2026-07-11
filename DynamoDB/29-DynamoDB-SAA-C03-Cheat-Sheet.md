# 29 - AWS Certified Solutions Architect - Associate SAA-C03 DynamoDB Cheat Sheet

> Goal: close out this folder with a one-page, exam-oriented consolidation of Notes 01-28.

---

## 1. The core facts

| Topic | One-line takeaway |
|---|---|
| Data model | Key-value/document NoSQL, no fixed schema, no joins (Notes 01-02) |
| Primary key | Simple (partition key) or composite (partition + sort key) (Note 04) |
| Scaling | Automatic partitioning by hashed partition key — watch for hot partitions (Note 06) |
| Read consistency | Eventually consistent (default, half RCU cost) vs. strongly consistent (Note 07) |
| Write consistency | Always durably committed; Transactions for multi-item atomicity, ~2x cost (Note 08) |
| RCU | 1 = one strongly consistent 4KB read/sec; eventual = half cost (Note 09) |
| WCU | 1 = one standard 1KB write/sec; transactional = double cost (Note 10) |
| Capacity modes | On-Demand (pay-per-request, unpredictable traffic) vs. Provisioned + Auto Scaling (predictable, cheaper) (Notes 11-12) |
| Warm Throughput | Pre-warm capacity ahead of a known spike, free by default, billed only if proactively increased (Note 13) |
| LSI | Same partition key, alternate sort key, must be created with the table, max 5, supports strongly consistent reads (Note 15) |
| GSI | Different partition/sort key, addable anytime, own throughput, max 20, eventually consistent only (Note 16) |
| Encryption | Always on by default (AWS owned / AWS managed / customer managed KMS key), changeable after creation (Note 18) |
| Resource policies | Attach access-control policy directly to a table for cross-account access, no AssumeRole needed (Note 19) |
| Global Tables | Multi-active, multi-Region, sub-second replication, built on Streams, last-writer-wins (Note 20) |
| Backup | On-Demand (manual, indefinite) vs. PITR (continuous, restore to any second) (Note 22) |
| Export to S3 | Analytics-oriented, no impact on table capacity, full/point-in-time/incremental (Notes 23-24) |
| Streams & Triggers | 24-hour change log, Lambda Triggers react in near real time (Note 25) |
| Kinesis integration | Longer retention (365 days), multi-consumer fan-out, separate from native Streams (Note 26) |
| DAX | API-compatible in-memory cache, microsecond reads, minimal code change, reads only (Note 27) |

---

## 2. The recurring exam patterns

- **"Massive scale, simple key-based access, low predictable latency"** → DynamoDB, full stop (vs. RDS).
- **"Reduce read latency further, minimal code change"** → DAX (vs. generic ElastiCache, which needs custom cache-aside code).
- **"Query by a different attribute than the primary key"** → GSI by default; LSI only if strongly consistent reads on the index are explicitly required.
- **"React to changes in near real time"** → Streams + Lambda (simple) or Kinesis integration (longer retention, multi-consumer).
- **"Multi-Region, active-active"** → Global Tables.
- **"Analytics without touching the live table"** → Export to S3 (or the case-study pattern from Note 03, feeding a proper data warehouse).

---

## 3. Recap

- This closes the `DynamoDB` folder: Notes 01-03 covered fundamentals and a relational-vs-non-relational case study, 04-06 core architecture, 07-08 consistency, 09-13 capacity, 14-17 secondary indexes, 18-19 security, 20-22 Global Tables and backup, 23-26 analytics/streaming integrations, and 27-28 DAX.
- Paired with the `RDS` folder's Note 39 database overview, this gives a complete map of AWS's relational and non-relational database services for the exam.

### Sources
- [What is Amazon DynamoDB? — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)
- [Amazon DynamoDB best practices — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
