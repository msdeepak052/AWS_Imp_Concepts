# 17 - FSx for NetApp ONTAP (Hands-On)

> Goal: build a real FSx for ONTAP file system using the console's **Quick create** path, see the SVM and volume it creates automatically, then mount that volume over NFS from an EC2 instance — the concrete version of [FSx for NetApp ONTAP](16-FSx-for-NetApp-ONTAP.md)'s file system → SVM → volume hierarchy.

---

## 1. Prerequisites

- One running EC2 instance (Amazon Linux 2023), reachable via Session Manager, in the VPC you'll create the file system in.
- That instance's security group will need inbound NFS access from FSx — Section 3 creates a dedicated security group for this, same chained-SG pattern as the [EFS hands-on](14-EFS-HandsOn.md).

---

## 2. Create the security group first

1. **EC2 console** → **Security Groups** → **Create security group**.
2. **Name**: `demo-ontap-sg`.
3. **Inbound rules**: allow the following from your EC2 instance's own security group (chained-SG pattern, not a broad CIDR):
   - **NFS**, port `2049`
   - **TCP** `111` and **UDP** `111` (NFS's portmapper)
   - **TCP** `635` and **UDP** `635` (NFS lock manager)
   - (Optional, only if you'll test SMB/iSCSI later) **SMB** `445`, **iSCSI** `3260`
4. **Create security group**.

---

## 3. Create the file system — Quick create

1. **FSx console** → **Create file system**.
2. **Select file system type**: **Amazon FSx for NetApp ONTAP** → **Next**.
3. **Creation method**: **Quick create** (this is what auto-generates the first SVM and volume for you).
4. **File system name**: `demo-ontap`.
5. **Deployment type**: **Single-AZ** (cheapest option for this demo — Multi-AZ is the same idea as everywhere else in this repo: replication + automatic failover, at extra cost).
6. **SSD storage capacity**: `1024` GiB (the minimum).
7. **Throughput capacity**: leave the recommended default.
8. **VPC**: your VPC → **Subnet**: pick one → **Security group**: `demo-ontap-sg`.
9. **Storage efficiency**: **Enabled** (turns on ONTAP's own compression/deduplication/compaction — worth seeing on by default).
10. **Next** → review → **Create file system**.

**Quick create** automatically produces one SVM named `fsx` and one volume named `vol1`, with junction path `/vol1` — this is exactly [FSx for NetApp ONTAP](16-FSx-for-NetApp-ONTAP.md)'s hierarchy, just built for you in one step instead of three.

---

## 4. Find the volume's mount details

1. **FSx console** → **Storage virtual machines** → `fsx` → **Endpoints** panel → copy the **NFS DNS name**.
2. **Volumes** → `vol1` → **Summary** panel → confirm the **Junction path** (`/vol1`).

---

## 5. Mount from the EC2 instance

Connect via **Session Manager**, then:

```bash
sudo mkdir /ontap-data
sudo mount -t nfs -o nfsvers=4.1 <nfs-dns-name>:/vol1 /ontap-data
```

Confirm it mounted:

```bash
df -h /ontap-data
echo "hello from FSx for ONTAP" | sudo tee /ontap-data/hello.txt
cat /ontap-data/hello.txt
```

---

## 6. See a storage-efficiency feature in action: a FlexClone-style snapshot

FSx for ONTAP assigns a **default snapshot policy** to `vol1` automatically. Take a manual one to see the mechanism:

1. **FSx console** → **Volumes** → `vol1` → **Snapshots** tab → **Create snapshot**.
2. Name it `demo-snapshot-1` → **Create**.
3. Write a new file, then delete it:
   ```bash
   echo "this will be deleted" | sudo tee /ontap-data/temp.txt
   sudo rm /ontap-data/temp.txt
   ```
4. Browse the snapshot's contents from the **Snapshots** tab (or via the volume's hidden `.snapshot` directory on some clients) — `temp.txt` still exists inside the snapshot, even though it's gone from the live volume. This is the same point-in-time-recovery idea as an [EBS snapshot](08-EBS-Snapshot-Backup-HandsOn.md) or an EFS backup, just implemented with ONTAP's own native snapshot technology instead.

---

## 7. (Optional) Add a second, Active-Directory-joined SVM for SMB

This mirrors [FSx for NetApp ONTAP](16-FSx-for-NetApp-ONTAP.md) Section 2's "multiple SVMs on one file system" point — skip this if you don't have an Active Directory set up yet ([Active Directory for FSx](21-Active-Directory-for-FSx.md) covers building one for the FSx for Windows File Server hands-on, and it works identically here).

1. **FSx console** → **Storage virtual machines** → **Create storage virtual machine**.
2. **File system**: `demo-ontap`.
3. **Storage virtual machine name**: `demo-ontap-smb`.
4. **Microsoft Active Directory configuration**: **Join a Microsoft Active Directory**.
5. **Domain join service account credentials**: **Managed in Secrets Manager** → select or create the secret holding your AD service account credentials.
6. Fill in the remaining AD fields (domain name, DNS IPs, organizational unit) → **Create storage virtual machine**.

Once joined, this second SVM can host its own volumes shared over **SMB** to Windows clients — the same underlying file system, now serving both protocols from separate SVMs.

---

## 8. Clean up

1. On the EC2 instance: `sudo umount /ontap-data`.
2. **FSx console** → **Volumes** → delete any non-root volumes you created.
3. **Storage virtual machines** → delete any SVMs you created (the default `fsx` SVM's root volume goes with it).
4. **File systems** → `demo-ontap` → **Actions** → **Delete file system** (choose whether to keep a final backup).
5. Delete `demo-ontap-sg` once nothing references it.

---

## 9. Troubleshooting

| Symptom | Likely cause |
|---|---|
| `mount` hangs or times out | `demo-ontap-sg` is missing one of the NFS-related ports (2049, 111 tcp/udp, 635 tcp/udp) from the EC2 instance's security group |
| `mount.nfs: Protocol not supported` | Wrong `nfsvers` value — FSx for ONTAP supports 3, 4.0, 4.1, 4.2; double-check the version you passed matches what's enabled |
| Can't find the NFS DNS name | It belongs to the **SVM**, not the file system — look under **Storage virtual machines** → your SVM → **Endpoints**, not the file system's own overview page |
| Second SVM creation fails at the AD step | Confirm the Secrets Manager secret actually contains valid AD service-account credentials, and that `demo-ontap-sg` (or the AD's own security group) allows the necessary AD ports between the file system's subnet and the domain controllers |

---

## 10. Recap

- Built `demo-ontap` via **Quick create**, which auto-generated an SVM (`fsx`) and a volume (`vol1`, junction path `/vol1`) in one step.
- Mounted the volume over **NFS** from an EC2 instance, exactly like the [EFS hands-on](14-EFS-HandsOn.md)'s mount — but this time backed by real ONTAP.
- Took a manual snapshot and confirmed a deleted file was still recoverable from it — ONTAP's native snapshot technology, the foundation SnapMirror and FlexClone build on.
- (Optional) Added a second, AD-joined SVM — the concrete version of "one file system, multiple SVMs, multiple protocols" from [FSx for NetApp ONTAP](16-FSx-for-NetApp-ONTAP.md).
- Next: [FSx for OpenZFS](18-FSx-for-OpenZFS.md) — a different specialized FSx type, this time built around ZFS's snapshot/clone model instead of ONTAP's.

### Sources
- [Getting started with Amazon FSx for NetApp ONTAP — AWS docs](https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/getting-started.html)
- [Managing SVMs — AWS docs](https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/managing-svms.html)
- [Managing volumes — AWS docs](https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/managing-volumes.html)
- [Working with snapshots — AWS docs](https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/snapshots-ontap.html)
- [File system access control with Amazon VPC — AWS docs](https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/limit-access-security-groups.html)
