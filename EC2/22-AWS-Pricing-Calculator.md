# 22 - AWS Pricing Calculator

> Goal: learn to **estimate the cost** of EC2 (and other AWS) workloads **before** you build them, using the free **AWS Pricing Calculator** — with a step-by-step EC2 estimate.

---

## 1. What is the AWS Pricing Calculator?

A **free web tool** (no login required) at **<https://calculator.aws>** that lets you model AWS services and get a **monthly / annual cost estimate** before spending a rupee/dollar.

Use it to:
- Compare **On-Demand vs Savings Plans vs Reserved** for the same workload.
- Estimate a full architecture (EC2 + EBS + data transfer + RDS + S3…).
- Produce a **shareable link / exportable** estimate for budgeting and approvals.

> 🧠 It only **estimates** — your real bill depends on actual usage, data transfer, and Free Tier. But it's the standard tool for planning and the SAA exam expects you to know it exists for cost planning.

---

## 2. Why estimate first?

- **Avoid bill shock** — know the cost before launching.
- **Choose the right purchase option** — see how much a 1-yr Savings Plan actually saves vs On-Demand for *your* numbers.
- **Right-size** — compare instance types/sizes side by side.
- **Justify budgets** — share a documented estimate with your team/manager.

---

## 3. Hands-On — estimate an EC2 web server

**Step 1 — Open and start:**
1. Go to **<https://calculator.aws>**.
2. Click **Create estimate**.

**Step 2 — Add EC2:**
1. Search services for **EC2** → **Configure**.
2. **Region**: pick yours (e.g. *Asia Pacific (Mumbai)* — price varies by Region).
3. **Tenancy**: Shared.
4. **Operating system**: Linux.
5. **Instance type**: search/select e.g. `t3.medium` (or use the *advanced/quick estimate* to let it suggest by vCPU/RAM).
6. **Number of instances**: e.g. `2`.
7. **Usage**: e.g. *100% utilized / 730 hours per month* (24/7), or set a percentage if it only runs part-time.

**Step 3 — Choose a pricing model and compare:**
- Under **Pricing strategy / Purchasing option**, toggle between:
  - **On-Demand**
  - **Compute Savings Plans (1-yr / 3-yr, No/Partial/All upfront)**
  - **EC2 Instance Savings Plans**
  - **Reserved**
- Watch the **monthly estimate change** — this is the key learning: see the % saved by committing.

**Step 4 — Add storage (EBS):**
- Add **EBS volume**: e.g. `gp3`, `30 GB` per instance. EBS is billed even when the instance is **stopped**.

**Step 5 — Add data transfer (often forgotten!):**
- Estimate **outbound data transfer to the internet** (e.g. 100 GB/month). Inbound is usually free; **outbound** is where data-transfer cost lives.

**Step 6 — Review & save:**
1. Click **Add to my estimate**.
2. See the **total monthly + 12-month** cost.
3. **Save and share** → get a URL, or **Export** to CSV/PDF for your records.

---

## 4. What drives EC2 cost (so your estimate is realistic)

| Cost driver | Notes |
|---|---|
| **Instance hours** | type × number × hours/month (730 = 24/7). |
| **Purchase option** | On-Demand vs Savings/Reserved can cut 30–70%. |
| **EBS storage** | per GB-month, billed even when stopped; plus IOPS/throughput for some types. |
| **Data transfer OUT** | to internet / cross-Region / cross-AZ. Inbound usually free. |
| **Elastic/Public IPv4** | small hourly charge per public IPv4 (2024+). |
| **Snapshots, extra IPs, load balancers** | add separately. |
| **OS license** | Windows/RHEL cost more than Linux. |

---

## 5. Tips

- **Always include data transfer and EBS** — beginners estimate only instance hours and undershoot.
- Set **realistic hours**: a dev box used 8h×22 days ≈ 176 hrs, not 730.
- Use it to **prove the Savings Plan case** before committing for 1–3 years.
- Combine with **AWS Cost Explorer** + **Budgets** (in the console) once you're actually running, to track real spend and get alerts.
- The **Free Tier** (new accounts) isn't auto-applied in the calculator — subtract it mentally for the first 12 months.

---

## 6. Recap

- **AWS Pricing Calculator (calculator.aws)** = free pre-build cost estimator.
- Model EC2 = Region + OS + instance type + count + hours + **purchase option** + **EBS** + **data transfer out**.
- Its biggest value: **compare On-Demand vs Savings Plans/Reserved** in real numbers.
- Don't forget EBS, data transfer, and public IPv4 charges.
- Track real spend later with **Cost Explorer + Budgets**.
- Next (Note 23): **AWS CLI (Hands-On)** — manage EC2 from the command line.

---

### Sources
- [AWS Pricing Calculator](https://calculator.aws/)
- [AWS Pricing Calculator – documentation](https://docs.aws.amazon.com/pricing-calculator/latest/userguide/what-is-pricing-calculator.html)
- [Amazon EC2 pricing](https://aws.amazon.com/ec2/pricing/)
