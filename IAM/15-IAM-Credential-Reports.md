# 15 - IAM Reports, Part 1: IAM Credential Reports

> Goal: generate and read an account-wide **IAM credential report** — a single CSV snapshot of every user's credential hygiene (password age, access key age, MFA status, last usage) that turns "is anyone in this account using stale or risky credentials?" from a guess into a fact.

---

## 1. What a credential report actually contains

A **credential report** is a **CSV file**, covering **every IAM user in the account**, one row per user, with columns including:

- Whether a password exists, its age, and when it was last used.
- Whether **MFA is enabled**.
- Whether **access keys 1 and 2** exist, their age, when each was last used, and last rotation date.
- Account creation date.

> 🧠 **Mental model:** think of this as an account-wide "credential hygiene audit" you can hand to a security review — instead of clicking into every single user's **Security credentials** tab one at a time, you get every user's status in one spreadsheet, ready to filter and sort.

---

## 2. Generate and download the report

1. **IAM console** → **Access reports** (or **Credential report**, depending on console layout) → **Generate report**.
2. Once generated, **Download report** (`.csv`).
3. Reports can be regenerated at will, but AWS **caches** the underlying data for up to **4 hours** — regenerating sooner than that returns the same snapshot rather than fresher data.

> ⚠️ A credential report is **account-wide and covers only IAM users** (not roles — roles don't have long-term passwords or access keys to report on in the same way). This scope (all users, one point-in-time CSV) is what distinguishes it from Note 16's Access Advisor (per-identity, service-level, "what did they actually use") and Note 17's Access Analyzer (policy-logic-based, focused on external/unused access findings) — the three IAM reporting tools cover genuinely different questions.

---

## 3. What to actually look for in the report

| Signal in the CSV | What it means |
|---|---|
| `mfa_active = false` for a user with console access | A user who can sign in with just a password — a Note 12-style MFA gap, but for a regular user instead of root |
| `password_last_used` is very old, or blank, despite `password_enabled = true` | A likely-stale account that should probably be deactivated |
| `access_key_1_last_rotated` (or key 2) far in the past | An access key overdue for rotation — long-term credentials get riskier the longer they've gone unrotated |
| `access_key_1_last_used_date` blank despite the key being active | An access key that was created but never actually used — a candidate for deletion entirely |

---

## 4. How this feeds real account hygiene

A credential report is a natural input to a recurring security review process: pull the report on a schedule, flag every row that fails one of Section 3's checks, and follow up (enforce MFA, rotate or delete keys, deactivate unused accounts). This is exactly the kind of housekeeping that, left undone, is how "an old, forgotten access key with broad permissions" ends up being the credential that eventually leaks and gets used maliciously.

> 🎯 **Exam tip:** "get a downloadable, account-wide view of every IAM user's password age, access key age, and MFA status" is the precise, textbook description of the **credential report** — if a question instead asks about *which services* a user or role actually used, that's Access Advisor (Note 16), not the credential report.

---

## 5. Recap

- The **IAM credential report** is a single, account-wide CSV covering every IAM user's password/access-key age, last-used dates, and MFA status — generated on demand, cached for up to 4 hours.
- It answers "how healthy are this account's long-term credentials, across every user, right now?" — a different question from Access Advisor's per-identity service usage (Note 16) or Access Analyzer's policy-logic findings (Note 17).
- Regular review of this report (stale passwords, unrotated/unused keys, missing MFA) is a core, low-effort piece of ongoing IAM hygiene.
- Next: Note 16 — IAM Reports, Part 2: IAM Access Advisor Reports, narrowing the lens from "credential age" to "which services has this specific identity actually used."

### Sources
- [Getting credential reports for your AWS account — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_getting-report.html)
- [Security best practices in IAM — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
