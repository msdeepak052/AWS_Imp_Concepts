# 18 - AWS S3 Server Side Encryption (SSE-S3)

> Goal: cover **SSE-S3** — the simplest, fully AWS-managed server-side encryption method, and (since 2023) the automatic default for every object in every bucket.

---

## 1. What SSE-S3 is

**SSE-S3** encrypts object data using **AES-256**, with **AWS managing every part of the encryption key lifecycle** — generation, rotation, storage, and protection — entirely behind the scenes. You never see, choose, or manage the key in any way.

- Header used to request it explicitly: `x-amz-server-side-encryption: AES256`.
- **No additional cost** — unlike SSE-KMS (Note 19), which incurs KMS API request charges, SSE-S3 has no per-request encryption fee.
- **No configuration required** — since 2023, this is the automatic baseline applied to every object, even with zero setup (Note 15, Section 2).

> 🧠 **Mental model:** SSE-S3 is the "just handle it for me" option — zero decisions to make, zero visibility into or control over the key, and zero extra cost. It's the right choice whenever there's no specific requirement to see, rotate, or control access to the encryption key itself.

---

## 2. Upload with SSE-S3 explicitly

```bash
aws s3 cp file.txt s3://demo-bucket/ --sse AES256
```

Since this is now the automatic default, this command produces the same result as a plain `aws s3 cp` with no `--sse` flag at all — included here mainly to show the explicit header, and because older buckets/tooling created before the 2023 default change may still benefit from setting it explicitly or as a bucket default.

---

## 3. Set as an explicit bucket default (belt-and-suspenders)

1. **S3 console** → bucket → **Properties** tab → **Default encryption** → **Edit**.
2. **Encryption type**: **Server-side encryption with Amazon S3 managed keys (SSE-S3)** → **Save changes**.
3. Every future upload to this bucket that doesn't specify a different method explicitly will use SSE-S3.

---

## 4. What SSE-S3 does NOT give you

Compared to SSE-KMS (Note 19), SSE-S3 has no:

- **Visibility into individual key usage** — no CloudTrail record of "who decrypted this specific object, using this specific key," since there's no separate KMS key to log against.
- **Fine-grained access control on the key itself** — you can't restrict "who is allowed to *use* this encryption key" separately from who's allowed to `GetObject`/`PutObject` on the bucket, since there's no customer-controlled key policy at all.
- **Customer-managed key rotation policy** — AWS handles this on its own schedule, invisibly.

These are exactly the gaps SSE-KMS (Note 19) fills, at the cost of some KMS request fees and a bit more configuration.

> 🎯 **Exam tip:** "we need encryption at rest, but have no specific requirement around key rotation policy, audit trail of key usage, or fine-grained key access control" is the signature **SSE-S3** scenario — the moment a question mentions **auditing key usage** or **restricting who can use the key** specifically, that's pointing at SSE-KMS (Note 19) instead.

---

## 5. Recap

- **SSE-S3** uses AES-256 with AWS managing the entire key lifecycle — zero configuration, zero extra cost, and (since 2023) the automatic default for every S3 object.
- It lacks the fine-grained key-usage auditing and access control that a customer-managed KMS key (Note 19) provides.
- The right default choice whenever there's no specific compliance/auditing requirement pointing toward KMS.
- Next: Note 19 — AWS S3 Server Side Encryption With Key Management Service (SSE-KMS), the step up in control (and complexity) from this note.

### Sources
- [Using server-side encryption with Amazon S3 managed keys (SSE-S3) — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingServerSideEncryption.html)
- [Protecting data with encryption — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingEncryption.html)
