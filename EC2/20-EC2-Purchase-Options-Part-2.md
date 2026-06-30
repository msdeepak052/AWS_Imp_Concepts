# 20 - EC2 Instance Purchase Options — Part 2 (Savings Plans & Spot Instances)

> Goal: master the two options that matter most for **modern cost optimization** — **Savings Plans** (flexible commitment discount) and **Spot Instances** (cheapest, interruptible). Builds on Part 1.

---

## 1. Savings Plans

**What:** Instead of committing to a *specific instance* (like a Reserved Instance), you commit to a **steady amount of spend ($/hour)** for **1 or 3 years**. AWS discounts everything up to that committed spend.

**Discount:** up to **~72%** (similar to RIs), in exchange for a usage commitment.

### 1.1 Two types of Savings Plans

| Type | Applies to | Flexibility | Max discount |
|---|---|---|---|
| **Compute Savings Plan** | EC2 **+ Fargate + Lambda**, any **family, size, Region, OS, tenancy** | **Most flexible** | up to ~66% |
| **EC2 Instance Savings Plan** | A specific **instance family in a chosen Region** (any size/OS within it) | Less flexible (locked to family + Region) | up to ~72% |

> 🧠 **Compute Savings Plan** is the crowd favorite: you commit to, say, "$10/hour of compute for 1 year," and the discount automatically follows you as you switch instance types, move Regions, or even shift to Lambda/Fargate. Maximum flexibility, slightly lower max discount.

### 1.2 Payment options
Same as RIs: **All Upfront** (best discount), **Partial Upfront**, **No Upfront**.

### 1.3 Savings Plans vs Reserved Instances

| | **Savings Plan** | **Reserved Instance** |
|---|---|---|
| Commit to | **$/hour spend** | **Specific instance config** |
| Flexibility | High (esp. Compute SP) | Lower (Standard) / medium (Convertible) |
| Covers Lambda/Fargate? | ✅ (Compute SP) | ❌ |
| Can sell on Marketplace? | ❌ | ✅ (Standard RI) |
| Capacity reservation? | ❌ | ✅ (Zonal RI only) |

> AWS now generally recommends **Savings Plans over RIs** for most customers because they're simpler and more flexible. Use RIs when you need a **capacity reservation** (Zonal) or want to **sell unused** commitment.

**✅ Best for:** predictable **baseline** compute you'll run for 1–3 years, but where you want freedom to evolve instance types/Regions.

---

## 2. Spot Instances

**What:** Buy **spare/unused EC2 capacity** at a steep discount — **up to ~90% off** On-Demand. The catch: **AWS can reclaim (interrupt) the instance with a 2-minute warning** when it needs the capacity back.

### 2.1 How Spot works (2026)
- You pay the current **Spot price**, which fluctuates with supply/demand (but is far below On-Demand).
- You can set a **max price** you're willing to pay; if the Spot price exceeds it (rare now), the instance is interrupted.
- AWS gives a **2-minute interruption notice** (via instance metadata / EventBridge) so your app can checkpoint and exit gracefully.

### 2.2 Interruption behaviors
When interrupted, you choose what happens: **Terminate** (default), **Stop**, or **Hibernate**.

### 2.3 Spot Fleet / Spot in Auto Scaling
- **Spot Fleet / EC2 Fleet / mixed-instances ASG** can request a **mix of Spot + On-Demand** across **multiple instance types and AZs**, automatically replacing interrupted Spot capacity → resilient *and* cheap.
- A **Capacity-Optimized** allocation strategy picks pools least likely to be interrupted.

**✅ Best for (fault-tolerant, flexible, stateless work):**
- Batch processing, big-data jobs (EMR/Spark), CI/CD build farms.
- Stateless web servers behind a load balancer (with On-Demand baseline).
- ML training with checkpointing, rendering, data analysis.

**❌ Avoid Spot for:**
- Databases or **stateful** servers that can't tolerate sudden loss.
- Workloads needing **guaranteed, uninterrupted** runtime.

---

## 3. Combining options (real-world cost strategy)

A mature setup blends them:

```
Steady baseline   → Savings Plan / Reserved   (cheap, always-on minimum)
Normal variability → On-Demand                (reliable, flexible top-up)
Bursty / batch     → Spot                      (cheapest, interruptible extra)
```

Example for a web app with Auto Scaling:
- Reserve/Savings-Plan the **minimum 4 instances** that always run.
- Let Auto Scaling add **On-Demand** instances for daily peaks.
- Add **Spot** instances for big, fault-tolerant surges to cut cost further.

---

## 4. Decision quick-reference

| Need | Option |
|---|---|
| Cheapest, work can be interrupted | **Spot** (up to 90% off) |
| Steady baseline, flexible config, want simplicity | **Savings Plan (Compute)** |
| Steady baseline, single family, max discount | **EC2 Instance Savings Plan** or **Standard RI** |
| Unpredictable, can't interrupt | **On-Demand** |

---

## 5. Recap

- **Savings Plans** = commit to **$/hour** for 1–3 yrs (up to ~72%); **Compute SP** is most flexible (covers Lambda/Fargate, any family/Region).
- **Spot** = spare capacity, **up to 90% off**, but **interruptible (2-min warning)** — only for **fault-tolerant/stateless** work.
- Real cost optimization **blends** Reserved/Savings (baseline) + On-Demand (flex) + Spot (cheap bursts).
- Next (Note 21 / Part 3): **Dedicated Hosts** & **Capacity Reservations**, plus the full comparison table.

---

### Sources
- [Savings Plans – AWS docs](https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html)
- [Amazon EC2 Spot Instances – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances.html)
- [Amazon EC2 Spot Instances pricing](https://aws.amazon.com/ec2/spot/pricing/)
