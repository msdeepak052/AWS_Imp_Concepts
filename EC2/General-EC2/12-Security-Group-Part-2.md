# 12 - Security Group — Part 2 (Rules in Depth)

> Goal: master **how to write good rules** — understanding **sources/destinations** (CIDR, "My IP", "Anywhere", security-group references), **multiple security groups**, and reading CIDR notation. Continues from Part 1's core idea that security groups are **stateful, allow-only firewalls attached to instances** (deny everything inbound by default, allow all outbound by default).

---

## 1. Reading CIDR notation (you must be comfortable with this)

A **CIDR** block describes a range of IPs: `IP_address/prefix`.

| CIDR | Meaning | # of addresses |
|---|---|---|
| `0.0.0.0/0` | **Anywhere** (the whole internet) | all IPv4 |
| `203.0.113.25/32` | **One specific IP** (the `/32` = single host) | 1 |
| `10.0.0.0/16` | A network (10.0.x.x) | 65,536 |
| `10.0.1.0/24` | A subnet (10.0.1.x) | 256 |
| `::/0` | Anywhere, **IPv6** | all IPv6 |

> 🧠 The smaller the number after `/`, the **bigger** the range. `/32` = one host; `/0` = everything.

---

## 2. The source/destination options when adding a rule

In the console "Source" (inbound) or "Destination" (outbound) dropdown you'll see:

1. **My IP** — auto-fills *your current public IP* as `x.x.x.x/32`. ✅ Safest for SSH/RDP while learning. (Note: it changes when your ISP gives you a new IP.)
2. **Anywhere-IPv4** — `0.0.0.0/0`. Use **only** for public services (HTTP 80 / HTTPS 443). ❌ Never for SSH/RDP/DB.
3. **Anywhere-IPv6** — `::/0`.
4. **Custom** — type any CIDR (e.g. office network `198.51.100.0/24`) or...
5. **Another Security Group** — reference an SG instead of an IP or CIDR. This means "allow traffic from any instance that is currently a member of that other security group," so the rule keeps working automatically as instances are added/removed (see section 5 below for a worked example).

---

## 3. Inbound vs Outbound rules — a worked example

Imagine a **web server** that users browse to, and which you also SSH into:

**Inbound rules:**
| Type | Port | Source | Why |
|---|---|---|---|
| HTTP | 80 | `0.0.0.0/0` (Anywhere) | Public website |
| HTTPS | 443 | `0.0.0.0/0` | Secure website |
| SSH | 22 | `My IP` /32 | Only you can log in |

**Outbound rules:**
| Type | Port | Destination | Why |
|---|---|---|---|
| All traffic | All | `0.0.0.0/0` | Default — server can fetch updates, call APIs |

Because SGs are **stateful**, you do **not** add outbound rules for the HTTP/SSH **responses** — they're automatically allowed.

---

## 4. Multiple security groups on one instance

- You can attach **several SGs** to a single instance.
- The effective permission is the **union (sum) of all allow rules** across those SGs.
- Example: SG-Web (allows 80/443) + SG-Admin (allows 22 from office) → instance allows 80, 443, and 22.
- This lets you build **reusable, layered** groups (one for web, one for admin, one for DB access).

> Because rules are purely additive and there's no deny, adding a group can only **open more**, never close existing access.

---

## 5. Referencing another Security Group as the source (intro)

Instead of an IP, a rule's source can be **another security group**. This means: "allow traffic from any instance that is a member of *that* security group."

Example — a web tier talking to a database tier:
- **DB security group** inbound rule: allow **MySQL 3306** from **source = `web-sg`** (the web servers' security group).
- Now **any** web server (whatever its IP) can reach the DB on 3306, and you never hard-code IPs.
- When Auto Scaling adds new web servers, they're automatically allowed (they're in `web-sg`).

This is hugely important for dynamic, multi-tier apps: because the rule points at the *group*, not at fixed IPs, it stays correct automatically as instances are added, removed, or replaced (e.g. by Auto Scaling) — nobody has to go back and edit firewall rules every time the fleet changes. Part 3 goes further and chains this pattern across a full three-tier app (load balancer → app → database).

---

## 6. Protocols you can specify

- **TCP** — most things (HTTP, SSH, RDP, MySQL).
- **UDP** — DNS (53), some streaming/games.
- **ICMP** — ping/traceroute (choose "All ICMP - IPv4" to allow ping).
- **All traffic** — every protocol/port (use sparingly).

> To allow **ping**, add an inbound rule **Type: All ICMP - IPv4** — ping is ICMP, not a TCP port.

---

## 7. Good rule-writing habits

- **Least privilege:** open the **narrowest** port range to the **narrowest** source that works.
- **Always add descriptions** ("office VPN", "ALB only") — future-you will thank you.
- **SSH/RDP → never `0.0.0.0/0`.** Use My IP, a VPN CIDR, or SSM Session Manager (no inbound port at all).
- Group rules logically into **purpose-based SGs** (web-sg, db-sg, bastion-sg).
- Prefer **SG references** over hard-coded IPs for internal tiers.

---

## 8. Quick reference: typical rule sets

**Bastion / jump host:** inbound SSH 22 from office/VPN only.
**Public web (behind ALB):** inbound 80/443 from the **ALB's security group** only.
**Database:** inbound 3306/5432 from the **app SG** only; no public access.

---

## 9. Recap

- **CIDR**: `/32` = one IP, `/0` = everything; smaller number = bigger range.
- Source options: **My IP**, **Anywhere (0.0.0.0/0)**, **Custom CIDR**, **another Security Group**.
- Stateful → no return rules needed.
- **Multiple SGs = additive union** of allows.
- **Reference SGs** instead of IPs for internal tiers (web→db).
- Least privilege; never expose 22/3389 to the world.
- Next (Note 13 / Part 3): SG vs NACL, SG references in depth, limits, troubleshooting.

---

### Sources
- [Security group rules – AWS docs](https://docs.aws.amazon.com/vpc/latest/userguide/security-group-rules.html)
- [Control traffic with security groups – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security-groups.html)
