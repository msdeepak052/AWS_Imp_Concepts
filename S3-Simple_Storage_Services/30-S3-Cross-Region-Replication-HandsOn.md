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
