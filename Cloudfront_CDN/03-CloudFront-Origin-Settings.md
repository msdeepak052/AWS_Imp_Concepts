# 03 - AWS CloudFront Origin Setting

> Goal: cover every origin-configuration option in depth — S3 vs. custom origins, origin path, custom headers, and connection tuning — building on the origin-type choice previewed in Note 02.

---

## 1. The two origin types

| Origin type | Examples | Key trait |
|---|---|---|
| **S3 origin** | An S3 bucket's REST endpoint | Can be kept fully private, accessed only via CloudFront (Origin Access Control, Note 06) |
| **Custom origin** | An ALB, an EC2 instance, an on-prem server, an S3 **website** endpoint, or any other HTTP(S) server | Must be reachable over HTTP/HTTPS directly; CloudFront talks to it like any HTTP client |

> ⚠️ An **S3 website endpoint** (Note 02) is technically configured as a **custom origin**, not an "S3 origin" in CloudFront's own terminology — this is a commonly confused point, since it's still an S3 bucket underneath, but CloudFront treats it as a generic HTTP origin because website endpoints don't support the AWS Signature-based authentication that true "S3 origin" mode (REST endpoint + OAC) requires.

---

## 2. Origin path — serving from a subdirectory

**Origin path** lets a distribution serve content from a specific **prefix** within the origin, rather than its root — e.g. setting origin path to `/production` means a viewer request for `/logo.png` actually fetches `/production/logo.png` from the origin. Useful for serving multiple environments (staging/production) or multiple apps from one shared bucket/origin, each behind its own distribution or cache behavior.

---

## 3. Custom headers — passing extra information to the origin

CloudFront can attach **custom HTTP headers** to every request it forwards to the origin (not visible to or settable by the end viewer) — commonly used to:

- Pass a **shared secret header** that the origin (e.g. an ALB or application server) checks for, so the origin can verify a request genuinely came through CloudFront and reject anything hitting it directly — a lightweight defense-in-depth measure for custom origins (S3 has OAC/OAI for this instead, Note 06).
- Pass environment or routing metadata the origin application expects.

---

## 4. Origin connection settings — tuning resilience

For **custom origins** specifically, CloudFront exposes tunable connection behavior:

| Setting | What it controls |
|---|---|
| **Origin connection attempts** | How many times CloudFront retries connecting to the origin before giving up (default 3) |
| **Origin connection timeout** | How long CloudFront waits for the origin to respond before considering the attempt failed (default 10 seconds) |
| **Origin keep-alive / response timeout** (custom origins) | How long a connection to the origin stays open for reuse, and how long CloudFront waits for a full response |

Tuning these matters most for **slow-responding origins** (e.g. a backend doing heavy computation) — too aggressive a timeout can cause CloudFront to give up and serve an error page (Note 17) before a legitimately-slow-but-successful origin response ever arrives.

---

## 5. Origin Shield — an additional caching tier

**Origin Shield** adds one extra, centralized caching layer **between** the many edge locations and the origin — all edge locations funnel their cache misses through this single shield location first, rather than each independently hitting the origin. This further **reduces origin load** for very high-traffic distributions with many edge locations experiencing simultaneous cache misses (e.g. right after a cache invalidation, Note 18, or for content with many simultaneous first-time viewers across the globe).

> 🎯 **Exam tip:** "origin is being overwhelmed with duplicate requests from many different edge locations for the same rarely-cached content" is the signature **Origin Shield** scenario.

---

## 6. Multiple origins on one distribution

A single distribution isn't limited to one origin — you can configure **multiple origins** (e.g. one S3 bucket for static assets, one ALB for a dynamic API), then use **cache behaviors** (Note 04) with different **path patterns** to route different URL paths to different origins within the same distribution — e.g. `/api/*` → the ALB, everything else → the S3 bucket.

---

## 7. Recap

- Origins are either **S3 origin** (REST endpoint, supports OAC) or **custom origin** (everything else, including S3 website endpoints) — a distinction that matters for which access-control mechanisms are available (Note 06).
- **Origin path** scopes a distribution/cache-behavior to a subdirectory of the origin; **custom headers** let CloudFront pass origin-only metadata, including a shared-secret pattern for verifying traffic came through CloudFront.
- **Origin Shield** adds a centralized caching tier to protect origins from duplicate cache-miss traffic across many edge locations.
- One distribution can have **multiple origins**, routed to by path pattern via multiple cache behaviors.
- Next: Note 04 — Default Cache Behavior Option, covering the caching rules applied to requests reaching this origin.

### Sources
- [Working with origins — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/DownloadDistS3AndCustomOrigins.html)
- [Using an origin path — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/distribution-web-values-specify.html#DownloadDistValuesOriginPath)
- [Using Origin Shield — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/origin-shield.html)
