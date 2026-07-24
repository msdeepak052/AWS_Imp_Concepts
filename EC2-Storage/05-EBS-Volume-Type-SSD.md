# 05 - EBS Volume Type SSD

> Goal: know the four SSD-backed EBS volume types (`gp2`, `gp3`, `io1`, `io2` / `io2 Block Express`) cold — their IOPS models, size limits, and the scenarios each is built for. This is one of the most exam-dense topics in the whole storage domain.

---

## 1. The two SSD families

| Family | Types | Optimized for |
|---|---|---|
| **General Purpose SSD** | `gp2`, `gp3` | A balance of price and performance for most workloads |
| **Provisioned IOPS SSD** | `io1`, `io2`, `io2 Block Express` | Mission-critical, I/O-intensive workloads needing sustained, guaranteed high IOPS |

> 🧠 **Mental model:** General Purpose SSD is "good enough for almost everything, cheap" — the default choice unless you have a specific reason not to use it. Provisioned IOPS SSD is "I know exactly how many IOPS I need, and I'm willing to pay for a guarantee," used for the tail of workloads where GP SSD's baseline isn't enough.

---

## 2. gp2 — the older General Purpose SSD

- **IOPS model:** baseline **3 IOPS per GB** provisioned, minimum 100 IOPS, scaling up to a cap of **16,000 IOPS** (reached at 5,334 GB and above).
- **Burst bucket:** small volumes get a **burst credit bucket** — every volume starts with 5.4 million I/O credits (enough for 30 minutes at 3,000 IOPS), letting small volumes burst above their baseline temporarily, then throttling back down once credits run out.
- **Size range:** 1 GiB – 16 TiB.
- **Use case today:** mostly superseded by gp3 — still exists for compatibility/legacy volumes, but AWS recommends gp3 for new volumes since it's both cheaper and more flexible.

---

## 3. gp3 — the current-generation General Purpose SSD (default recommendation)

- **Baseline performance included free, regardless of size:** **3,000 IOPS** and **125 MiB/s throughput** — no need to over-provision size just to get more IOPS, unlike gp2.
- **Independently scalable:** you can provision **up to 16,000 IOPS** and **up to 1,000 MiB/s throughput** for an additional cost, *decoupled from the volume's size* — this decoupling is gp3's headline improvement over gp2.
- **Size range:** 1 GiB – 16 TiB.
- **Cost:** typically **~20% cheaper per GB** than gp2 for the same baseline performance.
- **Default for new volumes** in the console today, and the right first choice for the overwhelming majority of EBS use cases: boot volumes, dev/test, low-latency interactive apps, most small-to-medium databases.

> 🎯 **Exam tip:** "need more IOPS but the volume is already large enough / don't want to pay for extra space" is the classic gp2 → gp3 migration story. gp3 lets you buy IOPS and throughput separately from GiB size; gp2 forces you to over-provision size just to unlock more IOPS.

---

## 4. io1 — the original Provisioned IOPS SSD

- **You provision the IOPS explicitly** (not derived from size) — up to **64,000 IOPS per volume** (on Nitro instances; 32,000 on non-Nitro), with a maximum IOPS-to-GiB ratio of 50:1.
- **Size range:** 4 GiB – 16 TiB.
- **Multi-Attach support:** io1 (and io2) can be attached to **multiple instances simultaneously** (up to 16, within the same AZ) — but this shares raw *blocks*, not a filesystem, so it requires cluster-aware software (like a clustered database) that manages concurrent writes itself; a plain filesystem does not become magically shareable just by enabling Multi-Attach.
- **Use case:** legacy Provisioned IOPS workloads; largely superseded by io2 for new deployments (io2 offers better durability at the same or lower price).

---

## 5. io2 and io2 Block Express — the current-generation Provisioned IOPS SSD

- **io2:** same IOPS-provisioning model as io1, but with **higher durability** — designed for **99.999%** durability (vs. 99.8–99.9% for gp2/gp3/io1) — and higher IOPS-to-GiB ratio (up to 500:1).
- **io2 Block Express:** the highest-performance EBS tier available — up to **256,000 IOPS**, **4,000 MiB/s throughput**, and **64 TiB** volume size per volume, sub-millisecond latency — for the largest, most demanding databases (e.g. SAP HANA, large Oracle/SQL Server deployments).
- **Use case:** mission-critical relational databases, workloads needing guaranteed, sustained high IOPS regardless of size, and the very largest single-volume performance requirements.

---

## 6. Side-by-side summary

| Type | Max IOPS | Max throughput | Max size | IOPS tied to size? | Multi-Attach | Durability |
|---|---|---|---|---|---|---|
| **gp2** | 16,000 | ~250 MiB/s | 16 TiB | Yes (3 IOPS/GB, burstable) | No | 99.8–99.9% |
| **gp3** | 16,000 | 1,000 MiB/s | 16 TiB | No (3,000 IOPS/125 MiB/s free baseline, rest provisioned separately) | No | 99.8–99.9% |
| **io1** | 64,000 | 1,000 MiB/s | 16 TiB | No (explicitly provisioned) | Yes | 99.8–99.9% |
| **io2** | 64,000 | 1,000 MiB/s | 16 TiB | No (explicitly provisioned) | Yes | **99.999%** |
| **io2 Block Express** | 256,000 | 4,000 MiB/s | 64 TiB | No (explicitly provisioned) | Yes | **99.999%** |

---

## 7. Recap

- **gp3** is the modern default General Purpose SSD: free 3,000 IOPS / 125 MiB/s baseline, both scalable independently of size, cheaper than gp2.
- **gp2** is the older General Purpose SSD, IOPS tied to size (3 IOPS/GB) with a burst-credit model — still around, but gp3 is strictly better for nearly every case.
- **io1/io2** are Provisioned IOPS SSD for mission-critical, high, guaranteed-IOPS workloads; **io2** adds much higher durability (99.999%) over io1.
- **io2 Block Express** is the top tier: up to 256,000 IOPS, 4,000 MiB/s, 64 TiB — for the largest, most demanding single-volume databases.
- io1/io2 support **Multi-Attach** (shared blocks across up to 16 instances in one AZ) — but only cluster-aware software can safely use this; it doesn't turn EBS into shared file storage.
- Next: Note 06 — EBS Volume Type HDD (st1, sc1).

### Sources
- [Amazon EBS volume types — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html)
- [General Purpose SSD volumes — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/general-purpose.html)
- [Provisioned IOPS SSD volumes — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/provisioned-iops.html)
- [Amazon EBS Multi-Attach — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volumes-multi.html)
