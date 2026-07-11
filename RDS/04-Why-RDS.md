# 04 - Why RDS?

> Goal: make the explicit business/operational case for RDS — the concrete pains it removes versus self-hosting a database on EC2.

---

## 1. The pains of self-managing a database on EC2

If you ran MySQL or PostgreSQL yourself on an EC2 instance, **you** would be responsible for:

- Installing, patching, and upgrading both the **OS** and the **database engine** — including urgent security patches, on your own schedule.
- Configuring and testing **backups**, and building your own restore/point-in-time-recovery tooling.
- Building your own **replication** setup for high availability, and writing/testing your own **failover** logic.
- Monitoring disk space, memory, CPU, and replication lag yourself, wiring up your own alerting.
- Scaling storage — manually resizing EBS volumes and the filesystem, then the database, without downtime if possible.

---

## 2. What RDS removes

| Self-managed pain | RDS's answer |
|---|---|
| Manual OS/engine patching | Automated **maintenance windows** (Note 26) with configurable auto-patching |
| Building your own backup tooling | **Automated backups** with point-in-time recovery, plus on-demand **manual snapshots** (Note 23) |
| Building your own HA/failover | **Multi-AZ** deployments — AWS handles synchronous replication and automatic failover (Notes 09-10) |
| Manual storage resizing | **Storage auto scaling** — RDS grows storage automatically as needed (Note 15) |
| Building your own monitoring | Built-in **CloudWatch metrics**, **Enhanced Monitoring**, and **Performance Insights** (Notes 18-21) |
| Scaling reads by hand | **Read Replicas** — a few clicks (Note 27) |

---

## 3. What you give up

- **Root/OS-level access** — you can't SSH into the underlying instance or install arbitrary OS-level software.
- Some **engine-specific advanced configuration** — RDS restricts certain settings/extensions that would conflict with its managed operations model (though **Parameter Groups**, Note 22, expose a great deal of tunability).
- **Engine version choice is bounded** by what RDS currently supports for that engine — you don't control the exact build.

> 🎯 **Exam tip:** "reduce operational overhead of managing a database" and "automated backups/patching/failover without building it ourselves" are the standard RDS-signaling phrases on the SAA-C03 exam — contrasted against "need full OS-level control of the database server," which points back toward self-managed EC2.

---

## 4. Recap

- RDS trades a small amount of low-level control (no OS/root access, bounded engine versions) for a large reduction in operational burden: patching, backups, HA/failover, storage scaling, and monitoring are all handled for you.
- Next: Note 05 — On-Premises Vs Amazon EC2 Vs Amazon RDS, placing all three options side by side.

### Sources
- [Overview of Amazon RDS — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)
- [Amazon RDS features](https://aws.amazon.com/rds/features/)
