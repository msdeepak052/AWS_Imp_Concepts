# 25 - AWS RDS Log Exports

> Goal: cover publishing RDS engine logs to CloudWatch Logs — closing the gap between "the database has logs" and "you can actually search/alert on them."

---

## 1. Why this exists

By default, RDS engine logs (error logs, slow query logs, audit logs, general logs — engine-dependent) are only viewable/downloadable through the **RDS console or API**, in limited chunks — not searchable, not retained long-term, and not connected to alerting.

**Log Exports** publishes these logs continuously into **CloudWatch Logs**, where they can be:

- Searched with **CloudWatch Logs Insights** queries.
- Retained per your own configured retention policy (independent of RDS's own log rotation).
- Used as the trigger for **metric filters and alarms** (e.g. alert on a spike in slow-query log entries).

---

## 2. What's exportable (engine-dependent)

| Engine | Typical exportable logs |
|---|---|
| MySQL/MariaDB | Error log, slow query log, general log, audit log |
| PostgreSQL | PostgreSQL log, upgrade log |
| SQL Server | Error log, agent log |
| Oracle | Alert log, audit log, listener log, trace log |

---

## 3. Recap

- Log Exports streams RDS engine logs into **CloudWatch Logs**, unlocking searchability, custom retention, and alarm integration that the console's native log view doesn't provide.
- Exactly which logs are exportable depends on the engine.
- Next: Note 26 — AWS RDS Maintenance, covering patching windows.

### Sources
- [Publishing database logs to CloudWatch Logs — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.html#USER_LogAccess.Procedural.UploadtoCloudWatch)
