# 07 - Cloudfront Allowed HTTP Method

> Goal: understand the **Allowed HTTP Methods** cache-behavior setting — which verbs CloudFront will even forward to the origin at all — and why this setting works hand-in-hand with Note 06's OAC to let CloudFront proxy uploads, not just reads.

---

## 1. The two method-set options

| Option | Methods allowed |
|---|---|
| **GET, HEAD** | Read-only — the default, and correct choice for a distribution serving static/cacheable content only |
| **GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE** | Full read/write — required for a distribution that must also proxy uploads, form submissions, or API calls through to the origin |

> ⚠️ Choosing **GET, HEAD** only isn't just "extra security" — it's a **hard block**. A `POST` request against a distribution configured for GET/HEAD-only receives an error directly from CloudFront, and **never reaches the origin at all**, regardless of what the origin itself would have allowed.

---

## 2. Why this matters together with OAC (Note 06)

Recall Note 06: OAC supports more HTTP methods than legacy OAI, specifically enabling **PUT/POST proxying to S3**. But enabling the full method set on OAC alone isn't enough — the **cache behavior's Allowed HTTP Methods** setting must **also** include `PUT`/`POST` (etc.), or CloudFront rejects the write attempt before OAC's expanded capability ever comes into play. The two settings are independent gates that both need to agree — the same "every applicable layer must allow it" pattern that's recurred throughout this repo (`S3-Simple_Storage_Services/09`, `IAM/01`).

---

## 3. Which methods actually get cached

Even with the full method set allowed, **only `GET` and `HEAD` responses are ever cached** — `POST`/`PUT`/`PATCH`/`DELETE` requests are always **passed through live to the origin**, every single time, never served from cache. This makes sense: caching a `DELETE` response would be actively dangerous (serving a stale "deleted successfully" to a request that never actually reached the origin).

> 🧠 **Mental model:** "Allowed HTTP Methods" answers *which verbs get through CloudFront at all*; caching behavior (Note 09) separately answers *which of those get served from a cached copy* — and the answer to the second question is always "only the read-only ones," regardless of the first setting.

---

## 4. Typical configurations by use case

| Use case | Allowed methods |
|---|---|
| Static website / asset CDN (images, JS, CSS) | GET, HEAD only |
| API gateway-style distribution proxying a backend | Full method set (GET/HEAD/OPTIONS/PUT/POST/PATCH/DELETE) |
| Distribution serving both static assets **and** an API (multiple cache behaviors, Note 04) | GET/HEAD-only on the static-asset cache behavior; full method set on the `/api/*` cache behavior |

> 🎯 **Exam tip:** "users can view content through CloudFront but form submissions/uploads fail with an error, even though the origin itself accepts them" is the signature **Allowed HTTP Methods** misconfiguration — the fix is enabling the full method set on the relevant cache behavior, not touching the origin or OAC configuration.

---

## 5. Recap

- **Allowed HTTP Methods** is a hard gate at the CloudFront layer — a disallowed method never reaches the origin, regardless of what the origin or OAC (Note 06) would otherwise permit.
- Even with all methods allowed, **only GET/HEAD responses are ever cached** — everything else is always forwarded live.
- A distribution serving both static content and a dynamic API typically needs **separate cache behaviors** (Note 04) with different method sets for each path pattern.
- Next: Note 08 — AWS CloudFront Default Cache Behavior Restrict Viewer Access, controlling *who* (not just *what verbs*) can reach the content at all.

### Sources
- [Cache behavior settings — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/distribution-web-values-specify.html#DownloadDistValuesCacheBehavior)
- [Restricting access to an Amazon S3 origin — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html)
