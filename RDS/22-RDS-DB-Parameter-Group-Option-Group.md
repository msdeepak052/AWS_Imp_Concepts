# 22 - AWS RDS - DB Parameter Group & Option Group

> Goal: cover how RDS exposes engine-level tuning without giving you OS-level config file access — the mechanism reconciling Note 04's "you don't get root access" trade-off.

---

## 1. DB Parameter Groups

A **DB Parameter Group** is a named collection of **engine configuration parameters** (e.g. `max_connections`, buffer/cache sizes, timeout values) — the equivalent of hand-editing `my.cnf` or `postgresql.conf` yourself, exposed instead as a managed, API-controlled set of key-value settings.

- Every DB instance uses **exactly one** parameter group (per engine/version).
- **Default parameter groups** are AWS-managed and **cannot be modified** — you must create a **custom parameter group**, copy in your desired changes, and attach it to the instance.
- Some parameters apply **immediately**; others are **"pending reboot"** and only take effect after the instance restarts.

> 🧠 **Mental model:** the parameter group is RDS's answer to "I need engine-level tuning, but you won't give me the actual config file" — same underlying knobs, just exposed as a managed API resource instead of a flat file you'd SSH in to edit.

---

## 2. Option Groups

An **Option Group** enables **optional engine features/plugins** that aren't part of the engine's core configuration — e.g. Oracle's Transparent Data Encryption, SQL Server's Native Backup/Restore, or MySQL's `MEMCACHED` interface.

- Not every engine uses option groups the same way — MySQL/PostgreSQL rely more heavily on parameter groups; Oracle/SQL Server use option groups more extensively for licensed add-on features.

---

## 3. Recap

- **Parameter Groups** manage core engine configuration values (some immediate, some requiring reboot); **Option Groups** enable optional engine features/plugins — both exist because RDS won't give you direct config-file or OS-level access.
- Both require a **custom** group (not the read-only default) to make any changes.
- Next: Note 23 — RDS Automated Backups & Manual Snapshots.

### Sources
- [Working with DB parameter groups — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithParamGroups.html)
- [Working with option groups — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithOptionGroups.html)
