# 12 - AWS RDS Setting Option

> Goal: map out the full RDS instance configuration surface at a glance, before Notes 13-17 go deep on each individual section.

---

## 1. The configuration sections, in creation order

| Section | Covered in |
|---|---|
| Engine options | Note 03 |
| Templates (Production / Dev-Test / Free tier) | This note |
| **Settings** — identifier, credentials | Note 13 |
| **Instance configuration** — class, burstable vs. standard | Note 14 |
| **Storage** — type, allocated size, auto scaling | Note 15 |
| **Connectivity** — VPC, subnet group, public access, security groups, port | Note 16 |
| **Database authentication** — password / IAM / Kerberos | Note 17 |
| Monitoring | Notes 18-21 |
| Additional configuration — initial DB name, parameter/option groups, backup retention, encryption, log exports, maintenance | Notes 22-26 |

---

## 2. Templates

- **Production**: defaults tuned for durability/availability (e.g. Multi-AZ suggested, deletion protection on).
- **Dev/Test**: fewer safety defaults, cost-oriented.
- **Free tier**: constrained to free-tier-eligible instance classes and storage, Single-AZ only.

> 🧠 Templates only set **initial defaults** — every individual setting underneath remains fully editable regardless of which template you start from.

---

## 3. Recap

- RDS instance creation walks through Engine → Template → Settings → Instance configuration → Storage → Connectivity → Authentication → Monitoring → Additional configuration — each covered in its own note going forward.
- Templates are just a starting-default convenience, not a locked-in configuration.
- Next: Note 13 — RDS Setting Option, Credentials Setting, covering the master username/password options in depth.

### Sources
- [Settings for DB instances — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.DBInstance.html)
- [Creating an Amazon RDS DB instance — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.html)
