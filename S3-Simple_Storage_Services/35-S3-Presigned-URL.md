# 35 - AWS S3 Presigned URL

> Goal: generate a **presigned URL** — a time-limited, signed link that grants temporary access to a private object without the recipient needing any AWS credentials of their own — and understand exactly whose permissions it actually uses.

---

## 1. The problem presigned URLs solve

Every bucket/object in this folder defaults to **private** (Note 02). But there are plenty of legitimate cases where you want to give **one specific person, temporarily**, access to **one specific private object** — without making the object public (Notes 23-25) and without creating an IAM user for them. A **presigned URL** is exactly this: a normal-looking HTTPS URL, with a cryptographic signature and expiration baked into its query string, that anyone holding the link can use directly in a browser or `curl` — no AWS credentials needed on the recipient's end at all.

> 🧠 **Mental model:** a presigned URL is like a hotel keycard programmed to unlock exactly one door, for exactly the next few hours, that anyone holding the physical card can use — the front desk (the identity that generated it) already proved who they were; the card itself carries all the temporary authority needed after that.

---

## 2. Whose permissions does the URL actually carry?

A presigned URL is generated **by** a specific IAM identity (a user or role), using **that identity's own credentials** to compute the signature — meaning **the URL's effective access is exactly whatever permissions the generating identity has**, no more and no less. If the generating identity's permissions are later revoked, or their credentials expire/rotate, **any presigned URL they already issued stops working too**, even before its own stated expiration time.

> ⚠️ This is a frequently tested subtlety: a presigned URL is **not** an independent grant of access — it's a **delegation of the issuer's own existing permissions**, wrapped in a signature and a time limit. If the issuing user never had `s3:GetObject` on that object in the first place, generating a presigned URL for it fails outright; you cannot presign your way past a permission you don't have.

---

## 3. Generate one

```bash
aws s3 presign s3://demo-bucket/private-report.pdf --expires-in 3600
```

Output: a full HTTPS URL with `X-Amz-Signature`, `X-Amz-Expires`, `X-Amz-Credential`, and related query parameters baked in. Anyone with this URL can `GET` the object directly — no `Authorization` header, no AWS CLI, no credentials needed — until the URL expires (here, in 3,600 seconds / 1 hour).

Via the SDKs (e.g. Python `boto3`):
```python
import boto3
s3 = boto3.client('s3')
url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': 'demo-bucket', 'Key': 'private-report.pdf'},
    ExpiresIn=3600
)
```

---

## 4. Presigned URLs for uploads, not just downloads

Presigned URLs aren't limited to `GetObject` — a presigned URL for `PutObject` lets an untrusted client (e.g. a browser, or a mobile app) **upload** a file directly to a specific bucket/key, without ever holding AWS credentials, and without the upload passing through your own application server as a relay:

```python
url = s3.generate_presigned_url(
    'put_object',
    Params={'Bucket': 'demo-bucket', 'Key': 'uploads/user123/photo.jpg'},
    ExpiresIn=900
)
```

This is a very common real-world pattern: a web/mobile app's backend generates a short-lived presigned upload URL and hands it to the client, which then uploads the large file **directly to S3**, bypassing the backend entirely for the actual data transfer — reducing load on the application server considerably.

---

## 5. Expiration limits

- For a presigned URL signed with **IAM user credentials**, the maximum expiration is up to **7 days**.
- For a presigned URL signed using **temporary credentials** (e.g. from an assumed role, `IAM/07-11`), the URL's expiration **cannot exceed** the remaining lifetime of those temporary credentials themselves — a presigned URL can never outlive the session that created it.

> 🎯 **Exam tip:** "grant temporary, time-limited access to a specific private object to someone without an AWS account, without making the object public" is the textbook **presigned URL** scenario. If instead the requirement is "many different external accounts each need ongoing, not time-limited, access," that points back toward a **bucket policy** (Note 12) instead — presigned URLs are inherently temporary and issued per-use, not a standing access grant.

---

## 6. Recap

- A **presigned URL** grants temporary, credential-free access to a specific object, but its effective permissions are always **exactly the issuing identity's own permissions** — it delegates, it doesn't independently grant.
- Works for both `GetObject` (downloads) and `PutObject` (direct client uploads, bypassing the application server).
- Expiration is capped at 7 days for IAM user-signed URLs, and cannot exceed the remaining life of the credentials used to sign it for role-based/temporary-credential cases.
- Next: Note 36 — AWS S3 Multi Factor Authentication (MFA) Delete, another access-control mechanism, this time protecting against permanent version deletion specifically.

### Sources
- [Sharing objects with presigned URLs — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html)
- [Generating a presigned URL to upload an object — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html)
