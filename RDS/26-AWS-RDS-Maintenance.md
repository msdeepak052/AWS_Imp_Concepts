# 26 - AWS RDS Maintenance

> Goal: cover the maintenance window mechanism — how RDS applies OS and engine patches without surprising you, and the difference between required and optional updates.

---

## 1. The maintenance window

A weekly **30-minute (minimum) window** you configure (day + time), during which RDS applies any **pending maintenance items** — OS patches, engine minor-version upgrades, or scheduled changes you made that require a reboot.

- Outside a required item's window, most **non-critical** pending changes just sit queued until the next window; you can also **apply them immediately** on demand instead of waiting.
- **Multi-AZ deployments** apply patches to the **standby first**, fail over, then patch the (now-standby) former primary — minimizing downtime to roughly one failover's worth, versus a full outage on a Single-AZ instance during the same patch.

---

## 2. Required vs. optional updates

- **Security patches classified as required** will be applied automatically even outside your chosen window if left pending too long — AWS won't let a known critical vulnerability go unpatched indefinitely.
- **Engine version upgrades** (e.g. MySQL 8.0.x → 8.0.y) can be configured for **auto minor version upgrade**, letting RDS apply them automatically during your maintenance window as they become available.
- **Major version upgrades** (e.g. MySQL 5.7 → 8.0) are **never automatic** — always a deliberate, manually-triggered action, since they can include breaking changes.

> 🎯 **Exam tip:** "minimize downtime during patching" is a Multi-AZ signal (patch-standby-then-failover pattern); "we need to control exactly when patches apply" points to a **deliberately chosen maintenance window**, disabling auto minor version upgrade if even minor-version timing needs to be fully manual.

---

## 3. Recap

- The **maintenance window** is when RDS applies pending patches/upgrades; Multi-AZ deployments patch the standby first and fail over, minimizing downtime versus Single-AZ.
- Minor version upgrades can be automated; major version upgrades are always manual and deliberate.
- Next: Note 27 — AWS RDS Read Replica, the first of the scaling/modern-features notes.

### Sources
- [Maintaining a DB instance — AWS docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html)
