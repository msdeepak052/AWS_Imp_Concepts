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

<details>

If you choose **"Choose from existing IAM role"** instead of letting S3 create one, you need an IAM role that S3 can assume and that has permissions on both the **source and destination buckets**.

For your example:

```text
Source:      ap-south-1
Destination: ap-southeast-1

Source bucket:      demo-source-bucket
Destination bucket: demo-destination-bucket
```

The replication flow is:

```text
                         AWS Account
                              │
                    ┌─────────┴─────────┐
                    │                   │
              Source Bucket       Destination Bucket
              ap-south-1          ap-southeast-1
                    │                   ▲
                    │                   │
                    ▼                   │
              S3 Replication ──────────┘
                    │
                    │ assumes
                    ▼
             S3ReplicationRole
```

The role has **two important pieces**:

1. **Trust policy** → allows S3 to assume the role.
2. **Permissions policy** → tells the role what S3 replication operations it can perform.

---

# 1. Create the IAM Role

Go to:

**AWS Console → IAM → Roles → Create role**

For:

### Trusted entity type

Select:

```text
AWS service
```

For the service/use case, choose:

```text
S3
```

If the console gives you a specific S3 replication use case, select that.

However, for learning purposes, you should understand the actual trust policy.

---

# 2. Trust Policy

The role needs to trust the **S3 service**.

The trust relationship should look like:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "s3.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

The important part is:

```json
"Principal": {
  "Service": "s3.amazonaws.com"
}
```

This means:

> S3 is allowed to assume this IAM role.

So:

```text
S3
 │
 │ sts:AssumeRole
 ▼
S3ReplicationRole
```

---

# 3. Create the Permissions Policy

Now the role needs permission to:

### Read from the source bucket

```text
demo-source-bucket
```

and:

### Write replication data to the destination bucket

```text
demo-destination-bucket
```

A good learning example is:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReadFromSource",
      "Effect": "Allow",
      "Action": [
        "s3:GetObjectVersionForReplication",
        "s3:GetObjectVersionAcl",
        "s3:GetObjectVersionTagging"
      ],
      "Resource": "arn:aws:s3:::demo-source-bucket/*"
    },
    {
      "Sid": "ReadSourceBucket",
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::demo-source-bucket"
    },
    {
      "Sid": "ReplicateToDestination",
      "Effect": "Allow",
      "Action": [
        "s3:ReplicateObject",
        "s3:ReplicateDelete",
        "s3:ReplicateTags"
      ],
      "Resource": "arn:aws:s3:::demo-destination-bucket/*"
    }
  ]
}
```

---

# 4. Understand what each permission does

This is easier if you split it into:

```text
             S3ReplicationRole
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
     SOURCE                DESTINATION
        │                       │
        │ READ                  │ WRITE
        ▼                       ▼
demo-source-bucket       demo-destination-bucket
```

### Source

```json
"s3:GetObjectVersionForReplication"
```

Allows S3 to retrieve the object version that needs to be replicated.

Because S3 replication works with **object versions**.

---

```json
"s3:GetObjectVersionAcl"
```

Allows S3 to read the object's ACL information when relevant.

---

```json
"s3:GetObjectVersionTagging"
```

Allows S3 to read object tags so they can be replicated.

---

```json
"s3:ListBucket"
```

Applies to:

```text
arn:aws:s3:::demo-source-bucket
```

rather than:

```text
arn:aws:s3:::demo-source-bucket/*
```

because `ListBucket` operates on the **bucket itself**.

---

# 5. Destination permissions

This is where S3 gets permission to create the replica.

```json
"s3:ReplicateObject"
```

Allows S3 to replicate objects.

```json
"s3:ReplicateDelete"
```

Allows replication of delete markers/deletions.

```json
"s3:ReplicateTags"
```

Allows S3 to replicate object tags.

These apply to:

```text
arn:aws:s3:::demo-destination-bucket/*
```

because we're talking about objects.

---

# 6. Your final role

So you would have:

```text
IAM
└── Roles
    └── S3ReplicationRole
         │
         ├── Trust Policy
         │     │
         │     └── S3 service
         │
         └── Permissions Policy
               │
               ├── Read source bucket
               │
               └── Replicate to destination
```

---

# 7. Then configure the replication rule

Go back to:

**S3 → demo-source-bucket → Management → Replication rules → Create replication rule**

Configure:

### Rule scope

```text
Apply to entire bucket
```

### Destination

```text
demo-destination-bucket
```

Region:

```text
ap-southeast-1
```

### IAM role

Choose:

```text
Choose from existing IAM role
```

Then select:

```text
S3ReplicationRole
```

Save the rule.

---

# 8. One important thing: versioning

Both buckets need Versioning enabled for normal S3 replication.

```text
Source
demo-source-bucket
Versioning: ENABLED ✓

             │
             │ Replication
             ▼

Destination
demo-destination-bucket
Versioning: ENABLED ✓
```

So before creating the rule:

```text
Source       → Versioning ON
Destination  → Versioning ON
```

---

# 9. If you enable "Replicate existing objects"

This is where your previous step becomes important.

Suppose before replication:

```text
Source bucket

file1.jpg
file2.jpg
file3.jpg
```

Then you create the replication rule.

Normally, the rule handles **new qualifying objects/versions** after replication is configured.

If you select:

> **Replicate existing objects**

S3 can backfill those existing objects using **S3 Batch Replication**.

Conceptually:

```text
Existing objects
      │
      ▼
S3 Batch Replication
      │
      ▼
Destination bucket
```

Your replication role therefore needs the permissions appropriate to the replication operation you're configuring.

---

## One more important real-world case: KMS

If your objects use:

```text
SSE-KMS
```

then the replication role also needs appropriate **KMS permissions**, and the destination KMS key policy must allow the replication workflow.

The architecture becomes:

```text
Source S3
   │
   │ encrypted with KMS
   ▼
KMS Key
   │
   ▼
S3 Replication Role
   │
   │ decrypt/read
   ▼
Destination
   │
   ▼
Destination KMS Key
   │
   │ encrypt
   ▼
Replicated Object
```

So the simple policy above is excellent for your **first replication demo with SSE-S3/default encryption**. For an SSE-KMS replication lab, add the KMS permissions and key-policy configuration separately.

### The key mental model

Don't memorize the JSON. Remember:

```text
                 S3 Replication
                       │
                       ▼
                Assume Role
                       │
                       ▼
              S3ReplicationRole
                  /          \
                 /            \
                ▼              ▼
        READ SOURCE        WRITE DESTINATION
             │                    │
             ▼                    ▼
       Source Bucket        Destination Bucket
```

**Trust policy:** `S3 → can assume this role`

**Identity policy:** `Role → can read source + replicate to destination`


</details>

5. Save the replication rule. For a new replication configuration or when adding a new destination, S3 may then ask whether to replicate existing objects. Choosing "Yes, replicate existing objects" creates an S3 Batch Replication job to backfill objects that existed before live replication was configured
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

![Uploading image.png…]()


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
## Additional replication options

**Four options are easy to mix up**, because three of them sound like "replication monitoring/sync." The easiest way is to take one real setup and see what each option changes.

Assume:

```text
Source bucket                         Destination bucket
ap-south-1                            ap-southeast-1

prod-source                           prod-dr
    │                                     │
    │────── S3 Replication ──────────────►│
```

You create a replication rule:

```text
prod-source
    │
    └── Replicate objects → prod-dr
```

The four options in your screenshot control **what happens beyond the basic object copy**.

---

# 1. Replication Time Control (RTC)

### What problem does it solve?

Normal S3 replication is **asynchronous**. You don't get a guaranteed replication time.

For example:

```text
10:00:00
Application uploads:
financial-report.pdf

        ↓

S3 starts replication

        ↓

10:00:05
Replica appears
```

Maybe it takes seconds.

But under load or unusual conditions, you don't have a 15-minute guarantee with ordinary replication.

### Enable RTC

When you enable:

> **Replication Time Control (RTC)**

S3 provides a **15-minute replication SLA**: 99.9% of new objects are replicated within 15 minutes according to the current AWS documentation. RTC also enables replication metrics and threshold events. ([AWS Documentation][1])

Think:

```text
              Object uploaded
                    │
                    ▼
              S3 Replication
                    │
                    │
             ┌──────┴──────┐
             │             │
          Usually       RTC
          seconds        │
                         ▼
                15-minute SLA
```

### Example

Suppose your business says:

> "Our DR copy must reach Mumbai/Singapore within a predictable time because of compliance requirements."

Then:

```text
Replication
      +
RTC
```

is appropriate.

### Important

RTC is **not**:

> "Make replication synchronous."

It is still asynchronous replication.

It's about a **predictable replication-time commitment**, not real-time synchronous copying.

---

# 2. Replication Metrics

This one is about **monitoring**, not making replication faster.

Suppose:

```text
Source
  │
  │ 10,000 objects
  ▼
Replication
  │
  ├── 9,500 replicated
  └── 500 pending
```

Without replication metrics, it's harder to get detailed visibility into replication backlog.

Enable:

> **Replication metrics**

and S3 provides metrics through CloudWatch, including:

```text
BytesPendingReplication
OperationsPendingReplication
OperationsFailedReplication
ReplicationLatency
```

AWS documents these as the main S3 replication metrics. ([AWS Documentation][2])

---

## Example

Suppose:

```text
Source bucket
       │
       │ replication
       ▼
Destination bucket
```

You upload:

```text
10 GB
```

and replication is taking time.

CloudWatch could show conceptually:

```text
Bytes Pending Replication
        7 GB

Operations Pending
        240

Replication Latency
        180 seconds

Operations Failed
        3
```

Now you know:

> "Replication is falling behind."

---

### RTC vs Replication Metrics

This is the easiest distinction:

```text
RTC
 │
 └── "How quickly must replication happen?"
             │
             └── 15-minute SLA

Replication Metrics
 │
 └── "What's happening with replication?"
             │
             ├── Pending?
             ├── Failed?
             ├── How many bytes?
             └── How much latency?
```

Also important: **RTC automatically enables replication metrics**, but you can enable replication metrics independently. ([AWS Documentation][2])

---

# 3. Delete Marker Replication

This one is particularly important because you've just learned about **S3 Versioning + Delete Markers**.

Suppose:

```text
Source bucket

financial-report.pdf

v3 ← CURRENT
v2
v1
```

You delete the object normally:

```text
DELETE financial-report.pdf
```

Because Versioning is enabled, S3 creates:

```text
DELETE MARKER ← CURRENT
v3
v2
v1
```

Now the question is:

> Should that delete marker also be replicated to the destination?

---

## Without Delete Marker Replication

Source:

```text
Source

DELETE MARKER
v3
v2
v1
```

Destination might still have:

```text
Destination

v3
```

So:

```text
Source:      object appears deleted
Destination: object still appears available
```

This is actually a **security/data-protection feature** of S3 replication by default. AWS says delete markers created by ordinary DELETE requests are not replicated by default for current replication configurations unless you enable delete-marker replication. ([AWS Documentation][3])

---

## With Delete Marker Replication

Enable:

> **Delete marker replication**

Now:

```text
Source
   │
   │ DELETE
   ▼
DELETE MARKER
   │
   │ replicated
   ▼
Destination
   │
   ▼
DELETE MARKER
```

Therefore:

```text
Source:
financial-report.pdf → appears deleted

Destination:
financial-report.pdf → appears deleted
```

AWS specifically notes that delete markers created by **S3 Lifecycle expiration rules are not replicated**, even when delete-marker replication is enabled. ([AWS Documentation][3])

---

# Why would you enable it?

Imagine a DR setup:

```text
Production                         DR
   │                                │
   ▼                                ▼
S3 Mumbai  ───── replication ───►  S3 Singapore
```

You want the DR bucket to behave like the source.

If a user deletes:

```text
customer-data/123.pdf
```

you may want:

```text
Mumbai
   │
   └── deleted

Singapore
   │
   └── deleted
```

Then enable **Delete Marker Replication**.

---

# 4. Replica Modification Sync

This is probably the most confusing option.

Normally replication is:

```text
SOURCE
   │
   │ object + metadata
   ▼
DESTINATION
```

It's basically **one-way**.

For example:

```text
Mumbai
  │
  │ replicate
  ▼
Singapore
```

Suppose:

```text
report.pdf
```

gets replicated.

Then you modify metadata **on the replica in Singapore**.

For example, you change:

```text
Tag:
Environment=Production
```

to:

```text
Environment=DR
```

By default:

```text
Singapore replica
       │
       └── metadata changed
              │
              X
              │
       Mumbai source
       doesn't automatically
       receive that change
```

---

# Enable Replica Modification Sync

With:

> **Replica modification sync**

S3 can synchronize supported metadata changes made to the replica **back to the source**.

AWS describes this as making metadata replication **bidirectional**. Supported metadata includes things such as object tags, ACLs, annotations, and Object Lock settings. ([AWS Documentation][4])

So:

```text
              Mumbai
             SOURCE
                │
                │ object replication
                ▼
             Singapore
             REPLICA
                │
                │ metadata changed
                │
                ▼
             Mumbai
             SOURCE
```

That's why the console says:

> "Replicate metadata changes to replicas from the destination bucket to the source bucket."

---

# Important: This does NOT mean full two-way object replication

This is a very common misunderstanding.

Replica Modification Sync is primarily about **metadata changes to replicas**, not:

> "Anything I upload in Singapore automatically becomes a new object in Mumbai."

For true two-way object replication, you configure replication rules in **both directions**:

```text
Mumbai
  │
  │ Rule 1
  ▼
Singapore

Singapore
  │
  │ Rule 2
  ▼
Mumbai
```

AWS describes this as two-way/bidirectional replication. ([AWS Documentation][5])

Replica Modification Sync helps keep **metadata changes** synchronized as part of that design. AWS also notes it needs to be enabled on the relevant source/destination buckets for the two-way setup. ([AWS Documentation][4])

---

# Putting all 4 together

Here's the easiest cheat sheet:

| Option                             | Main purpose                                          | Think                                                   |
| ---------------------------------- | ----------------------------------------------------- | ------------------------------------------------------- |
| **Replication Time Control (RTC)** | Predictable replication time                          | ⏱️ **15-min SLA**                                       |
| **Replication metrics**            | Monitor replication                                   | 📊 **What's happening?**                                |
| **Delete marker replication**      | Replicate deletes represented by delete markers       | 🗑️ **Delete on source → delete marker on destination** |
| **Replica modification sync**      | Sync metadata changes made on replicas back to source | 🔄 **Metadata can go back**                             |

---

# A complete real-world example

Imagine you're building:

```text
              Production
                  │
                  ▼
          S3 Mumbai Bucket
          prod-data-ap-south
                  │
                  │ CRR
                  ▼
          S3 Singapore Bucket
          dr-data-ap-southeast
```

You might configure:

### RTC

```text
☑ RTC
```

Because you have a business requirement for predictable replication time.

### Replication Metrics

```text
☑ Replication metrics
```

So CloudWatch can tell you:

```text
Objects pending
Bytes pending
Replication latency
Failed operations
```

### Delete Marker Replication

```text
☑ Delete marker replication
```

Because you want a normal user deletion in production to also make the object appear deleted in DR.

### Replica Modification Sync

```text
☑ Replica modification sync
```

If you have a **two-way replication/failover architecture** and need metadata changes made to replicas to synchronize back to the source.

---

# One picture to remember

```text
                       S3 REPLICATION
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
        SPEED             MONITORING          DATA
          │                  │                  │
          ▼                  ▼                  ├── Delete markers
        RTC              Replication           │
          │               Metrics              │
          │                  │                 │
          │                  │                 └── Metadata
          │                  │                     sync
          ▼                  ▼                       │
     "Within 15m"      "What's pending?"             ▼
                                               Replica Modification
                                                     Sync
```

### If you're doing a normal S3 CRR lab

I'd start with:

```text
☐ RTC
☑ Replication metrics
☐ Delete marker replication
☐ Replica modification sync
```

Then test each option individually.

For a **production DR/compliance architecture**, the choices depend on the business requirements—you don't automatically turn all four on. In particular, **RTC and CloudWatch replication metrics incur additional charges**, and delete-marker/metadata synchronization changes the behavior of your DR copy. ([AWS Documentation][2])

[1]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-time-control.html?utm_source=chatgpt.com "Meeting compliance requirements with S3 Replication Time Control - Amazon Simple Storage Service"
[2]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/repl-metrics.html?utm_source=chatgpt.com "Using S3 Replication metrics - Amazon Simple Storage Service"
[3]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/delete-marker-replication.html?utm_source=chatgpt.com "Replicating delete markers between buckets - Amazon Simple Storage Service"
[4]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-for-metadata-changes.html?utm_source=chatgpt.com "Replicating metadata changes with replica modification sync - Amazon Simple Storage Service"
[5]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/mrap-create-two-way-replication-rules.html?utm_source=chatgpt.com "Create two-way replication rules for your Multi-Region Access Point - Amazon Simple Storage Service"


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
