# 08 - AWS S3 Lifecycle Rule — Part 2

> Goal: cover the other half of Lifecycle rules — **expiration actions** that actually delete objects, non-current versions, and delete markers, plus the incomplete-multipart-upload cleanup action — completing the automated storage-hygiene picture Note 07 started.

---

## 1. Expiration actions — the four flavors

| Action | What it deletes | Applies to |
|---|---|---|
| **Expire current version** | The current version of an object, after N days | Any bucket |
| **Permanently delete non-current versions** | Old (non-current) versions, after N days of being non-current | Versioning-enabled buckets |
| **Delete expired object delete markers** | A delete marker that has become "orphaned" (no non-current versions left underneath it) | Versioning-enabled buckets |
| **Delete incomplete multipart uploads** | Parts from a multipart upload (Note 38) that was started but never completed or aborted | Any bucket |

> 🧠 **Mental model:** Note 07's transitions move data to cheaper storage; this note's expirations **remove it entirely**. A mature lifecycle policy almost always uses both together: transition current versions down the cost ladder while they're still "current," and aggressively expire non-current versions and abandoned multipart uploads that serve no ongoing purpose.

---

## 2. Expire current versions

```json
{
  "Rules": [
    {
      "ID": "expire-old-logs",
      "Filter": { "Prefix": "logs/" },
      "Status": "Enabled",
      "Expiration": { "Days": 365 }
    }
  ]
}
```

Any object under `logs/` is **permanently deleted** 365 days after its creation date — on a versioned bucket, this specifically means the current version becomes a delete marker (Note 06's mechanics), not an instant hard-delete of data, unless combined with non-current-version expiration (Section 3) to also clean up what's left underneath.

---

## 3. Expire non-current versions — the essential pairing with versioning

This is the action that actually controls the storage-cost problem versioning introduces (Note 06, Section 4):

```json
{
  "Rules": [
    {
      "ID": "clean-up-old-versions",
      "Filter": {},
      "Status": "Enabled",
      "NoncurrentVersionExpiration": { "NoncurrentDays": 90 }
    }
  ]
}
```

Any version that has been **non-current** (i.e., superseded by a newer upload) for 90 days is permanently deleted — keeping a bounded, recent version history instead of every version ever created accumulating forever.

> ⚠️ **Enabling versioning without ever pairing it with a non-current-version-expiration rule is one of the most common real-world S3 cost surprises** — buckets with frequent overwrites (e.g. a nightly backup job overwriting the same key) can silently accumulate years of full-price version history with no automatic cleanup unless a rule like this exists.

---

## 4. Clean up incomplete multipart uploads

```json
{
  "Rules": [
    {
      "ID": "abort-incomplete-uploads",
      "Filter": {},
      "Status": "Enabled",
      "AbortIncompleteMultipartUpload": { "DaysAfterInitiation": 7 }
    }
  ]
}
```

A multipart upload (Note 38) that's started but never finished (e.g. a client crashed mid-upload) leaves **already-uploaded parts sitting in the bucket, billed as storage**, even though no complete object ever resulted. This action automatically aborts and cleans up any such abandoned upload after 7 days — a low-effort, easy-to-forget cost-hygiene rule that AWS explicitly recommends enabling on every bucket that accepts multipart uploads.

> 🎯 **Exam tip:** "storage costs are higher than expected, and the bucket accepts large file uploads" is a common signal pointing at **abandoned multipart uploads** as the hidden cause — the fix is exactly this lifecycle action, not a change to storage class.

---

## 5. Combining transitions and expirations in one rule

A single Lifecycle rule can include **both** transition and expiration actions together, applying the full aging pipeline in one place:

```json
{
  "Rules": [
    {
      "ID": "full-lifecycle-reports",
      "Filter": { "Prefix": "reports/" },
      "Status": "Enabled",
      "Transitions": [
        { "Days": 30, "StorageClass": "STANDARD_IA" },
        { "Days": 90, "StorageClass": "GLACIER" }
      ],
      "Expiration": { "Days": 2555 },
      "NoncurrentVersionExpiration": { "NoncurrentDays": 90 }
    }
  ]
}
```

Reports age from Standard → Standard-IA (30d) → Glacier (90d) → permanently deleted after ~7 years (2,555 days, a common compliance retention window), while any superseded version is cleaned up after 90 days non-current.

---

## 6. Recap

- **Expiration actions** delete current versions, non-current versions, orphaned delete markers, and abandoned multipart upload parts — the cleanup half of Lifecycle rules, complementing Note 07's transitions.
- **Non-current-version expiration is the essential pairing with versioning (Note 06)** — without it, version history can silently accumulate full-price storage costs indefinitely.
- **Aborting incomplete multipart uploads** after a set number of days is a recommended, low-effort default on any bucket accepting large uploads.
- This closes the two-part Lifecycle rule series (Notes 07-08). Next: Note 09 — Controlling Access To AWS S3 Buckets, moving from storage-cost automation to who can actually read/write this data.

### Sources
- [Expiring objects — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html#intro-lifecycle-rules-actions)
- [Setting lifecycle configuration on a bucket — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/how-to-set-lifecycle-configuration-intro.html)
- [Aborting incomplete multipart uploads — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpu-abort-incomplete-mpu-lifecycle-config.html)
