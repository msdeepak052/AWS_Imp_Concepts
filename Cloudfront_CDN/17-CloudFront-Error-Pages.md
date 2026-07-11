# 17 - AWS CloudFront Tutorial: AWS CloudFront Error Pages

> Goal: configure **Custom Error Responses** so viewers see a branded, friendly error page instead of the origin's raw error output — and control how long CloudFront caches an error response itself, independent of Note 04's normal content-caching TTLs.

---

## 1. Why the origin's own error page usually isn't good enough

Left unconfigured, an error from the origin (a raw S3 `403`/`404` XML document, or an ALB's generic error page) is passed straight through to the viewer — functionally correct, but a poor user experience and inconsistent with the rest of a branded site. **Custom Error Responses** let CloudFront intercept specific HTTP status codes and serve a **different, custom object** (e.g. a nicely designed `error.html` from an S3 bucket) instead.

---

## 2. Configure a custom error response

1. **CloudFront console** → distribution → **Error pages** tab → **Create custom error response**.
2. **HTTP error code**: `403` (a common one, especially relevant for the private-bucket-via-OAC pattern from Note 06, where a disallowed direct request naturally returns 403).
3. **Customize error response**: **Yes**.
4. **Response page path**: `/error-pages/403.html` (a path within one of the distribution's own origins).
5. **HTTP response code**: choose what the viewer's browser actually receives — often deliberately set to `200` for a friendly page (so browsers/crawlers don't treat it as a hard failure) or kept as the original code if that distinction matters to the calling application.
6. **Error caching minimum TTL**: how long CloudFront caches **this error response itself** before trying the origin again on the next request.

---

## 3. Error Caching Minimum TTL — a setting worth understanding on its own

This TTL is **independent** of Note 04's normal content TTLs — it controls how long CloudFront serves the **cached error** before attempting a fresh request to the origin again, even for a URL that would otherwise have a much longer (or shorter) normal-content TTL.

> ⚠️ Setting this **too high** means a since-recovered origin keeps getting masked by a stale cached error for longer than necessary — visitors keep seeing "content unavailable" even after the underlying issue is fixed, until the error TTL expires. Setting it **too low** means a still-struggling origin gets hit with retries very frequently, potentially worsening an already-degraded situation. This is a genuine tuning trade-off, not a "set and forget" value.

---

## 4. Error pages combined with Geographic Restrictions (Note 14) and Origin Groups (Notes 15-16)

- A geo-restricted request (Note 14) returning `403` can be given a custom, friendly "not available in your region" page via this exact mechanism.
- When an Origin Group (Notes 15-16) fails over successfully, the viewer never even sees an error at all — the secondary origin's actual content is returned transparently. Custom Error Responses matter for the case where **both** the primary **and** the failover attempt fail, or where no Origin Group is configured at all.

---

## 5. Recap

- **Custom Error Responses** let CloudFront serve a friendly, branded page (and optionally a different HTTP status code to the viewer) in place of an origin's raw error output, for specific HTTP status codes.
- **Error Caching Minimum TTL** independently controls how long an error response itself stays cached before CloudFront retries the origin — a real tuning trade-off between masking a since-recovered origin and hammering a still-struggling one.
- Next: Note 18 — AWS CloudFront Cache Invalidation, the mechanism for forcibly clearing cached content before its TTL naturally expires — the final note in this folder.

### Sources
- [Creating custom error pages for specific HTTP status codes — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/HTTPStatusCodes.html#custom-error-pages)
- [How CloudFront processes and caches HTTP 4xx and 5xx status codes — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/HTTPStatusCodes.html)
