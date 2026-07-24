# 15 - AWS S3 Encryption

> Goal: map the full encryption landscape before diving into each option individually (Notes 16-22) — the two axes every S3 encryption choice sits on: **where** encryption happens (server-side vs. client-side) and **who controls the key**.

---

## 1. Encryption at rest vs. encryption in transit

- **Encryption in transit**: protects data **while it travels** over the network (HTTPS/TLS) — enforced via the `aws:SecureTransport` bucket policy condition from Note 12.
- **Encryption at rest**: protects data **while it's stored** on S3's underlying disks — this note and Notes 16-22 are entirely about this side.

These are independent — a bucket can (and should) have both, but they solve different threats: in-transit protects against network interception; at-rest protects against someone gaining access to the underlying storage media directly.

---

## 2. Every object in S3 is encrypted at rest today

Since 2023, **S3 automatically applies SSE-S3 encryption to every new object by default**, with no configuration required — the historical "should I encrypt this bucket?" decision is largely obsolete for the baseline case. What Notes 16-22 actually cover is **which specific encryption method and key-management model** to use, not whether to encrypt at all.

---

## 3. The four server-side encryption options (previewed)

| Method | Who manages the encryption key | Covered in |
|---|---|---|
| **SSE-S3** | AWS manages the key entirely, transparently | Note 18 |
| **SSE-KMS** | AWS KMS, using a key you (or AWS) create and control access to via key policies | Note 19-20 |
| **DSSE-KMS** | Same as SSE-KMS, but applies **two independent layers** of encryption | Note 21 |
| **SSE-C** | **You** supply your own encryption key with every request; AWS never stores it | Note 22 |

> 🧠 **Mental model:** moving down this list, **AWS's control over the key decreases and your responsibility increases** — SSE-S3 is "AWS handles everything," SSE-C is "you bring your own key and AWS forgets it the instant the request finishes." Note 17 covers the **server-side vs. client-side** distinction in full before Notes 18-22 cover each server-side method individually.

---

## 4. Client-side encryption — the other side entirely

All four methods above are **server-side** — S3 itself performs the encryption/decryption. **Client-side encryption** means the data is already encrypted **before** it ever leaves your application, using a key you manage entirely outside of AWS (e.g. via the AWS Encryption SDK) — S3 just stores already-encrypted bytes and has no idea they're encrypted at all. Note 17 covers this contrast directly.

---

## 5. Specifying encryption at upload time

```bash
# SSE-S3 (also now the automatic default)
aws s3 cp file.txt s3://demo-bucket/ --sse AES256

# SSE-KMS with a specific customer managed key
aws s3 cp file.txt s3://demo-bucket/ --sse aws:kms --sse-kms-key-id alias/my-key
```

A bucket can also set a **default encryption configuration** so every upload automatically gets a specified method without the uploader needing to specify it per-request — the standard way to enforce a consistent encryption method account/bucket-wide, similar in spirit to the `DenyInsecureTransport` bucket policy pattern from Note 12 (a bucket policy can also **deny** uploads that don't specify the desired encryption header, forcing compliance rather than just defaulting to it).

---

## 6. Recap

- Encryption **in transit** (HTTPS) and **at rest** (this note's focus) are independent protections against different threats.
- Every S3 object is encrypted at rest **by default today** (SSE-S3) — the real decision is **which** method and key-control model fits the workload, not whether to encrypt.
- Four server-side options (SSE-S3, SSE-KMS, DSSE-KMS, SSE-C) trade AWS's key-management convenience against your own control, in that order — plus a distinct **client-side** option where encryption happens before data ever reaches S3.
- Next: Note 16 — S3 Encryption Part 2: Symmetric Vs Asymmetric Encryption, a cryptography-fundamentals detour needed to fully understand how KMS keys (Notes 19-21) actually work.

### Sources
- [Protecting data with encryption — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingEncryption.html)
- [Default encryption for S3 buckets — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-encryption.html)
- [Amazon S3 now applies server-side encryption by default — AWS](https://aws.amazon.com/about-aws/whats-new/2023/01/amazon-s3-automatically-enable-server-side-encryption-buckets/)
