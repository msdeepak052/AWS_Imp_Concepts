# 20 - RDS Monitoring - CloudWatch

> Goal: cover the standard, always-on CloudWatch integration every RDS instance has by default — the baseline monitoring layer beneath Performance Insights and Enhanced Monitoring.

---

## 1. What's included by default

Every RDS instance automatically publishes standard metrics to **CloudWatch** at **no extra cost**, hypervisor-sourced, at **1-minute granularity**:

- `CPUUtilization`, `FreeableMemory`, `FreeStorageSpace`
- `DatabaseConnections`
- `ReadIOPS` / `WriteIOPS`, `ReadLatency` / `WriteLatency`
- `ReplicaLag` (for Read Replicas and Multi-AZ readers)

---

## 2. Alarms on top

Standard CloudWatch **alarms** (`Monitoring` folder covers CloudWatch alarms generically) can trigger on any of these metrics — e.g. alert when `FreeStorageSpace` drops below a threshold, or `CPUUtilization` stays elevated, feeding into SNS notifications or automated remediation.

---

## 3. Where CloudWatch fits versus Notes 18-19

| | CloudWatch (this note) | Enhanced Monitoring (Note 19) | Performance Insights (Note 18) |
|---|---|---|---|
| Source | Hypervisor | Guest OS agent | Database engine's own performance data |
| Granularity | 1 minute | Down to 1 second | Per-query, continuous |
| Answers | "Is a metric abnormal?" | "What is the OS actually doing?" | "Which query, which wait event?" |
| Cost | Free, always on | Free (small CloudWatch Logs storage cost) | Free tier (7 days) or paid (up to 2 years) |

---

## 4. Recap

- Standard CloudWatch metrics are free, always-on, hypervisor-sourced, and the natural basis for **alarms** — the first layer of RDS monitoring, with Enhanced Monitoring and Performance Insights adding progressively deeper visibility on top.
- Next: Note 21 — RDS Monitoring, Performance Insights Vs Enhanced Monitoring Vs CloudWatch, consolidating all three.

### Sources
- [Monitoring Amazon RDS metrics with Amazon CloudWatch — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/MonitoringOverview.html)
