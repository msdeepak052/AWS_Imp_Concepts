# 13 - Security Group — Part 3 (SG vs NACL, References, Limits, Troubleshooting)

> Goal: finish the security-group picture — **chaining SGs by reference**, **Security Group vs Network ACL**, **limits/quotas**, and a **troubleshooting checklist** you'll use constantly.

---

## 1. Security Group references (the multi-tier pattern in full)

A rule's source/destination can be **another security group ID** instead of an IP range. It means *"allow traffic from instances that belong to that SG."*

**Three-tier web app:**

```
Internet → [ALB:  alb-sg ] → [ Web/App EC2: app-sg ] → [ RDS DB: db-sg ]
```

| SG | Inbound rule | Source |
|---|---|---|
| `alb-sg` | HTTP 80 / HTTPS 443 | `0.0.0.0/0` (public) |
| `app-sg` | HTTP 80 | **`alb-sg`** (only the load balancer can reach the app) |
| `db-sg` | MySQL 3306 | **`app-sg`** (only app servers can reach the DB) |

**Why this is great:**
- **No hard-coded IPs** — works even as instances scale in/out and IPs change.
- **Self-documenting tiers** — you can read the security posture from the references.
- Add a new app server (Auto Scaling) → it's in `app-sg` → instantly allowed to the DB. No rule edits.

> An SG can even **reference itself** — e.g. allow all instances in `cluster-sg` to talk to each other on a port (useful for clustered apps).

---

## 2. Security Group vs Network ACL (NACL) — the classic comparison

Both are firewalls, but at **different layers**:

| Feature | **Security Group** | **Network ACL (NACL)** |
|---|---|---|
| Level | **Instance / ENI** | **Subnet** |
| State | **Stateful** (return traffic auto-allowed) | **Stateless** (must allow both directions) |
| Rules | **Allow only** | **Allow AND Deny** |
| Rule evaluation | All rules evaluated (union) | **Numbered order**, first match wins (lowest # first) |
| Applies to | The instances it's attached to | **All** instances in the subnet |
| Default | New SG: deny inbound, allow outbound | Default NACL: allow all in/out |
| Use case | Primary, everyday control | Coarse subnet-wide guardrails, **explicit deny** (e.g. block a bad IP) |

**Key takeaways:**
- SGs are your **primary** tool. NACLs are a secondary, subnet-wide layer.
- Only **NACLs can DENY** — use them to block a specific malicious IP range.
- NACLs being **stateless** is the gotcha: you must allow **ephemeral ports (1024–65535)** for return traffic.
- Traffic must pass **both** the NACL (subnet) and the SG (instance) to reach the instance.

---

## 3. Limits / quotas (defaults, can be raised)

| Item | Default limit |
|---|---|
| Security groups per VPC | 2,500 |
| Inbound rules per SG | 60 (IPv4) + 60 (IPv6) |
| Outbound rules per SG | 60 (IPv4) + 60 (IPv6) |
| Security groups per ENI | 5 (can raise to 16) |

> If you hit "too many rules," consolidate using **prefix lists** (a named set of CIDRs) or **SG references**.

---

## 4. Stateful behavior — the subtle detail

- SGs track connections. A reply to an allowed inbound request is allowed out **regardless** of outbound rules; a reply to an allowed outbound request is allowed back in.
- This is why you rarely touch outbound rules — the default "allow all outbound" plus statefulness covers most needs.

---

## 5. Troubleshooting checklist — "I can't connect to my instance"

Work down this list:

1. **Right Region?** Instance + SG are Region-scoped (top-right of console).
2. **Instance running + 2/2 status checks?**
3. **Security group inbound rule** for the port exists? (22 for SSH, 3389 RDP, 80/443 web.)
4. **Source** of that rule includes **your current IP**? (Your home IP may have changed → set "My IP" again.)
5. **Public IP / Elastic IP** assigned? A brand-new instance in a public subnet gets an auto-assigned public IPv4 address that changes if you stop/start it; an **Elastic IP** is a static public IP you allocate and attach yourself so it doesn't change. Without one of these attached, there's no address for the internet to reach.
6. **Public subnet**? Route table has `0.0.0.0/0 → Internet Gateway`?
7. **Network ACL** on the subnet allows the port **and** ephemeral return ports (1024–65535)?
8. **OS-level firewall** (Windows Firewall, `firewalld`/`ufw`) not blocking?
9. **Correct username/key** for SSH? (`ec2-user`, `ubuntu`, etc. + the right `.pem`.)
10. App actually **listening** on the port? (`sudo ss -tlnp` on Linux.)

> 95% of beginner connection failures = step 3 or 4 (missing/incorrect SG inbound rule).

---

## 6. Best practices summary

- **Least privilege**: smallest ports, smallest sources.
- **Never** open 22/3389 to `0.0.0.0/0`; prefer **My IP**, VPN, or **SSM Session Manager** (zero inbound ports).
- Use **SG references** for internal tiers, not IPs.
- One **purpose per SG** (web/db/bastion) for reuse and clarity.
- Add **descriptions** to every rule.
- Use **NACLs** only for coarse subnet rules or explicit **deny**.

---

## 7. Recap

- **SG references** chain tiers (alb→app→db) without IPs — scales automatically.
- **SG = stateful, instance-level, allow-only**; **NACL = stateless, subnet-level, allow+deny, ordered**.
- Traffic must pass **both** NACL and SG.
- Memorize the **troubleshooting checklist**.
- Next (Note 14): **hands-on** — create SGs, add/edit rules, and test allow vs block.

---

### Sources
- [Security groups vs network ACLs – AWS docs](https://docs.aws.amazon.com/vpc/latest/userguide/infrastructure-security.html)
- [Network ACLs – AWS docs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html)
- [Amazon VPC quotas – AWS docs](https://docs.aws.amazon.com/vpc/latest/userguide/amazon-vpc-limits.html)
