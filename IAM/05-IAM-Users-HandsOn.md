# 05 - IAM Entities: IAM Users (Hands-On)

> Goal: create an IAM user the complete way — console access, programmatic access, a custom password policy, and tags — and understand the two independent access methods a user can hold at once.

---

## 1. What an IAM user is (and its two independent access methods)

An IAM user represents **one specific person or application** with **long-term credentials**. A user can have either or both of:

| Access method | Credential | Used for |
|---|---|---|
| **Console access** | A password (with optional MFA) | Signing into the AWS Management Console in a browser |
| **Programmatic access** | An access key ID + secret access key | AWS CLI, SDKs, direct signed API requests |

These are **independent** — a user can have console access only, programmatic access only, both, or (rare, but valid) neither yet.

> ⚠️ **Access keys are long-term credentials** — unlike the role-based temporary credentials from Note 01, a leaked access key stays valid until someone manually deactivates or deletes it. This is exactly why every later "best practice" note in this folder pushes toward roles over long-term access keys wherever an alternative exists.

---

## 2. Create a user with console access

1. **IAM console** → **Users** → **Create user**.
2. **User name**: `demo-console-user`.
3. Check **Provide user access to the AWS Management Console** → **I want to create an IAM user** → choose **Custom password**, set one → optionally **Require password reset** on first sign-in (recommended for real onboarding).
4. **Set permissions** → attach `AmazonEC2ReadOnlyAccess` (an AWS managed policy, Note 02) directly, or add to a group if one already exists (Note 06).
5. **Create user** — note the **console sign-in URL** shown on the confirmation page; this is account-specific and is what you'd hand to the actual person.

---

## 3. Add programmatic access (access keys) to an existing user

1. Open `demo-console-user` → **Security credentials** tab.
2. **Access keys** → **Create access key**.
3. Choose a use case (e.g. **Command Line Interface (CLI)**) — the console tailors its warning/guidance text based on this choice, but the resulting key works the same regardless of which use case you pick.
4. **Create access key** — the **secret access key is shown exactly once**; download the `.csv` or copy it now, because it cannot be retrieved again later (only regenerated as a brand-new key pair).

> 🎯 **Exam tip:** "the secret access key was lost / not saved" always means **create a new access key and deactivate/delete the old one** — there is no way to retrieve a previously-generated secret access key from the console after the fact.

---

## 4. Set an account-wide password policy

1. **IAM console** → **Account settings** → **Password policy** → **Edit**.
2. Configure requirements such as minimum length, character-type requirements, password expiration, password reuse prevention, and whether users can rotate their own expired password.
3. **Save changes** — this policy applies to **every** IAM user in the account going forward, not per-user.

---

## 5. Tag the user

1. `demo-console-user` → **Tags** tab → **Add new tag**.
2. Example: `Team = Analytics`, `CostCenter = 4471`.
3. Tags don't grant any permission by themselves, but they're the basis for **attribute-based access control (ABAC)** — policies can use `Condition` blocks that reference a principal's tags (e.g. "only allow access if `aws:PrincipalTag/Team` equals the resource's own `Team` tag"), letting permissions scale by attribute instead of needing a hand-written policy per user.

---

## 6. Console vs. programmatic access — quick reference

| | Console access | Programmatic access |
|---|---|---|
| Credential | Password (+ optional MFA) | Access key ID + secret access key |
| Where it's used | Browser sign-in | CLI, SDKs, direct API calls |
| Governed by | Password policy (Section 4) | No password policy equivalent — rotate/deactivate manually, or better, avoid long-term keys entirely (Note 07) |
| Can view secret again after creation? | N/A (you set your own password) | **No** — secret access key is shown only once |

---

## 7. Recap

- An IAM user can hold **console access** (password) and/or **programmatic access** (access keys) independently — most users need only one, not both.
- A **secret access key is shown exactly once** — losing it means creating a replacement, never retrieving the original.
- An account-wide **password policy** applies to every user's console password, configured once in **Account settings**.
- **Tags** on a user don't grant permissions directly but enable attribute-based access control (ABAC) patterns.
- Next: Note 06 — IAM Entities: IAM Groups (Hands-On), organizing users like this one at scale.

### Sources
- [IAM users — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html)
- [Managing access keys for IAM users — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)
- [Setting an account password policy for IAM users — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_passwords_account-policy.html)
- [Tagging IAM resources — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html)
