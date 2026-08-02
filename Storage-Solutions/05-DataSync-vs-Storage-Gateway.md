# 05 - AWS DataSync vs. AWS Storage Gateway

> Goal: pull the decision criteria from the [DataSync](01-AWS-DataSync.md) and [Storage Gateway](02-AWS-Storage-Gateway.md) notes into one place — the exam loves a scenario where the "correct" service depends entirely on one small detail in the wording.

---

## 1. The one-sentence distinction

- **DataSync** = **move** data from A to B (a copy job — one-time or scheduled).
- **Storage Gateway** = **be** the storage, continuously, so an application can keep reading and writing to it as if it were local.

<img width="1543" height="1023" alt="image" src="https://github.com/user-attachments/assets/86dd2e40-6cf3-49f4-86c3-83303a6b4da5" />


If the scenario is about *transferring* or *migrating* data, it's DataSync. If it's about an application that needs to keep *actively using* AWS-backed storage as if it were a local disk/share/tape drive, it's Storage Gateway.

---

## 2. Side-by-side

| | **AWS DataSync** | **AWS Storage Gateway** |
|---|---|---|
| **What it fundamentally does** | Copies data between two locations, verifying and retrying as needed | Presents AWS storage as a local file share, block volume, or tape library |
| **Interaction model** | You define a **Task** and run it once or on a schedule — it finishes and stops | The gateway runs **continuously**, actively serving reads/writes the whole time |
| **The application's experience** | Doesn't interact with DataSync directly — DataSync works on the files/objects, the app is usually not even running during the transfer | The application talks to the gateway **live**, exactly as if it were a normal local disk/share/tape drive |
| **Typical trigger** | "Migrate this file share into S3," "keep two locations in sync on a schedule" | "This legacy app needs a local-looking file share / block volume / tape library, but we want the data actually in AWS" |
| **Underlying protocol** | Its own managed transfer protocol, not a standard file/block protocol | Standard protocols the application already speaks — **NFS/SMB** (File Gateway), **iSCSI** (Volume Gateway, Tape Gateway) |
| **Needs an agent/appliance?** | Only when a side isn't AWS-native (on-premises, self-managed, another cloud) — see [DataSync](01-AWS-DataSync.md) Section 3 | **Always** — the gateway appliance itself *is* the product, whether VM, EC2, or hardware |

---

## 3. When they actually get used together

These two aren't mutually exclusive picks — a real migration often uses both, in sequence:

1. **Storage Gateway (File Gateway)** first, to let a legacy on-premises application keep working unmodified against what looks like a local file share, while its data actually accumulates in S3 in the background — no disruption, no rewrite.
2. Later, once the data already lives in S3 and any downstream migration/consolidation is needed (say, moving it into a different bucket, account, or Region as part of a broader project), **DataSync** handles that S3-to-S3 movement — the exact agentless case from [DataSync](01-AWS-DataSync.md) Section 3.

> 🎯 **Exam tip**: watch for "one-time migration" vs. "ongoing, live storage" language. "We need to migrate 50 TB from our file server into S3" → DataSync. "Our backup software needs to keep writing to tape drives, but we don't want physical tape infrastructure anymore" → Storage Gateway (Tape Gateway specifically). "Our NFS-dependent legacy app can't be rewritten, but we want its data in S3" → Storage Gateway (File Gateway).

---

## 4. Recap

- **DataSync** = a transfer job that starts, runs, and finishes (or repeats on a schedule).
- **Storage Gateway** = a continuously running appliance an application actively depends on, presenting AWS storage as something locally familiar.
- Both can use the same underlying AWS storage (S3) as their backing store — the difference is entirely about *how* an application or process interacts with that data: a finite copy operation, versus a live, ongoing local-storage illusion.
- They're often used together in a real migration: Storage Gateway to unblock a legacy app without touching it, DataSync to move the resulting data further once it's already in AWS.

### Sources
- [What is AWS DataSync? — AWS docs](https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html)
- [What is AWS Storage Gateway? — AWS docs](https://docs.aws.amazon.com/storagegateway/latest/userguide/WhatIsStorageGateway.html)
- [AWS Storage Gateway FAQs — AWS](https://aws.amazon.com/storagegateway/faqs/)
