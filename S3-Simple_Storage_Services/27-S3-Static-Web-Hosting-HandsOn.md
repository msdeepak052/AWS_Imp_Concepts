# 27 - AWS S3 Static Web Hosting (Hands-On)

> Goal: actually host a working static site from an S3 bucket — combine Note 25's public-access steps with Note 26's website-hosting configuration end to end.

---

## 1. Create the bucket and upload site files

1. **S3 console** → **Create bucket** → `demo-static-site-<unique-suffix>` → Region of choice.
2. Upload `index.html` and `error.html`:
   ```html
   <!-- index.html -->
   <!DOCTYPE html><html><body><h1>Hello from S3 static hosting</h1></body></html>
   ```
   ```html
   <!-- error.html -->
   <!DOCTYPE html><html><body><h1>404 — Page Not Found</h1></body></html>
   ```

---

## 2. Make the bucket public (Note 25's two steps)

1. **Permissions** tab → **Block public access** → **Edit** → uncheck the two bucket-policy-related settings → confirm.
2. **Permissions** tab → **Bucket policy** → **Edit**:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "PublicReadForWebsite",
         "Effect": "Allow",
         "Principal": "*",
         "Action": "s3:GetObject",
         "Resource": "arn:aws:s3:::demo-static-site-<unique-suffix>/*"
       }
     ]
   }
   ```
   Save.

---

## 3. Enable static website hosting

1. **Properties** tab → **Static website hosting** → **Edit**.
2. **Enable** → **Hosting type**: **Host a static website**.
3. **Index document**: `index.html`. **Error document**: `error.html`.
4. **Save changes** — the console now shows a **Bucket website endpoint** URL, e.g. `http://demo-static-site-<unique-suffix>.s3-website.ap-south-1.amazonaws.com`.

---

## 4. Test it

```bash
curl http://demo-static-site-<unique-suffix>.s3-website.ap-south-1.amazonaws.com/
curl http://demo-static-site-<unique-suffix>.s3-website.ap-south-1.amazonaws.com/does-not-exist
```

The first request returns `index.html`'s content; the second returns `error.html`'s content with a 404 status — confirming both the index and error document routing configured in Section 3.

---

## 5. Troubleshooting

| Symptom | Likely cause |
|---|---|
| `403 Forbidden` on every request | Block Public Access still blocking the bucket policy, or the bucket policy wasn't saved/scoped correctly (Section 2) |
| `404` even for `index.html` at the root | Index document filename in Section 3 doesn't exactly match the uploaded file's name/casing |
| Site loads over the **REST endpoint** but not the **website endpoint** | Using the wrong endpoint URL format — website hosting requires the `s3-website` endpoint, not the standard `s3.amazonaws.com` REST endpoint, for index/error document behavior to apply |
| Browser shows a security warning / won't load via `https://` on this URL | Expected — the S3 website endpoint is **HTTP-only** (Note 26); HTTPS requires CloudFront in front of it |

---

## 6. Recap

- A working static site needs: uploaded site files, a public-read bucket policy (with Block Public Access relaxed), and static website hosting enabled with index/error documents configured.
- The resulting **website endpoint** (not the standard REST endpoint) is what actually applies index/error document routing.
- Next: Note 28 — AWS S3 Static Web Hosting With Route 53 (Hands-On), putting a friendly custom domain name in front of this same bucket.

### Sources
- [Hosting a static website using Amazon S3 — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html)
- [Tutorial: Configuring a static website on Amazon S3 — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/HostingWebsiteOnS3Setup.html)
