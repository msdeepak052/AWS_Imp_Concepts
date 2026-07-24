# 29 - AWS S3 Cross-Origin Resource Sharing (CORS) (Hands-On)

> Goal: understand the browser same-origin restriction CORS exists to relax, then configure a real CORS rule letting a webpage on one origin fetch resources from an S3 bucket on another.

---

## 1. The problem: the browser's same-origin policy

Browsers enforce a **same-origin policy**: JavaScript running on a page from `https://app.cloudmart.example` is, by default, **blocked** from making a fetch/XHR request to a different **origin** — defined as the combination of scheme + domain + port — such as `https://demo-assets-bucket.s3.amazonaws.com`, even if that S3 bucket is genuinely public and would otherwise happily return the data to a direct browser navigation or a `curl` request.

> 🧠 **Mental model:** this restriction has nothing to do with S3's own permissions (Notes 09-13) — those already say the request is allowed. It's the **browser itself** refusing to hand the response back to the calling page's JavaScript, as a security measure against malicious cross-site scripts silently reading data from other origins on a user's behalf. **CORS** is the mechanism by which the *resource's own server* (S3, here) can explicitly tell the browser "it's fine, let JavaScript from this other origin read my response."

---

## 2. What a CORS rule actually configures

A **CORS configuration** on a bucket is a list of rules, each specifying:

| Element | Meaning |
|---|---|
| **AllowedOrigins** | Which origin(s) are permitted to make cross-origin requests (e.g. `https://app.cloudmart.example`, or `*` for any) |
| **AllowedMethods** | Which HTTP methods are allowed (`GET`, `PUT`, `POST`, `DELETE`, `HEAD`) |
| **AllowedHeaders** | Which request headers the browser is allowed to send as part of the cross-origin request |
| **ExposeHeaders** | Which response headers JavaScript is allowed to actually read (some headers aren't exposed to JS by default even if the request itself succeeds) |
| **MaxAgeSeconds** | How long the browser can cache the preflight response, to avoid re-checking on every single request |

---

## 3. Configure CORS via the console

1. **S3 console** → bucket (e.g. the Note 27/28 static site's asset bucket) → **Permissions** tab → **Cross-origin resource sharing (CORS)** → **Edit**.
2. Paste:
   ```json
   [
     {
       "AllowedOrigins": ["https://app.cloudmart.example"],
       "AllowedMethods": ["GET"],
       "AllowedHeaders": ["*"],
       "MaxAgeSeconds": 3000
     }
   ]
   ```
3. **Save changes**.

---

## 4. Test the difference CORS makes

```javascript
// Running as JavaScript on https://app.cloudmart.example
fetch('https://demo-assets-bucket.s3.amazonaws.com/logo.png')
  .then(r => console.log('Success', r.status))
  .catch(e => console.error('Blocked by CORS', e));
```

- **Without** the CORS rule from Section 3: the browser's developer console shows a CORS error, even though the underlying HTTP request may have actually succeeded at the network level — the browser withholds the response from the calling script.
- **With** the CORS rule in place, naming `https://app.cloudmart.example` as an allowed origin: the fetch succeeds, and the script can read the response normally.

> ⚠️ A plain `<img src="...">` tag or direct browser navigation to the S3 URL is **never** blocked by CORS — the same-origin policy specifically restricts **script-initiated** cross-origin reads (`fetch`, `XMLHttpRequest`), not ordinary resource loading like images, stylesheets, or direct navigation. This is a common point of confusion: "the image loads fine in a new tab, but my JavaScript `fetch()` to the same URL fails" is the exact signature of a missing CORS configuration.

---

## 5. Recap

- **CORS** is a browser-enforced, same-origin-policy relaxation mechanism — it has nothing to do with S3's own IAM/bucket-policy/ACL permissions (Notes 09-13), which are a completely separate, already-satisfied check by the time CORS even comes into play.
- A CORS rule on the bucket explicitly allows specific origins, methods, and headers for **script-initiated** cross-origin requests.
- Direct navigation, `<img>` tags, and similar non-script resource loads are **never** subject to CORS — only `fetch`/`XMLHttpRequest`-style calls are.
- Next: Note 30 — AWS S3 Cross-Region Replication (CRR) (Hands-On), automatically copying objects to a bucket in a different Region.

### Sources
- [Cross-origin resource sharing (CORS) — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/cors.html)
- [Enabling and configuring CORS — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ManageCorsUsing.html)
- [MDN: Cross-Origin Resource Sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
