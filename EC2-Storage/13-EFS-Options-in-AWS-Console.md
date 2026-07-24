# 13 - EFS Options in AWS Console

> Goal: walk every setting on EFS's file system creation screen, tying each console option back to the concepts from Note 12, so nothing on the "Create file system" page is a surprise before the hands-on build in Note 14.

---

## 1. Creation flow: "Customize" vs. one-click "Create"

The EFS console offers a fast path (**Create** — accepts every default) and a **Customize** path that exposes every setting below. For anything beyond a throwaway test, walk through **Customize** at least once so you know exactly what each default actually is.

---

## 2. General settings

| Setting | What it controls |
|---|---|
| **Name** | A tag, purely for your own identification in the console |
| **Storage class** (availability and durability) | **Regional** (default — multi-AZ, the standard choice) vs. **One Zone** (single-AZ, cheaper, lower availability — trades Note 12's multi-AZ redundancy for cost, useful for non-critical or easily-regenerable data) |
| **Automatic backups** | Whether AWS Backup takes automatic daily backups of this file system — recommended **on** for anything holding data you can't easily regenerate |
| **Lifecycle management** | Which storage-class transition rules to apply (Note 12, Section 6) — e.g. "transition to IA after 30 days of no access," and optionally "transition back to Standard on first access" |
| **Encryption** | Encryption at rest is **on by default**, using an AWS KMS key you choose (the account's default `aws/elasticfilesystem` key, or a custom CMK) |

---

## 3. Performance settings

Maps directly to Note 12, Sections 4-5:

- **Performance mode**: **General Purpose** (default) or **Max I/O** — locked at creation, cannot change later.
- **Throughput mode**: **Elastic** (recommended default), **Bursting**, or **Provisioned** (with a throughput value in MiB/s you set explicitly if chosen).

---

## 4. Network access — mount targets

- For each **Availability Zone** in the chosen VPC, the console lets you configure a **mount target**: pick the **subnet** and the **security group(s)** to attach to that mount target's ENI.
- The default suggestion is one mount target per AZ in the VPC — matching Note 12's "one mount target per AZ" model. You can omit an AZ if no instance there needs to mount this file system, but omitting an AZ means instances there cannot reach this file system without crossing to a mount target in a different AZ (extra latency, and depending on network ACLs/routing, possibly not reachable at all).
- **Security group** here is exactly the same chained-security-group pattern used throughout this repo: the mount target's security group must allow inbound **NFS (port 2049)** from whatever security group your EC2 instances use.

> 🎯 **Exam tip:** "EC2 instance can't mount the EFS file system" scenario questions almost always resolve to one of two causes: **(1)** the mount target's security group doesn't allow inbound port 2049 from the instance's security group, or **(2)** the instance is in a subnet/AZ that has no mount target and no route to one that does. Check these two first.

---

## 5. File system policy (optional)

- An **EFS file system policy** is a resource-based IAM policy (conceptually similar to an S3 bucket policy) that can, for example, **enforce that all clients must connect using encryption in transit** (mounting with the `tls` option), or restrict which IAM principals can perform administrative actions on the file system. Optional, but a common security hardening step for anything beyond a demo.

---

## 6. Tags

- Standard AWS resource tags — useful here specifically because DLM-style automation and cost allocation both commonly key off tags, the same pattern seen with DLM's tag-based volume targeting in Note 11.

---

## 7. Recap

- The EFS creation screen's **Customize** path exposes: storage class (Regional vs. One Zone), automatic backups, lifecycle management, encryption, performance mode, throughput mode, per-AZ mount targets (subnet + security group), an optional file system policy, and tags.
- The two settings that are **locked in at creation** and cannot change later: **performance mode** and (implicitly) the **storage class** choice of Regional vs. One Zone.
- Most "can't mount EFS" troubleshooting comes down to mount-target security groups or missing mount targets in the instance's AZ.
- Next: Note 14 — EFS (Hands-On), actually creating a file system and mounting it from two instances in two different AZs.

### Sources
- [Creating and configuring Amazon EFS file systems — AWS docs](https://docs.aws.amazon.com/efs/latest/ug/creating-using-create-fs.html)
- [Amazon EFS mount targets and security groups — AWS docs](https://docs.aws.amazon.com/efs/latest/ug/accessing-fs.html)
- [Amazon EFS file system policies — AWS docs](https://docs.aws.amazon.com/efs/latest/ug/access-control-overview.html)
- [Amazon EFS One Zone storage classes — AWS docs](https://docs.aws.amazon.com/efs/latest/ug/storage-classes.html)
