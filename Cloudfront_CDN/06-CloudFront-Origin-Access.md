# 06 - CloudFront Origin Access

> Goal: lock an S3 origin down so it's **only** reachable through CloudFront, never by a direct S3 URL — covering both **Origin Access Control (OAC)**, the modern, recommended mechanism, and **Origin Access Identity (OAI)**, the legacy one it's replacing.

---

## 1. The problem: a "private-looking" bucket that's actually still directly reachable

Note 02's lab used an S3 **website endpoint**, which only works when the bucket is fully public — anyone with the bucket's direct URL bypasses CloudFront entirely, skipping any edge-level protections, custom domains, or access logging you set up at the CloudFront layer. For an **S3 REST-endpoint origin** (Note 03), you can do better: keep the bucket **entirely private**, and grant access **only to CloudFront itself**.

> 🧠 **Mental model:** this is the same goal as the CloudMart capstone's ALB-node-vs-target pattern (`Capstone-Project/Project-1/02`) — the public-facing thing (CloudFront, or the ALB) is the only allowed path in; the actual data store (S3, or the private EC2 targets) is unreachable directly, no matter how permissive its own settings might otherwise look.

---

## 2. Origin Access Control (OAC) — the modern, recommended mechanism

**OAC** lets CloudFront sign every request to the S3 origin using **AWS SigV4**, with short-lived, frequently-rotated credentials — and the bucket policy grants access only to that **specific distribution's** OAC, keyed by the distribution's own ARN.

- Supports **all S3 Regions**, including ones launched after December 2022 (OAI does not).
- Supports **SSE-KMS encrypted objects** (`S3-Simple_Storage_Services/19`) — OAI cannot read KMS-encrypted content at all.
- Supports more HTTP methods (`GET`, `PUT`, `POST`, `PATCH`, `DELETE`, `OPTIONS`, `HEAD`), enabling CloudFront to proxy **uploads** to S3, not just reads.
- Better protection against the **confused deputy problem** (`IAM/09`) via a `aws:SourceArn` condition scoped to the exact distribution.

---

## 3. Configure OAC (recommended path)

1. **CloudFront console** → distribution → **Origins** → edit the S3 origin.
2. **Origin access**: **Origin access control settings (recommended)** → **Create control setting** → accept defaults (signs GET/HEAD/etc. requests) → **Save**.
3. CloudFront shows a generated **bucket policy** — copy it.
4. **S3 console** → bucket → **Permissions** → **Bucket policy** → paste the generated policy:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": { "Service": "cloudfront.amazonaws.com" },
         "Action": "s3:GetObject",
         "Resource": "arn:aws:s3:::demo-bucket/*",
         "Condition": {
           "StringEquals": { "AWS:SourceArn": "arn:aws:cloudfront::111122223333:distribution/EDFDVBD6EXAMPLE" }
         }
       }
     ]
   }
   ```
5. Confirm the bucket's **Block Public Access** (`S3-Simple_Storage_Services/24`) stays fully **enabled** — OAC doesn't require any public grant at all; the `Principal: cloudfront.amazonaws.com` + `SourceArn` condition is what grants access, entirely independent of public/private bucket status.
6. Test: a direct S3 URL now returns **Access Denied**; the CloudFront distribution's domain still serves the content normally.

---

## 4. Origin Access Identity (OAI) — the legacy mechanism

**OAI** is the older approach: CloudFront creates a special **CloudFront user identity**, and the bucket policy grants that identity read access. It still works and AWS continues to support it, but has real limitations OAC doesn't:

- Doesn't support SSE-KMS-encrypted S3 objects.
- Doesn't support Regions launched after December 2022.
- Only supports `GET`/`HEAD` — no proxying uploads through to S3.

> 🎯 **Exam tip:** **AWS now recommends OAC over OAI for all new distributions** — a question describing a **new** setup should point to OAC; OAI mainly appears on the exam as the "older, still-functional but limited" contrast option, or in the context of an existing/legacy distribution.

---

## 5. OAC/OAI only work with the S3 REST endpoint, never the website endpoint

Both mechanisms depend on **SigV4-signed requests**, a capability the S3 **website endpoint** doesn't support at all (it's designed for pure public HTTP access, `S3-Simple_Storage_Services/26`). This is exactly why Note 03 flagged that a website-endpoint origin can never be paired with OAC/OAI — if you need S3's index/error-document routing **and** a fully private bucket, the common workaround is handling routing/error pages at the CloudFront layer itself instead (Notes 12, 17) with a REST-endpoint + OAC origin.

---

## 6. Recap

- **Origin Access Control (OAC)** is the modern, recommended way to keep an S3 origin **fully private**, reachable only by the specific CloudFront distribution — supporting all Regions, SSE-KMS, and more HTTP methods than the legacy **Origin Access Identity (OAI)**.
- Both depend on SigV4 signing, which only the S3 **REST endpoint** supports — never the **website endpoint** (Note 03's distinction).
- With OAC/OAI configured correctly, Block Public Access can (and should) remain fully enabled on the bucket — no public grant is needed at all.
- Next: Note 07 — CloudFront Allowed HTTP Method, covering which verbs a cache behavior actually forwards to the origin.

### Sources
- [Restricting access to an Amazon S3 origin — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html)
- [Migrating from OAI to OAC — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-migrate-oai-to-oac.html)
- [Amazon CloudFront introduces Origin Access Control (OAC) — AWS blog](https://aws.amazon.com/blogs/networking-and-content-delivery/amazon-cloudfront-introduces-origin-access-control-oac/)
