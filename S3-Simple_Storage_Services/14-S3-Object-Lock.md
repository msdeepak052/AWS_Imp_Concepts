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



## S3 Object Lock — AWS Console Demo

Object Lock is used to prevent S3 objects from being deleted or overwritten for a defined period.

Think:

```text
S3 Bucket
   │
   └── Object Lock
         │
         ├── Governance Mode
         │
         └── Compliance Mode
```

It works with **S3 Versioning**, because the retention is applied to a **specific object version**.

---

## Step 1 — Create the S3 bucket

Go to:

**AWS Console → S3 → General purpose buckets → Create bucket**

Enter:

```text
Bucket name:
demo-locked-bucket
```

Choose your region, for example:

```text
Asia Pacific (Mumbai) ap-south-1
```

Scroll down to:

### Object Ownership

You can leave the default:

```text
ACLs disabled
```

---

## Step 2 — Enable Object Lock

In the **Object Lock** section, enable:

```text
☑ Enable Object Lock
```

You will see a message indicating that:

> Object Lock requires versioning.

When you enable Object Lock during bucket creation, **S3 automatically enables Versioning** for the bucket.

So you don't need to separately enable Versioning.

Conceptually:

```text
Create Bucket
     │
     └── Enable Object Lock
             │
             └── Versioning automatically enabled
```

Then click:

**Create bucket**

---

## Step 3 — Open the bucket

After creation:

**S3 → Buckets → demo-locked-bucket**

You'll see the bucket.

Go to:

**Properties**

Scroll down until you find:

### Object Lock

You should see that Object Lock is enabled.

You'll also see the default retention configuration.

Click:

**Edit**

---

## Step 4 — Configure Default Retention

You'll get options for the default retention.

You can configure:

### Retention mode

There are two choices:

```text
Governance
Compliance
```

Let's understand them.

---

## Governance Mode

Governance mode provides protection against accidental deletion or modification.

Normal users cannot delete/modify a locked version during the retention period.

However, specially authorized users with appropriate permissions can bypass Governance mode.

Think:

```text
Governance

Normal user
    │
    └── ❌ Delete

Privileged user
    │
    └── ✅ Can bypass
```

This is useful when you want protection but still need an administrative override.

---

## Compliance Mode

Compliance mode is much stricter.

Once an object version is locked under Compliance mode:

```text
Retention period
      │
      ├── Normal user       ❌
      ├── Admin             ❌
      └── Root              ❌
```

The object version cannot be deleted or have its retention shortened before the retention date.

Think:

> **Compliance = absolutely no early deletion.**

This is commonly associated with regulatory/WORM requirements.

---

## Step 5 — Choose the default retention period

Suppose you want:

```text
Retention mode:
COMPLIANCE

Retention period:
3 Years
```

Configure:

```text
Default retention period

☑ Enable

Mode:
Compliance

Days:
1095
```

or choose the available years/months/days fields in the console.

Then click:

**Save changes**

---

## What does "default retention" actually mean?

This is very important.

Suppose you upload:

```text
financial-record.pdf
```

on:

```text
January 1, 2026
```

Your default retention is:

```text
Compliance
3 years
```

S3 applies the retention to the **new object version**.

Conceptually:

```text
financial-record.pdf
        │
        ▼
Version ID: abc123
        │
        ├── Retention: COMPLIANCE
        │
        └── Retain Until:
            January 1, 2029
```

The object version is protected until the retention date.

---

## Step 6 — Upload an object

Go to:

**Objects → Upload**

Choose:

```text
financial-record.pdf
```

Click:

**Upload**

Now S3 creates a version:

```text
financial-record.pdf

Version ID: abc123
       │
       └── COMPLIANCE
           Retain Until: 2029
```

Because you configured **default retention**, the retention is automatically applied to newly uploaded object versions.

---

## Step 7 — View Object Lock information

Click:

```text
financial-record.pdf
```

You'll see the object's details.

Look for the **Object Lock** / retention information.

You can see things such as:

```text
Retention mode:
COMPLIANCE

Retain until date:
<date>
```

The exact console layout can vary slightly as AWS updates the S3 console.

---

## Step 8 — Lock a specific object version from the Console

You can also configure retention on an individual object version.

Go to:

```text
S3
 ↓
demo-locked-bucket
 ↓
Objects
 ↓
financial-record.pdf
```

Because Versioning is enabled, you can access the object's versions.

Select the specific version you want to protect.

Then look for the **Actions** menu.

Choose the Object Lock / retention option, such as:

```text
Edit retention
```

or the corresponding **Object Lock** action shown by the console.

You'll be able to specify:

```text
Retention mode:
Governance / Compliance

Retain until date:
01/01/2033
```

Save the change.

Now that specific version has its own retention configuration.

---

## Step 9 — Legal Hold

Object Lock also has another mechanism:

> **Legal Hold**

This is different from retention.

Suppose:

```text
financial-record.pdf
Version: abc123
```

You don't know exactly how long you need to preserve it.

Instead, you can place a:

```text
LEGAL HOLD = ON
```

Conceptually:

```text
financial-record.pdf
       │
       └── Version abc123
              │
              └── Legal Hold: ON
```

While the legal hold is ON, the object version is protected from deletion, regardless of a configured retention period.

---

## Step 10 — Enable Legal Hold from the Console

Go to:

```text
S3
 ↓
demo-locked-bucket
 ↓
Objects
 ↓
financial-record.pdf
```

Select the relevant object version.

Go to:

**Actions**

Look for the Object Lock / Legal Hold option.

Choose:

```text
Legal hold
```

Set:

```text
ON
```

and save.

You should then see something like:

```text
Legal Hold: ON
```

for that object version.

---

## Retention vs Legal Hold

This is an important interview question.

### Retention

You specify **until when** the object must be protected.

Example:

```text
Mode:
COMPLIANCE

Retain Until:
01-Jan-2029
```

Think:

> **Protect this object until this date.**

---

### Legal Hold

There is **no expiry date**.

```text
Legal Hold:
ON
```

The object stays protected until someone with appropriate permission turns the legal hold **OFF**.

Think:

> **Don't delete this object until the investigation/legal requirement is finished.**

---

## Complete Console Demo

You can demonstrate the whole thing like this:

```text
AWS Console
     │
     ▼
S3
     │
     ▼
Create bucket
     │
     ├── Name: demo-locked-bucket
     │
     └── Enable Object Lock ✓
              │
              ▼
       Versioning automatically enabled
              │
              ▼
         Create bucket
              │
              ▼
        Properties
              │
              ▼
        Object Lock
              │
              ▼
             Edit
              │
              ├── Governance
              │
              │       OR
              │
              └── Compliance
                       │
                       ▼
                  3 Years
                       │
                       ▼
                   Save
                       │
                       ▼
                  Objects
                       │
                       ▼
             Upload financial-record.pdf
                       │
                       ▼
              New object version
                       │
                       ▼
             Retention automatically
                    applied
```

---

## One thing to remember

There are **three different concepts** here:

```text
                 S3 Object Lock
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
      Governance   Compliance   Legal Hold
          │            │            │
      Can bypass   Cannot       No fixed
      with proper  bypass       expiry date
      permission   retention    until OFF
```

And Object Lock is **version-specific**:

```text
financial-record.pdf

v3 ← locked until 2029
v2 ← not necessarily locked
v1 ← not necessarily locked
```

So if you have versioning enabled and upload the same object three times, **each new version can have its own Object Lock/retention state**.

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
