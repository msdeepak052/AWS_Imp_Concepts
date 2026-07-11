# 10 - AWS CloudFront Default Cache Behavior — Response Header Policy

> Goal: use a **Response Headers Policy** to add, override, or remove HTTP headers on the way back to the viewer — independent of whatever headers the origin itself sends — most commonly for security headers and CORS (`S3-Simple_Storage_Services/29`).

---

## 1. What a Response Headers Policy does

Attached to a cache behavior, a **Response Headers Policy** lets CloudFront modify the **response** headers sent to viewers, regardless of what the origin actually returned — the origin can be completely unaware this is happening. This is useful when you don't control the origin's code directly, or want a single, consistent header policy enforced at the edge across multiple origins/cache behaviors.

> 🧠 **Mental model:** this is the same "modify traffic in flight, transparently to the origin" idea as Note 03's custom request headers, just applied to the **response** side instead of the request side.

---

## 2. Common categories of headers set this way

| Category | Example headers | Purpose |
|---|---|---|
| **Security headers** | `Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options`, `Content-Security-Policy` | Harden the browser's handling of the response — CloudFront ships a managed **Security headers policy** with sensible defaults for exactly this |
| **CORS headers** | `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods` | Serve the same role as an S3 bucket's own CORS configuration (`S3-Simple_Storage_Services/29`), but enforced at the CloudFront edge instead of (or in addition to) the origin |
| **Custom headers** | Any application-specific header | E.g. a header identifying which cache behavior/distribution served the response, useful for debugging |

---

## 3. CORS at CloudFront vs. CORS at S3 — which one actually matters

If a distribution sits in front of an S3 bucket that already has its own CORS configuration (`S3-Simple_Storage_Services/29`), you now have **two possible places** CORS headers could come from: the origin (S3) or the CloudFront Response Headers Policy. Whichever one actually reaches the browser is what the browser evaluates — if CloudFront's policy is configured to **override** existing headers rather than just adding when absent, it takes precedence over whatever S3 itself sent.

> ⚠️ A CORS header set at the S3 origin only actually reaches the browser if CloudFront **forwards** it unmodified — and only takes effect for requests CloudFront doesn't already have cached with a *different* (or missing) CORS header from an earlier response. This is a real, sometimes-confusing interaction between Notes 09-10's caching rules and CORS, and a common source of "CORS works sometimes but not always" bug reports in production CloudFront setups.

---

## 4. Configure a managed Security Headers policy

1. **CloudFront console** → distribution → cache behavior → **Response headers policy** → **Create response headers policy** (or select the managed **`Managed-SecurityHeadersPolicy`**).
2. Review/adjust the security header values (e.g. `Strict-Transport-Security: max-age=63072000; includeSubdomains; preload`).
3. Attach it to the cache behavior → **Save changes**.
4. Verify:
   ```bash
   curl -I https://d1234abcdefgh.cloudfront.net/
   ```
   Confirm the security headers now appear in the response, even if the origin never set them.

---

## 5. Recap

- A **Response Headers Policy** adds/overrides/removes response headers at the CloudFront edge, independent of the origin's own behavior — most commonly used for **security headers** and **CORS**.
- When both S3 and CloudFront could set CORS/security headers, whichever policy actually reaches the browser (accounting for caching) is what governs — a real source of subtle bugs worth testing explicitly.
- Next: Note 11 — AWS CloudFront Function Associations, the most powerful cache-behavior customization: running actual code at specific points in the request/response lifecycle.

### Sources
- [Adding or removing HTTP headers in CloudFront responses — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/adding-response-headers.html)
- [Using the CloudFront managed Security headers policy — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/using-managed-response-headers-policies.html)
