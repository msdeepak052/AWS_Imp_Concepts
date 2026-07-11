# 28 - AWS RDS Readable Standby Instance Vs Read Replica

> Goal: directly resolve the recurring point of confusion between Note 10's Multi-AZ DB Cluster readable standbys and Note 27's Read Replicas — both serve reads, for very different reasons.

---

## 1. Side-by-side

| | Readable Standby (Multi-AZ DB Cluster, Note 10) | Read Replica (Note 27) |
|---|---|---|
| Primary purpose | High availability, with read capacity as a bonus | Read scaling, as the primary purpose |
| Replication | Semi-synchronous, engine-native | Asynchronous |
| Count | Exactly 2, fixed | Up to 5 direct (more via chaining) |
| Location | Same Region, different AZs (3 AZs total) | Same Region, cross-Region, or engine-dependent chaining |
| Failover role | Automatic promotion on primary failure (under ~35s) | Manual promotion only — breaks replication permanently |
| Engine support | MySQL, PostgreSQL only | Broad engine support |
| Endpoint | Cluster reader endpoint (automatically load-balances across both) | Each replica has its own distinct endpoint |

---

## 2. The core distinction

- A **readable standby** exists **first and foremost for HA** — its readability is a bonus feature layered on top of a failover mechanism.
- A **Read Replica** exists **first and foremost for read scaling** — any HA use (manual promotion during disaster recovery) is a secondary, deliberate, replication-breaking action.

> 🎯 **Exam tip:** if a scenario needs **both** fast automatic failover **and** extra read capacity, on MySQL/PostgreSQL, that's the strongest possible signal for **Multi-AZ DB Cluster** specifically — it gets you both properties from one feature, whereas combining Multi-AZ DB Instance + Read Replicas achieves a similar result via two separate features.

---

## 3. Recap

- Readable standbys (Multi-AZ DB Cluster) are an HA mechanism with read capacity as a bonus; Read Replicas are a read-scaling mechanism with manual-promotion DR as a bonus — the purposes are inverted, even though both "serve reads from a secondary instance."
- Next: Note 29 — AWS RDS Blue/Green Deployment, covering safe, low-downtime engine/schema upgrades.

### Sources
- [Multi-AZ DB cluster deployments — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/multi-az-db-clusters-concepts.html)
- [Working with DB instance read replicas — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html)
