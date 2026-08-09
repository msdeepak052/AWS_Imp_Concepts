# 08 - AWS S3 Lifecycle Rule — Part 2

> Goal: cover the other half of Lifecycle rules — **expiration actions** that actually delete objects, non-current versions, and delete markers, plus the incomplete-multipart-upload cleanup action — completing the automated storage-hygiene picture Note 07 started.

---

## 1. Expiration actions — the four flavors

| Action | What it deletes | Applies to |
|---|---|---|
| **Expire current version** | The current version of an object, after N days | Any bucket |
| **Permanently delete non-current versions** | Old (non-current) versions, after N days of being non-current | Versioning-enabled buckets |
| **Delete expired object delete markers** | A delete marker that has become "orphaned" (no non-current versions left underneath it) | Versioning-enabled buckets |
| **Delete incomplete multipart uploads** | Parts from a multipart upload (Note 38) that was started but never completed or aborted | Any bucket |

> 🧠 **Mental model:** Note 07's transitions move data to cheaper storage; this note's expirations **remove it entirely**. A mature lifecycle policy almost always uses both together: transition current versions down the cost ladder while they're still "current," and aggressively expire non-current versions and abandoned multipart uploads that serve no ongoing purpose.

<img width="1536" height="1024" alt="S3LCR3" src="https://github.com/user-attachments/assets/ef402870-fbcf-4bd6-8507-69bb1bc73e43" />


---

Absolutely. The easiest way to understand **S3 Lifecycle actions** is to imagine that your bucket contains real objects and, for some objects, multiple versions.

> Assume bucket: `my-images`
>
> Objects:
> `photo.jpg`, `report.pdf`, `video.mp4`
>
> And assume **S3 Versioning is enabled** where relevant.

---

# S3 Lifecycle Rule Actions

There are **6 different actions**. They operate on either the **current version**, **noncurrent versions**, or special S3 objects such as delete markers and incomplete multipart uploads.

![Image](https://images.openai.com/static-rsc-4/GpCnTmQ_GCyXqILsespLeHfHYNL3OOh-R-n5OJZ863yQ5iqXM2h63IISzuxwzgi0cdbsrp9LgwE2eW4oG3O0jc3b9qlc7mKXIwVycAHIJwDFIJTsLaw6VfA3hs_QxuZkEZ5O8wQjw-YBI3fvitFfuqZ4Yy1YRNep4j8bAzJpYlFlSS5f0SzED9uOjw0oKT6y?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/cRILj4rrhnUTzUYiL4B-5b3P7yUTinUd7Ysg1JgWm6CLcgmrDunQRlrDH7u9uNsC5uEqXhH90Og659ByrZCOMUlnTwGB8WSubRTfZzSm_sQtQa4fD8X7fPqT34KeqMor3NkPHC_nanzG2y2IxXo5QF4mUooHrWxBsUpG9WmLKQee41PSMp3xDVGUfMXcrpUt?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/JDhXYpT0mrWF_AV_QhOQ-DeT72cZTRoGEg_HVqkVr4zEy_BjxOBNlMwk8QwNCsZpwpjaCIXnLsC3FhZoJ_m2lNLWARip-42rNwIo2jkEBMIPG4Y0XNuCQBSzs0p22hZFOsElZ5soDIzmcfvtmHnirFKJMkRXU7N-5RtyjvrLeJEcuM7qMqfbM9SxOkz173lx?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/GiQYdJ2cM4HNBwuZXpylqNPwYr-H-YTxGCRus1YlADrcujpjTqt1JEg4h91gfnpjuhTwCvyQqQFjX08K9L6fOWcLW8D_BsQmBfKQxgoQBLV_cZR-yOfyuIJ9VSGfOcZbmZVLZkiEe9Kp_A4EQA4HaHfJl2iTZMf2xoAKkgVXYYulguDuhyG77hXMXymVllEl?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/SxvEhHddjnR5bIcmxpOCZ2LQslT6kFgGdJXiVSr1lTfb-JvdHvJsRPeXzGVQr4p2nXVyO71BtBRsM-Uxi1QZOwNkykLk0oAelb0YlTNY1NBD3mj47XI29cKbhX3nALxMSj5ZX-ZVio6TGzF9W2KNg5NcsWWwUI291nugWI-xhLqpKnhDDsiYgTMENts4ZD9F?purpose=fullsize)

---

## 1. Transition current versions of objects between storage classes

### Meaning

Move the **current version** of an object to a cheaper S3 storage class after a certain number of days.

For example:

```text
Day 0
photo.jpg
   ↓
S3 Standard

Day 30
photo.jpg
   ↓
S3 Standard-IA

Day 90
photo.jpg
   ↓
S3 Glacier Instant Retrieval
```

### Demo

Suppose:

```text
my-images/
└── photo.jpg
```

Uploaded on:

```text
January 1
```

Lifecycle rule:

```text
After 30 days → Standard-IA
After 90 days → Glacier Instant Retrieval
```

Timeline:

```text
Jan 1
│
│  photo.jpg
│  STANDARD
│
├── Day 30
│
│  photo.jpg
│  STANDARD-IA
│
└── Day 90
   │
   │  photo.jpg
   │  GLACIER INSTANT RETRIEVAL
```

The object **still exists**. Only its storage class changes.

### Important

This action applies to the **current version**.

---

# 2. Transition noncurrent versions of objects between storage classes

This requires **S3 Versioning**.

Imagine:

```text
photo.jpg
```

Initially:

```text
Version 1
photo.jpg
```

Then you upload a new `photo.jpg`:

```text
Version 2 ← CURRENT
Version 1 ← NONCURRENT
```

Now you can tell S3:

> Move noncurrent versions to a cheaper storage class.

Example:

```text
After 30 days of being noncurrent
        ↓
Standard-IA

After 90 days of being noncurrent
        ↓
Glacier
```

### Timeline

```text
Day 0

photo.jpg
└── v1 CURRENT
```

Then on Day 10:

```text
photo.jpg
├── v2 CURRENT
└── v1 NONCURRENT
```

After another 30 days:

```text
photo.jpg
├── v2 CURRENT → STANDARD
└── v1 NONCURRENT → STANDARD-IA
```

After another period:

```text
photo.jpg
├── v2 CURRENT → STANDARD
└── v1 NONCURRENT → GLACIER
```

### Key point

**Noncurrent does NOT mean deleted.**

It means:

> An older version that is no longer the current version.

---

# 3. Expire current versions of objects

This one is slightly confusing because of **S3 Versioning**.

Suppose:

```text
logs/
└── application.log
```

Lifecycle rule:

```text
Expire current objects after 30 days
```

For a **non-versioned bucket**, this essentially means:

```text
Day 0
application.log
       ↓
Day 30
DELETED
```

But with **Versioning enabled**, S3 doesn't simply erase the underlying version.

Instead, S3 creates a **delete marker**.

Example:

Before expiration:

```text
application.log

v3 ← CURRENT
v2
v1
```

Lifecycle expiration happens:

```text
application.log

DELETE MARKER ← CURRENT
v3
v2
v1
```

Now if you access:

```text
GET application.log
```

S3 behaves as though the object doesn't exist because the delete marker is current.

But:

```text
v3
v2
v1
```

can still physically exist.

That's why you often combine:

```text
Expire current versions
+
Permanently delete noncurrent versions
```

---

# 4. Permanently delete noncurrent versions

This is where you actually clean up old versions.

Suppose:

```text
photo.jpg

v4 ← CURRENT
v3
v2
v1
```

You configure:

```text
Permanently delete noncurrent versions
after 30 days
```

S3 looks at **how long each version has been noncurrent**.

Example:

```text
v4 → CURRENT

v3 → noncurrent for 10 days
v2 → noncurrent for 35 days
v1 → noncurrent for 90 days
```

Rule:

```text
Delete noncurrent versions
after 30 days
```

Result:

```text
v4 ← CURRENT
v3 ← NONCURRENT (10 days) → KEEP
v2 ← NONCURRENT (35 days) → DELETE
v1 ← NONCURRENT (90 days) → DELETE
```

So:

```text
BEFORE

v4
v3
v2
v1

       ↓ Lifecycle

AFTER

v4
v3
```

### Important distinction

This:

**Expire current version**

is about the current version becoming expired.

Whereas:

**Permanently delete noncurrent versions**

actually removes old versions.

---

# 5. Delete expired object delete markers

This applies to **versioned buckets**.

Let's build the scenario.

Initially:

```text
photo.jpg

v2 ← CURRENT
v1
```

Someone deletes `photo.jpg`.

S3 creates:

```text
photo.jpg

DELETE MARKER ← CURRENT
v2
v1
```

The object appears deleted to normal GET requests.

But the delete marker itself is an S3 versioning artifact.

You can configure lifecycle to remove **expired object delete markers**.

Then:

```text
DELETE MARKER
     ↓
removed
```

### Why is this useful?

Imagine your bucket has millions of deleted objects:

```text
DELETE MARKER
DELETE MARKER
DELETE MARKER
DELETE MARKER
...
```

Lifecycle can clean them up when there are no remaining object versions associated with them.

---

# 6. Delete incomplete multipart uploads

This is different from normal objects.

Suppose you're uploading a huge:

```text
video.mp4
```

using **Multipart Upload**.

Instead of uploading one giant file:

```text
video.mp4
     ↓
Part 1
Part 2
Part 3
Part 4
...
Part 100
```

S3 stores the uploaded parts temporarily until the multipart upload is completed.

But imagine:

```text
Part 1 ✓
Part 2 ✓
Part 3 ✓
Part 4 ✓

❌ Application crashes
❌ Upload never completed
```

Now you have an **incomplete multipart upload**.

The object itself hasn't been successfully created.

But the uploaded parts can consume storage.

So configure:

```text
Delete incomplete multipart uploads
after 7 days
```

Timeline:

```text
Day 0
Upload starts

        Part 1
        Part 2
        Part 3
        Part 4

Day 1
Application crashes

        ↓

Incomplete multipart upload
        ↓
still consuming storage

Day 7
        ↓
S3 deletes incomplete parts
```

### Very important

This does **NOT** mean:

```text
photo.jpg
     ↓
delete after 7 days
```

It specifically means:

```text
Multipart upload started
        ↓
Never completed
        ↓
Delete uploaded parts
```

---

# Now let's put all 6 together

Imagine your S3 bucket:

```text
my-bucket
│
├── images/
│   ├── photo1.jpg
│   └── photo2.jpg
│
├── documents/
│   └── report.pdf
│
└── videos/
    └── movie.mp4
```

Versioning is enabled.

You could create this lifecycle policy:

| Lifecycle action                        | Example rule                                |
| --------------------------------------- | ------------------------------------------- |
| **Transition current versions**         | Standard → Standard-IA after 30 days        |
| **Transition noncurrent versions**      | Noncurrent → Glacier after 60 days          |
| **Expire current versions**             | Expire objects after 365 days               |
| **Delete noncurrent versions**          | Permanently delete after 90 days noncurrent |
| **Delete expired delete markers**       | Remove unnecessary delete markers           |
| **Delete incomplete multipart uploads** | Delete after 7 days                         |

---

# The easiest way to remember

Think of an S3 object as having **three different things that lifecycle can deal with**:

```text
                 S3 BUCKET
                    │
       ┌────────────┼─────────────┐
       │            │             │
       ▼            ▼             ▼
 CURRENT       NONCURRENT     SPECIAL
 VERSION        VERSIONS      CLEANUP
       │            │             │
       │            │             ├─ Delete markers
       │            │             │
       │            │             └─ Incomplete
       │            │                multipart uploads
       │            │
       ▼            ▼
 Transition      Transition
 Expire          Permanently delete
```

### In one sentence each:

**1. Transition current versions**

> Move the **currently active object** to a cheaper storage class.

**2. Transition noncurrent versions**

> Move **old versions** to a cheaper storage class.

**3. Expire current versions**

> Make the **current object expire**; in a versioned bucket this results in a delete marker.

**4. Permanently delete noncurrent versions**

> Actually **remove old versions** from S3.

**5. Delete expired object delete markers**

> Clean up **delete markers** that no longer need to exist.

**6. Delete incomplete multipart uploads**

> Remove **unfinished multipart-upload parts** that are consuming storage.

### One important exam/interview distinction

```text
CURRENT VERSION
      │
      ├── Transition ──→ cheaper storage class
      │
      └── Expire ──────→ object expiration

NONCURRENT VERSION
      │
      ├── Transition ──→ cheaper storage class
      │
      └── Permanently delete ──→ physically removed
```

And:

```text
Incomplete Multipart Upload
             │
             └── Delete incomplete upload parts
```

That mental model will make the S3 Lifecycle console options much easier to understand.

---

## 6. Recap

- **Expiration actions** delete current versions, non-current versions, orphaned delete markers, and abandoned multipart upload parts — the cleanup half of Lifecycle rules, complementing Note 07's transitions.
- **Non-current-version expiration is the essential pairing with versioning (Note 06)** — without it, version history can silently accumulate full-price storage costs indefinitely.
- **Aborting incomplete multipart uploads** after a set number of days is a recommended, low-effort default on any bucket accepting large uploads.
- This closes the two-part Lifecycle rule series (Notes 07-08). Next: Note 09 — Controlling Access To AWS S3 Buckets, moving from storage-cost automation to who can actually read/write this data.

### Sources
- [Expiring objects — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html#intro-lifecycle-rules-actions)
- [Setting lifecycle configuration on a bucket — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/how-to-set-lifecycle-configuration-intro.html)
- [Aborting incomplete multipart uploads — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpu-abort-incomplete-mpu-lifecycle-config.html)
