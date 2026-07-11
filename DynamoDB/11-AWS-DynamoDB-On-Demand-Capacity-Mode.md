# 11 - AWS DynamoDB On-Demand Capacity Mode

> Goal: cover On-Demand mode — pay-per-request capacity with no provisioning or planning required, DynamoDB's fully-serverless billing model.

---

## 1. How it works

In **On-Demand mode**, you don't provision any RCU/WCU capacity at all — DynamoDB automatically scales to handle whatever request volume actually arrives, and you're billed **per request actually made** (still measured in RCU/WCU-equivalent units, Notes 09-10, just billed per-use rather than pre-provisioned).

- Instantly accommodates **traffic spikes** without any pre-planning or capacity management.
- No risk of **throttling due to under-provisioned capacity** the way Provisioned mode (Note 12) can experience if traffic exceeds what you provisioned.

---

## 2. Cost trade-off

On-Demand's **per-request price is higher** than the equivalent Provisioned-mode price — you're paying a premium for not having to plan capacity or accept any throttling risk. For **spiky, unpredictable, or new/unknown workloads**, this premium is usually worth it; for **stable, predictable workloads**, Provisioned mode (with or without Auto Scaling) is typically cheaper for the same effective throughput.

> 🎯 **Exam tip:** "unpredictable traffic," "new application, traffic pattern unknown," or "avoid managing capacity entirely" → **On-Demand**. "Steady, predictable traffic, cost-optimize" → **Provisioned** (Note 12).

---

## 3. Recap

- On-Demand mode removes all capacity planning — DynamoDB scales automatically per actual request volume, at a higher per-request price than Provisioned mode.
- The right choice for unpredictable or new workloads; not the cheapest choice for stable, well-understood traffic.
- Next: Note 12 — AWS DynamoDB Provisioned Capacity Mode, the alternative, planned-capacity model.

### Sources
- [Read/write capacity mode — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html)
