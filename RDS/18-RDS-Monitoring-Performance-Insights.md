# 18 - RDS Monitoring - Performance Insights

> Goal: cover Performance Insights — RDS's database-load visualization tool for diagnosing *why* a database is slow, not just *whether* it's under load.

---

## 1. What it shows

**Performance Insights** visualizes **database load** (measured in **Average Active Sessions**, AAS) over time, broken down by:

- **SQL statement** — which specific queries are consuming the most load.
- **Wait event** — what the database engine was actually waiting on (I/O, lock, CPU) while processing those queries.
- **Host / User** — which connections are generating the load.

> 🧠 **Mental model:** where basic CloudWatch metrics (Note 20) tell you *that* CPU or connections spiked, Performance Insights tells you **which exact query** and **what it was waiting on** — the difference between a smoke alarm and a fire investigation.

---

## 2. Retention and cost

- **Free tier**: 7 days of retention, included at no extra cost.
- **Paid tier**: up to **2 years** of retention, for longer-term trend analysis (e.g. "is query performance degrading month over month").

---

## 3. Recap

- Performance Insights answers **why** a database is under load — by SQL statement, wait event, host, or user — going beyond basic utilization metrics.
- 7 days of retention is free; longer retention (up to 2 years) is a paid upgrade.
- Next: Note 19 — RDS Monitoring, Enhanced Monitoring, covering OS-level metrics.

### Sources
- [Monitoring DB load with Performance Insights — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PerfInsights.html)
