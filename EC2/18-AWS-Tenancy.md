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

## 2. Shared Tenancy (default)

- Your instance may run on the same physical host as **other customers**, but each is strongly **isolated by virtualization** (you can't see or reach theirs).
- **Cheapest** and used for the vast majority of workloads.
- This is what you've been launching in earlier notes.

---

## 3. Dedicated Instance

- Runs on hardware **dedicated to a single customer (your account)** — no other AWS customers share that physical server.
- You **don't** get visibility/control over the specific physical host; AWS still places your instances on dedicated hardware for you.
- Billed **per instance** (plus a regional per-Region dedicated fee).
- ✅ Use when: regulatory/compliance rules require physical isolation from other tenants, but you don't need host-level control or socket-based licensing.

---

## 4. Dedicated Host

- You reserve an **entire physical server** and have **visibility into its sockets, physical cores, and host ID**.
- You control **which instances run on which host** and how they're placed.
- ✅ **Key use case — Bring Your Own License (BYOL):** software licensed **per physical socket/core** (e.g. some Windows Server, SQL Server, Oracle licenses) can be used legally because you can see and pin to the physical hardware.
- Can be purchased **On-Demand** or with a **Savings Plan / Dedicated Host Reservation** for discounts.
- Supports **host affinity** — keep an instance on the same host across stop/start (important for license tracking).
- Most management-heavy and **most expensive** option.

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

- **Placement Groups** (Note 17) → about *latency/fault isolation* among **your own** instances, not about sharing with other customers.
- **Reserved Instances / Savings Plans** (Notes 19–21) → about *pricing commitment*, not hardware sharing. (You **can** combine, e.g. Dedicated Host + Savings Plan.)

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
