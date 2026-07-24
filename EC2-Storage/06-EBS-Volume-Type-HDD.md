# 06 - EBS Volume Type HDD

> Goal: cover the two magnetic (HDD-backed) EBS volume types — `st1` and `sc1` — what makes them fundamentally different from every SSD type in Note 05, and the narrow band of workloads where they're actually the right (cheaper) choice.

---

## 1. The one rule that governs both HDD types

**Neither `st1` nor `sc1` can be a boot volume.** Both are optimized for large, **sequential** I/O (streaming through a big file start-to-finish), not the small, random I/O pattern a boot volume or a typical database needs. This single fact eliminates them from most general-purpose use immediately and is a frequently tested exam fact.

> 🧠 **Mental model:** SSD volumes (Note 05) are priced and rated in **IOPS** because they're built for hitting many small, scattered reads/writes fast. HDD volumes are priced and rated in **throughput (MiB/s)** because they're built for reading/writing one big continuous stream of data efficiently — think a spinning disk's read head sweeping across a long, mostly-sequential track, rather than jumping to thousands of random spots per second.

---

## 2. st1 — Throughput Optimized HDD

- **Optimized for:** frequently-accessed, throughput-intensive **sequential** workloads.
- **Typical use cases:** big data / data warehouses, log processing pipelines, streaming data ingestion.
- **Performance model:** rated in throughput (MiB/s), with a burst-credit system similar in spirit to gp2's IOPS burst bucket — a baseline throughput per GiB, with the ability to burst higher temporarily.
- **Size range:** 125 GiB – 16 TiB.
- **Cannot be a boot volume.**

---

## 3. sc1 — Cold HDD

- **Optimized for:** the **lowest-cost** EBS storage available, for data accessed **infrequently**.
- **Typical use cases:** infrequently-accessed data that still needs to be on a block volume — cold data archives, backups you occasionally need to attach and read (though S3, not EBS, is usually the better home for true archival data).
- **Performance model:** lower baseline throughput than st1, but cheaper per GB — the trade-off is explicitly "pay less, accept lower and less frequent throughput."
- **Size range:** 125 GiB – 16 TiB.
- **Cannot be a boot volume.**

---

## 4. SSD vs. HDD, side by side

| | SSD (gp2/gp3/io1/io2) | HDD (st1/sc1) |
|---|---|---|
| Rated in | IOPS | Throughput (MiB/s) |
| I/O pattern | Small, random | Large, sequential |
| Can be boot volume? | Yes | **No** |
| Typical use | Boot volumes, databases, transactional workloads | Big data, log processing, cold/archival data on a block device |
| Cheapest option | gp3 (of the SSDs) | **sc1** (cheapest EBS type overall) |

> 🎯 **Exam tip:** any scenario mentioning "boot volume" instantly rules out st1 and sc1 as the answer, regardless of how well their other described characteristics (cost, throughput) seem to fit — this is one of the fastest eliminations you can make on an EBS-type question.

---

## 5. Recap

- **st1 (Throughput Optimized HDD):** big/sequential throughput workloads — big data, log processing, data warehouses.
- **sc1 (Cold HDD):** the cheapest EBS option, for infrequently-accessed data that still needs block storage.
- Both are rated in **throughput**, not IOPS, both are tuned for **sequential** access, and **neither can ever be a boot volume**.
- Next: Note 07 — EBS (Hands-On), creating and attaching a real volume in the console.

### Sources
- [Amazon EBS volume types — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html)
- [HDD-backed volumes — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/hdd-backed.html)
