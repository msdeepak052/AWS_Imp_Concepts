# 22 - AWS S3 — S3 Server Side Encryption With Customer-Provided Key (SSE-C)

> Goal: cover **SSE-C** — the last of the four server-side encryption methods, where **you** supply the encryption key with every single request, and AWS **never stores it at all**. This closes out the encryption series (Notes 15-22).

---

## 1. What makes SSE-C different from every other method

With SSE-C, **you generate and manage the encryption key entirely outside of AWS** — S3 uses it to perform the actual encryption/decryption (still technically "server-side," since S3 does the work), but:

- **AWS never stores the key** — not in KMS, not anywhere. It exists only in your own key-management system.
- **You must supply the exact same key on every single request** — every `PutObject` and every `GetObject` must include the key (Base64-encoded) in the request headers, or the operation fails outright.
- If you **lose the key**, the data is **permanently unrecoverable** — there is no "AWS support can help retrieve it" path, since AWS genuinely never had a copy to begin with.

> ⚠️ This is the sharpest trade-off of any encryption method in this folder: **maximum control, zero safety net**. Losing an SSE-S3 or SSE-KMS key is not really possible in the same way (AWS or KMS always retains it); losing an SSE-C key means the data is gone, full stop.

---

## 2. Upload and download with SSE-C

```bash
# Generate a 256-bit key and base64-encode it (example, for illustration)
KEY_B64=$(openssl rand -base64 32)

aws s3api put-object \
  --bucket demo-bucket \
  --key sensitive-file.txt \
  --body sensitive-file.txt \
  --sse-customer-algorithm AES256 \
  --sse-customer-key "$KEY_B64"

aws s3api get-object \
  --bucket demo-bucket \
  --key sensitive-file.txt \
  --sse-customer-algorithm AES256 \
  --sse-customer-key "$KEY_B64" \
  downloaded-file.txt
```

Note that **the exact same key** must be supplied on both the upload and every subsequent download — S3 stores only a hash of the key (to verify future requests supply the correct one), never the key itself.

> ⚠️ **SSE-C requires HTTPS** — AWS will reject SSE-C requests made over plain HTTP, since the customer-provided key would otherwise be transmitted in the clear in request headers. This is enforced by S3 itself, not something you need a separate bucket policy condition for (though Note 12's `DenyInsecureTransport` statement is still good general hygiene regardless).

---

## 3. Why choose SSE-C over SSE-KMS

| Requirement | SSE-KMS (Note 19) | SSE-C |
|---|---|---|
| AWS ever stores/manages the key | Yes (in KMS) | **Never** |
| Key rotation | Configurable, but still an AWS-adjacent process | Entirely your own responsibility, using your own system |
| Regulatory driver: "our organization's own key-management system must be the sole source of truth for encryption keys, with AWS never retaining a copy" | ❌ Doesn't fully satisfy this | ✅ Exactly matches this |
| Operational complexity | Lower — KMS handles storage, rotation, access policy | Higher — you must track, distribute, and protect the key yourself, and supply it correctly on every request |
| Risk if key is lost | Effectively none (KMS always has it, assuming key isn't manually deleted) | **Total, permanent data loss** |

> 🎯 **Exam tip:** "the organization's own external key-management system must be the only place the encryption key ever exists, with no copy retained by AWS" is the signature **SSE-C** scenario. If the requirement is instead just "control and audit key usage" without that specific "AWS must never see/store the key" constraint, SSE-KMS (Note 19) is the better-fitting, lower-risk answer.

---

## 4. All four server-side methods, final comparison (Notes 18-22 combined)

| Method | Who manages key | AWS stores key? | Audit trail | Risk of key loss |
|---|---|---|---|---|
| **SSE-S3** | AWS, fully | Yes (invisible to you) | None (no separate KMS log) | None — AWS always has it |
| **SSE-KMS** | You, via KMS | Yes, in KMS | Yes, CloudTrail | Low — KMS key deletion has a mandatory waiting period |
| **DSSE-KMS** | You, via KMS (two layers) | Yes, in KMS | Yes, CloudTrail | Low — same as SSE-KMS |
| **SSE-C** | You, entirely outside AWS | **Never** | None from AWS's side | **Total** — no recovery possible if lost |

---

## 5. Recap

- **SSE-C** requires you to supply the encryption key on **every request**; AWS never stores it, meaning **losing the key means permanently losing the data** — the sharpest control/risk trade-off of any S3 encryption method.
- Requires HTTPS, enforced by S3 itself.
- Reserved for a specific requirement: AWS must **never** retain any copy of the key — distinct from SSE-KMS's "AWS manages it, but you control access and see an audit trail" model.
- This closes the full encryption series (Notes 15-22). Next: Note 23 — S3 Public Access Part 1: Two Ways To Grant Public Access, shifting from "how is data protected at rest" to "how could this bucket become reachable by the public at all."

### Sources
- [Using server-side encryption with customer-provided keys (SSE-C) — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerSideEncryptionCustomerKeys.html)
- [Protecting data with encryption — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingEncryption.html)
