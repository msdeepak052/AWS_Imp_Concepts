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

This is one of the most important AWS IAM patterns. It is used in almost every enterprise with multiple AWS accounts.

Let's build it exactly like a real company.

---

# Scenario

You have two AWS accounts:

```text
Account A (Development)
Account ID: 111111111111

Account B (Production)
Account ID: 222222222222
```

There is a Lambda running in the Development account.

It needs to read an S3 bucket in the Production account.

**We do NOT create IAM users in the Production account.**

Instead, the Lambda assumes a role in the Production account.

---

# Final Architecture

```text
                   Development Account
            (111111111111)

        +----------------------+
        | Lambda Function      |
        +----------------------+
                  |
                  | Automatically assumes
                  |
                  ▼
        +----------------------+
        | LambdaExecutionRole  |
        +----------------------+
                  |
                  | sts:AssumeRole
                  |
                  ▼

------------------------------------------------------------

                  Production Account
            (222222222222)

        +----------------------+
        | ProductionRole       |
        | (Trusts Account A)   |
        +----------------------+
                  |
                  |
                  ▼
            S3 Bucket
```

---

# Step 1 — Create the Lambda Execution Role (Account A)

IAM → Roles

Choose

```text
AWS Service
```

Service

```text
Lambda
```

AWS creates this trust policy:

```json
{
  "Statement": [{
      "Effect":"Allow",
      "Principal":{
          "Service":"lambda.amazonaws.com"
      },
      "Action":"sts:AssumeRole"
  }]
}
```

Attach:

* CloudWatch Logs
* Basic Lambda permissions

Do **not** attach S3 permissions from the production account.

---

# Step 2 — Allow the Lambda Role to Assume the Production Role

Attach this inline policy to `LambdaExecutionRole`:

```json
{
    "Version":"2012-10-17",
    "Statement":[
        {
            "Effect":"Allow",
            "Action":"sts:AssumeRole",
            "Resource":"arn:aws:iam::222222222222:role/ProductionRole"
        }
    ]
}
```

This policy simply says:

> "You are allowed to call STS and assume `ProductionRole`."

It **does not** grant S3 access directly.

---

# Step 3 — Go to the Production Account

Login to Account B.

IAM

Create Role

Choose

```text
AWS Account
```

Select

```text
Another AWS Account
```

Enter

```text
111111111111
```

This tells AWS:

> "I trust principals from Account A."

---

# Step 4 — Tighten the Trust Policy

By default, AWS trusts the **entire account**.

A better practice is to trust only the specific Lambda execution role.

Edit the trust policy to:

```json
{
    "Version":"2012-10-17",
    "Statement":[
        {
            "Effect":"Allow",
            "Principal":{
                "AWS":"arn:aws:iam::111111111111:role/LambdaExecutionRole"
            },
            "Action":"sts:AssumeRole"
        }
    ]
}
```

Now only that Lambda role can assume `ProductionRole`.

---

# Step 5 — Give Production Role Permissions

Attach:

```text
AmazonS3ReadOnlyAccess
```

or a custom policy:

```json
{
    "Version":"2012-10-17",
    "Statement":[
        {
            "Effect":"Allow",
            "Action":[
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource":[
                "arn:aws:s3:::production-bucket",
                "arn:aws:s3:::production-bucket/*"
            ]
        }
    ]
}
```

Notice:

The S3 permissions belong to **ProductionRole**, not to the Lambda execution role.

---

# Step 6 — Lambda Starts

AWS automatically does:

```text
Lambda Service

      │

Assume LambdaExecutionRole

      │

Temporary Credentials

      │

Lambda Code Starts
```

At this point the Lambda identity is:

```text
LambdaExecutionRole
```

---

# Step 7 — Lambda Calls STS

Inside your Lambda code:

```python
import boto3

sts = boto3.client("sts")

response = sts.assume_role(
    RoleArn="arn:aws:iam::222222222222:role/ProductionRole",
    RoleSessionName="LambdaSession"
)
```

AWS now checks two things.

---

## Check 1

Does LambdaExecutionRole have

```text
sts:AssumeRole
```

permission?

YES

↓

Continue

---

## Check 2

Does ProductionRole trust LambdaExecutionRole?

YES

↓

Continue

---

If either answer is **No**, AWS returns:

```text
AccessDenied
```

---

# Step 8 — STS Generates Temporary Credentials

AWS STS creates

```text
Access Key

Secret Key

Session Token

Expiration
```

Example:

```json
{
  "Credentials": {
      "AccessKeyId":"ASIA...",
      "SecretAccessKey":"...",
      "SessionToken":"...",
      "Expiration":"2026-07-27T11:00:00Z"
  }
}
```

---

# Step 9 — Lambda Uses Temporary Credentials

Create an S3 client with those credentials:

```python
import boto3

creds = response["Credentials"]

s3 = boto3.client(
    "s3",
    aws_access_key_id=creds["AccessKeyId"],
    aws_secret_access_key=creds["SecretAccessKey"],
    aws_session_token=creds["SessionToken"]
)
```

Now every S3 request is executed as:

```text
ProductionRole
```

not

```text
LambdaExecutionRole
```

---

# Step 10 — Access S3

Now the Lambda can:

```python
s3.list_objects_v2(Bucket="production-bucket")
```

because it is using the temporary credentials for `ProductionRole`.

---

# Step 11 — Credentials Expire

After (typically) 1 hour:

```text
Temporary Credentials

↓

Deleted

↓

Lambda must call AssumeRole again
```

No permanent keys are stored.

---

# End-to-End Authorization Flow

```text
                   ACCOUNT A (Development)
──────────────────────────────────────────────────────────────

      Lambda Service
             │
             │ 1. Automatically assumes
             ▼
+-----------------------------+
| LambdaExecutionRole         |
|-----------------------------|
| Trust: lambda.amazonaws.com |
| Policy:                     |
| sts:AssumeRole              |
+-------------+---------------+
              |
              | 2. sts:AssumeRole
              |
              ▼

                AWS STS
              (Global Service)

              │
              │ Checks
              │
              ├───────────────┐
              │               │
              ▼               ▼
 Has AssumeRole?      Is Trusted?
      YES                 YES

              │
              ▼

 Issues Temporary Credentials

              │
              ▼

──────────────────────────────────────────────────────────────
                   ACCOUNT B (Production)

+------------------------------+
| ProductionRole              |
|------------------------------|
| Trusts: LambdaExecutionRole |
| S3:GetObject                |
| S3:ListBucket               |
+--------------+--------------+
               |
               ▼
      Production S3 Bucket
```

## The Two-Sided Permission Model

A cross-account `AssumeRole` succeeds **only if both sides agree**:

| Side                        | Requirement                                                        |
| --------------------------- | ------------------------------------------------------------------ |
| **Caller (Account A)**      | IAM policy allowing `sts:AssumeRole` on the target role ARN        |
| **Target Role (Account B)** | Trust policy allowing the caller's IAM role ARN as the `Principal` |

Think of it like opening a secure door:

* The **caller** needs a **key** (permission to call `sts:AssumeRole`).
* The **door** must recognize that key holder as someone it trusts (trust policy).

If either the key is missing or the door doesn't trust the caller, the role assumption fails with `AccessDenied`. This "two-way handshake" is the core security model behind all cross-account role assumptions in AWS.


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
