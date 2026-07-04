# 19 - EC2 Instance Purchase Options — Part 1 (Overview, On-Demand, Reserved Instances)

> Goal: see the **full menu** of EC2 pricing models, then go deep on **On-Demand** (pay-as-you-go) and **Reserved Instances (RIs)** (commit to save). Parts 2–3 cover Savings Plans, Spot, Dedicated Hosts, and Capacity Reservations.

---

## 1. The full menu of purchase options (2026)

| Option | One-liner | Max saving vs On-Demand |
|---|---|---|
| **On-Demand** | Pay by the second/hour, no commitment | baseline (most expensive) |
| **Reserved Instances (RI)** | Commit to a config for 1 or 3 yrs | up to ~72% |
| **Savings Plans** | Commit to $/hour spend for 1 or 3 yrs | up to ~66–72% |
| **Spot Instances** | Bid on spare capacity, can be reclaimed | up to ~90% |
| **Dedicated Hosts** | Whole physical server (BYOL) | (licensing value) |
| **Capacity Reservations** | Reserve capacity in an AZ (no discount alone) | none (guarantees capacity) |

> 🧠 Mental model: **On-Demand = flexibility (no commit)**, **Reserved/Savings Plans = commitment for discount**, **Spot = cheapest but interruptible**, **Dedicated/Capacity = control/guarantee**.

---

## 2. On-Demand Instances

**What:** Pay for compute **by the second** (Linux, 60s minimum) or **by the hour**, with **no upfront cost and no commitment**. Start and stop whenever you want.

**Billing:** You pay only while the instance is **running**. Stop it → stop paying for compute (still pay for EBS storage).

**✅ Best for:**
- **Short-term, spiky, or unpredictable** workloads.
- **Dev/test** and experimentation.
- New apps where you don't yet know steady usage.
- Workloads that **can't be interrupted** but are too short to justify a 1-yr commitment.

**❌ Downside:** the **most expensive** per-hour rate. Running On-Demand 24/7 for a year wastes money vs a commitment plan.

> This is what every earlier hands-on used (the Free Tier covers ~750 hrs/month of `t3.micro`/`t2.micro` for 12 months).

---

## 3. Reserved Instances (RI)

**What:** You **commit to a specific instance configuration** for a **1-year or 3-year** term in exchange for a big discount (**up to ~72%** off On-Demand).

**You commit to (Standard RI) some of:** instance **type/family**, **Region** (or AZ), **OS**, **tenancy**, for the whole term.

### 3.1 Payment options (affect the discount)
| Payment | Upfront | Discount |
|---|---|---|
| **All Upfront** | Pay everything now | **Biggest** discount |
| **Partial Upfront** | Some now + lower hourly | Medium |
| **No Upfront** | Nothing now, just commit | Smallest (still good) |

### 3.2 Standard vs Convertible RIs
| | **Standard RI** | **Convertible RI** |
|---|---|---|
| Discount | Higher (up to ~72%) | Lower (up to ~54%) |
| Flexibility | Can change AZ/size (within family), can sell on RI Marketplace | Can **change instance family, OS, tenancy** (exchange for another Convertible RI) |
| Best when | You're sure of your needs | Needs may change over the term |

### 3.3 Regional vs Zonal RIs
- **Regional RI** → discount applies across **any AZ in the Region**, and gives **instance size flexibility** (a discount for a `large` can cover two `medium`s in the same family/Region). **No capacity reservation.**
- **Zonal RI** → tied to a **specific AZ**, and **does reserve capacity** in that AZ.

**✅ Best for:** **steady-state, always-on** workloads with **predictable** usage for 1–3 years (e.g. a production database or baseline web fleet running 24/7).

> ⚠️ With Standard RIs you're committed even if you stop using the instance — you keep paying. Choose the term/flexibility carefully. (Savings Plans, covered in Part 2, commit you to a **$/hour spend** instead of a specific instance configuration, so the discount keeps applying even if you change instance family, size, or Region — often easier and more flexible than an RI.)

---

## 4. On-Demand vs Reserved — when to use which

| Situation | Choose |
|---|---|
| Don't know usage yet / short project | **On-Demand** |
| Spiky, unpredictable traffic | **On-Demand** (+ Spot for extra) |
| Steady 24/7 baseline for ≥1 year | **Reserved** (or Savings Plan) |
| Need flexibility to change instance family later | **Convertible RI** or **Compute Savings Plan** |
| Need guaranteed capacity in a specific AZ | **Zonal RI** / Capacity Reservation |

---

## 5. A simple cost intuition

For a server running **24/7 all year**:
- **On-Demand** = 100% (baseline).
- **No-Upfront 1-yr RI** ≈ ~60% of On-Demand.
- **All-Upfront 3-yr RI** ≈ ~30–40% of On-Demand.

The longer and more upfront you commit, the cheaper each hour becomes — at the cost of **flexibility**.

---

## 6. Recap

- Six options; **On-Demand** (flexible, priciest) and **Reserved** (commit 1/3 yr, up to ~72% off) covered here.
- RI knobs: **payment** (All/Partial/No upfront), **class** (Standard vs Convertible), **scope** (Regional vs Zonal).
- Use **On-Demand** for unknown/spiky/short; **RI** for steady, long-running baseline.
- Next (Note 20 / Part 2): **Savings Plans** and **Spot Instances**.

---

### Sources
- [Amazon EC2 billing and purchasing options – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-purchasing-options.html)
- [Reserved Instances – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-reserved-instances.html)
- [Amazon EC2 On-Demand pricing](https://aws.amazon.com/ec2/pricing/on-demand/)
