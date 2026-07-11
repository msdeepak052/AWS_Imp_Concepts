# 03 - Difference Between Instance Store & EBS Volume — Part 2

> Goal: finish the comparison started in Note 02 by covering **performance, cost, and boot-volume eligibility** — the practical axes that decide which one to reach for.

---

## 1. Performance: Instance Store usually wins

Because Instance Store is physically local NVMe hardware with no network hop and no virtualization layer for the storage path, it typically delivers:

- **Higher, more consistent IOPS** than even the fastest EBS volume types (io2 Block Express aside).
- **Lower latency** — no network round-trip to a separate storage fleet.
- **No separate throughput/IOPS billing** to worry about — it's just the raw hardware.

EBS, being network-attached, always has some latency overhead compared to local disk, though modern EBS types (gp3, io2 Block Express) close this gap enormously for most workloads and remain the right default for anything that must survive the instance.

> 🧠 **Mental model:** Instance Store trades durability for raw speed. If your workload can tolerate losing the data (because it's temporary, reconstructible, or already replicated elsewhere), Instance Store gives you the best performance AWS offers for free. If it can't, that speed doesn't matter — EBS (or a purpose-built database/file service) is the only correct choice.

---

## 2. Cost: Instance Store is "free," EBS is metered

| | Instance Store | EBS |
|---|---|---|
| **Billing** | Bundled into the instance's hourly price — no separate line item | Billed separately: per-GB provisioned, sometimes per-IOPS/per-throughput depending on volume type, plus snapshot storage in S3 |
| **Scaling cost** | Fixed — can't provision more even if you wanted to | Scales with how much you provision — pay for exactly what you allocate |

This makes Instance Store attractive for high-throughput scratch space where paying extra for guaranteed durability/IOPS would be wasted money — but it's never "free" in the sense of being risk-free.

---

## 3. Boot volume eligibility

- **EBS-backed instances** (the overwhelming majority of instances you'll launch, and the default for the AWS-provided AMIs) use an **EBS volume as the root/boot volume**. This is what lets you **stop and start** the instance at all — an EBS-backed instance can be stopped (billing pauses on compute, EBS storage keeps billing) and later started again, possibly on different underlying hardware, with the root volume's contents intact.
- **Instance Store-backed AMIs** exist but are increasingly rare/legacy — an instance booted from one **cannot be stopped**, only **rebooted** or **terminated**. There is no "stopped" state for a pure instance-store root volume, because stopping would mean surviving on host hardware you no longer occupy, which instance store cannot do.

> ⚠️ **Exam wording trap:** "Can this instance be stopped and restarted?" is really asking "is the root volume EBS or Instance Store?" — EBS-backed: yes. Instance-store-backed: no (terminate/reboot only).

---

## 4. Side-by-side summary

| Axis | Instance Store | EBS |
|---|---|---|
| Physical location | Same host as the instance | Separate, redundant storage fleet, network-attached |
| Durability | None — lost on stop/terminate/host failure | Replicated within the AZ automatically |
| Performance | Highest, most consistent (no network hop) | Very good (gp3/io2), but still network-attached |
| Cost | Bundled into instance price | Billed separately (GB + IOPS/throughput as applicable) |
| Resizable | No — fixed by instance type | Yes — can grow (and for some types, change volume type/IOPS) live |
| Can be a boot volume? | Yes, on legacy Instance Store-backed AMIs (no stop/start) | Yes, and is the default/typical choice (supports stop/start) |
| Detach and move to another instance? | No | Yes |
| Typical use | Cache, buffer, scratch, temp/replicated data | Root volumes, databases, anything that must persist |

---

## 5. Recap

- Instance Store wins on **raw performance and cost** (bundled, no network hop) but loses **everything** on durability — stop, terminate, or a host hardware fault all destroy the data.
- EBS costs more (billed separately) and has a network hop, but **survives stop/start, survives host hardware failure** (AZ-level replication), and can be **detached and reattached** to a different instance.
- Whether an instance can be "stopped" at all depends on whether its **root volume** is EBS (yes) or Instance Store (no — terminate/reboot only).
- Next: Note 04 — Instance Store & EBS Volume Scenarios, where these trade-offs get applied to concrete "which one would you pick" exam-style situations.

### Sources
- [Amazon EC2 instance store — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/InstanceStorage.html)
- [Amazon EBS features — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSFeatures.html)
- [Instance stop and start behavior — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Stop_Start.html)
