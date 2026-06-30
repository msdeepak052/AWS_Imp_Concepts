# 21 - EC2 Instance Purchase Options — Part 3 (Dedicated Hosts, Capacity Reservations & Full Comparison)

> Goal: finish purchase options with **Dedicated Hosts** (BYOL/compliance) and **On-Demand Capacity Reservations** (guarantee capacity), then bring **all options together** in one comparison and decision guide.

---

## 1. Dedicated Hosts (pricing view)

(Tenancy concept covered in Note 18 — here we focus on the **purchasing** angle.)

**What:** Pay for an **entire physical EC2 server dedicated to you**, with visibility into **sockets/physical cores**.

**Why (purchasing-wise):**
- **Bring Your Own License (BYOL):** legally use **per-socket / per-core** software licenses (Windows Server, SQL Server, Oracle) because you can see and pin to the physical hardware.
- **Compliance / regulatory** isolation requirements.

**How you pay:**
- **On-Demand Dedicated Host** — hourly for the whole host.
- **Dedicated Host Reservation** (1 or 3 yr) — discounted commitment, like an RI but for hosts.
- Can be combined with **Savings Plans**.

**✅ Best for:** socket/core-based licensing and strict compliance. **❌ Most expensive & most management overhead** — not for general workloads.

---

## 2. On-Demand Capacity Reservations

**What:** Reserve EC2 **capacity in a specific Availability Zone** for **any duration**, so the capacity is **guaranteed to be available** when you need it.

**Key points:**
- **No commitment term and no automatic discount** — you pay On-Demand rates (whether or not you actually run instances in the reservation).
- Solves a different problem from RIs/Savings Plans: those save **money**; Capacity Reservations guarantee **availability** (no "Insufficient Capacity" errors).
- **Can be combined** with a Savings Plan or Regional RI to get **both** the discount **and** the capacity guarantee.
- Create/cancel **anytime**.

**✅ Best for:**
- **Mission-critical** workloads that must launch in a specific AZ (e.g. disaster-recovery failover, end-of-quarter batch, big events).
- Guaranteeing capacity for a known **future spike**.

> 🧠 Remember: **Capacity Reservation = guarantee capacity, not save money.** Pair it with a Savings Plan/RI for the discount.

---

## 3. The full comparison table

| Option | Commitment | Discount | Capacity guarantee | Interruptible? | Best for |
|---|---|---|---|---|---|
| **On-Demand** | None | None (baseline) | No | No | Short/spiky/unknown workloads |
| **Reserved Instance** | 1 or 3 yr (config) | up to ~72% | Only **Zonal** RIs | No | Steady, predictable baseline |
| **Savings Plan** | 1 or 3 yr ($/hr) | up to ~72% | No | No | Steady baseline, flexible config |
| **Spot** | None | up to ~90% | No | **Yes (2-min notice)** | Fault-tolerant, stateless, batch |
| **Dedicated Host** | On-Demand or 1/3 yr | License value | Host-level | No | BYOL, compliance, host visibility |
| **Capacity Reservation** | None (any duration) | None alone | **Yes** (specific AZ) | No | Guarantee capacity for critical/peak |

---

## 4. The master decision guide

Ask these questions in order:

1. **Can the workload be interrupted?** → **Spot** (cheapest). (Pair with On-Demand baseline.)
2. **Is it steady & long-running (≥1 yr)?**
   - Want flexibility / also Lambda-Fargate? → **Compute Savings Plan**.
   - Single family, want max discount? → **EC2 Instance Savings Plan / Standard RI**.
3. **Need a capacity guarantee in an AZ?** → **Capacity Reservation** (+ Savings Plan/RI for discount).
4. **Per-socket/core licensing or compliance?** → **Dedicated Host**.
5. **None of the above / short-term / unsure?** → **On-Demand**.

---

## 5. Putting it together — a realistic example

A production e-commerce platform:
- **Baseline 6 instances 24/7** → **Compute Savings Plan** (cheap, flexible).
- **Daily traffic peaks** → Auto Scaling adds **On-Demand** instances.
- **Black Friday guaranteed capacity** → **Capacity Reservation** in 2 AZs ahead of time (+ covered by the Savings Plan for discount).
- **Nightly analytics/batch jobs** → **Spot** instances (90% cheaper, interruption-tolerant).
- **Legacy licensed SQL Server** → **Dedicated Host** (BYOL).

This blend minimizes cost while meeting reliability and licensing needs — exactly the kind of trade-off the SAA exam tests.

---

## 6. Recap (all three parts)

- **On-Demand** — flexible, no commit, priciest.
- **Reserved Instances** — commit to config 1/3 yr, up to ~72% off.
- **Savings Plans** — commit to $/hr 1/3 yr, up to ~72%, more flexible (Compute SP covers Lambda/Fargate).
- **Spot** — spare capacity, up to 90% off, interruptible.
- **Dedicated Hosts** — whole physical server, BYOL/compliance.
- **Capacity Reservations** — guarantee AZ capacity (no discount alone; combine with SP/RI).
- Next (Note 22): **AWS Pricing Calculator** — estimate all this before you spend.

---

### Sources
- [Amazon EC2 billing and purchasing options – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-purchasing-options.html)
- [On-Demand Capacity Reservations – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-capacity-reservations.html)
- [Dedicated Hosts pricing – AWS](https://aws.amazon.com/ec2/dedicated-hosts/pricing/)
