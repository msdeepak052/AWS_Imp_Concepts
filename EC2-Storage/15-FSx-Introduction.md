# 15 - FSx Introduction

> Goal: understand where **Amazon FSx** fits next to EFS — the same "shared, managed file storage" idea from Notes 12-14, but for the workloads EFS deliberately doesn't try to serve: Windows/SMB shares, HPC/ML scratch space, and enterprise NAS feature sets. This closes out the EC2-Storage folder.

---

## 1. Why FSx exists alongside EFS

EFS is excellent, but it made one deliberate choice that rules it out for a whole category of workloads: it's **NFS-only, Linux-native**. Two real needs fall outside that:

- **Windows workloads** that need a true **SMB** share with NTFS permissions and Active Directory integration — NFS doesn't speak that language.
- **Specialized, high-performance, or enterprise-NAS-feature workloads** (HPC/ML at hundreds of GB/s, or NetApp-specific features like snapshots/cloning/deduplication) that a general-purpose NFS service isn't built to optimize for.

**Amazon FSx** is actually **four separate managed file system services** under one brand, each one a fully-managed version of a specific, well-known third-party or purpose-built file system technology — you pick the one whose native protocol and feature set matches your workload, rather than forcing every workload onto one general-purpose file system.

> 🧠 **Mental model:** if EFS is "AWS's own elastic NFS service," FSx is "AWS running the actual, familiar file system software your workload already expects" — Windows admins get real Windows Server SMB shares; HPC/ML teams get a real Lustre parallel file system; NetApp shops get a real ONTAP cluster; ZFS users get real OpenZFS — all fully managed, patched, and made highly available by AWS instead of self-hosted.

---

## 2. The four FSx file systems, at a glance

| FSx type | Native protocol(s) | Built for | Signature features |
|---|---|---|---|
| **FSx for Windows File Server** | SMB (2.0-3.1.1), NTFS | Windows-native workloads needing a real network share | Active Directory integration, NTFS ACLs, DFS Namespaces, shadow copies (previous-versions/self-service restore) |
| **FSx for Lustre** | Lustre (POSIX-like) | HPC and ML training — massively parallel, very high throughput | Hundreds of GB/s aggregate throughput, sub-millisecond latencies, native S3 import/export (a Lustre file system can be backed directly by an S3 bucket) |
| **FSx for NetApp ONTAP** | NFS (v3/v4), SMB, **iSCSI** (block) | Lift-and-shift of existing NetApp workloads; multi-protocol environments needing both NFS and SMB on the same data | NetApp's own feature set: SnapMirror replication, FlexClone instant cloning, deduplication/compression, storage-efficiency tiering |
| **FSx for OpenZFS** | NFS (v3/v4.1/v4.2) | Linux/Unix workloads wanting ZFS's specific feature set on SSD-backed low-latency storage | ZFS-native snapshots and near-instant clones, high per-operation IOPS, sub-millisecond latency |

---

## 3. What matters most for the exam

- **FSx for Windows File Server** is the answer whenever a scenario mentions **Windows**, **SMB**, or **Active Directory** integration for a shared drive — this is by far the most exam-relevant FSx type, since it's the direct Windows-equivalent of what EFS does for Linux.
- **FSx for Lustre** is the answer whenever a scenario mentions **HPC**, **machine learning training**, or extremely high aggregate throughput requirements, especially when the data set already lives in (or needs to end up back in) **S3** — Lustre's native S3 linkage is a frequently-tested detail.
- **FSx for NetApp ONTAP** and **FSx for OpenZFS** are newer, more specialized additions — good to recognize by name and headline feature (ONTAP → SnapMirror/multi-protocol NAS migration; OpenZFS → ZFS snapshots/clones), but less central to SAA-C03 than the first two.
- **Availability Zone model matters and differs by type:** FSx for Windows File Server, NetApp ONTAP, and OpenZFS all support both **Single-AZ** and **Multi-AZ** deployments (Multi-AZ gives automatic failover, the same HA instinct as everything else in this repo). **FSx for Lustre is Single-AZ only** — a detail worth remembering specifically because it's an exception to the "AWS managed service = automatically Multi-AZ" assumption many other services train you to make.

> 🎯 **Exam tip:** the fastest way to eliminate wrong FSx answers is to look for the **protocol** keyword first — "SMB"/"Active Directory" → Windows File Server; "Lustre"/"HPC"/"ML training" → Lustre; "SnapMirror"/"iSCSI"/"multi-protocol" → NetApp ONTAP; "ZFS" → OpenZFS. Don't reach for EFS at all once you see any of these Windows- or specialized-NAS-flavored keywords — EFS's NFS-only, Linux-only design is precisely why FSx exists as a separate service family.

---

## 4. FSx vs. EFS — the one-line distinction to remember

| | EFS | FSx |
|---|---|---|
| Protocol | NFS only | SMB (Windows), Lustre, NFS+SMB+iSCSI (ONTAP), or NFS (OpenZFS) — pick per workload |
| OS fit | Linux-native | Whichever OS/protocol matches the chosen FSx type — including full Windows support |
| "One size fits most" or "purpose-built"? | One general-purpose elastic NFS service | Four distinct, purpose-built managed file systems, chosen by workload |

---

## 5. Recap

- **FSx** is a family of four fully-managed, purpose-built file systems — **Windows File Server** (SMB/AD), **Lustre** (HPC/ML, S3-linked), **NetApp ONTAP** (multi-protocol, NetApp features), **OpenZFS** (ZFS features) — filling exactly the gaps EFS's Linux-only NFS design leaves open.
- For the exam, recognize each type by its protocol/keyword signature, and remember **Lustre is Single-AZ only** while the other three support Multi-AZ.
- This closes the EC2-Storage folder: **Instance Store/EBS** (Notes 02-11) cover single-instance block storage and its backup lifecycle; **EFS/FSx** (Notes 12-15) cover shared, multi-instance file storage for Linux and beyond.

### Sources
- [What is Amazon FSx? — AWS docs](https://docs.aws.amazon.com/fsx/latest/WhatIsFSx/what-is-fsx.html)
- [Amazon FSx for Windows File Server — AWS docs](https://docs.aws.amazon.com/fsx/latest/WindowsGuide/what-is.html)
- [Amazon FSx for Lustre — AWS docs](https://docs.aws.amazon.com/fsx/latest/LustreGuide/what-is.html)
- [Amazon FSx for NetApp ONTAP — AWS docs](https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/what-is-fsx-ontap.html)
- [Amazon FSx for OpenZFS — AWS docs](https://docs.aws.amazon.com/fsx/latest/OpenZFSGuide/what-is-fsx.html)
- [Help me choose an Amazon FSx file system — AWS](https://aws.amazon.com/fsx/when-to-choose-fsx/)
