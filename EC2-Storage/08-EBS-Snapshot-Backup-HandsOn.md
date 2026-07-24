# 08 - EBS Snapshot Backup (Hands-On)

> Goal: take a point-in-time snapshot of the volume from Note 07, understand what actually happens when you do (incremental, stored in S3 behind the scenes), then restore it into a brand-new volume to prove a snapshot really is a full, independent backup.

---

## 1. What an EBS snapshot actually is

- A snapshot is a **point-in-time backup of an EBS volume**, stored durably in **Amazon S3** behind the scenes (you don't see or manage the S3 bucket directly — AWS does).
- The **first snapshot** of a volume copies all used blocks. **Every snapshot after that is incremental** — it only stores the blocks that **changed** since the previous snapshot, even though each snapshot still represents the **complete volume** at that point in time when you restore it (AWS reassembles the full picture from the chain of incrementals automatically).
- Snapshots are **regional by default** but can be **copied to another Region** (Section 5) or **shared** with other AWS accounts (or made public), which is how AMIs and community datasets often get distributed.

> 🧠 **Mental model:** think of each snapshot as a "diff" layered on the one before it, the same conceptual idea as a git commit — small incremental storage cost, but each one is still a complete, independently-restorable point in time, not a fragile chain that breaks if you delete an old link (AWS manages the underlying block references so deleting an older snapshot doesn't corrupt newer ones).

---

## 2. Take a snapshot of the Note 07 volume

1. **EC2 console** → **Elastic Block Store** → **Volumes** → select the volume created in Note 07.
2. **Actions** → **Create snapshot**.
3. **Description**: `demo-volume-snapshot-1`.
4. **Create snapshot**.
5. **Elastic Block Store** → **Snapshots** — wait for **Status: Completed**.

> ⚠️ A snapshot taken while the volume is **attached and actively being written to** is still crash-consistent (AWS snapshots complete asynchronously and safely), but it is not necessarily **application-consistent** unless the application's writes were flushed/quiesced first (e.g. briefly pausing writes, or using a filesystem-freeze step) — for a real production database, tools like AWS Backup or database-native backup features coordinate this properly. This hands-on's single test file doesn't need that care, but it's worth knowing the distinction exists.

---

## 3. Make a change, then take a second (incremental) snapshot

1. Reconnect to the instance via Session Manager, remount the volume if needed, and add a second file:
   ```bash
   echo "added after the first snapshot" | sudo tee /data/test2.txt
   ```
2. Back in the console: **Actions** → **Create snapshot** again on the same volume → description `demo-volume-snapshot-2`.
3. Notice in the snapshot list that `snapshot-2` completes faster and reports a smaller incremental size than `snapshot-1` — it only had to store the blocks that changed (the new file), not the whole volume again.

---

## 4. Restore a snapshot into a brand-new volume

1. **Snapshots** → select `demo-volume-snapshot-1` → **Actions** → **Create volume from snapshot**.
2. **Volume type**: `gp3`; **Availability Zone**: same AZ as your instance (so you can attach and verify it).
3. **Create volume**.
4. Attach this new volume to the instance (same process as Note 07, Section 3), mount it at a new path (e.g. `/data-restored`), and confirm:
   ```bash
   sudo mkdir /data-restored
   sudo mount /dev/nvme2n1 /data-restored   # use whatever device name lsblk actually shows
   ls /data-restored
   ```
   You should see `test.txt` but **not** `test2.txt` — proving this volume was restored from the **first** snapshot, taken before the second file was created.

---

## 5. Copy a snapshot to another Region (disaster-recovery pattern)

1. **Snapshots** → select `demo-volume-snapshot-2` → **Actions** → **Copy snapshot**.
2. **Destination Region**: pick a different Region than the one you're working in.
3. **Copy snapshot** → switch the console to that destination Region to confirm it landed.

This is the standard pattern for cross-region disaster recovery of EBS-backed data: snapshots (and AMIs built from them) copy cleanly between Regions, letting you restore a volume in a Region that never had the original attached instance at all.

---

## 6. Clean up

- Detach and delete the restored volume from Section 4.
- Delete both snapshots (`Actions` → `Delete snapshot`) and the copied cross-region snapshot from Section 5, once you no longer need them — snapshots bill for their stored size until deleted.

---

## 7. Recap

- A snapshot is an incremental, point-in-time backup of an EBS volume, stored in S3, but each one restores to a **complete, independent** volume.
- Creating a volume **from** a snapshot is how you restore data, move data to a new AZ, or seed a brand-new volume with existing content.
- Snapshots can be **copied cross-region** — the standard building block for EBS-based disaster recovery.
- Next: Note 09 — Snapshot Use Case, covering the broader patterns (AMIs, volume migration, cross-account sharing) snapshots enable beyond simple backup/restore.

### Sources
- [Amazon EBS snapshots — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSSnapshots.html)
- [Create Amazon EBS snapshots — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-creating-snapshot.html)
- [Restore an Amazon EBS volume from a snapshot — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-restoring-volume.html)
- [Copy an Amazon EBS snapshot — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-copy-snapshot.html)
