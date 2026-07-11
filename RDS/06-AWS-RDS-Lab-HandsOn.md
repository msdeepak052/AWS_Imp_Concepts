# 06 - AWS Relational Database Service (RDS) Lab

> Goal: launch a real RDS instance end to end, connecting the configuration concepts from Notes 12-17 (covered in depth later) to a concrete, working database for the first time.

---

## 1. Prerequisites

- A VPC with at least **2 subnets in different AZs** (RDS requires a **DB subnet group** spanning multiple AZs, even for a Single-AZ instance — Note 16 covers this in depth).
- A **security group** that will allow inbound database-port traffic only from trusted sources (e.g. an application security group — Note 16).

---

## 2. Create the RDS instance

1. **RDS console** → **Databases** → **Create database**.
2. **Engine**: choose one (e.g. **MySQL**) — Note 03's engine list.
3. **Templates**: choose **Free tier** or **Dev/Test** for a lab (skips Multi-AZ, uses a small instance class).
4. **Settings**: DB instance identifier, master username, master password (Note 13 covers credential options in depth).
5. **Instance configuration**: pick a small burstable instance class (e.g. `db.t3.micro`) for a lab — Note 14 covers instance class selection in depth.
6. **Storage**: default `gp3` storage, a small allocated size — Note 15 covers storage in depth.
7. **Connectivity**: choose the VPC, the DB subnet group, and whether to allow **public access** (leave **No** for a production-realistic setup — connect via EC2 in the same VPC instead, Note 07) — Note 16 covers connectivity in depth.
8. **Create database** — provisioning typically takes several minutes.

---

## 3. Connect to it

Once status shows **Available**, note the **endpoint** (a DNS name) and **port**.

```bash
mysql -h <rds-endpoint> -P 3306 -u admin -p
```

- If public access was disabled (recommended), this only works from **within the VPC** — Note 07 sets up an EC2 instance specifically to connect from inside the VPC.

---

## 4. Recap

- A working RDS instance requires, at minimum, a **DB subnet group** (spanning multiple AZs) and a **security group** scoping inbound access — even before touching any of the deeper configuration options covered later in this folder.
- Keeping **public access off** and connecting only from within the VPC (via EC2, Note 07) is the production-realistic, more secure default.
- Next: Note 07 — EC2-RDS Connection Lab, setting up an EC2 instance specifically to reach this database privately.

### Sources
- [Creating an Amazon RDS DB instance — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.html)
- [Working with DB subnet groups — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html)
