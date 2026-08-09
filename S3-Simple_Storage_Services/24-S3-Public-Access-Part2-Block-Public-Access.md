# 24 - AWS S3 — S3 Public Access Part 2: Block Public Access

> Goal: understand **Block Public Access (BPA)** — the override sitting above both mechanisms from Note 23 — its four independent settings, and why it's enabled by default on every new bucket and every new AWS account today.

---

## 1. What Block Public Access does

**Block Public Access** is a safety-net setting, configurable at both the **account level** and the **individual bucket level**, that can **force-deny** public access even when a bucket policy or ACL (Note 23) explicitly tries to grant it. It doesn't remove or edit the underlying policy/ACL — it just **prevents S3 from honoring** the public-granting parts of it.

> 🧠 **Mental model:** Block Public Access is a master override switch positioned *above* Note 23's two granting mechanisms — think of it as a facility-wide "no public entry" rule that stays in effect even if someone individually props a door open (a bucket policy or ACL); the door being propped open doesn't matter if the master rule still says no.

---

**S3 Block Public Access** is a set of **4 safety controls** that prevent an S3 bucket or its objects from accidentally becoming publicly accessible.

The important thing is that these are **not permissions themselves**. They are **guardrails** that can override/prevent certain public-access configurations.

![Image](https://images.openai.com/static-rsc-4/iKKw4KLmWtktfHPukQ8tgKO9uPRA7J73QaV54W1WHUz-iIxLWNFuHzh0qFx44dWJXRo4OcfzYArGCIZhojwzLeQliijoPNjYiC6nKTlFkLj55Za4SVbiNTlyS1ezChV0NgyuRuUiKOxVZwC1362N13ZhYQ-J69nZOPTc2fiqzWvdrnosJsY8fMugcYUmV2hr?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/MKszEzSUJT0D2a0Z1a3E64LZBkj41-Hy136i8Q75dErGwiIgvaHHGUiWeB9_K1Ez9lBbmHqTlhv0JeTfLgnX8kwDvqQr-JGcWx3u4qGdhGAqBYC3bqHXorMuOqYTgW6dF1rIA8sfDIksQ7-vIiLda5NzACPfgh7M3X7uzKuH59yxhgV39liIMFB8bXTxirB1?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/bZDJ6Pm2xWy3ruMuAtUPshI4IEJPgwsWIjYJY9p2JzYrg6FhcxYJWMen30uKeA__j_E7kcysPt9vELGG7y2fO2o6cLCkbQqLZhBe-uIDmZ14VEh_XksMk6jHU_hmWYDdcLfVJmGBzIkAHs5iNa9Q74AVrOZzQ8n4MWzgJ_LHgMT8mH6qIl43GDv6rLUBRl6C?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/AadiTquzhmBcNKQ7BH4RuK_OWAQ__QL7ZJtG51plOAfle1FrBJ1ukEExhgrfK0UKIcz4OuaFRtIv9ZFm7CYn7A-jEIPp18BOPB_BxN1J2iPCOzAc2MXQXIxS-hsY4cVNT1Z4Fny0daJKullxqULMBKhFXQywjjhdzbzWMT7NDZmBcT3xBv_F1AvIZROOA0Lv?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/_CRyaZFgHSVy40M2NFLd3jr9G5qcCc1Y6LURN-2W7gEPN7x5y9Q4iUejKrD3OrMJxuBUC4h4SDqK8RYxXD2qdMj3laJJ9odhCGE0lWvPsvm_dneM8_b5_7BfhlkNgQAjvPRFlgRga-iL6rOGpcSC_ukMNlu3ATUcWC1YBz2iaOkijEp_SB33j6kNscPQ_yQ-?purpose=fullsize)

---

# 1. The 4 Block Public Access options

In the S3 console you'll see:

```text
Block public access

☑ Block public access to buckets and objects granted through new access control lists (ACLs)
☑ Block public access to buckets and objects granted through any access control lists (ACLs)
☑ Block public access to buckets and objects granted through new public bucket or access point policies
☑ Block public and cross-account access to buckets and objects through any public bucket or access point policies
```

AWS uses these four settings:

```text
1. BlockPublicAcls
2. IgnorePublicAcls
3. BlockPublicPolicy
4. RestrictPublicBuckets
```

Let's understand each with a real example.

---

# 2. First: ACL vs Bucket Policy

Before the four options, remember that S3 historically had two ways to grant access:

```text
                    S3 Access
                       │
             ┌─────────┴─────────┐
             │                   │
            ACL             Bucket Policy
             │                   │
       Object/Bucket       Resource-based
       permissions          policy
```

Today, **Bucket Policies** are much more commonly used, and AWS generally recommends keeping ACLs disabled unless you specifically need them.

The four Block Public Access settings protect against public access through **ACLs and policies**.

---

# 3. Option 1 — BlockPublicAcls

Console:

> **Block public access to buckets and objects granted through new access control lists (ACLs)**

API name:

```text
BlockPublicAcls
```

### What does it do?

It prevents you from creating **new public ACL grants**.

Suppose someone tries to make an object public using an ACL:

```text
financial-report.pdf
        │
        ▼
ACL
        │
        └── Everyone → READ
```

That's a public ACL.

With:

```text
BlockPublicAcls = TRUE
```

S3 blocks that attempt.

---

## Example

Suppose:

```text
demo-bucket
└── image.jpg
```

Someone attempts:

```text
image.jpg
   │
   └── ACL:
       Everyone → READ
```

With BlockPublicAcls enabled:

```text
Public ACL
    │
    ▼
❌ BLOCKED
```

### Important

It specifically protects against **new public ACL configurations**.

It doesn't mean:

> "Remove every existing public ACL."

That's where the next setting comes in.

---

# 4. Option 2 — IgnorePublicAcls

Console:

> **Block public access to buckets and objects granted through any access control lists (ACLs)**

API name:

```text
IgnorePublicAcls
```

This one is slightly different.

Suppose an object already has:

```text
image.jpg
    │
    └── ACL:
        Everyone → READ
```

Now:

```text
IgnorePublicAcls = TRUE
```

S3 essentially says:

> "I don't care what public ACL says. Ignore it."

So:

```text
Existing Public ACL
        │
        ▼
IgnorePublicAcls
        │
        ▼
🚫 Public ACL permission ignored
```

### Difference between #1 and #2

This is a common exam question.

| Setting              | What it does                     |
| -------------------- | -------------------------------- |
| **BlockPublicAcls**  | Prevents **new** public ACLs     |
| **IgnorePublicAcls** | Ignores **existing** public ACLs |

Think:

```text
BlockPublicAcls
     ↓
STOP creating public ACL

IgnorePublicAcls
     ↓
IGNORE public ACL
```

---

# 5. Option 3 — BlockPublicPolicy

Now we move from **ACLs** to **Bucket Policies**.

Console:

> **Block public access to buckets and objects granted through new public bucket or access point policies**

API name:

```text
BlockPublicPolicy
```

Suppose you try to attach this bucket policy:

```json id="7s3i4d"
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::demo-bucket/*"
    }
  ]
}
```

Look at:

```text
"Principal": "*"
```

This means:

> Anyone.

So you're trying to make:

```text
demo-bucket
      │
      └── Anyone → GetObject
```

If:

```text
BlockPublicPolicy = TRUE
```

S3 prevents the public bucket policy from being applied.

```text
Public Bucket Policy
        │
        ▼
BlockPublicPolicy
        │
        ▼
       ❌
```

---

# 6. Important difference

This setting prevents **new public policies**.

So:

```text
BlockPublicPolicy
        ↓
Prevents new public bucket/access-point policies
```

It doesn't mean:

> "Ignore an already-existing public policy."

That's what `RestrictPublicBuckets` is about.

---

# 7. Option 4 — RestrictPublicBuckets

Console:

> **Block public and cross-account access to buckets and objects through any public bucket or access point policies**

API name:

```text
RestrictPublicBuckets
```

This is the one people often find confusing.

Imagine the bucket has a public policy:

```json id="a6djlv"
{
  "Effect": "Allow",
  "Principal": "*",
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::demo-bucket/*"
}
```

That's a public bucket policy.

If:

```text
RestrictPublicBuckets = TRUE
```

S3 restricts access granted through that public policy.

The key idea is:

> **A bucket with a public policy becomes restricted so that only AWS principals within the bucket owner's account can access it through that policy.**

So imagine:

```text
Public Bucket Policy

Principal: *
     │
     ├── Account A → potentially allowed
     │
     ├── Account B → blocked
     │
     └── Anonymous internet → blocked
```

This is especially useful as a **safety net** if a bucket accidentally has a public policy.

---

# 8. The easiest way to remember all 4

Think about **ACLs vs Policies**:

```text
                 S3 Block Public Access
                         │
             ┌───────────┴───────────┐
             │                       │
            ACLs                   Policies
             │                       │
       ┌─────┴─────┐           ┌─────┴─────┐
       │           │           │           │
       ▼           ▼           ▼           ▼
   BlockPublic  IgnorePublic  BlockPublic  RestrictPublic
      Acls         Acls         Policy       Buckets
```

Or even simpler:

| Setting                   | Think                                          |
| ------------------------- | ---------------------------------------------- |
| **BlockPublicAcls**       | 🛑 Stop **new** public ACLs                    |
| **IgnorePublicAcls**      | 🙈 Ignore public ACLs                          |
| **BlockPublicPolicy**     | 🛑 Stop **new** public policies                |
| **RestrictPublicBuckets** | 🔒 Restrict access through **public policies** |

---

# 9. Real-world example

Suppose you have:

```text
AWS Account
     │
     ▼
S3
     │
     └── production-data
            │
            ├── customer-data/
            ├── invoices/
            └── backups/
```

You absolutely don't want:

```text
Internet
   │
   ▼
production-data
   │
   └── customer-data
```

So you enable all four:

```text
☑ BlockPublicAcls
☑ IgnorePublicAcls
☑ BlockPublicPolicy
☑ RestrictPublicBuckets
```

Now you have multiple layers of protection:

```text
                   S3
                    │
        ┌───────────┴───────────┐
        │                       │
       ACL                    Policy
        │                       │
   Block/Ignore          Block/Restrict
        │                       │
        └───────────┬───────────┘
                    │
                    ▼
              Public access
                    │
                    ▼
                   ❌
```

---

# 10. Why does AWS recommend enabling all 4?

For a typical private bucket:

```text
Private application bucket
        │
        ├── BlockPublicAcls ✓
        ├── IgnorePublicAcls ✓
        ├── BlockPublicPolicy ✓
        └── RestrictPublicBuckets ✓
```

This protects you if someone accidentally does something like:

### Mistake 1

```text
ACL:
Everyone → READ
```

Blocked/ignored.

### Mistake 2

Someone adds:

```json id="x1z4vn"
"Principal": "*"
```

to a bucket policy.

Blocked.

### Mistake 3

A public policy somehow exists.

`RestrictPublicBuckets` provides another layer of protection against public/cross-account access through that public policy.

---

# 11. What if I actually WANT a public S3 bucket?

For example, imagine a website hosting public images:

```text
Internet
   │
   ▼
CloudFront
   │
   ▼
S3
 ├── logo.png
 ├── banner.jpg
 └── product1.jpg
```

You may intentionally need public-read access **or, preferably, CloudFront-based access without making the bucket public**.

If you deliberately make the bucket public through a bucket policy:

```json id="j9sy8a"
{
  "Effect": "Allow",
  "Principal": "*",
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::public-assets/*"
}
```

then Block Public Access can prevent that configuration from working.

So:

```text
Private bucket
      +
Block Public Access = ON
      ↓
Excellent default
```

But:

```text
Intentionally public bucket
      +
Block Public Access = ON
      ↓
Public policy/ACL configuration may be blocked
```

---

# 12. One important modern AWS architecture

For a website, instead of:

```text
Internet
   │
   ▼
S3 public bucket
```

a better architecture is often:

```text
                    Internet
                       │
                       ▼
                  CloudFront
                       │
                       │ OAC
                       ▼
                  S3 Bucket
                       │
              Block Public Access
                    enabled
```

The bucket stays **private**.

CloudFront gets permission through an S3 bucket policy specifically for the CloudFront distribution.

So:

```text
Public Internet
      │
      ▼
CloudFront
      │
      ▼
Private S3
```

rather than:

```text
Public Internet
      │
      ▼
Public S3 ❌
```

---

# 13. One subtle but VERY important point

**Block Public Access does not mean "block all access to S3."**

It does **not** stop:

```text
EC2 Role ─────────► S3
Lambda Role ──────► S3
ECS Task Role ────► S3
IAM User ─────────► S3
CloudFront OAC ───► S3
```

provided those are authorized appropriately.

It specifically targets **public access mechanisms**.

So:

```text
IAM Role
   │
   │ Authorized
   ▼
S3
   ✅
```

while:

```text
Principal: *
   │
   │ Public
   ▼
S3
   ❌ if Block Public Access prevents it
```

---

# Final mental model

Memorize this:

```text
             S3 BLOCK PUBLIC ACCESS
                       │
             ┌─────────┴─────────┐
             │                   │
            ACL                POLICY
             │                   │
       ┌─────┴─────┐       ┌─────┴──────┐
       │           │       │            │
       ▼           ▼       ▼            ▼
    Block       Ignore   Block       Restrict
     New         ACL      New          Public
     ACLs       grants   Policies     Policies
```

### In exam language:

**BlockPublicAcls** → blocks **new public ACLs**

**IgnorePublicAcls** → ignores **public ACLs**

**BlockPublicPolicy** → blocks **new public bucket/access-point policies**

**RestrictPublicBuckets** → restricts access through **public bucket/access-point policies**, including public/cross-account access, to principals in the bucket owner's account.

And for a normal private S3 bucket:

> **Enable all four Block Public Access settings.**


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
