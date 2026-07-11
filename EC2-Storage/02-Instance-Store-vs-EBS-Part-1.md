# 02 - Difference Between Instance Store & EBS Volume — Part 1

> Goal: understand **what Instance Store actually is**, physically and conceptually, and contrast it with EBS along the first and most important axis — **where the data lives, and what happens to it when the instance stops**. Part 2 (Note 03) continues with performance and cost.

---

## 1. Two very different ideas of "the instance's disk"

Every EC2 instance needs at least a root volume to boot from, and most instance types let you attach more storage. AWS gives you two fundamentally different mechanisms for this:

- **Instance Store** — physical disk(s) **bolted to the exact physical host** your instance happens to be running on.
- **EBS (Elastic Block Store)** — a **virtual disk delivered over the network** from a separate, redundant storage layer, independent of any specific physical host.

> 🧠 **Mental model:** Instance Store is like the internal SSD soldered onto a laptop's motherboard — blazing fast, but if the laptop is destroyed, that data is gone with it. EBS is like a network-attached drive in another room — a little slower to reach, but it keeps existing (and can be reattached to a different laptop) even if this one dies.

---

## 2. Instance Store, in detail

- **Physical location:** NVMe SSD (or, historically, HDD) hardware physically installed in the same host server as your instance's hypervisor slot.
- **Cost:** **included in the instance price** — it's not billed separately, unlike EBS which has its own per-GB/per-IOPS charges.
- **Availability:** only certain instance types/families offer it (commonly indicated by a `d` in the instance type name, e.g. `m6id`, `i4i`, `c8gd`) — not every instance type has Instance Store at all; many (like most `t3`/`t4g`/`m7g`) are **EBS-only**.
- **Size:** fixed by the instance type — you cannot resize or add more Instance Store volumes after launch; whatever the instance type specifies is what you get.

---

## 3. The critical difference: data persistence

This is the single most exam-tested fact in this whole folder:

| Event | Instance Store data | EBS volume data |
|---|---|---|
| **Reboot** | ✅ Survives | ✅ Survives |
| **Stop / Start** (EBS-backed instance) | ❌ **Lost** | ✅ Survives (volume stays, just detached from a stopped instance conceptually, but reattaches on start) |
| **Terminate** | ❌ **Lost** | ✅ Survives, **unless** "Delete on Termination" is set (default **true** for the root volume, default **false** for extra attached volumes) |
| **Underlying hardware failure** | ❌ **Lost** (it *is* that hardware) | ✅ Survives — EBS replicates data within its AZ across multiple hardware devices automatically |

> ⚠️ **"Stop" is not "reboot."** A reboot keeps the instance on the same physical host, so Instance Store survives a reboot. Stopping (and later starting) an EBS-backed instance can move it to a *different* physical host entirely — and Instance Store data does not travel with it. This "stop kills Instance Store data, reboot doesn't" distinction is a favorite exam wording trap.

---

## 4. Why EBS can survive host failure and Instance Store can't

EBS volumes are **replicated within their Availability Zone** across multiple underlying storage devices by AWS automatically — this is transparent to you and is why a single EBS volume already has a baseline level of durability without you doing anything, and why an EBS volume can be detached from one instance and reattached to a completely different instance (even in a different AZ, if restored from a snapshot first).

Instance Store has no such replication: it is literally the disk in the box your instance is running on right now, with no redundancy layer underneath it at all.

---

## 5. Recap

- **Instance Store** = physical, host-local NVMe storage, free (bundled into instance price), fixed size per instance type, **not available on every instance type**.
- **EBS** = network-attached virtual disk, billed separately, resizable, replicated within its AZ, detachable/reattachable to other instances.
- The core trade-off: Instance Store data disappears on **stop or terminate** (and on any host hardware failure); EBS data survives all of those (terminate only wipes it if Delete on Termination is enabled).
- Next: Note 03 — Instance Store vs. EBS Volume, Part 2 (performance and cost).

### Sources
- [Amazon EC2 instance store — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/InstanceStorage.html)
- [Amazon EBS volumes — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volumes.html)
- [Preserving Amazon EC2 instance store data — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/InstanceStorage.html#instance-store-lifetime)
