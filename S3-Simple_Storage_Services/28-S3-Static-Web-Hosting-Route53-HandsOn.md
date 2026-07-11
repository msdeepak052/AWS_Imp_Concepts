# 28 - AWS S3 Static Web Hosting With Route 53 (Hands-On)

> Goal: put a friendly custom domain name in front of the Note 27 bucket, using a Route 53 **Alias record** — and the one hard naming requirement this trick depends on.

---

## 1. The hard requirement: bucket name must match the domain name exactly

To point a custom domain directly at an S3 website endpoint, the **bucket name must exactly match the domain name** you want to serve it from (e.g. bucket `www.example.com` serves `http://www.example.com`). This is a real, non-negotiable S3 requirement for this specific pattern — S3 uses the `Host` header of the incoming request to match it against a bucket of the same name.

> ⚠️ If you already created a bucket with an arbitrary name (like Note 27's `demo-static-site-<unique-suffix>`), this pattern requires either renaming (S3 buckets can't be renamed — you'd need a new bucket with the correct name and re-upload/copy the content) or accepting that this specific direct-to-S3 domain mapping won't apply to that bucket as-is.

---

## 2. Create (or rename to) a domain-matching bucket

1. Create a new bucket named exactly `www.cloudmart-demo.example` (matching whatever domain/subdomain you actually control and want to use).
2. Repeat Note 27's steps: upload `index.html`/`error.html`, make it public (Note 25), enable static website hosting (Note 26) with the same index/error document settings.

---

## 3. Create the Alias record in Route 53

1. **Route 53 console** → **Hosted zones** → select the hosted zone for your domain (e.g. `cloudmart-demo.example`).
2. **Create record**.
3. **Record name**: `www`.
4. **Record type**: `A`.
5. **Alias**: toggle **On**.
6. **Route traffic to**: **Alias to S3 website endpoint** → select the Region the bucket lives in → select the bucket from the list (only domain-matching, website-hosting-enabled buckets appear here).
7. **Create records**.

> 🧠 This is an **Alias record**, not a CNAME — S3 website endpoints (unlike, say, an ALB) are one of the handful of AWS resource types Route 53 Alias records can point directly at, at the **zone apex** or a subdomain, without the CNAME restriction of never being usable at a zone apex. Alias records are also free of the extra DNS lookup a CNAME would need, and Route 53 doesn't charge extra for Alias record queries to AWS resources.

---

## 4. Test

```bash
dig www.cloudmart-demo.example
curl http://www.cloudmart-demo.example
```

The domain now resolves and serves the same `index.html` content as the raw S3 website endpoint did in Note 27 — but under a friendly, branded name instead of the long `s3-website-region.amazonaws.com` URL.

---

## 5. Why this still doesn't get you HTTPS

Exactly as Note 26 flagged: the underlying S3 website endpoint is **HTTP-only**. Pointing a friendly domain at it via Route 53 doesn't change that — `https://www.cloudmart-demo.example` still won't work. Getting HTTPS on this custom domain requires putting **CloudFront** in front of the S3 bucket instead (with an ACM certificate attached to the CloudFront distribution), and pointing the Route 53 Alias record at the CloudFront distribution rather than directly at the S3 website endpoint — the standard, secure production pattern, covered in this repo's `CDN` folder.

> 🎯 **Exam tip:** "host a static site on S3 under a custom domain, requiring HTTPS" always resolves to **S3 + CloudFront + ACM + Route 53 Alias to the CloudFront distribution** — direct Route 53-to-S3-website-endpoint (this note's pattern) is only ever the right answer when HTTPS isn't a stated requirement.

---

## 6. Recap

- Pointing a custom domain directly at an S3 website endpoint requires the **bucket name to exactly match the domain name**.
- Route 53's **Alias record**, pointed at **"Alias to S3 website endpoint,"** is the mechanism — free, usable at the zone apex, no extra DNS lookup.
- This pattern is still **HTTP-only** — HTTPS on a custom domain requires CloudFront in front of the bucket instead.
- Next: Note 29 — AWS S3 Cross-Origin Resource Sharing (CORS) (Hands-On), needed the moment a *different* domain's JavaScript needs to fetch resources from this bucket.

### Sources
- [Routing traffic to a website that is hosted in an Amazon S3 bucket — AWS docs](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/RoutingToS3Bucket.html)
- [Choosing between alias and non-alias records — AWS docs](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-choosing-alias-non-alias.html)
- [Hosting a static website using Amazon S3 — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html)
