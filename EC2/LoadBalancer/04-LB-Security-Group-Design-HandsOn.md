# 04 - Load Balancer Security Group Design (Hands-On)

> Goal: build the **security-group chaining pattern** that makes `myapp-asg`'s backend instances completely unreachable from the internet except through `myapp-alb`. We create a new `myapp-alb-sg` and then tighten the existing `myapp-app-sg` (from `VPC\08`) to only trust it. Continues Note 03 (network prerequisites confirmed); Note 05 uses both security groups built here to actually create `myapp-alb`.

---

## 1. The problem with the current setup

Recall from `VPC\08-Public-and-Private-Subnets-HandsOn.md`: `myapp-app-sg` was originally scoped to trust `myapp-web-sg` (a single bastion-style public instance). Recall also from `EC2\ASG\02`'s prerequisites: it *assumed* `myapp-app-sg` already trusted "`myapp-alb`'s security group only" for HTTP:80 — but that security group didn't exist yet. **This note is where we build it for real.**

Without a dedicated ALB security group referenced as the source, you'd be tempted to either:
- Open `myapp-app-sg` inbound 80 to `0.0.0.0/0` (defeats the entire purpose of the private subnet), or
- Open it to the ALB's **subnet CIDRs** (`10.0.1.0/24`, `10.0.2.0/24`) — works, but also lets *anything else* in those subnets reach the app tier, not just the load balancer itself.

The correct pattern: give the load balancer **its own security group**, and reference *that security group* (not a CIDR) as the only trusted source on the app tier.

---

## 2. The SG-chaining pattern

```
Internet (0.0.0.0/0)
    │  HTTP 80 / HTTPS 443
    ▼
myapp-alb-sg  (attached to myapp-alb)
    │  outbound → myapp-app-sg only, on the app port
    ▼
myapp-app-sg  (attached to myapp-asg's instances)
    │  inbound ONLY from myapp-alb-sg
    ▼
myapp-asg instances
```

- **`myapp-alb-sg`** (new, built here): attached to `myapp-alb`. Inbound from the whole internet on the ports clients use; outbound restricted to only what the backend needs.
- **`myapp-app-sg`** (already exists, from `VPC\08` — updated here): inbound rule's **source** becomes `myapp-alb-sg` itself, not a CIDR, not "My IP."

> 🧠 This is the same tiered chaining pattern from `VPC\13-Security-Group-vs-NACL.md` and `VPC\08` (web-sg → app-sg), just one hop earlier in the chain: now it's **internet → alb-sg → app-sg → instances**.

**Why this is more secure:** with `myapp-app-sg` only trusting `myapp-alb-sg` as a source, `myapp-asg`'s instances become **completely unreachable directly from the internet**, even if someone discovers their private IPs (which shouldn't be routable from outside anyway, but defense in depth matters). Every single request **must** physically pass through `myapp-alb` first — there is no way to bypass it at the network layer.

---

## 3. Hands-on: create `myapp-alb-sg`

1. **EC2 console** → left nav → **Security Groups** → **Create security group**.
2. **Security group name**: `myapp-alb-sg`.
3. **Description**: `Security group for myapp-alb - allows inbound web traffic from the internet`.
4. **VPC**: `myapp-vpc`.
5. **Inbound rules** → **Add rule** (twice):

   | Type | Protocol | Port range | Source |
   |---|---|---|---|
   | HTTP | TCP | 80 | `0.0.0.0/0` |
   | HTTPS | TCP | 443 | `0.0.0.0/0` |

6. **Outbound rules** — remove the default "all traffic" rule and add a scoped one instead:

   | Type | Protocol | Port range | Destination |
   |---|---|---|---|
   | Custom TCP | TCP | 80 | `myapp-app-sg` (select the security group, not a CIDR) |

   This says: "`myapp-alb-sg` can only send traffic onward to whatever currently has `myapp-app-sg` attached, on port 80" — the load balancer can't accidentally (or maliciously, if compromised) reach anything else in the VPC.
7. **Create security group**.

> ⚠️ AWS Security Groups are **stateful** (Note `VPC\13`) — so you do **not** need a separate outbound rule to allow the *response* traffic back to clients; that's automatic. The outbound rule above only governs the ALB's **new, outbound-initiated** connections toward its targets.

---

## 4. Hands-on: update `myapp-app-sg` to trust only `myapp-alb-sg`

1. **Security Groups** → select the existing **`myapp-app-sg`**.
2. **Inbound rules** tab → **Edit inbound rules**.
3. Locate (or add) the rule for the application's listening port (HTTP:80, matching `myapp-tg`'s configuration in Note 05).
4. Set its **Source** to **Custom** → start typing `myapp-alb-sg` → select it from the dropdown (it resolves to the security group's ID, `sg-xxxxxxxx`).
5. **Remove** any inbound rule on this port sourced from `0.0.0.0/0` or a specific "My IP" — those defeat the purpose here.
6. **Save rules**.

`myapp-app-sg`'s inbound rules now look like:

| Type | Port | Source | Purpose |
|---|---|---|---|
| HTTP | 80 | `myapp-alb-sg` | Application traffic — **only from the load balancer** |
| SSH (demo/emergency) | 22 | Bastion/Session Manager path only (per `EC2\ASG\02` prerequisites) | Admin access, not app traffic |

---

## 5. Diagram: the complete SG chain

```mermaid
flowchart LR
    INTERNET(("Internet<br/>0.0.0.0/0")) -->|"HTTP 80 / HTTPS 443"| ALBSG["myapp-alb-sg<br/>(attached to myapp-alb)"]
    ALBSG -->|"outbound: port 80 only<br/>destination = myapp-app-sg"| ALB["myapp-alb"]
    ALB -->|"forwards via myapp-tg"| APPSG["myapp-app-sg<br/>inbound: port 80<br/>source = myapp-alb-sg ONLY"]
    APPSG --> INSTANCES["myapp-asg instances<br/>(myapp-private-subnet-1/2)"]

    INTERNET -.->|"direct attempt: BLOCKED"| INSTANCES

    style ALBSG fill:#1f6feb,color:#fff
    style APPSG fill:#8957e5,color:#fff
    style INSTANCES fill:#2ea043,color:#fff
```

A direct connection attempt from the internet straight to an instance's private IP never even reaches the SG evaluation stage in practice (private IPs aren't internet-routable), but even *if* traffic somehow arrived at the ENI, `myapp-app-sg` would drop it — the only permitted source is `myapp-alb-sg`.

---

## 6. Exam tips

🎯 **Exam tip:** referencing a **security group as a rule's source** (instead of a CIDR block) means the rule automatically covers **any instance that currently has that security group attached** — including instances launched later by scale-out, or ones that replace terminated instances. This is exactly why `myapp-app-sg` trusting `myapp-alb-sg` (rather than the ALB's subnet CIDRs or specific IPs) keeps working correctly as `myapp-asg` scales in and out (Notes `EC2\ASG\03-10`) with zero rule maintenance.

🎯 **Exam tip:** "how do you ensure backend instances are only reachable through the load balancer, never directly from the internet" → the expected answer is this exact SG-chaining pattern: create a dedicated SG for the load balancer, then scope the backend SG's inbound rule to that load balancer SG as the source — not a CIDR, not "0.0.0.0/0 restricted by NACL," and not relying on the instances simply lacking a public IP (defense in depth still applies even to private-subnet resources).

---

## 7. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `myapp-alb-sg` doesn't appear in `myapp-app-sg`'s source dropdown | Trying to reference a security group from a **different VPC** | Security group references only work within the same VPC (or specifically peered VPCs with extra config) — confirm both SGs are in `myapp-vpc` |
| ALB health checks fail after tightening `myapp-app-sg` | The health check port doesn't match the newly scoped inbound rule's port | Ensure `myapp-app-sg`'s inbound rule covers the same port as `myapp-tg`'s health check port (Note 05), not just the "main" traffic port if they differ |
| Clients can't reach `myapp-alb` at all | `myapp-alb-sg`'s inbound rule for 80/443 was scoped too narrowly (e.g. left as "My IP" from testing) | Re-open the appropriate port(s) to `0.0.0.0/0` (or your intended client CIDR) on `myapp-alb-sg` |
| Instances still reachable via an old rule | A leftover inbound rule (e.g. from `VPC\08`'s original `myapp-web-sg` reference, or an earlier `0.0.0.0/0` test rule) wasn't removed | Audit all inbound rules on `myapp-app-sg` and delete anything that isn't `myapp-alb-sg` or the controlled admin-access rule |

---

## 8. Recap

- Built **`myapp-alb-sg`**: inbound 80/443 from `0.0.0.0/0`, outbound restricted to `myapp-app-sg` on port 80 only.
- Updated **`myapp-app-sg`** (from `VPC\08`) to allow inbound **only from `myapp-alb-sg`**, removing any CIDR-based or "My IP" rules on the app port.
- This SG chain (`internet → myapp-alb-sg → myapp-alb → myapp-app-sg → myapp-asg instances`) makes the backend fleet unreachable from the internet by any path other than through the load balancer.
- Referencing a security group as a source (not a CIDR) is the exam-favored pattern precisely because it auto-covers instances added/replaced later — no rule maintenance needed as `myapp-asg` scales.
- Next: Note 05 — build `myapp-alb`, `myapp-tg`, and the HTTP:80 listener using exactly these two security groups.

---

### Sources
- [Security groups for your Application Load Balancer – AWS docs](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html#load-balancer-security-groups)
- [Update security groups for your Application Load Balancer – AWS docs](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-update-security-groups.html)
- [Security groups for your VPC – AWS docs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html)
