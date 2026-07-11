# 12 - AWS DynamoDB Provisioned Capacity Mode

> Goal: cover Provisioned mode — explicitly setting RCU/WCU capacity ahead of time, plus DynamoDB Auto Scaling on top of it, and what happens when traffic exceeds what's provisioned.

---

## 1. How it works

You explicitly set a number of **RCUs and WCUs** the table (or index) can sustain. Requests within that provisioned capacity succeed normally; requests **exceeding** it are **throttled** (rejected with a retryable error), unless **burst capacity** (a small, temporary buffer DynamoDB retains from recently unused capacity) happens to absorb the spike.

---

## 2. DynamoDB Auto Scaling

Rather than provisioning a single fixed value, **Auto Scaling** lets you set a **target utilization percentage** and a **min/max range** — DynamoDB automatically adjusts provisioned RCU/WCU up or down within that range to track actual load, using CloudWatch alarms under the hood.

- Smooths out the manual re-provisioning effort while still keeping the **cost benefit** of Provisioned mode (Note 11) over On-Demand for generally-predictable traffic with some variance.

---

## 3. Cost vs. On-Demand

For workloads with **predictable, relatively stable** traffic, Provisioned mode (with or without Auto Scaling) is typically **cheaper per unit of throughput** than On-Demand — the trade is accepting some planning effort and a small throttling risk if traffic spikes faster than Auto Scaling can react.

> 🎯 **Exam tip:** "predictable, steady traffic pattern, cost-optimize" → **Provisioned + Auto Scaling**. "Need guaranteed no-throttle behavior even on sudden unpredictable spikes" → **On-Demand** (Note 11), since Auto Scaling reacts to load rather than instantly matching an abrupt spike.

---

## 4. Recap

- Provisioned mode requires setting explicit RCU/WCU capacity, with **Auto Scaling** adjusting it automatically within a configured range based on target utilization — cheaper than On-Demand for predictable workloads, at the cost of some throttling risk during sudden, sharp spikes.
- Next: Note 13 — AWS DynamoDB Warm Throughput, a newer feature for proactively pre-warming capacity ahead of a known spike.

### Sources
- [Read/write capacity mode — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html)
- [Managing throughput capacity automatically with DynamoDB auto scaling — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/AutoScaling.html)
