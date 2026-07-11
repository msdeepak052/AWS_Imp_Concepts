# 11 - AWS S3 — AWS IAM Policy For S3 Bucket (Hands-On)

> Goal: author a real, resource-scoped IAM policy restricting a user to one specific bucket (and a specific prefix within it) — applying `IAM/03`'s customer-managed-policy pattern specifically to S3, including the two-ARN-form detail that trips people up most often.

---

## 1. Recall: S3 actions need two ARN forms

As first flagged in `IAM/03`, S3 policies almost always need **two** resource ARNs to fully cover a bucket:

- The **bucket itself**: `arn:aws:s3:::demo-bucket` (no trailing slash) — needed for bucket-level actions like `s3:ListBucket`.
- The **objects inside it**: `arn:aws:s3:::demo-bucket/*` — needed for object-level actions like `s3:GetObject`, `s3:PutObject`, `s3:DeleteObject`.

Forgetting one of these two forms is the single most common S3 IAM policy authoring mistake — a policy with only the objects ARN will fail on `ListBucket` calls (e.g. the console's file browser, or `aws s3 ls`), even though `GetObject` works fine.

---

## 2. A read-only policy scoped to one bucket

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ListBucketItself",
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::demo-bucket"
    },
    {
      "Sid": "ReadObjectsInBucket",
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::demo-bucket/*"
    }
  ]
}
```

Create this as a customer managed policy (`IAM/03`'s pattern) named `DemoBucketReadOnly`, and attach it to a test user.

---

## 3. Scoping down further — restrict to one prefix ("folder")

Real-world policies often need to restrict a user to only **part** of a bucket — e.g. each team can only touch their own prefix:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ListOnlyOwnPrefix",
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::demo-bucket",
      "Condition": { "StringLike": { "s3:prefix": ["team-a/*"] } }
    },
    {
      "Sid": "ReadWriteOwnPrefixOnly",
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": "arn:aws:s3:::demo-bucket/team-a/*"
    }
  ]
}
```

> 🧠 Notice `ListBucket` needs a `Condition` on `s3:prefix` (because `ListBucket` is a *bucket-level* action — the prefix restriction has to be expressed as a condition on that one action), while the object-level actions (`GetObject`/`PutObject`) are scoped simply by putting the prefix directly into the **Resource** ARN itself (`demo-bucket/team-a/*`). Two different restriction mechanisms for the same underlying goal, because they're two different kinds of actions.

---

## 4. Test it

1. Attach `DemoBucketReadOnly` (or the prefix-scoped version) to a test IAM user.
2. As that user:
   ```bash
   aws s3 ls s3://demo-bucket/            # succeeds — ListBucket allowed
   aws s3 cp s3://demo-bucket/file.txt .  # succeeds — GetObject allowed
   aws s3 cp newfile.txt s3://demo-bucket/  # fails — no PutObject in the read-only version
   ```
3. With the prefix-scoped version attached instead, confirm reads/writes succeed under `team-a/` but are denied under any other prefix in the same bucket.

---

## 5. This is still just an IAM policy — same limits as Note 10 apply

Nothing here can reach into a **different AWS account's** bucket, and nothing here can grant **public** access — both of those require a bucket policy (Notes 10, 12) written by the bucket's owner, regardless of how permissive this IAM policy is made.

> 🎯 **Exam tip:** "restrict a user to only their own folder/prefix within a shared bucket" is a textbook IAM-policy-with-`s3:prefix`-condition scenario, commonly paired with **policy variables** like `${aws:username}` in the resource ARN (e.g. `arn:aws:s3:::demo-bucket/${aws:username}/*`) so **one single policy**, attached to a whole group, automatically scopes each user to their own prefix without writing a separate policy per person.

---

## 6. Recap

- S3 IAM policies almost always need **two ARN forms**: the bucket itself (for bucket-level actions) and `/*` (for object-level actions).
- Restricting to a specific prefix uses a **`Condition` on `s3:prefix`** for `ListBucket`, but is simply baked into the **Resource ARN** for object-level actions like `GetObject`/`PutObject`.
- Policy variables (e.g. `${aws:username}`) let one shared policy automatically scope many users to their own prefix.
- Next: Note 12 — AWS Bucket Policy For S3 (Hands-On), the resource-based counterpart, needed the moment cross-account or public access enters the picture.

### Sources
- [Amazon S3 actions, resources, and condition keys — AWS docs](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazons3.html)
- [Example: Allowing a user access to a portion of a bucket — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-policies-s3.html)
- [Policy variables — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_variables.html)
