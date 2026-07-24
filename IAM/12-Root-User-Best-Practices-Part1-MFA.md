# 12 - IAM Root User Best Practices, Part 1: Multi-Factor Authentication (MFA)

> Goal: understand exactly why the **root user** is uniquely dangerous compared to every identity covered in Notes 01-11, and lock it down with MFA as the first, non-negotiable step. Parts 2-3 (Notes 13-14) continue with "stop using it at all" and the remaining account-level hardening steps.

---

## 1. Why the root user is different from everything else in this folder

The **root user** is created automatically the moment you make an AWS account, tied to the account's original email address, and it is the **only** identity that can never be permission-restricted by any IAM policy — no `Deny` statement, no permissions boundary, no SCP (in most configurations) can take away root's access to **everything** in the account, including the ability to close the account entirely.

> ⚠️ Every other identity in this folder — users, groups, roles, federated identities — is subject to IAM's policy evaluation logic from Note 01. **The root user is not** — it bypasses essentially all of it. This single fact is why root gets its own three-part best-practices series instead of being folded into Note 05's user-creation note.

---

## 2. Enable MFA on the root user — the very first security action on any new account

**Multi-Factor Authentication (MFA)** requires a **second, independent proof of identity** beyond the password — even if the root password is ever leaked or guessed, an attacker still cannot sign in without also possessing the second factor.

1. Sign in as the **root user** (the only identity that can configure its own MFA — this isn't delegable to anyone else).
2. Top-right account name menu → **Security credentials**.
3. **Multi-factor authentication (MFA)** → **Assign MFA device**.
4. Choose a device type:

| MFA type | What it is | Notes |
|---|---|---|
| **Virtual MFA device** | An authenticator app (e.g. a TOTP app) on a phone/tablet, generating a rotating 6-digit code | Free, fastest to set up, the most common choice |
| **Security key** (FIDO2/U2F/Passkey) | A physical hardware key (e.g. a USB/NFC security key) or a platform passkey | Phishing-resistant — AWS's recommended strongest option for root specifically |
| **Hardware TOTP token** | A dedicated physical device displaying a rotating 6-digit code, no phone required | Useful where phones aren't allowed/available, or as an air-gapped option |

5. Complete the device-specific setup flow (e.g. scanning a QR code with an authenticator app, then entering two consecutive generated codes to confirm).

> 🧠 **Mental model:** a password alone proves "you know a secret." MFA adds "you also possess a specific physical thing (or a passkey bound to a specific device)" — an attacker needs both, not just one, which is why a leaked/reused/phished password alone stops being enough to get in.

---

## 3. Why this specifically matters for root (more than for any IAM user)

- Root can **never be permission-limited**, so if it's ever compromised, the blast radius is the **entire account** — every resource, every bill, every other identity's permissions.
- Root, by design, has **no separate "least privilege" version of itself** — you cannot scope down what root can do the way you scope down a user's or role's policy.
- MFA is therefore not "one good practice among many" for root — it is the **single most load-bearing control** standing between a leaked/guessed password and total account compromise.

> 🎯 **Exam tip:** "which single action provides the most security benefit for protecting the root user?" is a recurring SAA-C03 phrasing, and **enabling MFA on the root user** is the textbook answer — ahead of things like password rotation alone, since MFA specifically defeats the "password got leaked/guessed" attack path that a strong password alone doesn't fully close.

---

## 4. Recap

- The root user is fundamentally different from every other identity in this folder — no IAM policy, deny statement, or (typically) SCP can restrict it.
- **Enabling MFA on root** is the first, highest-priority security action on any new AWS account, using a virtual MFA app, a hardware/passkey security key (AWS's strongest recommendation), or a hardware TOTP token.
- Because root can never be permission-limited, MFA carries disproportionately more weight here than on any ordinary IAM user.
- Next: Note 13 — Root User Best Practices, Part 2: Never Use the Root User — covering exactly which handful of tasks actually still require root, and why everything else should go through a dedicated IAM identity instead.

### Sources
- [AWS account root user — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html)
- [Using multi-factor authentication (MFA) in AWS — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa.html)
- [Security best practices in IAM — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
