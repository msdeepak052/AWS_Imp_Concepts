# 35 - AWS S3 Presigned URL

An **S3 presigned URL** lets you give someone **temporary access to a private S3 object** without giving them AWS credentials.

The most important idea is:

> **The URL carries temporary, signed authorization for a specific S3 operation.**

---

## 1. The problem Presigned URLs solve

Suppose you have:

```text
S3 Bucket: private-files

private-files/
├── report.pdf
├── invoice.pdf
└── photo.jpg
```

Your bucket is private:

```text
Internet
    │
    └── ❌ Direct access
             │
             ▼
        Private S3
```

Now your application wants to allow a customer to download:

```text
invoice.pdf
```

You **don't** want to make the bucket public.

You also don't want to give the customer:

```text
AWS Access Key
AWS Secret Key
IAM credentials
```

Instead:

```text
Customer
    │
    │ "I need invoice.pdf"
    ▼
Your Application
    │
    │ Generate presigned URL
    ▼
S3
    │
    └── Temporary URL
             │
             ▼
          Customer
             │
             │ HTTPS GET
             ▼
        Private S3 Object
```

---

# 2. What does a presigned URL look like?

It looks roughly like:

```text
https://private-files.s3.ap-south-1.amazonaws.com/invoice.pdf
?X-Amz-Algorithm=AWS4-HMAC-SHA256
&X-Amz-Credential=...
&X-Amz-Date=...
&X-Amz-Expires=900
&X-Amz-SignedHeaders=host
&X-Amz-Signature=...
```

The important part is:

```text
X-Amz-Expires=900
```

which means the URL is valid for the specified expiry period, subject to the credentials and signing conditions.

The URL itself contains the authorization information.

---

# 3. Does the user need AWS credentials?

**No.**

That's the whole point.

Normally:

```text
User
  │
  │ AWS credentials
  ▼
S3
```

With a presigned URL:

```text
User
  │
  │ HTTPS URL
  ▼
S3
```

The user doesn't need an IAM user, IAM role, access key, etc.

---

# 4. Who creates the presigned URL?

Usually your backend/application.

For example:

```text
                 AWS Account
                     │
              ┌──────┴──────┐
              │             │
          Application       S3
              │             │
          IAM Role          │
              │             │
              └──────┬──────┘
                     │
              Generate URL
                     │
                     ▼
                Customer
```

The application needs permission to access the object.

For example:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::private-files/*"
    }
  ]
}
```

The application uses its AWS credentials/role to create the presigned URL.

---

# 5. Very important mental model

The user receiving the URL **doesn't get the application's IAM permissions**.

Suppose your backend role has:

```text
s3:GetObject
s3:PutObject
s3:DeleteObject
```

and generates a presigned URL for:

```text
invoice.pdf
```

The customer doesn't suddenly get:

```text
DeleteObject
ListBucket
PutObject
```

The URL is created for a **specific operation**.

For example:

```text
Presigned GET
     ↓
GET
     ↓
invoice.pdf
```

or:

```text
Presigned PUT
     ↓
PUT
     ↓
customer-upload.jpg
```

---

# 6. Presigned GET URL — Download

This is the most common example.

Suppose:

```text
S3
└── private-files
      └── invoice.pdf
```

Your backend generates:

```text
Presigned GET URL
```

The customer gets:

```text
https://private-files.s3.../invoice.pdf?...signature...
```

Customer's browser:

```http
GET /invoice.pdf
```

S3 validates the signature.

If valid:

```text
200 OK
```

and returns:

```text
invoice.pdf
```

---

# 7. Demo — AWS CLI

You can generate a presigned URL using the AWS CLI:

```bash
aws s3 presign \
  s3://private-files/invoice.pdf \
  --expires-in 600
```

This generates a URL valid for:

```text
600 seconds
```

which is:

```text
10 minutes
```

You can then open that URL in a browser.

No AWS credentials are required in the browser.

---

# 8. Demo — Python / boto3

Install boto3:

```bash
pip install boto3
```

Example:

```python
import boto3

s3 = boto3.client("s3")

url = s3.generate_presigned_url(
    ClientMethod="get_object",
    Params={
        "Bucket": "private-files",
        "Key": "invoice.pdf"
    },
    ExpiresIn=600
)

print(url)
```

Output:

```text
https://private-files.s3.ap-south-1.amazonaws.com/invoice.pdf?X-Amz-Algorithm=...
```

Now give this URL to the user.

They can download the private object for the allowed period.

---

# 9. Complete application example

Imagine an online banking application.

Customer logs in:

```text
https://bank.example.com/statements
```

They click:

```text
Download Statement
```

Your backend receives:

```text
GET /api/statements/2026-july
```

Backend:

```text
1. Authenticate customer
2. Check customer owns statement
3. Generate S3 presigned URL
4. Return URL
```

Architecture:

```text
Customer
   │
   │ GET /statement
   ▼
Application
   │
   ├── Authenticate
   ├── Authorize
   │
   ▼
IAM Role
   │
   │ GetObject
   ▼
S3
   │
   └── Generate presigned URL
            │
            ▼
         Customer
            │
            │ HTTPS GET
            ▼
       private S3 object
```

The bucket can remain completely private.

---

# 10. Presigned PUT URL — Upload

Presigned URLs aren't only for downloads.

You can use them to allow users to **upload directly to S3**.

Suppose your application allows users to upload profile pictures.

Instead of:

```text
User
  │
  │ 10 MB image
  ▼
Application Server
  │
  │ 10 MB
  ▼
S3
```

you can do:

```text
User
  │
  │ Ask for upload URL
  ▼
Application
  │
  │ Generate presigned PUT URL
  ▼
User
  │
  │ Direct upload
  ▼
S3
```

This is much better for large files because your application server doesn't have to proxy the file.

---

# 11. Python — Presigned PUT URL

```python
import boto3

s3 = boto3.client("s3")

url = s3.generate_presigned_url(
    ClientMethod="put_object",
    Params={
        "Bucket": "private-files",
        "Key": "uploads/profile.jpg",
        "ContentType": "image/jpeg"
    },
    ExpiresIn=600
)

print(url)
```

The frontend can then upload directly:

```javascript
await fetch(presignedUrl, {
    method: "PUT",
    headers: {
        "Content-Type": "image/jpeg"
    },
    body: file
});
```

Architecture:

```text
Browser
   │
   │ PUT image.jpg
   │
   ▼
S3
```

The application server isn't handling the file contents.

---

# 12. GET vs PUT

Remember:

| Presigned URL | Purpose         |
| ------------- | --------------- |
| `GET`         | Download object |
| `PUT`         | Upload object   |

For example:

```text
Download
GET
 ↓
S3
```

```text
Upload
PUT
 ↓
S3
```

---

# 13. Presigned POST

There's another mechanism:

> **Presigned POST**

This is particularly useful for browser-based uploads because you can specify conditions such as:

```text
Maximum file size
Content type
Object key/prefix
Expiration
```

Architecture:

```text
Browser
   │
   │ Request upload information
   ▼
Backend
   │
   │ Generate presigned POST
   ▼
Browser
   │
   │ multipart/form-data
   ▼
S3
```

Example conceptually:

```python
response = s3.generate_presigned_post(
    Bucket="private-files",
    Key="uploads/${filename}",
    Fields={
        "Content-Type": "image/jpeg"
    },
    Conditions=[
        ["content-length-range", 1, 10485760],
        {"Content-Type": "image/jpeg"}
    ],
    ExpiresIn=600
)
```

Now you can enforce:

```text
Maximum:
10 MB

Content-Type:
image/jpeg
```

---

# 14. Presigned URL security

This is very important.

A presigned URL is effectively a **temporary bearer credential**.

If I give you:

```text
https://s3....?X-Amz-Signature=...
```

whoever possesses that URL may be able to use it until it expires.

Therefore:

### Don't put long expiry times unnecessarily

Instead of:

```text
7 days
```

consider:

```text
5 minutes
10 minutes
1 hour
```

depending on the use case.

---

# 15. Does deleting the IAM user/role invalidate the URL?

Potentially, yes, depending on what credentials were used to sign it.

A presigned URL is constrained by the lifetime of the credentials used to create it.

For example:

```text
Temporary STS credentials
        │
        ▼
Presigned URL
        │
        ▼
URL cannot outlive the credentials' validity
```

So `ExpiresIn` is **not necessarily the only factor determining how long a presigned URL can actually work**.

---

# 16. Presigned URL vs Public S3

This distinction is extremely important.

### Public bucket

```text
Internet
   │
   │ Anyone
   ▼
S3
```

Anyone can access the object according to the public policy.

---

### Presigned URL

```text
Internet
   │
   │ Temporary signed URL
   ▼
Private S3
```

The bucket stays private.

Only someone possessing the valid URL can use that specific temporary authorization.

---

# 17. Presigned URL vs CloudFront Signed URL

These are often confused.

### S3 Presigned URL

```text
Client
   │
   ▼
S3
```

Used to give temporary access directly to S3.

---

### CloudFront Signed URL

```text
Client
   │
   ▼
CloudFront
   │
   ▼
S3
```

Useful when you want:

* CDN caching
* Global distribution
* Edge locations
* Custom domain
* CloudFront security controls

For a large media platform:

```text
User
  │
  ▼
CloudFront
  │
  │ Signed URL
  ▼
S3
```

is often more appropriate than sending users directly to S3.

---

# 18. A very realistic architecture

Suppose you build a photo-sharing application.

### Upload

```text
                    ┌──────────────┐
                    │   Backend    │
                    └──────┬───────┘
                           │
                   Generate PUT URL
                           │
                           ▼
User ───────────────────► S3
         Direct upload
```

### Download

```text
User
 │
 │ Request photo
 ▼
Backend
 │
 │ Generate GET URL
 ▼
User
 │
 │ GET
 ▼
S3
```

Your application never needs to handle the actual 500-MB file.

---

# 19. One complete demo

Let's say:

```text
Bucket:
demo-presigned-bucket

Object:
private/report.pdf
```

### Step 1 — Create private bucket

```text
S3
└── demo-presigned-bucket
      └── private/
            └── report.pdf
```

Keep:

```text
Block Public Access
☑ ON
```

---

### Step 2 — IAM role

Your application role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::demo-presigned-bucket/private/*"
    }
  ]
}
```

---

### Step 3 — Backend generates URL

```python
import boto3

s3 = boto3.client("s3")

url = s3.generate_presigned_url(
    "get_object",
    Params={
        "Bucket": "demo-presigned-bucket",
        "Key": "private/report.pdf"
    },
    ExpiresIn=300
)

print(url)
```

5 minutes:

```text
300 seconds
```

---

### Step 4 — Give URL to user

```text
Backend
   │
   │
   └── https://demo-presigned-bucket.s3...?...signature...
                         │
                         ▼
                       User
```

User opens it.

S3 checks:

```text
Signature ✓
Expiration ✓
HTTP method ✓
Bucket/key ✓
Request conditions ✓
```

Then:

```text
200 OK
```

---

# 20. The most important mental model

Don't think:

> "The presigned URL makes the S3 object public."

It **doesn't**.

Think:

```text
                PRIVATE S3
                    │
                    │
             IAM Principal
                    │
                    ▼
           Generate signature
                    │
                    ▼
           Temporary URL
                    │
                    ▼
                 User
                    │
                    │ HTTPS
                    ▼
                  S3
                    │
            Validate signature
                    │
             ┌──────┴──────┐
             │             │
           Valid         Invalid
             │             │
             ▼             ▼
          ALLOW          DENY
```

### In one sentence:

> **A presigned URL is a temporary, signed URL generated by an authorized AWS principal that lets an otherwise unauthenticated client perform a specific S3 operation on a specific resource without receiving AWS credentials.**

And for your AWS SAA preparation, remember the three major patterns:

```text
Public S3
    → Anyone can access according to policy

Presigned URL
    → Temporary direct S3 access

CloudFront Signed URL
    → Temporary access through CloudFront
```

That's the core distinction.

### Sources
- [Sharing objects with presigned URLs — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html)
- [Generating a presigned URL to upload an object — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html)
