# 14 - AWS CloudFront Geographic Restrictions

> Goal: block or allow access to an entire distribution's content based on the viewer's **country**, using CloudFront's built-in geo restriction feature — and see how this is a fundamentally different tool from Route 53's geolocation/latency-based **routing** covered in this repo's `Route53` folder.

---

## 1. What geographic restriction actually does

CloudFront can determine a viewer's **country** (via its IP address, using a geo-IP lookup CloudFront performs automatically) and either **allow only specific countries** or **block specific countries** from reaching the distribution's content at all — a request from a disallowed country receives an error response instead of the actual content.

> 🧠 **Mental model:** this is an **allow/deny gate at the edge**, evaluated **before** anything else (caching, origin requests) — not a routing decision. Contrast this with Route 53 geolocation routing, which decides **which origin/endpoint** a DNS query resolves to based on the resolver's location — Route 53 routes *to* different destinations; CloudFront geo restriction simply **blocks or allows** access to the *same* distribution's content.

---

## 2. The two modes

| Mode | Behavior |
|---|---|
| **Allowlist** | Only the specified countries can access the content; every other country is blocked |
| **Blocklist** | The specified countries are blocked; every other country can access the content |

Configured per-distribution (not per cache behavior) — **CloudFront console** → distribution → **Geographic restrictions** tab → **Edit** → choose **Allow list** or **Block list** → select countries → **Save changes**.

---

## 3. Why this exists — the common real-world drivers

- **Licensing/content rights** — a media company may only be licensed to distribute certain video content in specific countries.
- **Regulatory/compliance requirements** — certain data or services may be legally restricted from being served to users in specific countries.
- **Reducing abuse from specific regions** — a blunt, country-level tool to cut off traffic from regions known to generate disproportionate abusive/fraudulent traffic (WAF, Note 13, is the more precise tool for this, but geo restriction is a simpler first line).

---

## 4. Custom error responses for blocked requests

A blocked request returns an HTTP 403 by default — this can be customized (Note 17's error-page mechanism) to show a friendly "not available in your country" message instead of a generic error.

> 🎯 **Exam tip:** "block or allow access to content based on the end user's country" is the CloudFront **geographic restriction** scenario — direct and specific enough that it rarely gets confused with anything else on the exam, **except** the deliberate distinction from Route 53 geolocation routing (which chooses a destination, not an allow/deny decision) — expect the exam to test that exact distinction.

---

## 5. Recap

- **Geographic restriction** allow-lists or block-lists entire countries at the CloudFront edge, evaluated before caching or origin logic — a blunt allow/deny gate, not a routing mechanism.
- Distinct from **Route 53 geolocation routing**, which routes different users to different destinations rather than blocking access outright.
- Common drivers: content licensing, regulatory compliance, and coarse-grained abuse mitigation.
- Next: Note 15 — AWS CloudFront Origin Group Lab 1: EC2 & S3 Failover, moving from access-control features into CloudFront's own origin-level high-availability mechanism.

### Sources
- [Restricting the geographic distribution of your content — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/georestrictions.html)
- [Customizing error responses — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/HTTPStatusCodes.html)
