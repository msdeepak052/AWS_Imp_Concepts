# 36 - AWS S3 Multi Factor Authentication (MFA) Delete

> Goal: enable **MFA Delete** — a versioning-dependent bucket protection requiring a live MFA code for the two most destructive version-level operations — and understand its specific, narrow scope and its console/CLI limitation.

---

## 1. What MFA Delete actually protects against

**MFA Delete** requires the bucket owner's **root user** to provide a **current MFA code** (from a device registered per `IAM/12`) for exactly two specific operations:

1. **Permanently deleting an object version** (a real, hard delete of a specific Version ID — not just adding a delete marker, Note 06).
2. **Suspending versioning** on the bucket entirely (Note 06, Section 5).

Everything else — normal uploads, normal (soft) deletes that just add a delete marker, reads — is completely unaffected by MFA Delete.

> 🧠 **Mental model:** MFA Delete adds a second, physical-possession-required check specifically around the two actions that could **permanently destroy version history** — the exact same "why root's MFA matters so much" logic from `IAM/12`, now applied at the bucket-version level instead of account sign-in.

---

## 2. Prerequisite: versioning must already be enabled

Exactly like Object Lock (Note 14), MFA Delete requires **versioning enabled first** (Note 06) — it's a protection layered specifically on top of the version-history model, and has no meaning on a bucket without versioning.

---

## 3. Enable MFA Delete — CLI only, root credentials only

Unlike almost everything else in this folder, MFA Delete **cannot be enabled via the S3 console at all** — it must be configured via the **AWS CLI (or API)**, and critically, **only the bucket owner's root user's credentials** can enable or disable it (not even an `AdministratorAccess` IAM user can do this, echoing `IAM/13`'s "some things are genuinely root-only" theme):

```bash
aws s3api put-bucket-versioning \
  --bucket demo-mfa-protected-bucket \
  --versioning-configuration Status=Enabled,MFADelete=Enabled \
  --mfa "arn:aws:iam::111122223333:mfa/root-account-mfa-device 123456"
```

The `--mfa` parameter combines the **MFA device's ARN** and the **current 6-digit code** from that device, space-separated, in a single string.

> ⚠️ This root-only restriction is a frequently tested, easy-to-forget detail — a common exam trap is assuming any sufficiently-privileged IAM identity can enable MFA Delete, when in fact **only the root user's own credentials and active MFA device** can do it, regardless of what IAM policies say.

---

## 4. What it looks like in practice — deleting a version once enabled

```bash
aws s3api delete-object \
  --bucket demo-mfa-protected-bucket \
  --key sensitive-file.txt \
  --version-id <version-id> \
  --mfa "arn:aws:iam::111122223333:mfa/root-account-mfa-device 654321"
```

Attempting this same command **without** the `--mfa` parameter fails outright — the permanent version delete simply cannot proceed without a fresh, valid MFA code supplied at the moment of the request.

---

## 5. MFA Delete vs. Object Lock — don't confuse the two

| | MFA Delete (this note) | Object Lock (Note 14) |
|---|---|---|
| Protects against | Permanent version deletion, versioning suspension | Any modification/deletion for a defined retention period or legal hold |
| Who can bypass it | No one — a valid MFA code from the root user's device is always required for the two protected actions | Governance mode: specific-permission bypass possible. Compliance mode: no bypass, ever, until retention expires |
| Configurable via console? | ❌ No — CLI/API only | ✅ Yes |
| Scope | The whole bucket's version-deletion behavior | Per-object-version, with independent retention settings |

> 🎯 **Exam tip:** "require an additional authentication factor specifically to permanently delete object versions or disable versioning" is the signature **MFA Delete** scenario — distinct from Object Lock's broader, retention-period/legal-hold-based protection. If the question emphasizes a fixed **retention period** or **legal hold**, that's Object Lock; if it emphasizes requiring **MFA specifically for delete/suspend actions**, that's this note.

---

## 6. Recap

- **MFA Delete** requires a live MFA code from the **root user's** own MFA device for two specific actions: permanently deleting an object version, and suspending versioning.
- Requires **versioning already enabled**; configurable **only via CLI/API**, and **only by the root user** — no IAM identity, however privileged, can enable or disable it.
- Distinct from Object Lock (Note 14), which protects against a broader set of actions via retention periods/legal holds rather than an MFA requirement specifically.
- Next: Note 37 — AWS S3 Event Notification, triggering downstream automation whenever objects are created, deleted, or restored.

### Sources
- [Configuring MFA delete — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/MultiFactorAuthenticationDelete.html)
- [Using versioning in S3 buckets — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html)
