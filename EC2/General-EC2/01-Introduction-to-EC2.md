# 01 - Introduction to Elastic Compute Cloud (EC2)

> Goal of this note: understand **what EC2 is, why it exists, and the core building blocks** you will use in every later topic. No hands-on yet — this is the foundation.

---

## 1. What is EC2 in one line?

**Amazon EC2 (Elastic Compute Cloud)** is a web service that lets you **rent virtual servers (called "instances") in AWS data centers** and pay only for what you use.

Think of it as renting a computer in the cloud instead of buying a physical one and keeping it in your office.

- **Elastic** → you can scale up/down (add or remove servers) in minutes.
- **Compute** → it provides CPU + RAM + storage + networking, i.e. a full computer.
- **Cloud** → it runs on AWS-managed hardware, accessible over the internet.

---

## 2. Why was EC2 created? (The problem it solves)

**Traditional (on-premises) way:**
1. Estimate how many servers you need.
2. Buy physical servers (huge upfront cost).
3. Wait weeks for delivery + setup.
4. Pay for power, cooling, a data center, and staff.
5. If traffic spikes, you run out of capacity. If traffic drops, you wasted money.

**The EC2 (cloud) way:**
1. Click a few buttons (or run one command).
2. A server is ready in ~1 minute.
3. Pay per second/hour only while it runs.
4. Turn it off when not needed → stop paying.
5. Need 100 servers for an hour? Launch them, then terminate. Only pay for that hour.

This shift is called moving from **CapEx (capital expense)** to **OpEx (operational expense)**.

---

## 3. The core building blocks of an EC2 instance

When you launch an instance, you are really choosing a combination of these pieces. Each has its own dedicated note later — here is the big picture:

| Building block | What it decides | Covered in |
|---|---|---|
| **AMI (Amazon Machine Image)** | The OS + pre-installed software (the "template") | Note 05–06 |
| **Instance Type** | How much CPU / RAM / network the server has | Note 07 |
| **Network (VPC / Subnet / AZ)** | Where the server lives in AWS | Note 08, 09 |
| **Key Pair** | The SSH/RDP login credentials | Note 02–04 |
| **Security Group** | The virtual firewall (what traffic is allowed) | Note 11–14 |
| **Storage (EBS volume)** | The virtual hard disk attached to the server | (later sections) |
| **User Data** | A startup script that runs on first boot | Note 15 |
| **Purchase Option** | How you pay (On-Demand, Spot, Reserved…) | Note 19–21 |

> 🧠 **Mental model:** An EC2 instance = **AMI (software)** running on an **Instance Type (hardware)**, placed in a **Subnet/AZ (location)**, protected by a **Security Group (firewall)**, with an **EBS volume (disk)**, that you log in to with a **Key Pair**.

---

## 4. Key terms you must know from day 1

- **Instance** → a single running virtual server.
- **Region** → a geographic area (e.g. `us-east-1` = N. Virginia, `ap-south-1` = Mumbai). You pick the Region closest to your users.
- **Availability Zone (AZ)** → one or more isolated data centers inside a Region (e.g. `us-east-1a`, `us-east-1b`). Spreading instances across AZs survives a data-center failure.
- **AMI** → the OS image used to boot the instance (Amazon Linux, Ubuntu, Windows, etc.).
- **Instance type** → the hardware size, e.g. `t3.micro` (2 vCPU, 1 GiB RAM).
- **EBS volume** → network-attached virtual disk (your storage).
- **Key pair** → public/private key used to securely connect to the instance.
- **Security group** → stateful virtual firewall attached to the instance.

---

## 5. How EC2 pricing works (high level)

You are billed for several things separately:
1. **Instance running time** — per second (Linux, min 60s) or per hour, based on the instance type. **A stopped instance does NOT cost instance-hours.**
2. **EBS storage** — you pay for provisioned disk GB **even while the instance is stopped** (the disk still exists).
3. **Data transfer OUT** to the internet (data IN is usually free).
4. **Elastic IPs** when not in use, snapshots, etc.

The **AWS Free Tier** (for new accounts) historically includes **750 hours/month of `t2.micro` or `t3.micro`** for the first 12 months — enough to keep one small instance running all month for free. Always check current Free Tier terms in the console.

---

## 6. Ways to interact with EC2

1. **AWS Management Console** — the web UI (point-and-click). Best for learning. (Notes 02–04)
2. **AWS CLI** — command line, great for automation/scripts. (Note 23)
3. **SDKs** — call AWS from code (Python `boto3`, Java, etc.).
4. **Infrastructure as Code** — CloudFormation / Terraform (later).

---

## 7. The typical EC2 lifecycle

```
 Launch  →  Running  →  Stop  →  Stopped  →  Start  →  Running  →  Terminate  →  (gone)
```

- **Running**: billed for compute + storage.
- **Stopped**: billed for storage only (EBS), not compute. Public IP usually changes on restart.
- **Terminated**: instance is permanently deleted. Root EBS volume is deleted by default.

> ⚠️ **Terminate = permanent deletion.** Don't confuse "Stop" with "Terminate". We protect against accidental termination in Note 16.

---

## 8. Latest context (2026)

- EC2 now offers **850+ instance configurations** across families optimized for general purpose, compute, memory, storage, accelerated (GPU), and HPC workloads.
- AWS designs its own **Graviton** ARM processors — **Graviton4** powers the current `*8g` instances (C8g, M8g, R8g…), and **Graviton5** (M9g) became generally available in **June 2026**, offering better price-performance than Intel/AMD equivalents for many workloads.
- You will still start learning on small, cheap, Free-Tier-eligible instances like **`t3.micro` / `t2.micro`**.

---

## 9. Quick recap

- EC2 = rent virtual servers, pay per use, scale elastically.
- An instance is a **combination** of AMI + instance type + network + security group + storage + key pair.
- Regions contain AZs; spread across AZs for resilience.
- Stopped = pay for storage only; Terminated = gone forever.
- Next: we actually **launch our first instance** (a Windows server) in Note 02.

---

### Sources
- [Amazon EC2 instance types – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html)
- [Amazon EC2 billing and purchasing options – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-purchasing-options.html)
- [Amazon EC2 pricing – AWS](https://aws.amazon.com/ec2/pricing/)
- [AWS Graviton – Wikipedia](https://en.wikipedia.org/wiki/AWS_Graviton)
- [Amazon EC2 M9g instances – AWS](https://aws.amazon.com/ec2/instance-types/m9g/)
