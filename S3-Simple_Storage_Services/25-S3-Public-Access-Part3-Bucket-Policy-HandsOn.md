# 25 - S3 Public Access Part 3: Make An S3 Bucket Or Object Public Using Bucket Policy

> Goal: actually perform the deliberate, correct sequence of steps to make a bucket's contents public via a bucket policy — combining Notes 23-24 into one concrete, hands-on walkthrough, exactly the pattern static website hosting (Note 26 onward) depends on.

---

## 1. The two steps, always in this order

1. **Disable the relevant Block Public Access settings** (Note 24) — specifically the ones governing bucket policies, since that's the mechanism being used here.
2. **Attach a bucket policy granting public read access** (Note 23's first mechanism).

Doing this in the reverse order doesn't work — attempting to save a public-granting bucket policy while BPA still blocks it will be rejected by the console/API with a clear error, exactly as Note 24 described.

---

## 2. Disable Block Public Access for this bucket

1. **S3 console** → bucket → **Permissions** tab → **Block public access (bucket settings)** → **Edit**.
2. Uncheck **Block public access to buckets and objects granted through new public bucket or access point policies** and **...through any public bucket or access point policies** (the two policy-related settings from Note 24's four).
3. Confirm the warning prompt (typing "confirm" or similar) — a deliberate friction step, exactly as intended.
4. **Save changes**.

> ⚠️ Leave the two **ACL**-related BPA settings enabled if this bucket has no legitimate need for ACL-based public grants — disable only the specific settings the chosen mechanism (bucket policy, here) actually needs, per Note 24's "each of the four toggles independently" point.

---

## 3. Attach a public-read bucket policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::demo-public-bucket/*"
    }
  ]
}
```

**Permissions** tab → **Bucket policy** → **Edit** → paste → **Save changes**. Note this grants **read-only** access (`s3:GetObject`) to objects, to the public (`"Principal": "*"`) — not write, list, or delete; a public bucket almost always should only ever grant read access unless there's a very specific, deliberate reason otherwise.

---

## 4. Verify

```bash
curl https://demo-public-bucket.s3.ap-south-1.amazonaws.com/index.html
```

This should now succeed **without any AWS credentials at all** — a genuine anonymous request, confirming the object is truly public. Before Section 2's BPA change, this same request would have failed even with the bucket policy already in place.

---

## 5. Making just one object public, instead of the whole bucket

Scope the `Resource` down to a single key instead of a wildcard:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadOneFileOnly",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::demo-public-bucket/public-assets/logo.png"
    }
  ]
}
```

This is generally the **safer, more deliberate** pattern for buckets that mix public and private content — rather than a blanket `/*` wildcard exposing everything, only the specifically-listed key(s) become reachable.

> 🎯 **Exam tip:** "make a specific object public without exposing the rest of the bucket" points to a bucket policy scoped to that **specific object key**, not a wildcard — and remember Block Public Access must still be relaxed for the relevant policy settings before this will actually take effect, regardless of how correctly the policy itself is scoped.

---

## 6. Recap

- Making content genuinely public always requires **two** deliberate steps: relax the relevant **Block Public Access** settings (Note 24) first, then attach a **public-granting bucket policy** (Note 23).
- A public bucket policy should almost always grant **only `s3:GetObject`** (read), scoped as tightly as the use case allows — a single key where possible, rather than a blanket `/*`.
- This closes the three-part public access series (Notes 23-25). Next: Note 26 — AWS S3 Static Web Hosting, the single most common legitimate reason to actually make bucket content public.

### Sources
- [Blocking public access to your Amazon S3 storage — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html)
- [Bucket policy examples — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html)
- [How to Restrict Amazon S3 Bucket Access — AWS Security Blog](https://aws.amazon.com/blogs/security/how-to-restrict-amazon-s3-bucket-access-to-a-specific-iam-role/)
