# 13 - AWS S3 — AWS S3 Bucket Access Control List (ACL)

> Goal: understand what ACLs are, why they're the **oldest and least flexible** of S3's access mechanisms (Note 09), why AWS now recommends disabling them entirely on almost every bucket, and the one setting — **Object Ownership** — that controls whether they're even active.

---

## 1. What an ACL actually grants

An **ACL** is a short, coarse-grained permission list attached to a **bucket or an individual object**, predating both IAM and bucket policies. It grants one of a small, fixed set of permissions (`READ`, `WRITE`, `READ_ACP`/`WRITE_ACP` — read/write the ACL itself, `FULL_CONTROL`) to one of a small set of grantee types:

| Grantee type | What it means |
|---|---|
| A **specific AWS account** (by canonical ID or email) | Grant access to one named account |
| **Authenticated Users** (a predefined group) | Any AWS account, signed in — not just yours |
| **All Users** (a predefined group) | Literally anyone, unauthenticated — a real, historical way buckets accidentally became public |
| **Log Delivery** (a predefined group) | Used specifically to let S3's own log delivery mechanism write server access logs (Note 32) into a bucket |

> ⚠️ **"All Users"** and **"Authenticated Users"** ACL grants are exactly the kind of legacy misconfiguration responsible for a long history of real-world "S3 bucket left public by accident" incidents — a major reason AWS has steadily pushed the ecosystem away from ACLs entirely in favor of bucket policies (Note 12), which are far more explicit and readable.

---

## 2. Why ACLs are considered legacy today

- **Far less expressive** than a bucket policy — no `Condition` blocks, no fine-grained action lists, just a handful of coarse permission levels.
- **Harder to audit** — a bucket can have object-level ACLs scattered across thousands of individual objects, each potentially different, with no single place to review them all (unlike one bucket policy document).
- **Redundant** with what bucket policies + IAM policies already cover, for every legitimate use case except a couple of narrow, specific ones (Section 4).

---

## 3. Object Ownership — the setting that can disable ACLs entirely

**Object Ownership** (a bucket-level setting) controls whether ACLs even matter for a given bucket:

| Object Ownership setting | ACL behavior |
|---|---|
| **Bucket owner enforced** (the modern default for new buckets) | **ACLs are disabled entirely** — every object is owned by the bucket owner, and only IAM/bucket policies govern access |
| **Bucket owner preferred** | ACLs remain active, but new objects uploaded by other accounts are automatically owned by the bucket owner |
| **Object writer** (the old default) | ACLs remain fully active; whoever uploads an object owns it and controls its ACL |

> 🎯 **Exam tip:** AWS's current guidance — and the modern console default for new buckets — is **"Bucket owner enforced,"** which disables ACLs entirely. Any exam scenario emphasizing simplified, centralized access control (rather than per-object ACL management) is pointing at this setting, in favor of bucket policies and IAM policies instead.

---

## 4. The few legitimate remaining ACL use cases

- **Cross-account uploads where the bucket owner must retain control** — before "Bucket owner enforced" existed, ACLs (or "Bucket owner preferred") were how a bucket owner ensured objects uploaded by a different account's IAM identity were still owned and controlled by the bucket owner, not the uploader.
- Legacy applications/tools that were built directly against the ACL API and haven't been updated to use bucket policies instead.

For any new bucket, in Bucket owner enforced mode (default), ACLs are simply irrelevant — access is entirely IAM policy + bucket policy (Notes 10-12), which is the simpler mental model to design around going forward.

---

## 5. Recap

- ACLs are S3's **oldest, coarsest-grained** access mechanism — a short list of predefined permissions and grantee types, attached per bucket or per object.
- **"All Users" / "Authenticated Users" ACL grants** are a historical cause of accidental public bucket exposure.
- **Object Ownership: Bucket owner enforced** (the modern default) **disables ACLs entirely**, consolidating access control into IAM + bucket policies — the recommended approach for new buckets.
- Next: Note 14 — AWS S3 Object Lock, a genuinely different kind of restriction — not about *who* can access an object, but whether it can be **modified or deleted at all**, even by an otherwise fully-permitted principal.

### Sources
- [Access control list (ACL) overview — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html)
- [Controlling ownership of objects and disabling ACLs — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/about-object-ownership.html)
- [Amazon S3 Object Ownership — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ensure-object-ownership.html)
