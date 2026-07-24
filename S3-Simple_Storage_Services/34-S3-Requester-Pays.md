# 34 - AWS S3 Requester Pays

> Goal: understand **Requester Pays** — a bucket-level billing setting that shifts **data transfer and request costs** from the bucket owner to whoever downloads the data — and the specific consent mechanism it forces on requesters.

---

## 1. The default billing model — the bucket owner pays everything

Normally, the **bucket owner** pays for **everything**: storage, requests, and data transfer out — regardless of who is doing the downloading. For a bucket shared broadly (e.g. a public research dataset, or a bucket shared across many partner accounts), this can mean the owner absorbs a large, unpredictable data transfer bill driven entirely by **other people's** download activity.

> 🧠 **Mental model:** by default, S3 billing works like a landlord who pays the electric bill for the whole building regardless of which tenant runs the AC all day. **Requester Pays** flips this specific cost (data transfer + request fees) onto the tenant actually consuming it, while the landlord (bucket owner) still pays for the storage itself.

---

## 2. What Requester Pays actually shifts (and what it doesn't)

| Cost | Who pays, with Requester Pays enabled |
|---|---|
| **Storage** | Still always the **bucket owner** |
| **Requests** (GET, PUT, etc.) | The **requester** |
| **Data transfer out** | The **requester** |

Enabling Requester Pays doesn't change who pays for storing the data — only for the acts of **requesting and transferring** it.

---

## 3. The consent mechanism — a mandatory header

For Requester Pays to actually work, every requester must include a specific header confirming they accept the charges:

```bash
aws s3 cp s3://demo-shared-dataset/large-file.csv . --request-payer requester
```

Omitting `--request-payer requester` (or the equivalent HTTP header, `x-amz-request-payer: requester`) causes the request to **fail outright** — this is a deliberate design choice, ensuring no one is ever silently charged without explicitly acknowledging it first.

> ⚠️ Because Requester Pays requires this explicit header, it is **incompatible with anonymous/public access** in the way Notes 23-25 covered — an anonymous browser request or a plain `<img>` tag has no way to attach this header, so a Requester-Pays bucket cannot simultaneously be casually public in the way a normal public bucket can. Access is expected to come from requesters who are identified and billable, not anonymous walk-up traffic.

---

## 4. Enable it

1. **S3 console** → bucket → **Properties** tab → **Requester pays** → **Edit** → **Enable** → **Save changes**.

---

## 5. When this is the right feature

| Scenario | Requester Pays? |
|---|---|
| A research organization shares a large public dataset with many external consumers, and doesn't want to absorb everyone's download transfer costs | ✅ Yes |
| A bucket shared across specific partner AWS accounts, where each partner should bear their own usage cost | ✅ Yes |
| A typical application bucket accessed only by your own account's compute (e.g. an ASG's instances reading config) | ❌ No — no cost-shifting benefit when you're paying for both sides anyway |

> 🎯 **Exam tip:** "a bucket owner wants to share a large dataset publicly/with partners without paying for everyone else's downloads" is the exact, textbook **Requester Pays** scenario — a distinctive enough feature name and use case that it's usually a fairly direct identify-and-answer question rather than one requiring elimination of close alternatives.

---

## 6. Recap

- **Requester Pays** shifts **request and data transfer** costs (not storage) from the bucket owner to the requester, who must explicitly opt in via a `--request-payer requester` header on every request.
- This requirement makes Requester Pays buckets incompatible with casual anonymous/public access — requesters must be identifiable and billable.
- The standard use case: sharing large datasets broadly (publicly or cross-account) without the owner absorbing everyone else's download costs.
- Next: Note 35 — AWS S3 Presigned URL, another mechanism for controlled, time-limited access — this time via a signed URL rather than a billing shift.

### Sources
- [Requester Pays buckets — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/RequesterPaysBuckets.html)
- [Amazon S3 pricing — AWS](https://aws.amazon.com/s3/pricing/)
