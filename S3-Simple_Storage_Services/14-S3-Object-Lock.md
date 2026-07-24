# 14 - AWS S3 — AWS S3 Object Lock

> Goal: understand **Object Lock** — a fundamentally different kind of protection from every access-control mechanism in Notes 09-13, since it restricts **whether an object can be changed or deleted at all**, even by a principal with full `s3:*` permissions. This is what makes S3 usable as genuine **WORM** (Write Once, Read Many) storage.

---

## 1. Object Lock vs. everything in Notes 09-13

IAM policies, bucket policies, and ACLs all answer "**who** can do **what**." Object Lock answers a different question entirely: **"can this object version be deleted or overwritten by *anyone at all*, including the account's own root user or an `AdministratorAccess` identity, for a defined period?"** Once locked, the answer is **no** — not even the most powerful identity in the account can bypass it (short of deleting the entire AWS account, or in some modes, waiting out the retention period).

> 🧠 **Mental model:** Object Lock is like a bank vault with a built-in time-delay lock — the vault's *owner* still can't open it early, no matter how much authority they otherwise have, because the lock itself doesn't check permissions, it checks the clock (or an explicit legal hold flag).

---

## 2. Prerequisite: versioning must be enabled

Object Lock can **only** be enabled on a bucket with **versioning enabled** (Note 06) — and only at **bucket creation time**, or by contacting AWS Support to enable it on an existing bucket. This is because Object Lock protects **specific object versions**, reusing versioning's Version ID model directly.

---

## 3. Two lock modes

| Mode | Behavior |
|---|---|
| **Governance mode** | Protects against deletion/overwrite for everyone **except** users with the special IAM permission `s3:BypassGovernanceRetention` — a deliberate escape hatch for legitimate administrative overrides |
| **Compliance mode** | Protects against deletion/overwrite for **everyone, including the root user** — no bypass permission exists at all; the retention period cannot be shortened or the lock removed by any means until it expires |

> ⚠️ **Compliance mode is genuinely irreversible** until the retention period ends — this is not a "break glass" situation like `IAM/13`'s root-user recovery tasks; root has **zero** special authority over a Compliance-mode lock. Choosing Compliance mode is a decision to make deliberately, for data where regulatory requirements demand it (e.g. financial records, legal holds), not as a default.

---

## 4. Retention period vs. Legal Hold — two independent lock types

- **Retention period** (Governance or Compliance mode): locks an object version until a specific **date**. Can be set per-object, or defaulted bucket-wide.
- **Legal Hold**: locks an object version **indefinitely**, with **no expiration date** — it stays locked until someone with `s3:PutObjectLegalHold` permission explicitly **removes** the hold. Independent of retention period/mode — an object can have a Legal Hold, a retention period, both, or neither.

> 🎯 **Exam tip:** "we need to preserve specific records for an ongoing litigation, with no fixed end date" is the textbook **Legal Hold** scenario — as opposed to "we must retain records for exactly 7 years per regulation," which is a **retention period** (likely Compliance mode) scenario. The exam tests distinguishing an *open-ended* hold from a *fixed-duration* lock.

---

## 5. Configure Object Lock

1. **S3 console** → **Create bucket** → check **Enable Object Lock** (only available at creation time) → this automatically also enables versioning, since it's a hard prerequisite.
2. After creation, **Properties** tab → **Object Lock** → **Edit** → set a **default retention mode** (Governance/Compliance) and **default retention period** (e.g. 3 years) applied to every new object version uploaded, unless overridden per-object.
3. To lock a **specific** object version directly:
   ```bash
   aws s3api put-object-retention \
     --bucket demo-locked-bucket \
     --key financial-record.pdf \
     --version-id <version-id> \
     --retention '{"Mode":"COMPLIANCE","RetainUntilDate":"2033-01-01T00:00:00Z"}'
   ```
4. To apply a Legal Hold instead:
   ```bash
   aws s3api put-object-legal-hold \
     --bucket demo-locked-bucket \
     --key financial-record.pdf \
     --version-id <version-id> \
     --legal-hold '{"Status":"ON"}'
   ```

---

## 6. Recap

- **Object Lock** enforces WORM (Write Once, Read Many) behavior at the object-version level, independent of IAM/bucket policy permissions — requires **versioning** enabled, set at bucket creation.
- **Governance mode** allows a special-permission bypass; **Compliance mode** allows **no bypass at all**, not even by root, until the retention period expires.
- **Retention periods** lock until a fixed date; **Legal Holds** lock indefinitely until explicitly removed — the two are independent and can be combined.
- Next: Note 15 — AWS S3 Encryption, starting the encryption series that spans the rest of this folder's next several notes.

### Sources
- [Using S3 Object Lock — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)
- [Object Lock retention modes — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-overview.html#object-lock-retention-modes)
- [Object Lock legal holds — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-overview.html#object-lock-legal-holds)
