# 22 - Must-Know DynamoDB Backup for AWS Exams!

> Goal: cover DynamoDB's two backup mechanisms — On-Demand backups and Point-in-Time Recovery (PITR) — the DynamoDB analogue to RDS's manual snapshots vs. automated backups (`RDS/23`).

---

## 1. On-Demand backups

- Full backups of a table, taken **whenever you choose**, with **no performance impact** on the table (unlike some traditional database backup mechanisms).
- **Retained indefinitely**, until explicitly deleted — directly parallel to `RDS/23`'s manual snapshots.
- Restoring **always creates a new table** — never restores in place, same pattern as RDS.

---

## 2. Point-in-Time Recovery (PITR)

- Once enabled, continuously backs up the table, allowing restore to **any second** within the retention window — either **35 days** (standard) or up to **years**, depending on the retention option chosen.
- Directly parallel to `RDS/23`'s automated backups + point-in-time recovery — same underlying idea (continuous capture, restore to any second), applied to DynamoDB's data model.
- **Not enabled by default** — must be explicitly turned on per table.

---

## 3. Side-by-side

| | On-Demand Backup | Point-in-Time Recovery (PITR) |
|---|---|---|
| When taken | Manually, on demand | Continuous, automatic (once enabled) |
| Retention | Indefinite, until deleted | Configurable window (up to 35 days standard, longer available) |
| Restore granularity | To the exact moment the backup was taken | To **any second** within the retention window |
| Enabled by default | No (manual action each time) | No (must explicitly enable the feature, then it's continuous) |

> 🎯 **Exam tip:** "restore to a specific point in time, any second" → **PITR**. "Keep an indefinite, deliberately-taken backup, e.g. before a risky change" → **On-Demand backup**. Same conceptual split as `RDS/23`'s automated-backups-vs-manual-snapshots.

---

## 4. Recap

- **On-Demand backups** are manual, indefinite-retention full backups; **PITR** is continuous, once enabled, allowing restore to any second within its retention window — both always restore as a **new table**.
- Next: Note 23 — How To Export S3 In DynamoDB?, covering exporting table data to S3 for analytics.

### Sources
- [Backing up and restoring DynamoDB — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/BackupRestore.html)
- [Point-in-time recovery — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/PointInTimeRecovery.html)
