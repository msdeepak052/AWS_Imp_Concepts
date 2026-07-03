# 08 - Multi-AZ (Regions, Availability Zones & High Availability)

> Goal: understand **Regions**, **Availability Zones (AZs)**, and why spreading instances across **multiple AZs (Multi-AZ)** is the foundation of **high availability** in AWS.

---

## 1. The AWS global hierarchy

```
AWS Global Infrastructure
│
├── Region (e.g. ap-south-1 = Mumbai, us-east-1 = N. Virginia)
│     │
│     ├── Availability Zone  (e.g. ap-south-1a)  ← 1+ physical data centers
│     ├── Availability Zone  (e.g. ap-south-1b)
│     └── Availability Zone  (e.g. ap-south-1c)
│
└── Edge Locations (200+ for CloudFront CDN — not for EC2)
```

- **Region** = a geographic area with multiple isolated data centers. You choose a Region based on **latency (closeness to users)**, **price** (varies by Region), **compliance/data residency**, and **service availability**.
- **Availability Zone (AZ)** = **one or more discrete data centers** with independent power, cooling, and networking, within a Region.
- AZs in a Region are **physically separated** (km apart) but connected by **high-bandwidth, low-latency private links**.
- Each Region has **at least 3 AZs** (commonly 3–6).

---

## 2. Why multiple AZs exist

A single data center can fail (power outage, fire, flood, hardware failure). If **all** your instances are in **one AZ** and that AZ goes down, **your app goes down**.

**Multi-AZ** = run copies of your application in **2+ AZs**. If one AZ fails, the others keep serving traffic.

> 🧠 **Analogy:** Don't keep all your eggs in one basket. AZs are separate baskets in the same city; Regions are baskets in different cities.

---

## 3. Key facts about AZs (exam + real-world)

- **AZ names are per-account scrambled.** `us-east-1a` in your account may be a different physical data center than `us-east-1a` in mine. AWS does this to balance load. (AZ **IDs** like `use1-az1` are consistent across accounts.)
- **Subnets live in exactly one AZ.** To be Multi-AZ you create **one subnet per AZ** and launch instances into different subnets.
- **Data transfer between AZs** (in the same Region) is **low latency but NOT free** — you pay a small per-GB cost. Within the **same AZ** it's free.
- **EBS volumes are AZ-locked** — a volume in `az-a` can only attach to an instance in `az-a`. To move data across AZs you take a **snapshot** (snapshots are Region-wide) and create a new volume in the other AZ.

---

## 4. How Multi-AZ creates High Availability (the pattern)

The classic resilient web architecture:

```
            Internet
               │
        ┌──────────────┐
        │ Load Balancer│   (spans multiple AZs)
        └──────┬───────┘
        ┌──────┴───────┐
        ▼              ▼
   ┌─────────┐    ┌─────────┐
   │  EC2    │    │  EC2    │
   │ AZ-a    │    │ AZ-b    │   ← Auto Scaling Group across AZs
   └─────────┘    └─────────┘
        │              │
        ▼              ▼
   ┌────────────────────────┐
   │  RDS Multi-AZ (DB) │   primary in AZ-a, standby in AZ-b
   └────────────────────────┘
```

- **Elastic Load Balancer (ELB)** distributes traffic across instances in multiple AZs and stops sending traffic to a failed AZ.
- **Auto Scaling Group (ASG)** keeps the desired number of instances spread across AZs, replacing failed ones.
- **RDS Multi-AZ** keeps a synchronous standby DB in another AZ and **fails over automatically**.

> This combination (ELB + ASG + RDS Multi-AZ) is the bread-and-butter highly available design on the SAA exam.

---

## 5. Multi-AZ vs Multi-Region

| | **Multi-AZ** | **Multi-Region** |
|---|---|---|
| Protects against | Data-center / AZ failure | Entire Region failure, global latency |
| Distance | Same Region (km apart) | Different geographies |
| Latency between | Very low (ms) | Higher (cross-continent) |
| Complexity / cost | Moderate | High |
| Typical use | Standard HA (most apps) | Disaster recovery, global apps, compliance |

> Start with **Multi-AZ** for high availability. Add **Multi-Region** only for disaster recovery or global reach.

---

## 6. Related concepts (don't confuse them)

- **Local Zones** — AWS infrastructure placed **closer to large cities** for ultra-low latency (extension of a Region).
- **Wavelength Zones** — inside telecom 5G networks for mobile edge.
- **Outposts** — AWS hardware in **your own data center**.
- **Edge Locations** — CDN caching points for **CloudFront** (not EC2 compute).

---

## 7. Hands-on idea (optional)

1. Launch instance #1, in **Subnet** ending `...a` (AZ `a`).
2. Launch instance #2, in **Subnet** ending `...b` (AZ `b`).
3. EC2 → Instances → add the **Availability Zone** column → confirm they're in different AZs.
4. (Later) Put both behind an **Application Load Balancer** spanning both AZs.

---

## 8. Recap

- **Region** = geographic area; **AZ** = isolated data center(s) inside a Region (≥3 per Region).
- **Multi-AZ** = run across 2+ AZs → survive a data-center failure = **high availability**.
- Subnets and EBS volumes are **AZ-scoped**; snapshots are **Region-scoped**.
- HA pattern = **ELB + Auto Scaling across AZs + RDS Multi-AZ**.
- Multi-Region is for disaster recovery / global latency, not everyday HA.
- Next (Note 09): **Public vs Private IP addresses**.

---

### Sources
- [Regions and Availability Zones – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html)
- [AWS Global Infrastructure](https://aws.amazon.com/about-aws/global-infrastructure/)
- [Resilience in Amazon EC2 – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/disaster-recovery-resiliency.html)
