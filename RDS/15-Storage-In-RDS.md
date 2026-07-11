# 15 - Storage In RDS

> Goal: cover RDS storage types and storage auto scaling — the EBS-backed storage layer underneath every RDS instance (excluding Aurora, which uses a different, distributed storage architecture — Note 38).

---

## 1. Storage types

| Type | Best for |
|---|---|
| **General Purpose SSD (gp3)** | Default choice for most workloads — baseline IOPS/throughput included, both **independently scalable** without resizing the volume itself (same `gp3` model as `EC2-Storage`'s EBS notes) |
| **Provisioned IOPS SSD (io1/io2)** | I/O-intensive production workloads needing consistent, high IOPS beyond what gp3 offers |
| **Magnetic (deprecated)** | Legacy only — not recommended for new deployments |

> 🧠 This directly mirrors `EC2-Storage/03` through `05`'s EBS volume type coverage — RDS storage **is** EBS storage under the hood (for non-Aurora engines), so the same gp3-vs-io2 trade-offs apply.

---

## 2. Storage auto scaling

- RDS can **automatically increase allocated storage** when free space drops below a threshold, up to a **maximum you configure** — removing the need to manually monitor and resize storage (one of Note 04's self-managed pains).
- Storage can only **grow**, never shrink automatically — shrinking requires creating a new, smaller instance and migrating data.

---

## 3. Recap

- RDS storage (for non-Aurora engines) is EBS-backed, offering the same `gp3`/`io1`/`io2` trade-offs as standalone EC2 storage.
- **Storage auto scaling** removes manual capacity monitoring, growing storage automatically up to a configured ceiling — but never shrinking automatically.
- Next: Note 16 — AWS RDS Connectivity, covering VPC placement, subnet groups, and public access.

### Sources
- [Storage for Amazon RDS DB instances — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Storage.html)
- [Working with storage auto scaling — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIOPS.StorageTypes.html#USER_PIOPS.Autoscaling)
