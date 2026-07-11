# 13 - AWS DynamoDB Warm Throughput

> Goal: cover Warm Throughput — a comparatively recent DynamoDB feature for proactively pre-warming a table's or index's capacity ahead of a known traffic event, verified against current AWS documentation.

---

## 1. What "warm" throughput actually means

Every DynamoDB table and Global Secondary Index (Note 16) has a **warm throughput** value at all times — a measure of how much read/write load it can **instantaneously** support, based on **how it has scaled from historical usage**, available **by default at no extra cost**, for both **new and existing** tables/GSIs, regardless of capacity mode (Notes 11-12).

- This exists because DynamoDB's underlying partitions (Note 06) take a small amount of time to split and scale up in response to genuinely new load — "warm throughput" is effectively a readout of how much capacity is **already available right now**, without needing to wait for that scaling to happen reactively.

---

## 2. Proactively increasing it

You can **proactively raise** a table's (or GSI's) warm throughput value **ahead of a known event** — e.g. an upcoming product launch or flash sale — so the table is already able to instantaneously handle the expected spike the moment it arrives, rather than scaling reactively (and potentially throttling briefly) during the event itself.

- Available for **new tables at creation**, **existing tables**, and applies automatically to **all replica tables** in a Global Table (Note 20) once set.
- **Pricing**: the default warm throughput values are free; you're billed **only if you proactively increase them** above the default, pre-warming capacity you may not fully use immediately.

> 🎯 **Exam tip:** "we know exactly when a traffic spike is coming (e.g. a scheduled sale) and want to avoid any throttling risk at that moment" is the Warm Throughput signal — distinct from Auto Scaling (Note 12), which reacts to load **after** it starts changing, rather than being told about it in advance.

---

## 3. Recap

- Warm Throughput represents a table's/GSI's currently-available instantaneous capacity; it's free by default, but proactively raising it ahead of a known spike (to avoid any reactive-scaling throttling risk) incurs a cost for the additional pre-warmed capacity.
- Applies to single-Region tables, GSIs, and automatically propagates across all replicas in a Global Table.
- Next: Note 14 — AWS Secondary Indexes, introducing query flexibility beyond the primary key.

### Sources
- [Understanding DynamoDB warm throughput — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/warm-throughput.html)
- [Amazon DynamoDB introduces warm throughput for tables and indexes — AWS](https://aws.amazon.com/about-aws/whats-new/2024/11/amazon-dynamodb-warm-throughput-ondemand-provisioned-tables/)
