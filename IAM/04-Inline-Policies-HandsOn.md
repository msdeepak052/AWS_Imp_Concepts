# 04 - IAM Policies: Inline Policies (Hands-On)

> Goal: create an **inline policy**, the third and last policy type, and understand the one specific situation it exists for — a strict, permanent 1:1 relationship between a policy and a single identity, with no reuse and no independent lifecycle.

---

## 1. What makes a policy "inline"

An **inline policy** is written **directly inside** a single user, group, or role — it has no independent existence, no standalone ARN, and cannot be attached to any other identity. If the identity is deleted, its inline policy is deleted with it automatically.

> 🧠 **Mental model:** a managed policy (AWS or customer) is like a separate document you can hand to multiple people — reusable, has its own filing reference (ARN), survives independently. An inline policy is like writing directly on the one person's badge in permanent marker — it *is* part of that badge, travels and dies with it, and can never be handed to anyone else.

---

## 2. Create an inline policy on the Note 02/03 user

1. **IAM console** → **Users** → `demo-readonly-user` → **Permissions** tab.
2. **Add permissions** → **Create inline policy**.
3. **JSON** tab:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": "sts:GetCallerIdentity",
         "Resource": "*"
       }
     ]
   }
   ```
4. **Next** → **Policy name**: `AllowGetCallerIdentityInline` → **Create policy**.
5. Back on the **Permissions** tab, notice this policy appears under its own **"Inline policies"** heading — visually distinct from the "Attached policies" listing that Notes 02-03's managed policies show up under.

---

## 3. Confirm it can't be reused

1. Try to attach `AllowGetCallerIdentityInline` to a *different* user. It won't appear in the managed-policy attach search at all — inline policies are never listed there, because they aren't a separate, attachable object; they only exist embedded inside the one identity you created them on.
2. If you genuinely need the same permission set on multiple identities, that's the signal to use a **customer managed policy** (Note 03) instead, not an inline one.

---

## 4. Confirm the delete-with-identity behavior

1. Delete `demo-readonly-user` entirely (**Users** → select → **Delete**).
2. The inline policy `AllowGetCallerIdentityInline` disappears with it — there is no orphaned policy object left behind to clean up, unlike a customer managed policy (which persists as a standalone object even after every identity it was attached to is gone, and must be deleted separately).

---

## 5. When inline policies are (rarely) the right choice

| Situation | Inline policy? |
|---|---|
| A permission genuinely belongs to exactly one identity, permanently, and should never accidentally be reused elsewhere | ✅ Yes — e.g. a tightly-scoped permission that's part of *this specific role's* one-off purpose |
| You want the permission to be automatically cleaned up if the identity is ever deleted, with zero separate cleanup step | ✅ Yes |
| You might want to reuse this exact permission set on another user/group/role later | ❌ No — use customer managed (Note 03) |
| You want version history / rollback on this specific policy | ❌ No — inline policies have no version history at all |

> 🎯 **Exam tip:** "this permission must never be attached to any other user, and must be deleted automatically if the user is deleted" is the textbook inline-policy scenario. If a question instead emphasizes reusability across many identities, that's pointing at managed (AWS or customer), not inline.

---

## 6. Recap

- Inline policies are embedded **directly inside** one user/group/role — no standalone ARN, no reuse, no version history, and automatically deleted along with their identity.
- This is the opposite design point from both AWS managed and customer managed policies (Notes 02-03), which are standalone, reusable, and persist independently.
- Use inline policies sparingly, only when a permission is genuinely meant to be permanently, exclusively tied to one specific identity.
- This closes out the three-policy-type series (managed / customer managed / inline). Next: Note 05 — IAM Entities: IAM Users (Hands-On), covering user creation and console/programmatic access in full.

### Sources
- [Managed policies and inline policies — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html)
- [Choosing between managed policies and inline policies — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html#choosing-managed-or-inline)
