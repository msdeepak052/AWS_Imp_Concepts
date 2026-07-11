# 14 - AWS RDS Instance Configuration

> Goal: understand RDS instance class families — how they map to the same underlying EC2 instance type families this repo's `EC2` folder already covers.

---

## 1. Instance classes mirror EC2 families

RDS instance classes are named the same way as EC2 instance types, just prefixed `db.` — e.g. `db.t3.micro`, `db.m6i.large`, `db.r6g.xlarge` — and correspond to the **same underlying hardware families** (`EC2/General-EC2` covers the T/M/R family distinctions in depth).

| Class family | Best for |
|---|---|
| **db.t*** (burstable) | Dev/test, light/spiky workloads — CPU credits, same burstable model as EC2 `t` instances |
| **db.m*** (general purpose) | Balanced production workloads |
| **db.r*** (memory-optimized) | Large working sets, heavy caching needs, analytics-adjacent workloads |
| **db.x*** (extreme memory) | The largest in-memory workloads |

---

## 2. Sizing considerations specific to RDS

- **Storage IOPS and throughput can be capped by instance class**, not just by the storage type itself (Note 15) — a small instance class paired with high-IOPS `io2` storage may not be able to actually use all that provisioned IOPS; the instance's own network/EBS bandwidth ceiling matters.
- Changing instance class **requires a brief outage** (or a failover, if Multi-AZ) — it's a modification applied during a maintenance window or immediately, at your choice, but it's not a zero-downtime resize.

> 🎯 **Exam tip:** "the database is CPU/memory-bound during peak load" points to **scaling up the instance class** (vertical scaling); "the database is read-bound" points instead to **Read Replicas** (Note 27) — a common exam distinction between vertical and horizontal read scaling.

---

## 3. Recap

- RDS instance classes reuse EC2's family naming and hardware characteristics, prefixed `db.` — burstable, general purpose, and memory-optimized families cover the vast majority of workloads.
- Instance class changes require a brief outage/failover, and the class itself can bottleneck storage performance below what the storage type alone could provide.
- Next: Note 15 — Storage In RDS, covering storage types and auto scaling.

### Sources
- [DB instance classes — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html)
- [Amazon RDS instance types](https://aws.amazon.com/rds/instance-types/)
