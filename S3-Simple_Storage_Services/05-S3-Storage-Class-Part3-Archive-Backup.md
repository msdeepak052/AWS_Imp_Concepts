# 05 - AWS S3 Storage Class — Part 3: S3 Archive and Backup Storage Class

> Goal: cover the **Glacier family** — the cold end of the storage-class spectrum, opposite Note 04's Express One Zone — trading retrieval speed for the lowest possible per-GB storage cost.

---

## 1. The three Glacier-family classes

| Class | Retrieval time | Min. storage duration | Use case |
|---|---|---|---|
| **S3 Glacier Instant Retrieval** | **Milliseconds** (same as Standard) | 90 days | Archive data that's rarely accessed but must be available **instantly** when it is (e.g. medical images, media archives accessed a few times a year) |
| **S3 Glacier Flexible Retrieval** (formerly "S3 Glacier") | Minutes to hours (see Section 2) | 90 days | Archives accessed a couple of times a year, where a retrieval **wait** is acceptable |
| **S3 Glacier Deep Archive** | Hours (see Section 2) | 180 days | The **cheapest** storage AWS offers — long-term retention/compliance archives essentially never expected to be read (e.g. 7-10 year regulatory retention) |

> 🧠 **Mental model:** Glacier Instant Retrieval is "archive pricing, Standard-like speed" — the odd one out that doesn't actually make you wait, just commits to a longer minimum storage duration and a retrieval fee in exchange for the lower storage cost. Flexible Retrieval and Deep Archive are the "true" archive experience — you wait, on purpose, because that's what makes them so cheap.

---

## 2. Retrieval tiers within Flexible Retrieval and Deep Archive

Both Flexible Retrieval and Deep Archive offer **multiple retrieval speed options**, each with its own cost — faster retrieval always costs more:

| Retrieval tier | S3 Glacier Flexible Retrieval | S3 Glacier Deep Archive |
|---|---|---|
| **Expedited** | 1-5 minutes | Not available |
| **Standard** | 3-5 hours | Within 12 hours |
| **Bulk** | 5-12 hours (often free/lowest cost) | Within 48 hours |

> ⚠️ **Expedited retrieval isn't guaranteed** to always be available for Flexible Retrieval during exceptionally high-demand periods, unless you've purchased **provisioned retrieval capacity** ahead of time — worth knowing for any scenario emphasizing a hard retrieval-time SLA.

---

## 3. How data actually gets into Glacier

Two paths:

1. **Directly upload** an object with the target storage class set at upload time (`PutObject` with `x-amz-storage-class`).
2. **Transition** existing objects into a Glacier class automatically via an **S3 Lifecycle rule** (Notes 07-08) — by far the more common real-world pattern: objects start in Standard, then age into IA, then into Glacier, as they get less likely to be accessed over time.

> ⚠️ Objects **cannot be transitioned directly from S3 Standard into Deep Archive in fewer than 180 days total lifetime** in some lifecycle configurations, and more generally, **lifecycle transitions must move "down" the cost/retrieval-speed ladder in the documented order** — you can't, for instance, configure a lifecycle rule that jumps backward from Glacier to Standard; a restore (Section 4) is how you get data back into faster-access storage temporarily or permanently.

---

## 4. Restoring an archived object

Objects in Flexible Retrieval or Deep Archive **cannot be read directly** — they must first be **restored**, which temporarily creates a readable copy (in S3, at a storage class you choose, for a duration you specify) while the archived original remains in place:

```bash
aws s3api restore-object \
  --bucket demo-archive-bucket \
  --key old-report.csv \
  --restore-request '{"Days":7,"GlacierJobParameters":{"Tier":"Standard"}}'
```

After the requested retrieval time elapses (per the tier chosen, Section 2), the object becomes temporarily accessible for the number of `Days` specified, then automatically reverts to archive-only access again.

> 🎯 **Exam tip:** "an application tries to `GetObject` on a Glacier Flexible Retrieval or Deep Archive object and gets an error" is a recurring exam scenario — the fix is always **restore the object first**, then read it; Glacier Instant Retrieval is the only archive class that skips this step entirely, since it's designed to behave like Standard for read latency.

---

## 5. All S3 storage classes, one final comparison (Notes 03-05 combined)

| Class | AZs | Retrieval | Min. duration | Relative cost |
|---|---|---|---|---|
| Standard | 3+ | ms | None | Highest (of the non-Express tiers) |
| Intelligent-Tiering | 3+ (auto) | ms (mostly) | None | Auto-optimized |
| Standard-IA | 3+ | ms | 30 days | Lower |
| One Zone-IA | 1 | ms | 30 days | Lower still |
| Express One Zone | 1 | sub-ms, high request rate | None | Higher storage $/GB, much lower request $ |
| Glacier Instant Retrieval | 3+ | ms | 90 days | Low |
| Glacier Flexible Retrieval | 3+ | min-hours | 90 days | Lower |
| Glacier Deep Archive | 3+ | hours | 180 days | **Lowest** |

---

## 6. Recap

- The **Glacier family** (Instant Retrieval, Flexible Retrieval, Deep Archive) trades retrieval speed for the lowest per-GB storage costs S3 offers, with increasing minimum storage durations (90 → 90 → 180 days) as cost drops further.
- **Flexible Retrieval and Deep Archive objects must be explicitly restored** before they can be read — Glacier Instant Retrieval is the exception, behaving like Standard for read latency.
- Getting data into these classes is almost always done via **Lifecycle rules** (Notes 07-08) transitioning objects automatically as they age, rather than uploading directly at the target class.
- This closes the three-part storage class series (Notes 03-05). Next: Note 06 — S3 Versioning, layered independently on top of whichever storage class(es) an object's history spans.

### Sources
- [Amazon S3 storage classes — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html)
- [Restoring an archived object — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/restoring-objects.html)
- [Archive retrieval options — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/restoring-objects-retrieval-options.html)
