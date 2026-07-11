# 09 - AWS CloudFront Default Cache Behavior — Cache Key And Origin Requests

> Goal: understand exactly what makes two requests "the same" for caching purposes — the **cache key** — via the modern **Cache Policy** and **Origin Request Policy** objects that replaced the older, more limited legacy TTL/forwarding settings.

---

## 1. What a cache key actually is

The **cache key** is the set of request attributes CloudFront uses to decide whether an incoming request can be served from an **existing** cached copy, or needs to be treated as a **different** cacheable variant entirely. By default, the cache key is just the **request path** — meaning `/product?id=1` and `/product?id=2` would, without further configuration, be treated as the exact same cache entry, potentially serving the wrong product's data.

> ⚠️ This default-cache-key behavior is a classic real-world CloudFront misconfiguration: dynamic content that varies by query string, header, or cookie needs those specific elements **explicitly added to the cache key**, or CloudFront will happily serve one user's cached response to a completely different request.

---

## 2. Cache Policy — controlling the cache key

A **Cache Policy** (attached to a cache behavior) explicitly declares which of three categories of request data should be included in the cache key:

| Category | Example |
|---|---|
| **Query strings** | None / all / an allow-list of specific parameter names / a deny-list |
| **Headers** | None / an allow-list of specific header names (e.g. `Accept-Language`, to cache a different version per locale) |
| **Cookies** | None / all / an allow-list of specific cookie names |

Each additional included dimension **increases the number of distinct cached variants** stored — improving correctness (no more wrongly-shared cache entries) but potentially lowering the **cache hit ratio** (more distinct variants means each one is requested less often, so fewer requests find an existing cached copy).

> 🧠 **Mental model:** the cache key is the "address" CloudFront uses to file away a cached response — the narrower the address (path only), the more requests share one cache slot (higher hit ratio, but risk of serving the wrong content for anything actually variable); the wider the address (path + query + headers + cookies), the more precisely correct each cache slot is, at the cost of more cache misses overall.

---

## 3. Origin Request Policy — what CloudFront forwards to the origin on a cache miss

Separately, an **Origin Request Policy** controls what CloudFront sends **to the origin** on a cache miss — which can be **broader** than the cache key itself. For example, you might cache based on **only** the `Accept-Language` header (a small, controlled set of cache variants), while still forwarding the full set of headers/cookies/query strings the origin application actually needs to render a correct response — decoupling "what makes this cacheable as distinct" from "what the origin needs to know to answer the request."

> 🎯 **Exam tip:** "the cache hit ratio is too low because too much varies the cache key" or "dynamic content is being served incorrectly to the wrong users" are the two opposite-direction signals this note's settings resolve — too broad a cache key hurts hit ratio; too narrow a cache key (or none at all) risks serving stale/wrong content. The fix is always tuning the **Cache Policy**, with the **Origin Request Policy** handling anything the origin needs but that shouldn't affect caching itself.

---

## 4. Managed policies vs. custom policies

CloudFront ships several **AWS managed** cache policies and origin request policies for common cases (e.g. `CachingOptimized`, `CachingDisabled`, `AllViewer`) — usable directly without authoring your own, exactly parallel to `IAM/02`'s AWS managed IAM policies. A **custom** policy is created when the specific combination of query strings/headers/cookies needed doesn't match any managed option.

---

## 5. Recap

- The **cache key** (governed by a **Cache Policy**) determines which requests are treated as the same cached entry — by default, just the path, which is often too coarse for dynamic content varying by query string, header, or cookie.
- An **Origin Request Policy** independently controls what's forwarded to the origin on a cache miss, which can be broader than the cache key itself.
- Broadening the cache key improves correctness for variable content but can reduce the cache hit ratio — a real trade-off to tune deliberately, not a "more is always better" setting.
- Next: Note 10 — AWS CloudFront Default Cache Behavior: Response Header Policy, controlling what headers actually come back to the viewer.

### Sources
- [Understanding the cache key — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/understanding-the-cache-key.html)
- [Controlling the cache key with a cache policy — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/controlling-the-cache-key.html)
- [Controlling origin requests with an origin request policy — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/controlling-origin-requests.html)
