# 10 - Fast Snapshot Restore (Hands-On)

> Goal: understand the "lazy loading" problem a freshly-restored volume normally has, then enable **Fast Snapshot Restore (FSR)** on a snapshot and see how it removes that problem entirely.

---

## 1. The problem: lazy loading on a normal restore

When you create a volume from a snapshot (Note 08, Section 4) **without** FSR, the new volume is available for I/O **immediately** — but under the hood, its data is still being pulled in from S3 lazily, in the background, the first time each block is actually read.

- The **first read** of any given block on a freshly-restored volume incurs extra latency (AWS has to fetch that block from S3 behind the scenes) — this is called a **volume warm-up** period.
- Reads of blocks that have already been fetched once are fast from then on, same as any normal EBS volume.
- For a large volume, or a workload that immediately needs consistently fast reads across the whole disk (e.g. a database restarting and reading broadly across its data files right away), this warm-up latency can be a real, user-visible problem.

> 🧠 **Mental model:** a normal restore is like moving into a new house where all your boxes are still in a storage unit down the street — the house is livable immediately, but the first time you need something from a specific box, someone has to go fetch it, which takes a moment. FSR is paying to have every box already unpacked and put away before you move in.

---

## 2. What Fast Snapshot Restore does

**Fast Snapshot Restore (FSR)** pre-initializes every block of a snapshot **in a specific Availability Zone**, ahead of time, so that any volume created from that snapshot (in that AZ) is **fully initialized from the first I/O** — no lazy-loading warm-up latency at all, even on the very first read of any block.

- Enabled **per snapshot, per Availability Zone** — you choose exactly which AZs need this treatment (typically the AZs where you actually expect to restore volumes from this snapshot).
- Supports up to **50 snapshots per Region** with FSR enabled at a time (a soft limit, can be raised via a support request).
- **Billed hourly per snapshot per AZ** it's enabled in, regardless of whether you actually restore a volume from it during that time — this is a real, ongoing cost, not a one-time fee.

---

## 3. Enable FSR on a snapshot

1. **EC2 console** → **Elastic Block Store** → **Snapshots** → select an existing snapshot (e.g. `demo-volume-snapshot-2` from Note 08).
2. **Actions** → **Manage Fast Snapshot Restore**.
3. **Enable Fast Snapshot Restore** → select the Availability Zone(s) where you expect to restore volumes from this snapshot (e.g. `ap-south-1a`).
4. **Save**.
5. Wait for the **Fast snapshot restore state** column to show **Enabled** (this itself can take some minutes — the pre-initialization work has to actually finish before the benefit applies).

---

## 4. Create a volume and observe the difference

1. Once FSR shows **Enabled** for your chosen AZ, create a new volume from that snapshot in that same AZ (**Actions** → **Create volume from snapshot**, same as Note 08, Section 4).
2. Attach and mount it as before.
3. Every block you read — even ones you've never touched before — comes back at full EBS performance immediately, with no warm-up delay, because FSR already did that work ahead of time for this AZ.

> ⚠️ FSR is scoped to the **exact AZ** you enabled it in. If you create a volume from the same snapshot in a *different* AZ that doesn't have FSR enabled, that volume goes through the normal lazy-loading warm-up — FSR does not implicitly cover every AZ, only the ones you explicitly selected.

---

## 5. When FSR is actually worth the cost

| Scenario | Worth enabling FSR? |
|---|---|
| Restoring a large production database volume that must be at full performance the instant it's attached (e.g. disaster recovery drills, frequent test-environment refreshes from a prod snapshot) | ✅ Yes |
| A one-off, rarely-restored backup snapshot kept "just in case" | ❌ No — paying an hourly per-AZ fee for a restore that might never happen (or happen once a year) isn't worth it |
| A snapshot used as the golden image for frequently-launched dev/test environments where restore speed matters every time | ✅ Yes |

---

## 6. Clean up

- **Manage Fast Snapshot Restore** on the snapshot → disable it for the AZ(s) you enabled, once you're done testing, to stop the hourly charge.
- Detach and delete the volume created in Section 4 if no longer needed.

---

## 7. Recap

- A volume restored from a snapshot without FSR is usable immediately, but individual blocks incur extra latency on their **first** read (lazy loading from S3) until "warmed up."
- **Fast Snapshot Restore** pre-initializes a snapshot's data in a chosen AZ so restored volumes are at full performance from the very first I/O — enabled per snapshot, per AZ, billed hourly while enabled.
- Best reserved for frequently-restored, performance-sensitive snapshots (DR drills, frequently-refreshed test environments), not for rarely-touched long-term backups.
- Next: Note 11 — Data Lifecycle Manager, automating snapshot creation, retention, and cleanup instead of doing it by hand.

### Sources
- [Amazon EBS fast snapshot restore — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-fast-snapshot-restore.html)
- [Amazon EBS snapshots — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSSnapshots.html)
