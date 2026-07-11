# 02 - Introduction of AWS S3 Simple Storage Service

> Goal: get hands-on with the absolute basics — create a bucket, upload/download an object, and understand bucket naming rules and Regional scoping — before layering on storage classes, versioning, and access control in the rest of this folder.

---

## 1. Bucket naming rules

A bucket name must be:

- **Globally unique** across every AWS account and every Region — once someone takes a name, no one else anywhere can use it, even in a different Region or account.
- 3-63 characters, lowercase letters, numbers, hyphens, and dots only, must start/end with a letter or number.
- **Not formatted like an IP address** (e.g. `192.168.1.1` is rejected).

> ⚠️ Because bucket names are globally unique, a common naming convention includes something account/company-specific (e.g. `acmecorp-prod-app-logs`) to avoid collisions with names other AWS customers may have already claimed.

---

## 2. Create a bucket and upload an object

1. **S3 console** → **Create bucket**.
2. **Bucket name**: `demo-s3-intro-<unique-suffix>`; **Region**: pick one (e.g. `ap-south-1`) — this is a real, fixed choice: **a bucket lives in exactly one Region**, permanently (data doesn't silently move Regions later; Cross-Region Replication, Note 30, is how you deliberately copy it elsewhere).
3. Leave other settings at their defaults for now (Block Public Access stays on — Notes 23-25 cover this properly) → **Create bucket**.
4. Open the bucket → **Upload** → add a file → **Upload**.
5. Select the uploaded object → **Download**, or copy its **Object URL** to fetch it via HTTPS (if the bucket/object were public — by default, everything here stays private).

---

## 3. Keys, not folders

1. Upload a file using **Upload** → **Add folder**, or manually type a key like `reports/2026/q1.csv` when uploading.
2. The console visually shows a `reports` folder containing a `2026` folder containing `q1.csv` — but this is purely a **display convenience**. Internally, the object's actual key is the single string `reports/2026/q1.csv`.
3. Confirm via the AWS CLI:
   ```bash
   aws s3api list-objects-v2 --bucket demo-s3-intro-<unique-suffix>
   ```
   The output shows one object with `Key: "reports/2026/q1.csv"` — no separate "folder" objects exist unless you explicitly created a zero-byte object ending in `/` (which some tools do, purely for display purposes in other clients).

---

## 4. Object size limits and basic upload mechanics

- A single object can be up to **5 TB**.
- A single **PUT** request (simple upload) is capped at **5 GB** — anything larger must use **multipart upload** (Note 38), which splits the object into parts uploaded (and retried) independently, then assembled by S3.
- Every object, once uploaded, gets an **ETag** (essentially a checksum/version identifier for that exact upload) and can carry both **system metadata** (e.g. `Content-Type`) and **user-defined metadata** (custom key-value pairs you attach).

---

## 5. Basic access model preview

By default, a freshly created bucket and every object in it are **private** — accessible only to the bucket owner's account (and anyone that account's IAM policies explicitly grant access to). Nothing here is public unless you deliberately configure it to be, which Notes 09-13 and 23-25 cover as their own dedicated topics — this note deliberately doesn't touch public access at all, so as not to get ahead of that later, more careful treatment.

> 🎯 **Exam tip:** "a bucket name is rejected as already in use, even though the account has never created a bucket by that name" is a common early confusion — the fix is understanding bucket names are **globally unique across all of AWS**, not just within your own account.

---

## 6. Recap

- A bucket lives in exactly **one Region**, has a **globally unique name**, and holds **objects** identified by a flat **key** string (folders are a display-only illusion).
- Objects can be up to 5 TB; a single PUT tops out at 5 GB, beyond which multipart upload (Note 38) is required.
- Everything is **private by default** — public access is a deliberate, later configuration step (Notes 23-25), not a default behavior.
- Next: Note 03 — S3 Storage Class, where the same object's data can live in cheaper, differently-available tiers depending on access pattern.

### Sources
- [Bucket naming rules — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html)
- [Uploading objects — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/upload-objects.html)
- [Amazon S3 objects overview — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingObjects.html)
