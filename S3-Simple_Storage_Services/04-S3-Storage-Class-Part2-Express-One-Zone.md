# 04 - AWS S3 Storage Class — Part 2: S3 Express One Zone

> Goal: understand **S3 Express One Zone** — a fundamentally different kind of storage class from Note 03's IA/Intelligent-Tiering family, built for raw **performance** rather than cost savings on cold data, and backed by a genuinely different bucket type.

---

## 1. What problem Express One Zone solves

Every storage class in Note 03 targets a **cost/access-frequency** trade-off. **S3 Express One Zone** targets a completely different axis: **request latency**, for the most demanding, latency-sensitive workloads — think high-frequency ML training data loading, real-time analytics, or ad-tech bidding pipelines where every millisecond of S3 request latency compounds across millions of requests.

- Delivers **single-digit millisecond** data access, described by AWS as up to **10x faster** than S3 Standard.
- Supports very high **request rates** (directory buckets can handle up to **2 million requests/second**).
- **Request costs up to ~80% lower** than S3 Standard, even though per-GB storage pricing is higher — the economics favor **request-heavy**, not just storage-heavy, workloads.

> 🧠 **Mental model:** if Standard/IA/Intelligent-Tiering are about "how cheaply can I store data I rarely touch," Express One Zone is about "how fast and how often can I possibly hit this data" — it's optimized for the opposite end of the access-frequency spectrum from Note 03's IA classes.

---

## 2. Directory buckets — a different bucket type entirely

Express One Zone doesn't live in a normal S3 bucket — it uses a new bucket type called a **directory bucket**:

- Organizes objects into a **real hierarchical namespace** (actual directories), unlike a normal bucket's flat key-with-slashes illusion (Note 02, Section 3) — this is one of the few places S3 genuinely departs from "everything is a flat key."
- Data is stored across multiple devices **within a single Availability Zone you choose** — not spread across 3+ AZs like Standard/Standard-IA/Intelligent-Tiering.
- **No minimum storage duration and no retrieval fee** — unlike Standard-IA/One Zone-IA's 30-day minimum (Note 03), Express One Zone is priced for **frequent, active** use, not infrequent access, so there's no penalty for reading it constantly or deleting it quickly.

> ⚠️ Being single-AZ means Express One Zone carries the **same durability trade-off as One Zone-IA** (Note 03) — if the chosen AZ is lost, the data in that directory bucket is lost with it. It should never hold the only copy of data that can't be regenerated or isn't backed up elsewhere.

---

## 3. What it integrates with

- **SSE-KMS support** for server-side encryption with customer-managed keys (same concept as Note 19, applied to directory buckets too).
- **S3 Batch Operations** for bulk copying data between general-purpose buckets and directory buckets.
- Native integration with **AWS Glue** (cataloging/ETL) and **Amazon SageMaker** (optimized training data channels) — reflecting its core audience of analytics and ML workloads.
- **S3 Inventory** support, for auditing/reporting on directory bucket contents just like a normal bucket.

---

## 4. When to actually choose it

| Situation | Express One Zone? |
|---|---|
| Millions of small, latency-sensitive requests per second (ML training, real-time analytics, ad-tech) | ✅ Yes — this is exactly its target workload |
| Cost-sensitive, infrequently accessed backups/archives | ❌ No — see Note 03 (IA classes) or Note 05 (Glacier family) instead |
| Data that must survive the loss of an entire Availability Zone | ❌ No — it's single-AZ by design, same caveat as One Zone-IA |
| General-purpose application storage with typical access patterns | ❌ No — S3 Standard remains the right default |

> 🎯 **Exam tip:** "extremely high request rate, single-digit millisecond latency required, e.g. for machine learning training data" is the signature Express One Zone scenario — a newer addition to the storage-class lineup, and one the exam increasingly expects you to distinguish from Standard's "just fast enough for typical apps" latency profile.

---

## 5. Recap

- **S3 Express One Zone** optimizes for **request latency and throughput**, not cost-per-GB for cold data — the opposite design goal from Note 03's IA classes.
- It uses a distinct **directory bucket** type with a real hierarchical namespace, confined to a **single Availability Zone**, with no minimum storage duration or retrieval fee.
- Same single-AZ durability caveat as One Zone-IA applies — never the only copy of irreplaceable data.
- Next: Note 05 — S3 Storage Class, Part 3: S3 Archive and Backup Storage Class, covering the Glacier family at the opposite end of the access-frequency spectrum.

### Sources
- [S3 Express One Zone — AWS](https://aws.amazon.com/s3/storage-classes/express-one-zone/)
- [Directory buckets — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-buckets-overview.html)
- [Differences for directory buckets — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-express-differences.html)
