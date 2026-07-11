# 12 - AWS S3 — AWS Bucket Policy For S3 (Hands-On)

> Goal: author and attach a real bucket policy — granting cross-account access, then denying insecure (non-HTTPS) requests — the two most common real-world bucket policy patterns, and the resource-based counterpart to Note 11's IAM policy.

---

## 1. Attach a bucket policy via the console

1. **S3 console** → open a bucket → **Permissions** tab → **Bucket policy** → **Edit**.
2. Paste JSON (Section 2 or 3 below) → **Save changes**. The console validates JSON syntax and warns if the policy would make the bucket public (tying back to Block Public Access, Notes 24-25).

---

## 2. Grant cross-account access

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowPartnerAccountRead",
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::444455556666:root" },
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::demo-bucket",
        "arn:aws:s3:::demo-bucket/*"
      ]
    }
  ]
}
```

This grants **every** identity in account `444455556666` read access — often too broad for a real partnership; scoping the `Principal` down to one specific role/user ARN in that account (instead of its `:root`) is the tighter, more common production pattern, mirroring the same "trust the whole account vs. one specific principal" distinction from `IAM/09`'s cross-account role notes.

> 🧠 Note the **same two-ARN-form requirement** from Note 11 applies here too — the bucket ARN itself for `ListBucket`, and `/*` for `GetObject`.

---

## 3. Deny insecure (non-HTTPS) transport — a standard hardening statement

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyInsecureTransport",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::demo-bucket",
        "arn:aws:s3:::demo-bucket/*"
      ],
      "Condition": { "Bool": { "aws:SecureTransport": "false" } }
    }
  ]
}
```

This explicitly **denies every action, from every principal (`"Principal": "*"`)**, whenever the request didn't come over HTTPS. Because this is an explicit `Deny` (same rule from `IAM/01`), it overrides **any** other `Allow` anywhere else — including the cross-account grant in Section 2, or any IAM policy an identity might otherwise have. This exact statement is AWS's own commonly recommended baseline hardening addition for any bucket holding sensitive data.

> ⚠️ `"Principal": "*"` here does **not** make the bucket public — it means this specific **Deny** statement applies to *everyone*, which is the whole point: no principal, however permissive their other grants are, should be able to bypass encryption-in-transit.

---

## 4. Combine both statements in one policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowPartnerAccountRead",
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::444455556666:root" },
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": ["arn:aws:s3:::demo-bucket", "arn:aws:s3:::demo-bucket/*"]
    },
    {
      "Sid": "DenyInsecureTransport",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": ["arn:aws:s3:::demo-bucket", "arn:aws:s3:::demo-bucket/*"],
      "Condition": { "Bool": { "aws:SecureTransport": "false" } }
    }
  ]
}
```

Even the trusted partner account from the first statement is still bound by the second statement's HTTPS requirement — explicit denies apply universally, regardless of which other statement in the same policy (or a different policy entirely) tried to grant broader access.

---

## 5. Test from the partner account

From an identity in account `444455556666` (with its own IAM permission to call S3, per `IAM/09`'s two-sided trust requirement — the bucket policy alone isn't enough if that account's own IAM policy doesn't also allow the call):
```bash
aws s3 ls s3://demo-bucket/ --profile partner-account
aws s3 cp s3://demo-bucket/shared-file.csv . --profile partner-account
```
Both succeed over HTTPS; either would fail if attempted over plain HTTP (rare in practice via the CLI/SDKs, which default to HTTPS, but a real concern for custom HTTP clients).

---

## 6. Recap

- A bucket policy is authored and attached at **Permissions → Bucket policy**, and — like Note 11's IAM policy — needs both the bucket ARN and the `/*` object ARN to cover bucket-level and object-level actions respectively.
- Granting **cross-account** access is the signature bucket-policy use case (`Principal` naming another account or specific role/user ARN).
- **Denying insecure transport** (`aws:SecureTransport: false`) is a standard, widely-recommended hardening statement — and demonstrates explicit-deny's universal override, applying even to principals an earlier statement in the same policy trusted.
- Next: Note 13 — AWS S3 Bucket Access Control List, the older, coarser-grained access mechanism that predates bucket policies.

### Sources
- [Bucket policies for Amazon S3 — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-policies.html)
- [Requiring encryption in transit — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security_s3_object_ownership.html)
- [Bucket policy examples — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html)
