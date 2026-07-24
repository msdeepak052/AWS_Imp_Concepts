# 07 - AWS S3 Lifecycle Rule — Part 1

> Goal: author a **Lifecycle rule** that automatically **transitions** objects between storage classes as they age — turning the manual "move data to cheaper storage over time" idea from Notes 03-05 into a set-once, self-enforcing policy. Part 2 (Note 08) covers the **expiration** side (deleting objects/old versions).

---

## 1. What a Lifecycle rule is

A **Lifecycle rule** is a bucket-level configuration that automatically applies **actions** (Section 2) to objects matching a **scope** (a prefix and/or tag filter, or the whole bucket) once they reach a specified **age**. It runs continuously and automatically, in the background — exactly the same "set a rule, let AWS enforce it" philosophy as `EC2-Storage/11`'s Data Lifecycle Manager, just applied to S3 objects instead of EBS snapshots.

> 🧠 **Mental model:** a Lifecycle rule is S3's version of "someone should really move these old files to the cheap archive drive, and delete the really old ones" — except it's AWS doing it automatically, on a schedule you define once, instead of a person remembering to do it manually (or, more realistically, not remembering, and letting cold data sit in expensive Standard storage forever).

---

## 2. Transition actions — moving data down the cost ladder

A transition action says: *"once an object (or a specific version) reaches N days old, move it to storage class X."*

```json
{
  "Rules": [
    {
      "ID": "age-out-old-reports",
      "Filter": { "Prefix": "reports/" },
      "Status": "Enabled",
      "Transitions": [
        { "Days": 30, "StorageClass": "STANDARD_IA" },
        { "Days": 90, "StorageClass": "GLACIER" },
        { "Days": 365, "StorageClass": "DEEP_ARCHIVE" }
      ]
    }
  ]
}
```

This single rule automatically ages any object under the `reports/` prefix: Standard → Standard-IA at 30 days → Glacier Flexible Retrieval at 90 days → Deep Archive at 365 days, with **zero manual intervention** after the rule is created.

> ⚠️ Transitions must move **down** the cost/retrieval-speed ladder in AWS's defined order (e.g. you can't configure a transition straight from Standard into Deep Archive skipping the required minimum-day thresholds along the way in some configurations) — and transitions **into Standard-IA or One Zone-IA require the object be at least 30 days old**, matching those classes' own minimum storage duration from Note 03.

---

## 3. Filtering scope — prefix and tags

- **Prefix filter**: apply the rule only to keys starting with a given prefix (e.g. `logs/`, `reports/2025/`) — the most common scoping method.
- **Tag filter**: apply the rule only to objects carrying a specific tag (e.g. `Environment: dev`) — useful when the objects to target aren't cleanly separated by key prefix.
- **No filter at all**: applies to every object in the bucket.

---

## 4. Create a lifecycle rule via the console

1. **S3 console** → open a bucket → **Management** tab → **Create lifecycle rule**.
2. **Rule name**: `age-out-old-reports`.
3. **Rule scope**: **Limit the scope** → **Prefix**: `reports/`.
4. **Lifecycle rule actions** → check **Transition current versions of objects between storage classes** → add transitions: `30 days → Standard-IA`, `90 days → Glacier Flexible Retrieval`, `365 days → Glacier Deep Archive`.
5. **Create rule**.

---

## 5. Transitions apply per-version when versioning is on

If the bucket has versioning enabled (Note 06), the console/API distinguishes between transitioning **current versions** and **non-current (previous) versions** separately — each can have its own age thresholds and target storage classes. This distinction becomes especially important once expiration actions (Note 08) enter the picture, since a rule might want to keep the *current* version in Standard-IA indefinitely while aggressively archiving or deleting *old* versions much sooner.

> 🎯 **Exam tip:** "reduce storage costs for data that's rarely accessed after a known period, without manual intervention" is the textbook Lifecycle-rule scenario — if the access pattern is instead described as unknown or unpredictable, that points back to **Intelligent-Tiering** (Note 03) instead, which doesn't need a hand-authored rule at all.

---

## 6. Recap

- A **Lifecycle rule** automatically transitions objects between storage classes based on age, scoped by prefix and/or tag — the automated version of the manual cost-tiering trade-offs from Notes 03-05.
- Transitions must respect each target class's minimum age rules (e.g. 30 days before Standard-IA/One Zone-IA) and move down the cost ladder in order.
- When versioning is enabled, current and non-current versions can have independent transition schedules.
- Next: Note 08 — S3 Lifecycle Rule, Part 2, covering **expiration actions** — actually deleting objects and old versions once they're no longer needed at all.

### Sources
- [Managing your storage lifecycle — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)
- [Transitioning objects using Amazon S3 Lifecycle — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-transition-general-considerations.html)
- [Elements to describe lifecycle actions — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html)
