# 24 - AWS S3 — S3 Public Access Part 2: Block Public Access

> Goal: understand **Block Public Access (BPA)** — the override sitting above both mechanisms from Note 23 — its four independent settings, and why it's enabled by default on every new bucket and every new AWS account today.

---

## 1. What Block Public Access does

**Block Public Access** is a safety-net setting, configurable at both the **account level** and the **individual bucket level**, that can **force-deny** public access even when a bucket policy or ACL (Note 23) explicitly tries to grant it. It doesn't remove or edit the underlying policy/ACL — it just **prevents S3 from honoring** the public-granting parts of it.

> 🧠 **Mental model:** Block Public Access is a master override switch positioned *above* Note 23's two granting mechanisms — think of it as a facility-wide "no public entry" rule that stays in effect even if someone individually props a door open (a bucket policy or ACL); the door being propped open doesn't matter if the master rule still says no.

---

## 2. The four independent settings

| Setting | What it blocks |
|---|---|
| **Block public access to buckets and objects granted through new ACLs** | New ACLs that would grant public access, going forward |
| **Block public access to buckets and objects granted through any ACLs** | **All** ACL-based public access, including pre-existing ACLs |
| **Block public access to buckets and objects granted through new public bucket or access point policies** | New bucket/access point policies that would grant public access, going forward |
| **Block public access to buckets and objects granted through any public bucket or access point policies** | **All** bucket-policy-based public access, including pre-existing policies |

Each of the four can be toggled **independently** — e.g. you could block all *new* public grants while still honoring an intentionally-public policy that already exists, though enabling all four together is by far the most common, safest default.

---

## 3. Default: on, everywhere, for new resources

- Every **new AWS account** created today has Block Public Access **enabled by default at the account level**.
- Every **new bucket** created today has Block Public Access **enabled by default at the bucket level** too.
- This means making a bucket genuinely public today requires a **deliberate, explicit** decision to turn BPA off — accidental public exposure from a stray bucket policy or ACL, by itself, is no longer enough; BPA has to be knowingly disabled first (Note 25 walks through doing this correctly for a legitimate use case like static website hosting).

> ⚠️ **Account-level BPA settings can override bucket-level settings**, but not the other way around — if BPA is enabled at the **account** level, an individual bucket cannot "opt out" of that account-wide block on its own; the account-level setting must be relaxed first (by someone with sufficient permission) before any bucket-level setting even has a chance to matter.

---

## 4. Enable/inspect Block Public Access

1. **S3 console** → **Block Public Access settings for this account** (account-wide) → view/edit all four toggles.
2. Per-bucket: bucket → **Permissions** tab → **Block public access (bucket settings)** → **Edit**.
3. Attempting to save a bucket policy or ACL that would grant public access, while BPA still blocks it, produces a clear warning/error in the console — a deliberate friction point meant to make public exposure a conscious choice, not an accident.

> 🎯 **Exam tip:** "a bucket policy grants public read access, but objects still aren't reachable by the public" is a textbook **Block Public Access** scenario — the fix is disabling the relevant BPA setting (only after confirming public access is genuinely intended), not re-writing the bucket policy, which was likely already correct.

---

## 5. Recap

- **Block Public Access** is an override, at both **account** and **bucket** level, with **four independent settings**, that can force-deny public access even when a bucket policy or ACL (Note 23) explicitly grants it.
- Enabled **by default** on every new account and every new bucket — genuine public exposure today requires deliberately disabling it first.
- Account-level BPA settings take precedence over bucket-level settings, never the reverse.
- Next: Note 25 — S3 Public Access Part 3: Make An S3 Bucket Or Object Public Using Bucket Policy, walking through the deliberate, correct way to actually do this when public access is genuinely needed.

### Sources
- [Blocking public access to your Amazon S3 storage — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html)
- [The meaning of "public" — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html#access-control-block-public-access-policy-status)
