# 33 - AWS S3 CloudTrail Data Events

> Goal: enable **CloudTrail data events** for S3 — object-level API activity logging, distinct from CloudTrail's default (management-event-only) behavior, and the stronger, near-real-time alternative to Note 32's server access logs.

---

## 1. Management events vs. data events — the key CloudTrail distinction

**AWS CloudTrail** logs API calls across virtually every AWS service, but splits them into two categories:

| Event type | What it covers | Logged by default? |
|---|---|---|
| **Management events** | Control-plane operations — creating/deleting/configuring resources (e.g. `CreateBucket`, `PutBucketPolicy`) | ✅ Yes, by default |
| **Data events** | Data-plane operations — actually **reading or writing the data itself** (e.g. `GetObject`, `PutObject`) | ❌ **No** — must be explicitly enabled, since data events can be extremely high-volume |

By default, CloudTrail tells you **"someone changed this bucket's policy"** but not **"someone downloaded this specific object."** **S3 data events** is the setting that closes that gap.

> 🧠 **Mental model:** management events are like a log of "who rearranged the furniture in the store" — data events are "who actually picked up and bought (or returned) a specific item." Both matter, but they're tracked separately because the second one happens at vastly higher volume.

---

## 2. Enable S3 data events

1. **CloudTrail console** → **Trails** → select an existing trail (or create one) → **Edit**.
2. **Data events** → **Add data event type** → select **S3**.
3. Scope to **all S3 buckets in this account**, or a **specific bucket** (recommended for cost control, Section 4) → choose which operations to log (**Read**, **Write**, or both).
4. **Save changes**.

---

## 3. CloudTrail data events vs. server access logging (Note 32)

| | Server access logging (Note 32) | CloudTrail data events |
|---|---|---|
| Delivery speed | Best-effort, typically hours | Near-real-time (minutes) |
| Guaranteed delivery | No — best-effort | Stronger guarantee, backed by CloudTrail's own reliability model |
| Destination | Plain-text log objects in a target S3 bucket | CloudTrail's own event store, optionally also delivered to S3/CloudWatch Logs |
| Can trigger real-time alerting/automation? | Not directly — requires separately processing the log files | ✅ Yes — can integrate with **CloudWatch Events/EventBridge** for near-real-time alerting on specific API calls |
| Cost model | Storage cost for log files only | **Per-event charge** for data events — can get expensive at high request volume across many/all buckets |

> ⚠️ **CloudTrail data events can be genuinely expensive** at scale, since every single `GetObject`/`PutObject` call is billed — this is exactly why scoping data events to **specific, sensitive buckets** (rather than "all S3 buckets in the account") is the common, cost-aware real-world pattern, rather than blanket-enabling it everywhere.

---

## 4. A common real pairing: both, for different purposes

Many production setups actually use **both** together: **server access logging** (Note 32) as the cheap, broad, best-effort baseline across most buckets, and **CloudTrail data events** scoped narrowly to the **specific, sensitive buckets** that need near-real-time, reliable, alertable auditing (e.g. a bucket holding regulated financial or health records) — using each tool where its strengths matter most.

> 🎯 **Exam tip:** "we need near-real-time visibility into who is reading/writing objects in a specific sensitive bucket, potentially triggering an automated alert" is the signature **CloudTrail data events** scenario. "We just want a general, low-cost record of bucket activity for occasional after-the-fact analysis" points back to **server access logging** (Note 32) instead.

---

## 5. Recap

- CloudTrail logs **management events by default**; **S3 data events** (object-level `GetObject`/`PutObject`/etc.) must be **explicitly enabled** and billed per event.
- Data events deliver **faster and more reliably** than server access logs, and can drive **real-time alerting** via EventBridge — at a real per-event cost, making broad, all-bucket enablement expensive at scale.
- A common pattern: server access logging broadly, CloudTrail data events scoped narrowly to the buckets that actually need it.
- Next: Note 34 — AWS S3 Requester Pays, shifting from auditing to a specific cost-allocation feature for buckets shared broadly with other accounts.

### Sources
- [Logging data events for Amazon S3 — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/cloudtrail-logging-s3-info.html)
- [Logging data and management events for trails — AWS docs](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-management-events-with-cloudtrail.html)
- [AWS CloudTrail pricing](https://aws.amazon.com/cloudtrail/pricing/)
