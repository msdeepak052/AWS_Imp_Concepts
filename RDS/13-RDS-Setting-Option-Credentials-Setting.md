# 13 - RDS Setting Option - Credentials Setting

> Goal: cover the master username/password options in depth, including AWS Secrets Manager-managed credentials — the more secure, modern default.

---

## 1. The two options

| Option | How it works |
|---|---|
| **Self-managed** | You type a master password yourself at creation time; you own rotating/storing/protecting it. |
| **Managed in AWS Secrets Manager** | RDS generates a strong random password and stores it as a **Secrets Manager secret**; you never see or type the raw password, and can enable **automatic rotation** on a schedule. |

> 🧠 **Mental model:** this is the same "let AWS hold and rotate the secret" pattern as IAM access keys vs. STS temporary credentials (`IAM/08-IAM-Roles-Best-Practices-HandsOn`) — avoiding a long-lived, manually-managed secret in favor of a managed, rotatable one.

---

## 2. Why Secrets Manager-managed credentials are the better default

- **No hardcoded password** ever needs to exist in application config or in your own memory.
- **Automatic rotation** on a schedule (e.g. every 30/60/90 days) without any application downtime, since RDS coordinates the rotation with the secret update.
- Applications retrieve the current password at runtime via the **Secrets Manager API** (or SDK), always getting the live value — never a stale, manually-copied one.

> ⚠️ There's a small added cost (Secrets Manager charges per secret, per API call) and a dependency — your application now needs IAM permission to call Secrets Manager at runtime, and network reachability to it — but this is normally a worthwhile trade for eliminating hardcoded database passwords.

---

## 3. Recap

- RDS credentials can be **self-managed** (you set and remember the password) or **Secrets Manager-managed** (AWS generates, stores, and can auto-rotate it).
- The Secrets Manager option removes hardcoded passwords entirely and adds automatic rotation — the recommended default for anything beyond a quick lab.
- Next: Note 14 — AWS RDS Instance Configuration, covering instance class selection.

### Sources
- [Password management with Amazon RDS and AWS Secrets Manager — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-secrets-manager.html)
- [Rotating AWS Secrets Manager secrets — AWS docs](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets.html)
