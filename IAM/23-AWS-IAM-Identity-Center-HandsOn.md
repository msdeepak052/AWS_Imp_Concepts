# 23 - AWS IAM Identity Center Practical (Hands-On)

> Goal: enable Identity Center, create a permission set, assign a user to an account with it, and sign in through the AWS access portal — turning Note 22's concepts into a real, working single-sign-on setup across the Organization built in Notes 18-21.

---

## 1. Prerequisites

- An AWS Organization already exists, in **all features** mode (Note 18) — Identity Center requires Organizations to manage multi-account assignments.

---

## 2. Enable IAM Identity Center

1. From the **management account**, open the **IAM Identity Center console** → **Enable**.
2. Choose the **identity source** (Note 22, Section 2) — for this exercise, keep the default **Identity Center directory** (simplest, no external IdP wiring needed).
3. Note the generated **AWS access portal URL** shown on the dashboard — this is the single URL every assigned user will sign into going forward.

---

## 3. Create a user in the Identity Center directory

1. **Users** → **Add user**.
2. **Username**: `demo-sso-user`; fill in email and name fields → set how the user receives their initial sign-in instructions.
3. **Next** (skip group assignment for now, or add to a new group `Developers` if you want to test group-based assignment instead of a direct user assignment) → **Add user**.

---

## 4. Create a permission set

1. **Permission sets** → **Create permission set**.
2. **Permission set type**: **Predefined permission set** → choose `ReadOnlyAccess` (reuses an AWS managed policy under the hood, Note 02) for this exercise.
3. **Permission set name**: `ReadOnlyPS` → set a **session duration** (how long a signed-in session lasts before re-authentication is required) → **Create**.

> 🧠 A **Custom permission set** is also available, letting you attach customer managed policies (Note 03) or write an inline policy document directly — the exact same policy-authoring options covered earlier in this folder, just packaged for deployment across many accounts at once instead of one.

---

## 5. Assign the user to an account with this permission set

1. **AWS accounts** tab → select a specific member account from your Organization (e.g. the `dev-sandbox` account from Note 18's diagram).
2. **Assign users or groups** → select `demo-sso-user` → **Next** → select the `ReadOnlyPS` permission set → **Submit**.
3. Identity Center provisions a corresponding IAM role in that member account behind the scenes (Note 22, Section 3) — you don't create or manage that role by hand.

---

## 6. Sign in through the access portal

1. Open the **AWS access portal URL** from Section 2 in a browser (or the sign-in instructions link the new user received).
2. Sign in as `demo-sso-user`.
3. The portal shows exactly **one** account tile (`dev-sandbox`) with **one** available role (`ReadOnlyPS`) — clicking it opens the AWS Console already signed in with that permission set's access, no separate password or "Switch Role" step needed for that account.
4. Assign the same user to a **second** account with a **different** permission set, refresh the portal, and confirm a second tile now appears — this is exactly the "one identity, many accounts, one portal" promise from Note 22 made concrete.

---

## 7. Assign at the group level instead (the pattern that actually scales)

1. **Groups** → create `Developers` (if not already done in Section 3) → add `demo-sso-user` to it.
2. Repeat Section 5's assignment flow, but choose the **group** `Developers` instead of the individual user.
3. Any user added to `Developers` in the future automatically inherits this account + permission-set assignment — the same "attach once, apply to everyone in the group" principle as IAM groups (Note 06), just operating across accounts instead of within one.

---

## 8. Clean up

1. Remove the account assignments (**AWS accounts** tab → account → **Remove access**).
2. Delete the permission set, the group, and the user once no longer needed.
3. Identity Center itself can be left enabled at no charge if you plan to use it again, or disabled entirely from the Identity Center console's settings if the Organization no longer needs it.

---

## 9. Troubleshooting

| Symptom | Likely cause |
|---|---|
| User signs into the portal but sees no account tiles at all | No assignment exists yet for that user (directly or via a group) — revisit Section 5 or 7 |
| A newly-added group member doesn't see the expected account | Group-based assignments can take a short time to propagate; also confirm the user was added to the correct group |
| Permission set changes don't seem to apply | Existing sessions may still hold previously-provisioned permissions until re-authenticated — sign out and back in, or wait for the session duration configured in Section 4 to expire |

---

## 10. Recap

- Enabling Identity Center generates one central **AWS access portal URL** for the whole Organization.
- **Permission sets** (predefined or custom) define what access looks like once assigned; **assignments** connect a user or group + permission set + specific account.
- Assigning by **group** (Section 7) is the pattern that actually scales — new hires just get added to the right group and inherit access automatically, mirroring Note 06's IAM-group philosophy at the multi-account level.
- This closes the entire IAM folder: Notes 01-06 covered core identities and policies, 07-11 covered role assumption and federation, 12-14 covered root user hardening, 15-17 covered the three IAM reporting tools, and 18-23 covered AWS Organizations, SCPs, and IAM Identity Center for multi-account governance.

### Sources
- [Getting started — IAM Identity Center — AWS docs](https://docs.aws.amazon.com/singlesignon/latest/userguide/getting-started.html)
- [Permission sets — AWS docs](https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetsconcept.html)
- [Assign user access to AWS accounts — AWS docs](https://docs.aws.amazon.com/singlesignon/latest/userguide/useraccess.html)
- [AWS access portal — AWS docs](https://docs.aws.amazon.com/singlesignon/latest/userguide/using-the-portal.html)
