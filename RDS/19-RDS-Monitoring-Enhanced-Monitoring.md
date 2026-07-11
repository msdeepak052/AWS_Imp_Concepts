# 19 - RDS Monitoring - Enhanced Monitoring

> Goal: cover Enhanced Monitoring — real OS-level metrics gathered from the instance's actual operating system, distinct from both Performance Insights (Note 18) and standard CloudWatch (Note 20).

---

## 1. What it captures, and how

Enhanced Monitoring collects metrics directly from an **agent on the DB instance's operating system** — CPU (broken down by process), memory, file system, and disk I/O — at a granularity of up to **1 second**.

- This is fundamentally different from standard CloudWatch RDS metrics, which are gathered from the **hypervisor**, not the guest OS — hypervisor-level metrics can lag or smooth over short spikes that OS-level collection catches directly.

---

## 2. Retention and granularity

- Metrics can be gathered at intervals as low as **1 second** — far more granular than CloudWatch's standard 1-minute granularity for RDS.
- Retained in **CloudWatch Logs**, not the standard CloudWatch metrics namespace — with its own retention configuration.

> 🎯 **Exam tip:** "OS-level" or "process-level" CPU/memory visibility, or "sub-minute granularity," is the specific Enhanced Monitoring signal — plain CloudWatch metrics (Note 20) are hypervisor-sourced and capped at 1-minute granularity by default.

---

## 3. Recap

- Enhanced Monitoring gathers **OS-level** metrics via an agent on the instance itself, at up to **1-second** granularity — a different (and more granular, more truthful) data source than hypervisor-based CloudWatch metrics.
- Next: Note 20 — RDS Monitoring, CloudWatch, covering the standard hypervisor-level metrics and alarms.

### Sources
- [Enhanced Monitoring — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Monitoring.OS.html)
