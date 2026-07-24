# 14 - EFS (Hands-On)

> Goal: create a real EFS file system, mount it from two EC2 instances in two different Availability Zones, and prove a file written by one instance is instantly visible to the other — the concrete demonstration of Note 12's "many instances, same files, at the same time" claim.

---

## 1. Prerequisites

- Two running EC2 instances (Amazon Linux 2023), in **two different Availability Zones**, in the **same VPC**, both reachable via Session Manager.
- Both instances' security group must allow whatever you'll assign as the EFS mount targets' inbound rule (Section 3 creates a dedicated security group for this).

---

## 2. Create the EFS security group first

1. **EC2 console** → **Security Groups** → **Create security group**.
2. **Name**: `demo-efs-sg`.
3. **Inbound rules**: Type **NFS**, Port `2049`, **Source**: the security group your two EC2 instances use (chained security-group pattern, same as the rest of this repo — never a broad CIDR for this).
4. **Create security group**.

---

## 3. Create the EFS file system

1. **EFS console** → **File systems** → **Create file system** → **Customize**.
2. **Name**: `demo-efs`.
3. **Storage class**: **Regional** (multi-AZ, the default recommended choice per Note 12/13).
4. **Lifecycle management**: enable "Transition into IA" after 30 days (optional for this exercise, but worth seeing in the console).
5. **Performance mode**: General Purpose. **Throughput mode**: Elastic.
6. **Network settings**: for each AZ your two instances are in, confirm a mount target is created, and set its security group to `demo-efs-sg` (replacing the default VPC security group).
7. **Create**.

---

## 4. Mount the file system from both instances

1. On the EFS console, select `demo-efs` → **Attach** → copy the NFS mount command shown (it includes the correct DNS name and mount options).
2. Connect to **instance 1** via Session Manager:
   ```bash
   sudo yum install -y amazon-efs-utils
   sudo mkdir /efs-data
   sudo mount -t efs demo-efs:/ /efs-data
   ```
3. Connect to **instance 2** (in the other AZ) via Session Manager and repeat the exact same three commands.

> 🧠 Note that both instances mount the exact same file system ID (`demo-efs`), but each one connects through the mount target **in its own AZ** — this is the "one mount target per AZ, but one shared file system" model from Note 12 playing out for real.

---

## 5. Prove the shared-write behavior

1. On **instance 1**:
   ```bash
   echo "written from instance 1" | sudo tee /efs-data/shared.txt
   ```
2. On **instance 2**, immediately:
   ```bash
   cat /efs-data/shared.txt
   ```
   You should see the exact text instance 1 just wrote — with no copy step, no sync job, no S3 upload/download in between. Both instances are reading and writing the **same underlying file system**, live.
3. For contrast with Note 07's EBS hands-on: an EBS volume mounted the same way could never do this — it would need to be detached from one instance and reattached to the other, and even then only one instance could use it at a time (Multi-Attach aside, and even that needs cluster-aware software, not a plain mount).

---

## 6. Confirm elastic growth (no capacity planning needed)

1. On either instance, write a larger file:
   ```bash
   dd if=/dev/zero of=/efs-data/bigfile bs=1M count=500
   ```
2. **EFS console** → `demo-efs` → check the **Size** metric — it grows to reflect the new data automatically. There was no volume size to provision ahead of time, unlike every EBS example in this folder.

---

## 7. Clean up

1. On both instances: `sudo umount /efs-data`.
2. **EFS console** → `demo-efs` → **Delete** (this also removes its mount targets).
3. Delete `demo-efs-sg` once no longer referenced.

---

## 8. Troubleshooting

| Symptom | Likely cause |
|---|---|
| `mount` hangs or times out | `demo-efs-sg` doesn't allow inbound NFS (port 2049) from the instance's security group — the single most common EFS mounting failure |
| `mount.efs` command not found | `amazon-efs-utils` wasn't installed first (Section 4, step 2) |
| Instance in a third AZ can't mount at all | No mount target exists in that AZ — go back to Section 3, step 6 and add one |
| File written on one instance isn't visible on the other | Both instances must mount the **same** file system ID — double-check for a typo pointing at a different file system, or a stale/cached directory listing (re-`ls` the directory) |

---

## 9. Recap

- Created one EFS file system with mount targets in two AZs, protected by a dedicated NFS security group following this repo's chained-SG convention.
- Mounted the same file system from two instances in two different AZs and proved a write from one is instantly visible from the other — the defining EFS capability that no single EBS volume can offer.
- Confirmed EFS grows automatically with no pre-provisioned capacity, unlike every EBS volume type in this folder.
- Next: Note 15 — FSx Introduction, covering the managed, purpose-built file systems (Windows, Lustre, ONTAP, OpenZFS) that exist alongside EFS for workloads EFS doesn't fit (Windows/SMB, HPC, enterprise NAS features).

### Sources
- [Creating and configuring Amazon EFS file systems — AWS docs](https://docs.aws.amazon.com/efs/latest/ug/creating-using-create-fs.html)
- [Mounting Amazon EFS file systems — AWS docs](https://docs.aws.amazon.com/efs/latest/ug/mounting-fs.html)
- [Amazon EFS security — network access — AWS docs](https://docs.aws.amazon.com/efs/latest/ug/network-access.html)
