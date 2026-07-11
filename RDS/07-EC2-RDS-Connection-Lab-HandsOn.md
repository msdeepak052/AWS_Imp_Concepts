# 07 - EC2 - RDS Connection Lab

> Goal: connect to Note 06's private RDS instance from an EC2 instance in the same VPC — the standard, production-realistic way applications actually reach RDS.

---

## 1. Prerequisites

- The RDS instance from Note 06, with **public access disabled**.
- An EC2 instance launched in the **same VPC** (any subnet that has network reachability to the DB subnet group).

---

## 2. Security group wiring

This is the step that actually determines whether the connection works:

1. **RDS security group**: add an **inbound rule** for the database port (e.g. `3306` for MySQL), with source set to the **EC2 instance's security group** (not a CIDR range) — this is the same "reference a security group as the source" pattern used in `EC2/LoadBalancer/04-LB-Security-Group-Design-HandsOn`.
2. **EC2 security group**: no special inbound rule needed for this direction — outbound traffic is allowed by default in a security group's default outbound rule.

> ⚠️ A common lab mistake is leaving the RDS security group's inbound rule scoped to `0.0.0.0/0` or a broad CIDR "to make it work" — the correct fix is almost always referencing the **EC2 security group directly** as the source, keeping the database reachable only from instances that carry that specific security group.

---

## 3. Install a client and connect

```bash
sudo yum install -y mysql   # Amazon Linux; use mariadb105 or similar package name depending on AMI/engine
mysql -h <rds-endpoint> -P 3306 -u admin -p
```

- A successful connection from the EC2 instance, while the same connection attempt fails from outside the VPC (since public access is disabled), directly confirms the security-group-scoped, VPC-private access model.

---

## 4. Recap

- The database port's **inbound rule on the RDS security group** referencing the **EC2 security group as its source** is the actual mechanism enabling this connection — not any RDS-specific networking feature.
- This is the standard, production-realistic pattern: applications on EC2 (or, more commonly, behind an ALB/ASG) reach RDS privately within the VPC, with **no public access** needed at all.
- Next: Note 08 — RDS Availability & Durability, Single DB Instance, covering what happens (and doesn't happen) when this instance experiences a failure.

### Sources
- [Controlling access with security groups — AWS RDS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.RDSSecurityGroups.html)
- [Connecting to a DB instance running the MySQL engine — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ConnectToInstance.html)
