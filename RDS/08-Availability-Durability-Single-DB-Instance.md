# 08 - RDS Availability & Durability Single DB Instance

> Goal: understand exactly what a Single-AZ (single instance) RDS deployment gives you — and, more importantly, what it does *not* give you — as the baseline before Multi-AZ options (Notes 09-10).

---

## 1. What a Single DB instance is

The simplest RDS deployment: **one DB instance**, in **one AZ**, with storage on **EBS volumes** in that same AZ.

- **Durability**: EBS volumes replicate data **within their AZ** automatically — a single disk failure doesn't lose data.
- **Availability**: if that **entire AZ** has an outage, or the instance itself fails (hardware issue, OS crash), the database is **unavailable** until AWS (or you) recovers it — there is **no automatic failover** to another AZ.

> ⚠️ Single-AZ durability (EBS-level replication within an AZ) is **not** the same as availability across AZ failures — a common point of confusion. Note 09/10 add the **cross-AZ** protection this deployment lacks entirely.

---

## 2. Backups still apply

Even a Single-AZ instance gets **automated backups** and the ability to take **manual snapshots** (Note 23) — these protect against **data loss** (e.g. accidental deletion, corruption) via point-in-time recovery, but recovery from a backup is **not fast failover** — it means provisioning a new instance from the backup/snapshot, which takes time.

> 🎯 **Exam tip:** "Single-AZ" in a scenario is a strong signal of a **cost-optimized, non-critical** workload (e.g. dev/test) — any requirement mentioning "high availability" or "minimize downtime during an AZ failure" rules out Single-AZ and points to Multi-AZ (Notes 09-10).

---

## 3. Recap

- A Single DB instance deployment has **no cross-AZ redundancy** — an AZ-level or instance-level failure causes real downtime until manual/automated recovery from backup.
- EBS-level durability within the AZ and backup-based data protection still apply, but neither substitutes for the automatic failover Multi-AZ options provide.
- Next: Note 09 — RDS Availability & Durability Multi-AZ DB Instance, adding a standby in a second AZ.

### Sources
- [Amazon RDS instances — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.DBInstance.html)
- [High availability for Amazon RDS — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html)
