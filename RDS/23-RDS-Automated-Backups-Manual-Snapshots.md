# 23 - RDS Automated Backups & Manual Snapshots

> Goal: cover both RDS backup mechanisms — automated, continuous backups enabling point-in-time recovery, and manual, retained-until-deleted snapshots — and when each is the right tool.

---

## 1. Automated backups

- Enabled by default, with a configurable **retention period (1-35 days)** and a **backup window**.
- Takes a **daily full snapshot** plus **continuously captures transaction logs**, enabling **point-in-time recovery (PITR)** to any second within the retention window (not just to the daily snapshot boundary).
- Automated backups (and their transaction logs) are **automatically deleted** when the retention period elapses, and are **deleted entirely if the DB instance itself is deleted** (unless you explicitly choose to retain a final snapshot at deletion time).

---

## 2. Manual snapshots

- Taken **on demand**, at any point you choose.
- **Persist indefinitely** — until you explicitly delete them — regardless of retention period settings, and **survive deletion of the source DB instance**.
- Can be **shared across AWS accounts** or **copied to another Region**, the same cross-account/cross-region patterns this repo's `EC2-Storage` folder covered for EBS snapshots.

---

## 3. Restoring from either

Restoring **always creates a new DB instance** with a new endpoint — you cannot "restore in place" onto the existing instance. This means application connection strings need to be updated (or a DNS/endpoint abstraction layer used) after any restore.

> 🎯 **Exam tip:** "restore to a specific point in time" (any second, not just a snapshot boundary) signals **automated backups + PITR**; "keep a backup indefinitely, even after deleting the instance" or "share a backup with another account/Region" signals **manual snapshots**.

---

## 4. Recap

- **Automated backups** provide point-in-time recovery to any second within a 1-35 day retention window, but are lost if the instance is deleted (unless a final snapshot is retained); **manual snapshots** persist indefinitely and can be shared/copied cross-account/cross-Region.
- Both restore as a **brand-new DB instance**, never in place.
- Next: Note 24 — AWS RDS Encryption.

### Sources
- [Backing up and restoring an Amazon RDS DB instance — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_CommonTasks.BackupRestore.html)
- [Creating a DB snapshot — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_CreateSnapshot.html)
