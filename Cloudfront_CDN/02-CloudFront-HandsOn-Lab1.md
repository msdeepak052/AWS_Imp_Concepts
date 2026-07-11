# 02 - AWS CloudFront Hands-On Lab 1

> Goal: create a real CloudFront distribution in front of the S3 static site from `S3-Simple_Storage_Services/27`, and directly observe the cache-hit/cache-miss behavior Note 01 described.

---

## 1. Prerequisites

- The static site bucket from `S3-Simple_Storage_Services/27` (`demo-static-site-<unique-suffix>`), with `index.html`/`error.html` uploaded and static website hosting enabled.

---

## 2. Create the distribution

1. **CloudFront console** → **Distributions** → **Create distribution**.
2. **Origin domain**: select the S3 bucket. The console offers two sub-choices here worth noting up front (detailed fully in Note 03 and Note 06):
   - The bucket's **REST API endpoint** (`<bucket>.s3.amazonaws.com`) — works with Origin Access Control (Note 06) to keep the bucket private.
   - The bucket's **website endpoint** (`<bucket>.s3-website-<region>.amazonaws.com`) — required if you need S3's index/error-document routing (`S3-Simple_Storage_Services/26`) behind CloudFront, but this path **cannot** use Origin Access Control/OAI, since website endpoints only serve public content.
3. For this first lab, choose the **website endpoint** (simplest path, matching the bucket from Note 27) — leave the bucket public exactly as configured there.
4. **Default cache behavior**: leave defaults for now (fully explored in Note 04).
5. **Create distribution**. Provisioning takes several minutes to propagate to all edge locations.

---

## 3. Test it

1. Copy the distribution's **domain name** (e.g. `d1234abcdefgh.cloudfront.net`) once status shows **Enabled/Deployed**.
2. ```bash
   curl -I https://d1234abcdefgh.cloudfront.net/
   ```
3. Notice the response is served over **HTTPS** automatically, even though the underlying S3 website endpoint is HTTP-only (`S3-Simple_Storage_Services/26`) — CloudFront terminates HTTPS at the edge and can talk to the origin over whichever protocol the origin supports, decoupling the visitor-facing protocol from the origin's own capability.

---

## 4. Observe cache hit vs. cache miss

```bash
curl -sI https://d1234abcdefgh.cloudfront.net/index.html | grep -i x-cache
```

- **First request** (or the first after cache expiration): `X-Cache: Miss from cloudfront` — CloudFront had to fetch from the origin.
- **Subsequent requests** (within the cache TTL): `X-Cache: Hit from cloudfront` — served entirely from the edge, no origin hit at all.

> 🧠 The `X-Cache` response header is the single fastest way to confirm, hands-on, whether CloudFront actually served a request from cache or had to reach back to the origin — worth checking any time cache behavior needs debugging throughout this folder.

---

## 5. Recap

- A CloudFront distribution can be pointed at either an S3 **REST endpoint** (private-capable, via OAC) or **website endpoint** (public-only, but supports index/error document routing) — this choice matters and is expanded in Notes 03 and 06.
- CloudFront terminates HTTPS at the edge regardless of the origin's own protocol support.
- The `X-Cache` response header directly shows Hit vs. Miss — the fastest hands-on way to confirm caching behavior.
- Next: Note 03 — AWS CloudFront Origin Setting, covering every origin configuration option in depth.

### Sources
- [Getting started with a standard distribution — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/GettingStarted.SimpleDistribution.html)
- [Using Amazon S3 origins and custom origins — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/DownloadDistS3AndCustomOrigins.html)
