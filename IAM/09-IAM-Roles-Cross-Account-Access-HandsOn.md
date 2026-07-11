# 09 - IAM Entities: IAM Roles — Assume Role Cross Account Access (Hands-On)

> Goal: extend Note 08's assume-role pattern **across two separate AWS accounts**, and cover the **confused deputy problem** and its fix (the External ID condition) — a scenario that shows up constantly in real multi-account setups and on the exam.

---

## 1. Why cross-account roles, instead of separate users per account

A common real setup: **Account A** (e.g. a central security/ops team) needs to manage resources in **Account B** (e.g. a workload account) — or a third-party SaaS vendor needs limited access into your account to do its job. Creating a duplicate IAM user in every account it needs access to doesn't scale and multiplies long-term credentials across account boundaries. Instead, **Account B** creates a role that explicitly trusts **Account A**, and users/roles in Account A assume it.

> 🧠 **Mental model:** this is Note 08's same-account pattern, just with the "who's on the guest list" now naming an entirely different account instead of `:root` of your own account.

---

## 2. Create the role in the trusting account (Account B — the resource owner)

1. In **Account B**'s IAM console → **Roles** → **Create role**.
2. **Trusted entity type**: **AWS account** → **Another AWS account** → enter **Account A's** account ID.
3. **Add permissions**: attach `AmazonS3ReadOnlyAccess`.
4. **Role name**: `CrossAccount-S3ReadOnly-Role` → **Create role**.

Generated trust policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::222233334444:root" },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

(`222233334444` = Account A's ID.)

---

## 3. Grant a user in Account A permission to assume it

In **Account A**, attach a policy to the relevant user/role allowing:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sts:AssumeRole",
      "Resource": "arn:aws:iam::111122223333:role/CrossAccount-S3ReadOnly-Role"
    }
  ]
}
```

(`111122223333` = Account B's ID, the account that owns the role.)

Exactly the same "both sides must agree" requirement as Note 08 — Account B's trust policy names Account A, **and** the specific principal in Account A must separately be allowed to call `sts:AssumeRole` on that exact role ARN.

---

## 4. Assume the role from Account A

Same mechanics as Note 08's **Switch Role**, just entering **Account B's** account ID and the role name — or via CLI:
```bash
aws sts assume-role \
  --role-arn arn:aws:iam::111122223333:role/CrossAccount-S3ReadOnly-Role \
  --role-session-name demo-cross-account-session
```
The returned temporary credentials act with `AmazonS3ReadOnlyAccess` inside **Account B**, even though the caller's own identity lives entirely in Account A.

---

## 5. The confused deputy problem, and the External ID fix

When a **third party** (e.g. a SaaS monitoring vendor) is the one assuming a role into your account on behalf of many different customers, a subtle risk appears: the vendor's own systems might be tricked (by another one of the vendor's customers) into assuming **your** role instead of the intended one — the vendor becomes an unwitting "confused deputy" acting across the wrong customer's boundary.

The fix: add a **Condition** requiring a shared secret **External ID** in the trust policy, which only the legitimate customer relationship actually knows:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::999988887777:root" },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": { "sts:ExternalId": "unique-value-vendor-gave-you" }
      }
    }
  ]
}
```

Now, even if the vendor's account ID (`999988887777`) is correct, the `AssumeRole` call **also** must include the matching External ID — the vendor's system only sends the right one when it's genuinely acting on your specific behalf.

> 🎯 **Exam tip:** "third-party SaaS vendor needs cross-account access to my account, and I'm worried about the vendor being tricked into acting on the wrong customer's resources" is the exact textbook description of the confused deputy problem — the answer is always **add an External ID condition to the trust policy**, not a stronger IAM policy on the permissions side (the permissions side isn't where this problem lives).

---

## 6. Recap

- Cross-account role assumption follows the same two-sided trust model as Note 08, just naming a **different account's ID** as the trusted principal instead of your own account's root.
- The **confused deputy problem** arises specifically with third-party cross-account access serving multiple customers — fixed by requiring a unique, shared **External ID** as a trust-policy condition.
- Both sides of the trust (the target account's trust policy, and the calling identity's own `sts:AssumeRole` permission) must independently allow the assumption — missing either one blocks it.
- Next: Note 10 — IAM Roles: Web Identity/SAML 2.0 Federation (Hands-On), extending role assumption to identities that don't have an IAM user at all.

### Sources
- [Providing access to AWS accounts owned by third parties — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_third-party.html)
- [How to use an external ID when granting access to your AWS resources to a third party — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html)
- [Tutorial: Delegate access across AWS accounts using IAM roles — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_cross-account-with-roles.html)
