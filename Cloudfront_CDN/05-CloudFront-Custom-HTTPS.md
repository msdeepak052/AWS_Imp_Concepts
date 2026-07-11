# 05 - CloudFront Custom HTTPS

> Goal: put a custom domain (not the default `*.cloudfront.net` name) in front of a distribution with a real, trusted HTTPS certificate — completing the "friendly domain + HTTPS" gap `S3-Simple_Storage_Services/28` flagged as unsolvable with S3 website hosting alone.

---

## 1. Why the default CloudFront domain isn't enough for production

Every distribution gets a working `https://d1234abcdefgh.cloudfront.net` domain automatically, secured by a **default CloudFront certificate** — but real applications need a **branded domain** (`www.cloudmart.example`), and the default certificate **only covers the `*.cloudfront.net` name**, not any custom domain you'd want to use.

---

## 2. The three pieces required

1. **An SSL/TLS certificate** covering the custom domain, issued via **AWS Certificate Manager (ACM)** — and critically, **the certificate must be requested in the `us-east-1` (N. Virginia) Region**, regardless of where your users or origin actually are, since CloudFront is a global service that only looks for certificates in that one specific Region.
2. **Alternate Domain Names (CNAMEs)** configured on the distribution — e.g. `www.cloudmart.example` — telling CloudFront which domain(s) besides the default one should be accepted.
3. **A DNS record** (e.g. a Route 53 Alias record, same mechanism as `S3-Simple_Storage_Services/28`) pointing the custom domain at the distribution's `*.cloudfront.net` name.

> ⚠️ **The `us-east-1` certificate requirement is one of the most frequently tested CloudFront facts on SAA-C03** — requesting the certificate in any other Region (e.g. the Region your origin actually lives in) means CloudFront simply won't see it as available to attach.

---

## 3. Request the certificate and attach it

1. **ACM console**, switched to **us-east-1** → **Request a certificate** → **Request a public certificate**.
2. Domain name: `www.cloudmart.example` (add `cloudmart.example` too if the root domain should also work).
3. Validate ownership via **DNS validation** (ACM provides a CNAME record to add to the domain's hosted zone — Route 53 can do this with one click if the zone is already there).
4. Once **Issued**, go to the CloudFront distribution → **General** → **Edit** → **Alternate domain name (CNAME)**: add `www.cloudmart.example` → **Custom SSL certificate**: select the newly-issued certificate → **Save changes**.

---

## 4. Point DNS at the distribution

**Route 53 console** → hosted zone → **Create record** → Name: `www` → **Alias** → **Alias to CloudFront distribution** → select the distribution → **Create records** — the same Alias-record mechanism as `S3-Simple_Storage_Services/28`, just targeting a CloudFront distribution instead of an S3 website endpoint directly.

---

## 5. Viewer protocol policy — what happens to plain HTTP requests

Back in the cache behavior (Note 04), **Viewer protocol policy** decides what CloudFront does with a request that arrives over plain HTTP:

| Option | Behavior |
|---|---|
| **HTTP and HTTPS** | Both accepted as-is — generally discouraged for anything beyond a quick test |
| **Redirect HTTP to HTTPS** | Plain HTTP requests get a 301/302 redirect to the HTTPS version — the standard, recommended production setting |
| **HTTPS only** | Plain HTTP requests are rejected outright |

> 🎯 **Exam tip:** "users see a certificate error when their custom domain is attached to a distribution" almost always traces back to either **(1)** the certificate was requested in the wrong Region (must be `us-east-1`), or **(2)** the domain wasn't added as an **Alternate Domain Name** on the distribution — these two are the standard troubleshooting pair for this scenario.

---

## 6. Origin-side HTTPS is a separate, independent setting

Note 05's focus so far is the **viewer-to-CloudFront** leg. CloudFront **also** has an independent setting for the **CloudFront-to-origin** leg — **Origin Protocol Policy** (HTTP only / HTTPS only / Match viewer) — meaning a distribution can terminate HTTPS at the edge for viewers while still talking plain HTTP to an origin that doesn't support TLS at all (or vice versa) — the two legs of the connection are configured completely independently.

---

## 7. Recap

- Custom domain HTTPS needs **three pieces**: an ACM certificate **in `us-east-1`**, the domain added as an **Alternate Domain Name** on the distribution, and a DNS record (typically a Route 53 Alias) pointing at the distribution.
- **Viewer protocol policy** controls how plain-HTTP viewer requests are handled; **Origin protocol policy** independently controls the CloudFront-to-origin leg — the two are decoupled.
- Next: Note 06 — CloudFront Origin Access, securing the S3-origin path from Note 03 so the bucket is only reachable through CloudFront, not directly.

### Sources
- [Using HTTPS with CloudFront — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cnames-https-dedicated-ip-or-sni.html)
- [Requiring HTTPS for communication between viewers and CloudFront — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/using-https-viewers-to-cloudfront.html)
- [Requirements for using SSL/TLS certificates with CloudFront — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cnames-and-https-requirements.html)
