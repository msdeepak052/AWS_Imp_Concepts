# 26 - AWS S3 Static Web Hosting

> Goal: understand what "static website hosting" actually adds on top of a plain public bucket (Note 25) — index/error document routing and a dedicated website endpoint — before Notes 27-28 configure it hands-on.

---

## 1. What "static" means here

A **static** website is one made entirely of files that don't change based on server-side logic per request — HTML, CSS, JavaScript, images — as opposed to a **dynamic** site requiring a server to run application code (e.g. a database-backed page rendered per request). S3 can serve static files directly, but has **no ability to run server-side code** — anything dynamic (the CloudMart capstone's backend API, for instance) needs actual compute (EC2, Lambda, etc.), not S3 alone.

> 🧠 **Mental model:** S3 static hosting is a filing cabinet that can also politely hand out a specific default file when someone asks for "whatever's at the front" (the index document) — it's not a clerk who can look anything up or compute an answer.

---

## 2. What static website hosting adds over a plain public bucket

A bucket made public via Notes 23-25 already lets anyone fetch individual objects directly by key. **Enabling static website hosting** on top of that adds:

- A dedicated **website endpoint** URL, in the format `http://<bucket-name>.s3-website-<region>.amazonaws.com` — distinct from the normal REST API endpoint used for `GetObject` calls.
- An **Index document** setting (e.g. `index.html`) — the file served when a request doesn't specify one (e.g. a request to `/` or `/photos/` serves `index.html` or `photos/index.html` respectively).
- An **Error document** setting (e.g. `error.html`) — served for 4xx errors instead of S3's generic XML error response, letting a website show a proper branded "page not found" page instead of raw API error XML.
- Optional **redirect rules** — e.g. redirecting all requests for an old path to a new one, entirely configured within S3 itself.

> ⚠️ The **website endpoint** only supports **HTTP**, not HTTPS, directly — getting HTTPS on a custom domain requires putting **CloudFront** in front of the bucket (a separate topic, covered in this repo's `CDN` folder), which is also the standard production pattern regardless, since it adds caching, HTTPS, and a proper custom domain all at once.

---

## 3. Static hosting still requires the bucket to be public

Enabling static website hosting **does not**, by itself, make the bucket's content publicly readable — it's purely a routing/serving configuration layered on top. The bucket must **still** go through Note 25's two-step process (relax Block Public Access, attach a public-read bucket policy) for the website to actually be reachable by visitors; without that, the website endpoint just returns access-denied errors for every request.

---

## 4. Recap

- Static website hosting adds a dedicated **website endpoint**, **index document** routing, **error document** handling, and optional redirect rules on top of an already-public bucket.
- S3 can only serve **static** files — no server-side logic — anything dynamic needs real compute elsewhere.
- The website endpoint is **HTTP-only**; HTTPS on a custom domain requires CloudFront in front of it.
- The bucket must still be made public (Note 25) — static hosting configuration alone doesn't grant public read access.
- Next: Note 27 — AWS S3 Static Web Hosting (Hands-On), configuring and testing this for real.

### Sources
- [Hosting a static website using Amazon S3 — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html)
- [Configuring an index document — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/IndexDocumentSupport.html)
- [Amazon S3 website endpoints — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteEndpoints.html)
