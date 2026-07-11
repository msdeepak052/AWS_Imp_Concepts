# 07 - IAM Entities: IAM Roles Practical With AWS Best Practices (Hands-On)

> Goal: create and attach an IAM role to an EC2 instance — the canonical "AWS service needs permissions" pattern — and understand exactly why this is always preferred over putting access keys on the instance itself.

---

## 1. What a role is, precisely

A **role** is an identity with **no long-term credentials of its own** — instead, whoever/whatever is allowed to assume it (defined by its **trust policy**) receives **temporary security credentials** from **AWS STS** (Security Token Service) for a limited session (by default up to 1 hour, configurable up to 12 hours for most role types).

A role has exactly **two** policy attachments, serving different purposes:

| Policy | Answers |
|---|---|
| **Trust policy** (a.k.a. assume-role policy) | *"Who is allowed to assume this role?"* |
| **Permissions policy** (one or more, same as a user's) | *"What can this role do, once assumed?"* |

> 🧠 **Mental model:** the trust policy is the guest list for who's allowed to pick up the visitor badge; the permissions policy is what the badge actually unlocks once someone's wearing it. Notes 02-04's policy types (managed/customer managed/inline) all describe the *permissions* side — every role also needs a trust policy on top of that, which users and groups simply don't have.

---

## 2. Why roles beat hardcoded access keys, for a service like EC2

If you instead put an IAM user's access keys directly onto an EC2 instance (in a config file, environment variable, or baked into an AMI):

- The credentials are **long-term** — they don't expire on their own, so a leak (e.g. an accidentally-public GitHub repo, a compromised instance) stays exploitable indefinitely until someone notices and manually revokes them.
- They must be **manually rotated**, and every instance using them needs to be updated in sync — operationally painful at any real fleet size.
- They have to be **distributed** to every instance somehow — itself a secret-management problem.

A role attached to the instance (as an **instance profile**) solves all three at once: EC2 automatically fetches and rotates short-lived credentials behind the scenes via the instance metadata service, no secret ever needs to be distributed or embedded, and a leaked credential expires on its own within the hour.

> ⚠️ **This is the single most consistently tested IAM best practice on SAA-C03**: whenever a scenario describes an AWS service (EC2, Lambda, ECS task, etc.) needing to call another AWS service, the correct answer is almost always "attach an IAM role" — never "create an IAM user and give it access keys."

---

## 3. Create a role and attach it to an EC2 instance

1. **IAM console** → **Roles** → **Create role**.
2. **Trusted entity type**: **AWS service** → **Use case**: **EC2** (this auto-generates the correct trust policy allowing the EC2 service to assume this role).
3. **Add permissions**: attach `AmazonS3ReadOnlyAccess` (an AWS managed policy, Note 02).
4. **Role name**: `EC2-S3ReadOnly-Role` → **Create role**.
5. **EC2 console** → select a running (or new) instance → **Actions** → **Security** → **Modify IAM role** → choose `EC2-S3ReadOnly-Role` → **Update IAM role**.
6. Connect to the instance (Session Manager, matching this repo's no-SSH convention) and confirm the role is active:
   ```bash
   aws sts get-caller-identity
   aws s3 ls
   ```
   The output identity shows the **assumed role**, not a user — and S3 listing succeeds without a single access key ever having been configured on the instance.

---

## 4. Inspect the trust policy AWS generated

**Roles** → `EC2-S3ReadOnly-Role` → **Trust relationships** tab:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "ec2.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

The `Principal` here is the **EC2 service itself**, not a person or account — this is what makes the role "an EC2 role" rather than a role for a human or another account (those patterns come in Notes 08-11).

---

## 5. Least privilege still applies to roles

Attaching a role doesn't excuse skipping least privilege — `AmazonS3ReadOnlyAccess` here was a deliberate choice for a read-only workload; a real production role should scope permissions down further with a customer managed policy (Note 03) restricting to specific buckets, exactly as Note 03 demonstrated for a user.

---

## 6. Recap

- A role has **no long-term credentials** — only a **trust policy** (who can assume it) and **permissions policies** (what it can do once assumed), with temporary STS credentials issued on assumption.
- Attaching a role to EC2 (an **instance profile**) is the standard, best-practice way to give an instance AWS API access — no access keys to leak, distribute, or rotate manually.
- This "use a role, not hardcoded keys" principle is the most heavily tested IAM best practice on the exam.
- Next: Note 08 — IAM Roles: AWS Account Assume Role (Hands-On), where a *human user* (not a service) assumes a role within the same account.

### Sources
- [IAM roles — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)
- [IAM roles for Amazon EC2 — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html)
- [Temporary security credentials — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html)
