# 03 - What Is Relational Database Services?

> Goal: define precisely what RDS manages on your behalf versus what you still control, and list the database engines it supports.

---

## 1. What AWS manages for you

RDS takes over the **undifferentiated heavy lifting** of running a relational database:

- **Provisioning** the underlying EC2 instance and EBS storage.
- **OS and database engine patching** (with a configurable maintenance window — Note 26).
- **Automated backups** and point-in-time recovery (Note 23).
- **Replication** for Multi-AZ high availability (Notes 09-10) and Read Replicas (Note 27).
- **Monitoring** integration (Notes 18-21).
- **Failure detection and automatic failover** (Multi-AZ deployments).

---

## 2. What you still control

- **Schema design**: tables, indexes, relationships — RDS runs a real MySQL/PostgreSQL/etc. engine, so all normal database design work still applies.
- **Instance class and storage sizing** (Notes 14-15).
- **Security groups, VPC placement, subnet groups** (Note 16).
- **Database-level users/permissions** (Note 17), on top of IAM-level access control to the RDS *service* itself.
- **Query performance tuning** — RDS doesn't optimize your SQL for you.

---

## 3. Supported engines

| Engine | Notes |
|---|---|
| **MySQL** | Widely used open-source engine |
| **PostgreSQL** | Open-source, feature-rich, popular for complex data types |
| **MariaDB** | MySQL-compatible fork |
| **Oracle** | Commercial, license-included or bring-your-own-license (BYOL) |
| **SQL Server** | Commercial, license-included or BYOL |
| **Amazon Aurora** | AWS-built, MySQL/PostgreSQL-compatible, higher performance and different HA architecture (Note 38) |

> 🧠 **Mental model:** RDS is really a **managed hosting layer** wrapped around several distinct, real database engines — it doesn't invent a new query language or data model; it takes engines you likely already know and removes the operational burden of running them yourself.

---

## 4. Recap

- RDS manages provisioning, patching, backups, replication, and failover; you still own schema design, sizing, network/security configuration, and query tuning.
- RDS supports **MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, and Aurora** — the same relational engines you'd otherwise self-host, just with the operational burden removed.
- Next: Note 04 — Why RDS, making the explicit case for choosing it over self-managed alternatives.

### Sources
- [What is Amazon Relational Database Service (Amazon RDS)? — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)
- [Amazon RDS supported database engines](https://aws.amazon.com/rds/database-engines/)
