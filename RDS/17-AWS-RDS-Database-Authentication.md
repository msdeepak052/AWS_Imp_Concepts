# 17 - AWS RDS Database Authentication

> Goal: cover the three ways a client can authenticate to an RDS database engine itself — distinct from IAM's control over the RDS *service* API.

---

## 1. The three options

| Method | How it works |
|---|---|
| **Password authentication** | Standard database username/password, native to the engine itself |
| **IAM database authentication** | Clients generate a short-lived (15-minute) **auth token** via IAM/STS instead of a stored password, then use that token as the "password" in the normal connection handshake |
| **Kerberos authentication** | Integrates with **AWS Managed Microsoft AD**, for centralized enterprise identity — MySQL, PostgreSQL, Oracle, SQL Server support this |

---

## 2. IAM database authentication in depth

- Requires the connecting principal (an IAM user or role — e.g. an EC2 instance role) to have `rds-db:connect` permission scoped to the specific DB user.
- The **auth token replaces the password**, generated fresh per connection attempt and valid for **15 minutes** — removing the need to store or rotate a database password for that connection path at all.
- **Limitations**: currently supported only for MySQL, PostgreSQL, and MariaDB (not Oracle/SQL Server); not intended for very high connection-rate workloads, since token generation adds a small overhead per new connection — a **connection pooler** (e.g. RDS Proxy, Note 30) is the recommended pairing at scale.

> 🧠 **Mental model:** IAM database authentication is the database-login equivalent of `IAM/08`'s temporary STS credentials — no long-lived secret, short-lived token, generated on demand by an already-authenticated IAM principal.

---

## 3. Recap

- **Password auth** is the engine-native default; **IAM database authentication** replaces the password with a short-lived, IAM-generated token (MySQL/PostgreSQL/MariaDB only); **Kerberos** integrates with AWS Managed Microsoft AD for enterprise centralized identity.
- IAM auth removes stored database passwords for supported engines but is best paired with a connection pooler (RDS Proxy) at high connection rates.
- Next: Note 18 — RDS Monitoring, Performance Insights.

### Sources
- [IAM database authentication for MariaDB, MySQL, and PostgreSQL — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html)
- [Kerberos authentication — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/kerberos-authentication.html)
