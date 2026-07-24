# 02 - IAM Policies: AWS Managed Policies (Hands-On)

> Goal: attach a real **AWS managed policy** to a user, understand exactly what "managed by AWS" means in practice (you can attach/detach it, but never edit its contents), and see how AWS keeps it updated over time without any action on your part.

---

## 1. What makes a policy "AWS managed"

An **AWS managed policy** is a standalone policy **created and maintained by AWS itself** — visible to every AWS account, reusable across any number of users/groups/roles in your account, but **not editable** by you. AWS updates the policy's contents over time (e.g. adding permissions for new API actions in a service) — every identity the policy is attached to automatically gets the update, with zero action needed on your part.

- Recognizable in the console/CLI by their ARN prefix: `arn:aws:iam::aws:policy/...` (note: **no account ID** in the ARN — that's the tell that it's AWS-owned, not yours).
- Common examples: `AdministratorAccess`, `AmazonS3ReadOnlyAccess`, `AmazonEC2FullAccess`, `ReadOnlyAccess`.
- **Job function policies** are a curated subset of AWS managed policies aligned to common roles (e.g. `DataScientist`, `NetworkAdministrator`) — still AWS managed, just grouped by persona rather than by service.

> 🧠 **Mental model:** an AWS managed policy is like a pre-built recipe from a cookbook publisher — you can use it exactly as printed, or swap it out for a different recipe, but you can't scribble in the publisher's own cookbook. If you need a *modified* version, you copy it into your own (Note 03, customer managed policies) and edit that copy instead.

---

## 2. Create a user and attach an AWS managed policy

1. **IAM console** → **Users** → **Create user**.
2. **User name**: `demo-readonly-user`. Leave **Provide user access to the AWS Management Console** unchecked for now (programmatic-only, keeps this exercise simple).
3. **Set permissions** → **Attach policies directly**.
4. Search for `AmazonEC2ReadOnlyAccess` → check it → **Next** → **Create user**.
5. Open the new user → **Permissions** tab — confirm `AmazonEC2ReadOnlyAccess` is listed with **Type: AWS managed**.

---

## 3. Inspect the policy itself

1. **IAM console** → **Policies** → search `AmazonEC2ReadOnlyAccess` → open it.
2. **Policy usage** tab shows every identity in your account this policy is currently attached to — useful for impact analysis before ever detaching a shared managed policy.
3. **Permissions** tab (JSON view) shows the actual `Allow` statements — read-only EC2 actions (`ec2:Describe*`, etc.) plus a few related read-only permissions from adjacent services (e.g. ELB, Auto Scaling) that a full EC2 read-only view typically needs.
4. Notice there is **no Edit button that lets you change the JSON** — AWS managed policies are permanently read-only to every account.

---

## 4. Detach and swap for a different managed policy

1. Back on `demo-readonly-user`'s **Permissions** tab → check `AmazonEC2ReadOnlyAccess` → **Remove**.
2. **Add permissions** → **Attach policies directly** → search and attach `AmazonS3ReadOnlyAccess` instead.
3. This swap took seconds and required no policy authoring at all — the appeal of managed policies for common, well-understood access patterns.

---

## 5. When AWS managed policies are (and aren't) the right choice

| Situation | AWS managed policy? |
|---|---|
| Standard, well-known access pattern (e.g. "full EC2 access", "read-only S3") | ✅ Yes — fastest, AWS keeps it current |
| Need to restrict access to **specific resources** (e.g. only one S3 bucket, not all of S3) | ❌ No — managed policies are broad by design; you need a customer managed policy (Note 03) |
| Want a policy attached to exactly one identity, never reused | ❌ No — consider an inline policy instead (Note 04) |
| Want AWS's official recommendation for a job function (e.g. "database administrator") | ✅ Yes — the job-function managed policies exist exactly for this |

> 🎯 **Exam tip:** "the policy's permissions changed without anyone in my account editing anything" is a classic signature of an **AWS managed policy** being updated by AWS — customer managed and inline policies never change unless someone in your account explicitly edits them.

---

## 6. Recap

- AWS managed policies are maintained by AWS, reusable across your whole account, and automatically kept current — but you can never edit their JSON directly.
- ARN pattern `arn:aws:iam::aws:policy/...` (no account ID) is the tell for "AWS managed."
- Best for common, broad, well-understood access patterns; not for fine-grained, resource-specific restrictions.
- Next: Note 03 — IAM Policies: Customer Managed Policies (Hands-On), for exactly that fine-grained, resource-specific case.

### Sources
- [AWS managed policies — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html)
- [AWS managed policies for job functions — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_job-functions.html)
- [Adding and removing IAM identity permissions — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html)
