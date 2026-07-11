# 03 - IAM Policies: Customer Managed Policies (Hands-On)

> Goal: author a custom, standalone policy from scratch, restricting access to one specific resource — the fine-grained, resource-specific case AWS managed policies (Note 02) are deliberately too broad for — then see how policy **versions** work when you edit it later.

---

## 1. What makes a policy "customer managed"

A **customer managed policy** is a standalone policy that lives in **your own account**, which **you** author, own, and can edit at any time. Just like an AWS managed policy, it's reusable — attach the same one to any number of users, groups, or roles — but unlike an AWS managed policy, its contents only ever change when someone in your account changes them.

- ARN pattern: `arn:aws:iam::<your-account-id>:policy/<policy-name>` — the account ID in the ARN is the tell that it's yours, not AWS's.
- Authored either via the **visual editor** (point-and-click service/action/resource pickers) or by writing the **JSON** directly — both produce the same policy document.

---

## 2. Author a policy scoped to one specific S3 bucket

1. **IAM console** → **Policies** → **Create policy**.
2. Switch to the **JSON** tab and paste:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": ["s3:GetObject", "s3:ListBucket"],
         "Resource": [
           "arn:aws:s3:::demo-reports-bucket",
           "arn:aws:s3:::demo-reports-bucket/*"
         ]
       }
     ]
   }
   ```
3. **Next** → **Policy name**: `DemoReportsBucketReadOnly` → **Create policy**.

> 🧠 Note the two ARNs: the bucket itself (`arn:...:::demo-reports-bucket`, no trailing slash — needed for `s3:ListBucket`, which acts on the bucket) and the objects inside it (`.../*`, needed for `s3:GetObject`, which acts on individual objects). Forgetting one of these two ARN forms for S3 policies is one of the most common real-world IAM authoring mistakes.

---

## 3. Attach the new policy to the user from Note 02

1. **Users** → `demo-readonly-user` → **Permissions** tab → **Add permissions** → **Attach policies directly**.
2. Search `DemoReportsBucketReadOnly` → attach it.
3. This user can now read only from `demo-reports-bucket` specifically — not all of S3, which is exactly the restriction an AWS managed policy like `AmazonS3ReadOnlyAccess` couldn't give you.

---

## 4. Edit the policy and understand versioning

1. **Policies** → `DemoReportsBucketReadOnly` → **Permissions** tab → **Edit**.
2. Add `s3:PutObject` to the `Action` list → **Next** → **Save changes**.
3. Open the **Policy versions** tab: you now have **two versions** (`v1`, the original; `v2`, with the new action), with `v2` marked **Default** (the version actually in effect).
4. A customer managed policy can hold **up to 5 versions** at once. Once you'd try to create a 6th, you must delete an old **non-default** version first.
5. You can roll back instantly by selecting an older version → **Set as default** — no re-authoring needed, since AWS already kept the old JSON.

> ⚠️ **You cannot delete the version currently marked as default.** Switch the default to a different version first if you need to remove the one currently active.

---

## 5. Customer managed vs. AWS managed vs. inline (preview)

| | AWS managed | Customer managed | Inline (Note 04) |
|---|---|---|---|
| Who authors it | AWS | You | You |
| Reusable across identities | Yes | Yes | No — 1:1 with a single identity |
| Editable | No | Yes | Yes |
| Has version history | N/A (AWS updates it) | Yes, up to 5 versions | No |
| ARN gives away ownership | `...::aws:policy/...` | `...::<account-id>:policy/...` | No standalone ARN — it isn't a separate object |

---

## 6. Recap

- A customer managed policy is a standalone, reusable, **you-authored** policy — the right tool whenever you need resource-specific restrictions an AWS managed policy is too broad to express.
- Every edit creates a **new version** (up to 5 kept at once), and you can instantly roll back by changing which version is marked default — a real safety net AWS managed policies don't need (since AWS manages their history) and inline policies don't have at all.
- The S3-bucket example here needs **two** ARN forms — the bucket itself and its objects (`/*`) — to cover both bucket-level and object-level actions.
- Next: Note 04 — IAM Policies: Inline Policies (Hands-On), for the one-off, non-reusable case.

### Sources
- [Managed policies and inline policies — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html)
- [Versioning IAM policies — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-versioning.html)
- [Policies and permissions in IAM — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html)
- [Amazon S3 actions, resources, and condition keys — AWS docs](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazons3.html)
