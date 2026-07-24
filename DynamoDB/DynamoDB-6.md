## 📘 What is **DynamoDB Backup**?

DynamoDB offers **on-demand and continuous backups** to protect your data. You can back up entire tables (including GSIs, LSIs, and stream settings) **without affecting performance or availability**.

---

## 🔐 Backup Types in DynamoDB

| Backup Type                       | Description                                                 |
| --------------------------------- | ----------------------------------------------------------- |
| **On-Demand Backup**              | Create a backup manually at any time                        |
| **Point-in-Time Recovery (PITR)** | Automatically backs up every write for the last **35 days** |

---

## 🔧 1. On-Demand Backup

* **Manual or automated via scripts**
* Stored until **explicitly deleted**
* Good for **compliance, migrations, snapshots before updates**

### ✅ Example (AWS CLI):

```bash
aws dynamodb create-backup \
  --table-name Orders \
  --backup-name OrdersBackup-June30
```

### ✅ Terraform Example:

```hcl
resource "aws_dynamodb_table" "orders" {
  name         = "Orders"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "OrderID"

  attribute {
    name = "OrderID"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_dynamodb_table_backup" "orders_backup" {
  table_name = aws_dynamodb_table.orders.name
  backup_name = "OrdersSnapshot"
}
```

---

## 🔧 2. Point-in-Time Recovery (PITR)

* Automatically captures **every write** for **35 days**
* You can **restore** the table to **any second-level timestamp** in that range
* Ideal for recovery from accidental deletes, logic bugs, or corruption

### ✅ Example: Restore from PITR

```bash
aws dynamodb restore-table-to-point-in-time \
  --source-table-name Orders \
  --target-table-name Orders_Restored \
  --restore-date-time 2025-06-29T23:59:00Z
```

---

## ✅ Use Cases

| Use Case                                 | Backup Type | Why Useful                                        |
| ---------------------------------------- | ----------- | ------------------------------------------------- |
| 💼 **Data migration**                    | On-Demand   | Snapshot before moving to another region/account  |
| 🔄 **Schema upgrade/testing**            | On-Demand   | Backup before making risky schema or code changes |
| 🛠️ **Accidental item deletion**         | PITR        | Restore to just before deletion happened          |
| 🔍 **Audit & compliance**                | On-Demand   | Periodic backups for regulatory requirements      |
| 💣 **Corruption by faulty logic/deploy** | PITR        | Roll back to a known good point in time           |

---

## ⚠️ Important Notes

* **Backups are region-specific**
* PITR only supports **restoring to a new table**, not overwriting existing one
* Global Tables: PITR and on-demand backups **must be enabled per replica region**
* **Costs**: Backup size determines cost; PITR incurs **ongoing storage charges**

---

## 🧠 Summary

| Feature                 | On-Demand Backup      | Point-in-Time Recovery (PITR) |
| ----------------------- | --------------------- | ----------------------------- |
| **Manual/Auto**         | Manual                | Auto (once enabled)           |
| **Restore granularity** | Latest snapshot only  | Any second in last 35 days    |
| **Retention**           | Until deleted         | Always 35 days                |
| **Use cases**           | Migration, compliance | Bug fixes, accident rollback  |

---


