# 13 - AWS CloudFront Setting Options, Part 2

> Goal: cover the remaining distribution-wide settings that don't fit into a specific cache behavior — **Price Class**, **WAF association**, **standard logging**, and **IPv6** — closing out the general-settings tour started in Note 12.

---

## 1. Price Class — trading global edge coverage for cost

CloudFront's edge network spans **every region of the world**, but you can restrict **which edge locations are actually used** to serve your content, trading some geographic coverage for a lower cost:

| Price Class | Edge locations used |
|---|---|
| **Use all edge locations (best performance)** | Every edge location worldwide — highest cost, best performance for globally-distributed users |
| **Use North America and Europe** | A restricted subset — cheaper, but users outside these regions get routed to a farther-away edge location (still functional, just less optimal latency) |
| **Use North America, Europe, Asia, Middle East, and Africa** | A broader (but still not "all") subset |

> 🎯 **Exam tip:** "our users are concentrated in North America and Europe, and we want to reduce CloudFront cost without impacting performance for our actual audience" is the textbook **Price Class** scenario — it's purely a cost/coverage trade-off, never a caching or security setting.

---

## 2. AWS WAF association

A distribution can have an **AWS WAF Web ACL** attached, filtering malicious requests (SQL injection, XSS, rate-based rules, IP reputation lists) **before** they ever reach the cache-behavior logic or origin — configured via **AWS WAF console** → **Web ACLs** → associate with the specific CloudFront distribution. This is the standard way to add application-layer (L7) protection to content served through CloudFront, complementing CloudFront's built-in AWS Shield Standard DDoS protection (Note 01) with more granular, rule-based filtering.

---

## 3. Standard logging — access logs delivered to S3

CloudFront can deliver **detailed per-request access logs** to an S3 bucket — conceptually parallel to `S3-Simple_Storage_Services/32`'s server access logging, but for CloudFront requests specifically (viewer IP, requested object, response status, edge location that served the request, cache hit/miss, and more).

1. **Distribution** → **General** tab → **Edit** → **Standard logging** → **On** → select a destination S3 bucket and prefix.
2. Logs are delivered on a **best-effort basis** (same caveat as S3 server access logs) — not real-time, and not a hard delivery guarantee.

> 🧠 A common real use case: analyzing these logs (often via Athena) to compute actual **cache hit ratio** across a distribution, informing whether the cache-key tuning from Note 09 is working as intended.

---

## 4. IPv6 support

Distributions support IPv6 by default for viewer connections (dual-stack, alongside IPv4) — a simple toggle, with essentially no downside for standard web content, though relevant to disable only if downstream systems (e.g. WAF rules, custom logging pipelines) specifically aren't IPv6-aware yet.

---

## 5. Recap

- **Price Class** trades edge-location coverage for cost — pick based on where your actual audience is concentrated.
- **AWS WAF** attaches application-layer filtering (SQLi, XSS, rate limiting, IP reputation) directly to a distribution, ahead of cache behaviors and the origin.
- **Standard logging** delivers detailed, best-effort access logs to S3 — the CloudFront-level parallel to S3's own server access logging.
- This closes the distribution-wide settings tour (Notes 12-13). Next: Note 14 — AWS CloudFront Geographic Restrictions, controlling access by the viewer's country.

### Sources
- [Choosing the price class for a CloudFront distribution — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/PriceClass.html)
- [Using AWS WAF to control access to your content — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/distribution-web-awswaf.html)
- [Configuring and using standard logs (access logs) — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/AccessLogs.html)
