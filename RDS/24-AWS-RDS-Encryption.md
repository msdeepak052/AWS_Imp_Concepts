# 24 - AWS RDS Encryption

> Goal: cover RDS encryption at rest and in transit, and the one hard rule that trips people up most — encryption at rest **cannot be enabled after instance creation**.

---

## 1. Encryption at rest

- Backed by **AWS KMS** — encrypts the underlying storage, automated backups, manual snapshots, and Read Replicas.
- Uses **industry-standard AES-256**, applied transparently — no application-level changes needed.
- Can be enabled with the **AWS-managed key** or a **customer-managed KMS key** (for control over key rotation/policy — same trade-off as `S3-Simple_Storage_Services`'s SSE-S3 vs. SSE-KMS coverage).

> ⚠️ **The hard rule**: encryption at rest **must be chosen at DB instance creation time** — you **cannot** enable it on an existing unencrypted instance directly. The workaround is to take a **snapshot** of the unencrypted instance, **copy that snapshot while enabling encryption**, then **restore a new instance** from the encrypted copy — same "restore creates a new instance" mechanic as Note 23.

---

## 2. Encryption in transit

- RDS supports **SSL/TLS** connections between the client and the database engine, independent of at-rest encryption.
- Some engines/configurations can **enforce** SSL/TLS (rejecting unencrypted connections) via a parameter group setting (Note 22).

---

## 3. Encrypted Read Replicas and Multi-AZ

- A Read Replica or Multi-AZ standby of an **encrypted** source is **always encrypted** with the same key (or a re-encrypted copy, for cross-Region replicas using a Region-specific KMS key).
- You **cannot** create an unencrypted Read Replica of an encrypted source, or vice versa.

> 🎯 **Exam tip:** "we forgot to enable encryption and now need to encrypt an existing database" is a classic scenario testing whether you know the **snapshot → copy with encryption → restore** workaround, since there's no direct "enable encryption" toggle on a live instance.

---

## 4. Recap

- Encryption at rest (KMS-backed, AES-256) must be chosen at creation time — retrofitting it onto an existing instance requires the snapshot-copy-restore workaround.
- Encryption in transit (SSL/TLS) is independent and can be enforced via parameter groups.
- Next: Note 25 — AWS RDS Log Exports.

### Sources
- [Encrypting Amazon RDS resources — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.Encryption.html)
- [Using SSL/TLS to encrypt a connection — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL.html)
