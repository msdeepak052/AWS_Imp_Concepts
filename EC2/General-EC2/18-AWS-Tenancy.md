# 18 - AWS Tenancy (Shared, Dedicated Instance, Dedicated Host)

> Goal: understand **tenancy** — *who else's workloads share the physical server with you* — and the three options: **Shared (default)**, **Dedicated Instance**, and **Dedicated Host**. This matters for **compliance** and **bring-your-own-license**.

---

## 1. What is "tenancy"?

EC2 runs on big physical servers. **Tenancy** answers: **"Does my instance share that physical hardware with other AWS customers, or do I get the hardware to myself?"**

Three levels:

| Tenancy | Physical hardware | Cost | Why choose it |
|---|---|---|---|
| **Shared** (default) | Shared with other AWS customers (isolated by the hypervisor) | Cheapest | Normal workloads |
| **Dedicated Instance** | Hardware **dedicated to your account** (no other customers) | More | Compliance / isolation, without managing the host |
| **Dedicated Host** | A **whole physical server** you control & can see | Most | BYOL licensing, visibility into sockets/cores, compliance |

---

To clearly understand how instance placement changes across the three tenancy levels, visualize the underlying **physical racks/servers** inside an AWS data center.

Here is exactly how instances are placed relative to physical hosts and different AWS accounts:

---

### 1. Shared Tenancy (Default)

Your instance is placed on a server alongside virtual machines owned by completely different AWS customers. Strong logical isolation (via the hypervisor) keeps them secure, but you share the physical CPU, memory bus, and power supply.

```text
┌────────────────────────────────────────────────────────┐
│               PHYSICAL SERVER (HOST A)                 │
├───────────────┬──────────────────────┬─────────────────┤
│ Your Instance │ Customer B Instance  │ Cust. C Inst.   │
│  (Account 1)  │     (Account 2)      │   (Account 3)   │
└───────────────┴──────────────────────┴─────────────────┘

```

---

### 2. Dedicated Instance Tenancy

AWS dedicates the entire physical server hardware exclusively to *your* AWS account. No other customer's instances will ever be placed on this box. However, **AWS completely controls the placement.** If you stop and restart your instance, AWS might move it to a totally different physical box (Host B) that is also dedicated to you. You cannot see the underlying sockets or physical cores.

```text
┌────────────────────────────────────────────────────────┐
│               PHYSICAL SERVER (HOST B)                 │
├───────────────────────┬────────────────────────────────┤
│  Your Instance #1     │      Your Instance #2          │
│     (Account 1)       │        (Account 1)             │
└───────────────────────┴────────────────────────────────┘
  ▲
  │ AWS automatically manages placement. Stopping/starting 
  │ the instance might shift it to another dedicated server.

```

---

### 3. Dedicated Host Tenancy

You rent the entire physical server explicitly by its physical ID. You gain full visibility into the hardware layout (exactly how many physical sockets and cores exist). You choose exactly which instance lands on which socket. Because you own the host boundary, features like **Host Affinity** keep your instances permanently pinned to this exact physical box even through stops, restarts, and reboots—which is required to legally track socket/core-bound software licenses.

```text
┌────────────────────────────────────────────────────────┐
│          PHYSICAL SERVER ID: h-0123456789abcdef0       │
│  [Socket 1: 16 Cores]       │   [Socket 2: 16 Cores]   │
├─────────────────────────────┼──────────────────────────┤
│      Your Database          │     Your App Instance    │
│   (Pinned to Socket 1)      │   (Pinned to Socket 2)   │
└─────────────────────────────┴──────────────────────────┘
  ▲
  │ You control the physical sockets/cores. The instance 
  │ is structurally locked to this specific hardware host ID.

```
- You reserve an **entire physical server** and have **visibility into its sockets, physical cores, and host ID**.
- You control **which instances run on which host** and how they're placed.
- ✅ **Key use case — Bring Your Own License (BYOL):** software licensed **per physical socket/core** (e.g. some Windows Server, SQL Server, Oracle licenses) can be used legally because you can see and pin to the physical hardware.
- Can be purchased **On-Demand** or with a **Savings Plan / Dedicated Host Reservation** for discounts.
- Supports **host affinity** — keep an instance on the same host across stop/start (important for license tracking).
- Most management-heavy and **most expensive** option.
---

### 4. Summary of Placement Differences

* **Shared:** Multi-tenant box. Mixed accounts on one server.
* **Dedicated Instance:** Single-tenant box. Dedicated to your account, but you have no visibility into the host and AWS shifts instances around dynamically.
* **Dedicated Host:** Single-tenant box. Locked down to a specific host ID, providing layout visibility so you can manually map workloads to physical hardware sockets.


---

## 5. Comparison at a glance

| Feature | Shared | Dedicated Instance | Dedicated Host |
|---|---|---|---|
| Physical isolation from other accounts | ❌ (logical only) | ✅ | ✅ |
| Visibility of physical sockets/cores | ❌ | ❌ | ✅ |
| Control over instance placement on host | ❌ | ❌ | ✅ |
| BYOL (socket/core-based licenses) | ❌ | ❌ | ✅ |
| Billing unit | Per instance | Per instance (+ region fee) | Per host |
| Cost | $ | $$ | $$$ |
| Management overhead | Low | Low | High |

---

## 6. How to set tenancy (hands-on)

**At launch:**
1. Launch wizard → **Advanced details** → **Tenancy**:
   - **Shared** (default), **Dedicated** (Dedicated Instance), or **Dedicated host**.
2. For **Dedicated host**, first **allocate a host**: EC2 → **Dedicated Hosts → Allocate Dedicated Host** (pick instance family, AZ), then launch onto it.

> ⚠️ Dedicated Hosts/Instances cost significantly more — **don't allocate one just to experiment** unless you intend to pay. For learning, understanding the concepts is enough.

**Note:** Tenancy can be set at the **VPC** level too (default tenancy = dedicated forces all instances in that VPC to be dedicated).

---

## 7. When to choose what (decision guide)

- **Default everything → Shared.** (99% of cases.)
- Need **physical isolation** for compliance, but no licensing concerns → **Dedicated Instance**.
- Need **socket/core BYOL** or strict host visibility/placement (Windows/SQL/Oracle licensing, certain regulations) → **Dedicated Host**.

---

## 8. Don't confuse tenancy with...

- **Placement Groups** → a separate setting that controls how **your own** instances are physically arranged relative to each other (packed close for speed, or spread apart for fault isolation) — it's about *latency/fault isolation* among your instances, not about whether you share hardware with other AWS customers.
- **Reserved Instances / Savings Plans** → these are billing commitments where you agree to pay for a certain configuration or spend level for 1–3 years in exchange for a discount — about *pricing commitment*, not hardware sharing. (You **can** combine, e.g. Dedicated Host + Savings Plan.)

---

## 9. Recap

- **Tenancy = do you share the physical server?**
- **Shared** (default, cheapest) → **Dedicated Instance** (account-isolated hardware) → **Dedicated Host** (whole server, BYOL, full visibility, priciest).
- Dedicated Host is the answer for **per-socket/core licensing (BYOL)** and host-level control.
- Set at launch (Advanced details) or VPC default tenancy.
- Next (Note 19): **EC2 Purchase Options Part 1** — how you pay (On-Demand, Reserved, Savings Plans, Spot…).

---

### Sources
- [Dedicated Instances – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/dedicated-instance.html)
- [Dedicated Hosts – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/dedicated-hosts-overview.html)
- [Bring your own licenses with Dedicated Hosts – AWS](https://aws.amazon.com/ec2/dedicated-hosts/)
