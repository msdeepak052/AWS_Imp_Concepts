# 09 - Snapshot Use Case

> Goal: go beyond "snapshots are backups" and cover the concrete architectural patterns snapshots enable — the ones the exam actually builds scenario questions around.

---

## 1. Backup and restore (the baseline use case)

Already hands-on in Note 08: take periodic snapshots of a volume, restore into a new volume if the original is lost, corrupted, or needs to be rolled back to an earlier point in time. This alone justifies a snapshot schedule for any EBS volume holding data you can't easily regenerate — which is exactly why Note 11 (Data Lifecycle Manager) exists, to automate this instead of doing it by hand.

---

## 2. Migrating a volume across Availability Zones

An EBS volume is **locked to the AZ it was created in** — it cannot be attached to an instance in a different AZ directly. Snapshots solve this: a snapshot is **regional**, not AZ-specific, so you can:

1. Snapshot a volume in `ap-south-1a`.
2. Create a new volume from that snapshot, choosing `ap-south-1b` this time.
3. Attach the new volume to an instance in `ap-south-1b`.

> 🎯 **Exam tip:** "move data from one AZ to another" is one of the most reliable snapshot-scenario signals — the answer is almost always "snapshot the volume, then create a new volume from that snapshot in the target AZ," since there's no direct cross-AZ attach operation for EBS volumes.

---

## 3. Migrating a volume across Regions

Same idea, one level up: snapshots can be **copied to a different Region** (Note 08, Section 5), then used to create a volume there. This is the standard mechanism for:

- **Disaster recovery** — keeping a standby copy of critical data in a second Region.
- **Expanding an application to a new Region** — seeding a new Region's environment with existing data.

---

## 4. Changing volume type, size, or encryption status

Some volume properties can be changed live via **Modify Volume** (Note 07), but others — most notably **enabling encryption on a previously-unencrypted volume**, since encryption cannot be toggled on an existing volume in place — require the snapshot path instead:

1. Snapshot the unencrypted volume.
2. Copy the snapshot, choosing **encryption** during the copy step (this is the one point where an unencrypted snapshot can become an encrypted one).
3. Create a new volume from the now-encrypted snapshot copy.
4. Swap the new encrypted volume in for the old one (detach old, attach new).

> ⚠️ You cannot encrypt an existing volume or snapshot in place — encryption status is set at creation time. Going from unencrypted to encrypted always requires this **copy-with-encryption** snapshot step.

---

## 5. Creating an Amazon Machine Image (AMI)

An AMI's root volume is, under the hood, backed by a snapshot. When you create an AMI from a running instance, AWS snapshots its root volume (and any other attached EBS volumes included in the AMI) automatically — this is exactly how the "Customize AMI" workflow referenced elsewhere in this repo's `EC2/General-EC2` folder works. Launching new instances from that AMI creates new volumes from that underlying snapshot, giving every instance an identical starting disk state.

---

## 6. Sharing data across accounts, or publicly

A snapshot can be **shared with specific AWS account IDs**, or made **public**, without ever moving or duplicating the underlying data until someone actually creates a volume from it. This is how:

- A vendor might distribute a pre-built dataset or software image to customers.
- Separate environments (e.g. a security/audit account) can be given read access to a production volume's point-in-time contents without touching the live volume itself.

> 🧠 **Mental model:** sharing a snapshot is like sharing a link to a file, not emailing the file itself — no data actually moves until the recipient acts on it (creates their own volume from it).

---

## 7. Recap

- Beyond simple backup/restore, snapshots are the mechanism for: **cross-AZ volume migration**, **cross-Region migration/DR**, **enabling encryption on a previously-unencrypted volume**, **building AMIs**, and **sharing data across accounts** (or publicly).
- The recurring pattern underneath almost all of these: snapshots are **regional**, not tied to a single AZ or a single account, which is exactly what an AZ-locked EBS volume itself cannot do on its own.
- Next: Note 10 — Fast Snapshot Restore (Hands-On), removing the "first-read latency" that a freshly-restored volume would otherwise have.

### Sources
- [Amazon EBS snapshots — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSSnapshots.html)
- [Create an Amazon EBS-backed AMI — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/creating-an-ami-ebs.html)
- [Amazon EBS encryption — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html)
- [Share an Amazon EBS snapshot — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-modifying-snapshot-permissions.html)
