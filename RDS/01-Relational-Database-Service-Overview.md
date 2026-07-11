# 01 - Relational Database Service (RDS)

> Goal: set the stage for this whole folder — what RDS is, in one sentence, and the roadmap of what's covered across the notes that follow, before going deep on databases in general (Note 02) and RDS specifically (Note 03).

---

## 1. The one-sentence version

**Amazon RDS (Relational Database Service)** is a **managed relational database** service — AWS runs and operates the underlying database engine (MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, or Aurora) for you, taking over the operational burden (patching, backups, replication, failover) that you'd otherwise have to handle yourself running a database on EC2.

> 🧠 **Mental model:** this is the same "managed vs. self-managed" trade-off this repo has already seen elsewhere — e.g. `EC2-Storage`'s EFS/FSx (managed file systems) vs. running your own NFS server on EC2. RDS is that same trade-off, applied to relational databases.

---

## 2. What this folder covers

- **Notes 02-05**: database fundamentals, what RDS actually is, why you'd choose it, and how it compares to running a database yourself on EC2 or on-premises.
- **Notes 06-07**: hands-on labs — launching an RDS instance and connecting to it from EC2.
- **Notes 08-11**: availability and durability options — Single-AZ, Multi-AZ DB instance, Multi-AZ DB cluster, and how to choose between them.
- **Notes 12-17**: the actual instance configuration surface — settings, credentials, instance sizing, storage, connectivity, and authentication.
- **Notes 18-22**: monitoring and configuration management — Performance Insights, Enhanced Monitoring, CloudWatch, and Parameter/Option Groups.
- **Notes 23-26**: operational concerns — backups/snapshots, encryption, log exports, maintenance windows.
- **Notes 27-31**: scaling and modern features — Read Replicas, readable standbys, Blue/Green deployments, RDS Proxy, and Zero-ETL integration.
- **Notes 32-36**: ElastiCache as a caching layer in front of RDS.
- **Note 37**: restoring a database from S3.
- **Note 38**: Amazon Aurora, RDS's AWS-native, high-performance engine.
- **Note 39**: a closing, whole-database-landscape overview.

> ⚠️ This folder's pre-existing `RDS.md`, `RDS-2.md`, and `Aurora/Auroora_DB.md` files are earlier, unstructured notes kept only as background reference — they are **not** the template for these numbered notes, which follow this repo's standard structured convention instead.

---

## 3. Recap

- RDS is AWS's **managed relational database** service, removing the operational burden of running a database engine yourself.
- This folder is organized into fundamentals → hands-on → availability → configuration → monitoring → operations → scaling/modern features → caching → Aurora → a closing overview.
- Next: Note 02 — Introduction Of Database, covering relational database fundamentals before RDS specifics.

### Sources
- [What is Amazon Relational Database Service (Amazon RDS)? — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)
- [Amazon RDS product page](https://aws.amazon.com/rds/)
