# 21 - RDS Monitoring - Performance Insights Vs Enhanced Monitoring Vs CloudWatch

> Goal: consolidate Notes 18-20 into one decision framework for exam scenarios asking "which monitoring tool answers this question?"

---

## 1. Side-by-side

| Question being asked | Right tool |
|---|---|
| "Is CPU/connections/storage abnormal right now?" | **CloudWatch** (Note 20) — always on, free, 1-minute granularity |
| "What is the guest OS actually doing — per-process CPU, memory, disk I/O?" | **Enhanced Monitoring** (Note 19) — OS-agent-sourced, up to 1-second granularity |
| "Which specific SQL query is causing database load, and what is it waiting on?" | **Performance Insights** (Note 18) — per-query, wait-event-level detail |

---

## 2. They're complementary, not competing

A real troubleshooting flow typically layers all three: a **CloudWatch alarm** fires on elevated `CPUUtilization` → **Enhanced Monitoring** shows which OS-level process is consuming that CPU → **Performance Insights** pinpoints the exact query and wait event responsible.

> 🎯 **Exam tip:** questions naming a specific investigative need ("which query," "OS-level per-process metrics," "is a metric threshold breached") are testing whether you know **which of the three tools** answers that specific question — not whether you'd enable all three (which is also a fine real-world default, but not usually what's being tested).

---

## 3. Recap

- CloudWatch (baseline, hypervisor metrics + alarms), Enhanced Monitoring (OS-level detail), and Performance Insights (query-level detail) form a layered monitoring stack, each answering a progressively deeper question.
- Next: Note 22 — AWS RDS DB Parameter Group & Option Group, covering engine-level configuration management.

### Sources
- [Monitoring Amazon RDS — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/MonitoringOverview.html)
- [Monitoring DB load with Performance Insights — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PerfInsights.html)
