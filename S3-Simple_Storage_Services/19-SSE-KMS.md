# 19 - AWS S3 Server Side Encryption With Key Management Service (SSE-KMS)

> Goal: cover **SSE-KMS** — trading SSE-S3's zero-configuration simplicity (Note 18) for a customer-controlled key with fine-grained access control, audit trail, and rotation policy, backed by **AWS KMS**.

---

## 1. What SSE-KMS adds over SSE-S3

Like SSE-S3, SSE-KMS still uses **AES-256** to actually encrypt object data — the difference is entirely about **who controls and can audit the key**:

- Uses a **KMS key** — either an **AWS managed key** (`aws/s3`, created automatically, still limited control) or a **customer managed key** (one you create, fully control the key policy for, and can rotate/disable/delete yourself).
- Every use of the key (encrypt, decrypt) is **logged in CloudTrail** as a distinct KMS API event — giving you a genuine audit trail of exactly which principal decrypted which object, when, something SSE-S3 cannot provide at all (Note 18, Section 4).
- **Key policies** (a resource-based policy on the KMS key itself, conceptually parallel to an S3 bucket policy) let you control **who is allowed to use the key**, completely independently of who's allowed to call `s3:GetObject` — meaning access to an object can require **both** an S3-level grant **and** a KMS-level grant, a genuine two-factor authorization model.

> 🧠 **Mental model:** SSE-S3 is a lock AWS installs and manages invisibly. SSE-KMS is a lock **you** install (or at least, whose key policy you control), with a security log of every single time it's opened — the trade is more setup and a small per-request cost, for real visibility and a second, independent gate on access.

---

## 2. The header, and cost

```bash
aws s3 cp file.txt s3://demo-bucket/ --sse aws:kms --sse-kms-key-id alias/my-s3-key
```

Unlike SSE-S3, SSE-KMS **does** incur a small charge per KMS `Encrypt`/`Decrypt`/`GenerateDataKey` API call — a real, if usually small, cost at high request volumes, worth flagging in any cost-sensitive scenario the exam poses.

---

## 3. S3 Bucket Keys — reducing the KMS request cost

For workloads making very frequent KMS calls (e.g. millions of small objects), S3 offers **S3 Bucket Keys**: a bucket-level setting that has S3 request a **time-limited bucket-level key** from KMS once, then use that to encrypt many objects locally for a period, dramatically **reducing the number of direct KMS API calls** (and therefore cost) compared to calling KMS separately for every single object.

> 🎯 **Exam tip:** "SSE-KMS is the right encryption choice, but KMS request costs are too high at our request volume" is the textbook **S3 Bucket Keys** scenario — enabling them is the fix, not switching away from SSE-KMS entirely.

---

## 4. Quotas matter — KMS has request-rate limits SSE-S3 doesn't

Because SSE-KMS calls out to the separate KMS service per request (unless Bucket Keys are enabled), very high-throughput workloads can actually **hit KMS's own request-rate quotas** — a scaling limit that simply doesn't exist for SSE-S3, since SSE-S3 has no separate service being called at all. This is a genuine, sometimes-tested operational trade-off: KMS's flexibility and auditability comes with its own throughput ceiling to be aware of.

---

## 5. SSE-S3 vs. SSE-KMS — decision table

| Situation | Choose |
|---|---|
| No specific audit/key-control requirement | SSE-S3 (Note 18) — simpler, free, no quota concerns |
| Need an audit trail of exactly who decrypted what, when | **SSE-KMS** |
| Need to restrict *who can use the key* independently of bucket/IAM permissions | **SSE-KMS** |
| Need to control/rotate the key on your own schedule, or disable it to instantly cut off all decrypt capability | **SSE-KMS** (customer managed key) |
| Extremely high request volume, KMS cost/quota is a real concern | SSE-KMS **with S3 Bucket Keys** enabled |

---

## 6. Recap

- **SSE-KMS** uses AWS KMS to manage the encryption key, adding **CloudTrail-logged key usage**, **customer-controlled key policies** (a second, independent access gate beyond S3 permissions), and **customer-managed rotation** — at the cost of small per-request KMS fees and KMS's own request-rate quotas.
- **S3 Bucket Keys** reduce that per-request KMS cost for high-volume workloads without giving up SSE-KMS's benefits.
- Next: Note 20 — Server Side Encryption With Key Management Service (SSE-KMS) Practical, configuring this hands-on with a real customer managed key and key policy.

### Sources
- [Using server-side encryption with AWS KMS keys (SSE-KMS) — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html)
- [Reducing the cost of SSE-KMS with Amazon S3 Bucket Keys — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-key.html)
- [AWS KMS request quotas — AWS docs](https://docs.aws.amazon.com/kms/latest/developerguide/requests-per-second.html)
