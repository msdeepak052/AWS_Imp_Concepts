# 20 - AWS S3 — Server Side Encryption With Key Management Service (SSE-KMS) Practical

> Goal: create a real customer managed KMS key, write a key policy restricting who can use it, set it as a bucket's default encryption, and prove the "two independent gates" model from Note 19 by observing what happens when only one of the two gates is satisfied.

---

## 1. Create a customer managed KMS key

1. **KMS console** → **Customer managed keys** → **Create key**.
2. **Key type**: **Symmetric** (Note 16 — the standard choice for S3 object encryption).
3. **Alias**: `my-s3-key`.
4. **Key administrators**: select an admin group/role (can manage the key but not necessarily use it to encrypt/decrypt).
5. **Key usage permissions**: select the specific IAM users/roles allowed to **use** this key for encrypt/decrypt operations — e.g. `demo-console-user` from `IAM/05`.
6. **Finish**.

---

## 2. Inspect the key policy this generated

**KMS console** → `my-s3-key` → **Key policy** tab shows a JSON document, conceptually identical in structure to a bucket policy (Note 12) — statements with `Principal`, `Action` (KMS actions like `kms:Decrypt`, `kms:GenerateDataKey`), and `Resource` (the key itself).

```json
{
  "Sid": "AllowS3ServiceAndDemoUser",
  "Effect": "Allow",
  "Principal": { "AWS": "arn:aws:iam::111122223333:user/demo-console-user" },
  "Action": ["kms:Decrypt", "kms:GenerateDataKey"],
  "Resource": "*"
}
```

> 🧠 This key policy is the **second gate** from Note 19 — completely separate from whatever S3 bucket policy or IAM policy governs `s3:GetObject`. Both gates must open for a decrypt to succeed.

---

## 3. Set the bucket's default encryption to this key

1. **S3 console** → bucket → **Properties** → **Default encryption** → **Edit**.
2. **Encryption type**: **Server-side encryption with AWS Key Management Service keys (SSE-KMS)**.
3. **AWS KMS key**: choose `my-s3-key` (a customer managed key, not the AWS managed `aws/s3` default).
4. Optionally enable **Bucket Keys** (Note 19, Section 3) to reduce KMS request costs.
5. **Save changes**.

---

## 4. Upload and confirm

```bash
aws s3 cp file.txt s3://demo-bucket/
aws s3api head-object --bucket demo-bucket --key file.txt
```
The `head-object` output shows `"ServerSideEncryption": "aws:kms"` and `"SSEKMSKeyId"` pointing at `my-s3-key`'s ARN — confirming the bucket default applied without needing `--sse` flags on every individual upload.

---

## 5. Prove the two-gate model — deny at the KMS layer, allow at the S3 layer

1. Confirm `demo-console-user` **has** `s3:GetObject` permission on the bucket (via an IAM or bucket policy, Notes 11-12) — the S3-layer gate is open.
2. **Remove** `demo-console-user` from `my-s3-key`'s key usage permissions (Section 1, step 5) — closing the KMS-layer gate specifically.
3. As `demo-console-user`, attempt:
   ```bash
   aws s3 cp s3://demo-bucket/file.txt .
   ```
   This **fails** with an access denied error referencing KMS, even though the S3-level permission is fully intact — direct, hands-on proof that SSE-KMS access requires **both** gates independently, exactly as Note 19 described.
4. Re-add `demo-console-user` to the key's usage permissions to restore access.

---

## 6. Recap

- A **customer managed KMS key** has its own **key policy**, structurally similar to a bucket policy, that independently governs who can use the key to encrypt/decrypt.
- Setting a bucket's **default encryption** to a customer managed key means every future upload uses it automatically, without per-request flags.
- Section 5 directly demonstrated Note 19's core claim: **S3 permissions and KMS key permissions are two separate gates** — losing either one blocks access, regardless of how permissive the other is.
- Next: Note 21 — Dual-Layer Server Side Encryption With Key Management Service (DSSE-KMS), building on this same KMS key model with a second, independent encryption layer.

### Sources
- [Using server-side encryption with AWS KMS keys (SSE-KMS) — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html)
- [Creating keys — AWS KMS docs](https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html)
- [Key policies in AWS KMS — AWS docs](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html)
