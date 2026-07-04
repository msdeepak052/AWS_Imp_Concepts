# 11 - Security Group — Part 1 (Fundamentals)

> Goal: understand what a **Security Group (SG)** is, the single most important property (**stateful**), and the **default allow/deny behavior**. Parts 2–3 go deeper; Note 14 is the hands-on.

---

## 1. What is a Security Group?

A **Security Group** is a **virtual firewall** that controls **inbound and outbound traffic** for your EC2 instances (more precisely, for the instance's **Elastic Network Interface, ENI**).

- It sits **around the instance** (instance level), deciding which network traffic is allowed in and out.
- Every instance must have **at least one** security group.
- You can attach **multiple** SGs to one instance (rules are **combined/cumulative**).
- One SG can be attached to **many** instances.

> 🧠 **Analogy:** a security group is the **bouncer** at the instance's door, checking a guest list (the rules) for who may enter and leave.

---

## 2. The #1 thing to remember: Security Groups are STATEFUL

**Stateful** means: **if you allow traffic IN, the response is automatically allowed OUT** (and vice-versa) — you do **not** need a matching rule for the return traffic.

Example:
- You allow inbound **HTTP (80)** so users can reach your web server.
- The server's **response** back to the user is **automatically allowed out**, even if no outbound rule explicitly matches it.

This is different from **Network ACLs** (subnet-level), which are **stateless** — for a NACL, allowing inbound traffic does NOT automatically allow the matching outbound response; you must write a separate rule for each direction.

---

## 3. Allow-only model (no "deny" rules)

- Security group rules can only **ALLOW** traffic. **There is no explicit "deny" rule.**
- Anything **not explicitly allowed is implicitly denied.**
- So you build security by **listing what's permitted**, not by blocking things.

---

## 4. Default behavior (memorize)

When you create a **new** security group:

| Direction | Default rule | Meaning |
|---|---|---|
| **Inbound** | (empty) | **All inbound traffic is BLOCKED** by default. |
| **Outbound** | Allow **all** traffic (`0.0.0.0/0`) | The instance can reach out anywhere by default. |

So a brand-new SG: **nothing can come in, everything can go out.** You then add inbound rules for the ports you need (SSH 22, HTTP 80, etc.).

> The **default VPC security group** is slightly different: it allows all inbound traffic **from other instances in the same security group**, plus all outbound.

---

## 5. What a rule is made of

Each rule has:
- **Type / Protocol** — e.g. SSH, HTTP, HTTPS, Custom TCP, ICMP.
- **Port (range)** — e.g. 22, 80, 443, 3389, or a range.
- **Source** (inbound) / **Destination** (outbound) — who the rule applies to:
  - a single IP (`203.0.113.5/32`),
  - a CIDR range (`0.0.0.0/0` = anywhere, `10.0.0.0/16` = a network),
  - **another security group** (powerful — lets you allow traffic only from instances that belong to a specific security group, e.g. "allow port 3306 only from instances in the app-server SG", instead of hardcoding IP addresses),
  - a prefix list.
- **Description** (optional but recommended — e.g. "office VPN").

---

## 6. Common ports you'll allow

| Service | Port | Protocol |
|---|---|---|
| SSH (Linux login) | 22 | TCP |
| RDP (Windows login) | 3389 | TCP |
| HTTP (web) | 80 | TCP |
| HTTPS (secure web) | 443 | TCP |
| MySQL/Aurora | 3306 | TCP |
| PostgreSQL | 5432 | TCP |
| Ping (ICMP) | n/a | ICMP |

---

## 7. Scope and key facts

- Security groups are **Region- and VPC-specific** (an SG belongs to one VPC).
- Changes to SG rules take effect **immediately** (no reboot).
- SGs are attached to the **ENI**, so they follow the network interface.
- SGs are **free**.

---

## 8. The classic beginner symptom

> "My instance launched fine but I can't SSH / open the website."

90% of the time the cause is a **missing inbound security group rule** (e.g. port 22 or 80 not allowed for your IP). Because the default blocks all inbound, you must add the rule.

---

## 9. Recap

- Security Group = **stateful virtual firewall** at the instance/ENI level.
- **Stateful** → return traffic is auto-allowed (no return rule needed).
- **Allow-only** model; **everything not allowed is denied**.
- Default new SG: **inbound blocked, outbound all allowed**.
- A rule = protocol + port + source/destination.
- Next (Note 12 / Part 2): rules in depth — sources, CIDR, referencing other SGs, multiple SGs.

---

### Sources
- [Security groups for your VPC – AWS docs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html)
- [Control traffic to your EC2 instances using security groups – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security-groups.html)
