# 12 - AWS CloudFront Setting Options: Supported HTTP Versions & Default Root Object

> Goal: cover two **distribution-wide** settings (as opposed to Notes 04-11's cache-behavior-specific ones) — which HTTP protocol versions viewers can use, and what CloudFront serves for a bare root/subdirectory request.

---

## 1. Supported HTTP versions

A distribution can be configured to accept viewer connections over:

| Version | Notes |
|---|---|
| **HTTP/1.1** | The baseline, universally supported |
| **HTTP/2** | Multiplexes many requests over a single connection — reduces latency for pages loading many small assets (common for typical websites), widely supported by modern browsers |
| **HTTP/3 (QUIC)** | Built on UDP instead of TCP — faster connection establishment and better performance on lossy/high-latency networks (e.g. mobile), the newest option |

Enabling the newer versions is generally a **free performance improvement** with no downside for compatible clients — older/incompatible clients simply negotiate down to a version they support, so there's little reason not to enable HTTP/2 and HTTP/3 unless a specific legacy client requirement says otherwise.

> 🧠 **Mental model:** this setting only affects the **viewer-to-CloudFront** leg (same scope as Note 05's viewer protocol policy) — it has no bearing on what protocol CloudFront uses when talking to the **origin**, which is governed independently by the origin protocol policy.

---

## 2. Default Root Object

**Default Root Object** tells CloudFront what to serve when a viewer requests the **distribution's root URL** with no specific file path (e.g. `https://d1234abcdefgh.cloudfront.net/` with nothing after the trailing slash) — typically set to `index.html`.

> ⚠️ **Default Root Object only applies to the distribution's actual root** — it does **not** automatically apply to every subdirectory (e.g. a request for `/photos/` doesn't automatically get `/photos/index.html` from this setting alone). Getting subdirectory-level default-document behavior requires either an **S3 website endpoint origin** (which has its own index-document logic, `S3-Simple_Storage_Services/26`) or a **CloudFront Function** (Note 11) rewriting the URI, as shown in that note's own example.

---

## 3. Configure both

1. **CloudFront console** → distribution → **General** tab → **Edit**.
2. **Supported HTTP versions**: check **HTTP/2** and **HTTP/3** in addition to the default HTTP/1.1.
3. **Default root object**: `index.html`.
4. **Save changes**.

---

## 4. Verify

```bash
curl -I --http2 https://d1234abcdefgh.cloudfront.net/
curl https://d1234abcdefgh.cloudfront.net/       # should return index.html's content, not a 403/404
```

> 🎯 **Exam tip:** "requests to the root URL of a distribution return an error/access denied, but requests to `/index.html` directly work fine" is the textbook **missing Default Root Object** scenario.

---

## 5. Recap

- **Supported HTTP versions** governs the viewer-to-CloudFront protocol only — enabling HTTP/2 and HTTP/3 alongside HTTP/1.1 is a low-risk, generally-beneficial default.
- **Default Root Object** serves a specified file (e.g. `index.html`) for the distribution's bare root — but does **not** extend that behavior to subdirectories automatically; that needs an S3 website-endpoint origin or a CloudFront Function URI rewrite instead.
- Next: Note 13 — AWS CloudFront Setting Options, Part 2, covering the remaining distribution-wide settings (price class, logging, WAF association).

### Sources
- [Values that you specify when you create or update a distribution — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/distribution-web-values-specify.html)
- [Specifying a default root object — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/DefaultRootObject.html)
