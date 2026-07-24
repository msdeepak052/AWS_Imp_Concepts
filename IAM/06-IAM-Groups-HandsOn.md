# 06 - IAM Entities: IAM Groups (Hands-On)

> Goal: create a group, attach policies to it once, and add multiple users to it — the standard way to manage permissions for many users at scale instead of repeating the same policy attachment on every individual user.

---

## 1. What a group actually is

An IAM **group** is a named collection of users that exists purely so you can attach policies **once, to the group**, and have every current and future member automatically get those permissions. Covered already in Note 01, but worth restating here since it's the crux of this note: **a group is not an identity** — it has no credentials, cannot sign in, cannot be a principal in a resource-based policy, and cannot be assumed the way a role can.

> 🧠 **Mental model:** a group is a mailing list, not a person — you send the same message (policy) to the whole list at once, and everyone on it receives it, but the list itself never "does" anything on its own.

---

## 2. Create a group and attach a policy

1. **IAM console** → **User groups** → **Create group**.
2. **Group name**: `DevOps-ReadOnly`.
3. **Attach permissions policies**: search and check `AmazonEC2ReadOnlyAccess` and `AmazonS3ReadOnlyAccess`.
4. **Create user group**.

---

## 3. Add existing users to the group

1. Open `DevOps-ReadOnly` → **Users** tab → **Add users**.
2. Select `demo-console-user` (from Note 05) and any others → **Add users**.
3. Confirm on `demo-console-user`'s own **Permissions** tab: the group's two policies now show up under a **"Attached via group"** style listing, distinct from anything attached directly to the user — this distinction matters when troubleshooting *why* a user can do something they weren't individually granted.

---

## 4. A user can belong to multiple groups

1. Create a second group, `Billing-ReadOnly`, with `AWS Billing ReadOnly Access` (or an equivalent billing-scoped managed policy) attached.
2. Add `demo-console-user` to this group as well.
3. The user's **effective permissions** are now the **union** of everything from both groups plus anything attached directly — permissions across multiple sources are always additive (subject to the same explicit-deny-always-wins rule from Note 01).

> ⚠️ A user can belong to **up to 10 groups** by default (a soft limit, raisable via a support request), and an account can have **up to 300 groups** by default (also soft). These limits rarely bite in practice, but "too many groups" is a real, documented quota worth knowing exists.

---

## 5. Nested groups are not supported

Unlike some traditional directory services (e.g. Active Directory), **IAM groups cannot contain other groups** — only users. If you need a hierarchical structure, you either flatten it into separate groups with the right policies each, or move to a purpose-built hierarchy tool (AWS Organizations' OUs for account-level hierarchy, Note 18; or an external identity provider's own group nesting, federated in via Note 10/22).

---

## 6. Groups vs. roles — don't confuse the two

| | Group | Role |
|---|---|---|
| Is it an identity? | No — a policy-attachment container only | Yes — a full identity with its own credentials |
| Has credentials? | No | Yes — temporary, via STS, once assumed |
| Can be "signed into" or assumed? | No | Yes |
| Purpose | Attach policies to many users at once | Grant temporary access to a service, another account, or a federated identity |

> 🎯 **Exam tip:** a scenario that says "an EC2 instance needs permission to read from S3" is never solved with a group — instances assume **roles**, not groups. Groups exist strictly to organize permanent human/application **users**.

---

## 7. Recap

- A **group** is a policy-attachment container for users — not an identity itself, with no credentials and no ability to be assumed.
- Attaching policies to a group lets every member (current and future) inherit them automatically; a user's effective permissions are the union of everything from their direct attachments and every group they belong to.
- Groups cannot be nested inside other groups, and a user can belong to up to 10 groups by default.
- Groups are strictly for organizing users — an EC2 instance or any other AWS service needs a **role** instead (Note 07 onward).
- Next: Note 07 — IAM Entities: IAM Roles Practical With AWS Best Practices (Hands-On).

### Sources
- [IAM user groups — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_groups.html)
- [IAM object quotas — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html)
