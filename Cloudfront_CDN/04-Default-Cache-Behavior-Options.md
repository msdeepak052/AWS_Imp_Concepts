# 04 - Default Cache Behavior Option

> Goal: understand the **cache behavior** — the rule set governing how requests matching a given path pattern are handled — and specifically the **default** cache behavior every distribution must have. Notes 07-10 each go deep on one specific cache-behavior setting; this note is the map of the whole object.

---

## 1. What a cache behavior actually is

A **cache behavior** binds a **path pattern** (e.g. `/images/*`, or `*` for "everything else") to a specific set of rules: which **origin** to use, which **HTTP methods** to allow (Note 07), how to handle **viewer access restrictions** (Note 08), what governs the **cache key** (Note 09), and which **response headers policy** applies (Note 10).

- Every distribution has exactly **one default cache behavior**, matching path pattern `*` — the catch-all applied to any request that doesn't match a more specific behavior.
- Additional cache behaviors can be added for specific path patterns (e.g. `/api/*` routed to a different origin with no caching, while `/*` serves cached static assets) — evaluated in **priority order**, with the **first matching pattern** (most specific first) winning.

> 🧠 **Mental model:** think of cache behaviors like a router's rule table — the default behavior is the catch-all route, and any additional behaviors are more specific routes checked first, in priority order, before falling through to the default.

---

## 2. The core caching settings on any cache behavior

| Setting | What it controls |
|---|---|
| **Viewer protocol policy** | Whether HTTP requests are allowed, redirected to HTTPS, or rejected entirely (covered fully with certificates in Note 05) |
| **Allowed HTTP methods** | Which HTTP verbs CloudFront forwards to the origin (Note 07) |
| **Cache key and origin requests** | What varies the cached copy (query strings, headers, cookies) — either via a legacy TTL-based model or the modern **Cache Policy** / **Origin Request Policy** objects (Note 09) |
| **Compress objects automatically** | Whether CloudFront automatically gzip/brotli-compresses eligible text-based responses at the edge, reducing transfer size |
| **Response headers policy** | Add/override/remove specific HTTP response headers, e.g. security headers (Note 10) |
| **Function associations** | CloudFront Functions / Lambda@Edge triggers at specific request/response lifecycle points (Note 11) |

---

## 3. TTL settings — how long content stays cached

Three TTL values (when using the legacy caching model, or as a fallback even with a modern Cache Policy) control cache freshness:

| TTL | Meaning |
|---|---|
| **Minimum TTL** | The shortest time content is cached, even if the origin's own cache-control headers say less |
| **Maximum TTL** | The longest time content is cached, even if the origin says more — a ceiling |
| **Default TTL** | Used **only** when the origin doesn't specify its own caching duration at all (no `Cache-Control`/`Expires` header) |

> ⚠️ If the origin **does** send its own `Cache-Control: max-age=...` header, that value governs (within the Minimum/Maximum TTL bounds) — **Default TTL only kicks in when the origin is silent about caching entirely**. This is a frequently misunderstood detail: setting a high "Default TTL" doesn't override an origin that's actively telling CloudFront to cache for a shorter time.

---

## 4. Path pattern priority — a worked example

```
Cache behaviors (in priority order):
1. /api/*        → ALB origin, no caching
2. /images/*     → S3 origin, long TTL
3. *  (default)  → S3 origin, default TTL
```

A request for `/images/logo.png` matches pattern 2 (more specific, evaluated before the default) and gets long-TTL caching from the S3 origin; a request for `/api/products` matches pattern 1 and bypasses caching against the ALB entirely; anything else falls through to the default behavior.

> 🎯 **Exam tip:** "serve static assets from cache aggressively while ensuring API calls always reach the origin fresh" is the textbook **multiple cache behaviors, prioritized by path pattern** scenario — a single cache behavior can't express two different caching philosophies for two different URL spaces on the same distribution.

---

## 5. Recap

- A **cache behavior** maps a path pattern to origin, HTTP method, cache-key, and response-header rules; every distribution has one mandatory **default** (`*`) behavior, plus optional path-specific ones evaluated in priority order.
- **TTL settings** (Min/Max/Default) bound how long content is cached — Default TTL only applies when the origin sends no caching headers of its own.
- Notes 07-11 each expand one specific setting living inside this cache-behavior object in depth.
- Next: Note 05 — CloudFront Custom HTTPS, covering the **Viewer protocol policy** setting and custom domain certificates in full.

### Sources
- [Cache behavior settings — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/distribution-web-values-specify.html#DownloadDistValuesCacheBehavior)
- [Managing how long content stays in the cache (expiration) — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Expiration.html)
- [Path pattern precedence — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/HowCloudFrontWorks.html#HowCloudFrontWorks-PathPattern)
