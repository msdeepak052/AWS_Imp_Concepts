# 30 - AWS S3 Cross-Region Replication (CRR) (Hands-On)

> Goal: configure automatic, ongoing replication of objects from a bucket in one Region to a bucket in another — covering the hard prerequisites, what does/doesn't get replicated automatically, and how this differs from a one-time snapshot copy.

---

## 1. What CRR does, and why it's not just "copy the bucket once"

**Cross-Region Replication (CRR)** continuously and automatically copies **new** object writes (and optionally, existing objects via **Batch Replication**, Section 5) from a **source** bucket to a **destination** bucket in a **different Region**, asynchronously, typically completing within minutes. This is fundamentally different from a one-time backup/copy — it's an ongoing, live-replicating relationship between two buckets.

> 🧠 **Mental model:** CRR is S3's equivalent of the CloudMart capstone's cross-AZ redundancy idea, but at the Region level and for object storage specifically — a second, geographically-distant copy of your data that stays in sync automatically, for disaster recovery, latency reduction (serving users from a nearer Region), or compliance (data residency requirements needing a copy in a specific Region).

---

## 2. The hard prerequisites

1. **Versioning must be enabled on both the source and destination buckets** — CRR relies on the same Version ID mechanism from Note 06 to track exactly which object versions have and haven't been replicated yet.
2. An **IAM role** that S3 replication assumes on your behalf, with permission to read from the source bucket and write to the destination bucket.
3. Source and destination buckets **must be in different Regions** (same-Region replication, **SRR**, is also available for same-Region use cases like log aggregation across accounts, but CRR specifically means cross-Region).

---

## 3. Configure CRR via the console

1. **S3 console** → source bucket → confirm **Versioning** is enabled (Note 06) → **Management** tab → **Create replication rule**.
2. **Source bucket scope**: apply to the whole bucket, or filter by prefix/tag (same filtering model as Lifecycle rules, Note 07).
3. **Destination**: choose (or create) a bucket in a **different Region** — e.g. source in `ap-south-1`, destination in `ap-southeast-1`.
4. **IAM role**: let the console **create a new role** automatically (recommended for this exercise) — it generates exactly the trust and permissions policy needed.
5. Optionally check **Replicate existing objects** to also backfill objects that existed **before** this rule was created (this uses **S3 Batch Replication** under the hood, a related but distinct one-time bulk operation).
6. **Save**.

---

## 4. What gets replicated automatically, and what doesn't

| Does replicate | Does NOT replicate (by default) |
|---|---|
| New objects written **after** the rule is created | Objects that existed **before** the rule was created (unless Batch Replication/backfill is explicitly enabled) |
| Object metadata, tags, ACLs (if configured to include them) | Objects encrypted with **SSE-C** (Note 22) — since S3 never has the key, it cannot replicate what it cannot decrypt/re-encrypt |
| Object deletions, if **delete marker replication** is explicitly enabled | Actual permanent version deletions (a specific Version ID being hard-deleted) — this is deliberately never replicated, to avoid one accidental hard-delete silently propagating and destroying the DR copy too |

> ⚠️ **A permanent delete of a specific version is never replicated**, even with delete marker replication enabled — this is an intentional safety boundary: CRR happily replicates the "soft delete" (a new delete marker, Note 06) but never a hard, unrecoverable version deletion, precisely so that CRR itself can never become the vector for propagating an catastrophic accidental (or malicious) permanent deletion to the DR copy.

---

## 5. Backfilling pre-existing objects with Batch Replication

If a replication rule is added to a bucket that already has years of existing objects, those pre-existing objects are **not** retroactively replicated by the standard rule alone — checking **Replicate existing objects** at rule-creation time (Section 3, step 5) invokes **S3 Batch Replication**, a distinct one-time bulk job that walks the existing inventory and replicates everything that predates the rule.

---

## 6. Verify

```bash
aws s3 cp test-file.txt s3://source-bucket-ap-south-1/
# wait a few minutes
aws s3 ls s3://destination-bucket-ap-southeast-1/
```
The object appears in the destination bucket shortly after being written to the source — no manual copy step involved.

> 🎯 **Exam tip:** "we need a live, ongoing, automatically-synced copy of new objects in a different Region for disaster recovery or lower-latency regional access" is the **CRR** scenario. If instead the question describes a one-time migration of already-existing data, that's a **Batch Replication** or a manual `aws s3 sync`/`cp --recursive` job, not standard CRR's ongoing behavior.

---

## 7. Recap

- **CRR** requires **versioning enabled on both** buckets, an **IAM role**, and buckets in **different Regions** — it continuously replicates new writes, not a one-time copy.
- Pre-existing objects need explicit **Batch Replication** (the "Replicate existing objects" checkbox) to be backfilled.
- **SSE-C encrypted objects never replicate** (S3 lacks the key); **permanent version deletions never replicate**, by deliberate design, even with delete marker replication on.
- Next: Note 31 — AWS S3 Transfer Acceleration (Hands-On), speeding up **uploads** to a bucket from geographically distant clients — a different problem from CRR's post-upload, bucket-to-bucket replication.

### Sources
- [Replicating objects — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html)
- [Setting up replication — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-how-setup.html)
- [Replicating delete markers between buckets — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/delete-marker-replication.html)
- [S3 Batch Replication — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-batch.html)
