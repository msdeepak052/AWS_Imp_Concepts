# 16 - AWS RDS Connectivity

> Goal: cover the networking side of RDS in depth — DB subnet groups, public access, security groups, and ports — the mechanism behind Notes 06-07's hands-on labs.

---

## 1. DB subnet groups

A **DB subnet group** is a named collection of subnets (spanning **at least 2 AZs**) that RDS is allowed to place instances/standbys into — required even for a Single-AZ instance, since it defines the pool of AZs available if you later enable Multi-AZ.

---

## 2. Public access

- **Public access: No** (recommended default) — the instance gets **no public IP**; reachable only from within the VPC (directly, via VPC peering, VPN, Direct Connect, or a bastion/EC2 instance — Note 07's pattern).
- **Public access: Yes** — the instance gets a publicly resolvable endpoint; still gated by the **security group**, but exposes the database to the internet at the network layer, which is rarely appropriate for production.

> ⚠️ "Public access: Yes" does **not** mean "open to everyone" by itself — the security group's inbound rules are still enforced. But it does widen the attack surface unnecessarily for most architectures, where the application tier already lives in the same VPC.

---

## 3. Security groups and ports

- Each engine has a **default port** (MySQL/Aurora MySQL: 3306, PostgreSQL/Aurora PostgreSQL: 5432, SQL Server: 1433, Oracle: 1521) — configurable at creation.
- The RDS security group's inbound rule should reference the **application/EC2 security group** as its source (Note 07), not a broad CIDR range.

---

## 4. Recap

- A **DB subnet group** (2+ AZs) is required infrastructure regardless of availability tier; **public access** should default to **No** for anything beyond a quick public-facing lab; security group inbound rules should reference the calling tier's security group directly, not open CIDR ranges.
- Next: Note 17 — AWS RDS Database Authentication, covering password, IAM, and Kerberos authentication options.

### Sources
- [Working with a DB instance in a VPC — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html)
- [Controlling access with security groups — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.RDSSecurityGroups.html)
