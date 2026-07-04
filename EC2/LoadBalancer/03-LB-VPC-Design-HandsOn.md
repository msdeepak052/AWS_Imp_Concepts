# 03 - Load Balancer VPC Design (Hands-On)

> Goal: verify the **network prerequisites** an Application Load Balancer needs. This note does **not** create a VPC or subnets from scratch — it assumes you already have a VPC with public and private subnets (built however you like, in this repo or elsewhere), and walks through confirming that VPC's subnets actually satisfy what `demo-alb` will require in Note 05. Continues Note 02 (terminology); Note 04 layers security groups on top of this same network.

---

## 1. What an ALB/NLB actually requires from the network

Before you can even open the "Create Load Balancer" wizard successfully, the underlying VPC must satisfy a few hard requirements — these are **enforced by the console/API**, not just best-practice suggestions:

1. **At least 2 Availability Zones.** You must select subnets in **2 or more different AZs** — AWS will not let you create an ALB/NLB with only one AZ enabled. Each enabled AZ gets its own load balancer node.
2. **One subnet per AZ, per load balancer.** You cannot pick two subnets that happen to sit in the same AZ — the console will only let you select one subnet per AZ.
3. **Subnet size matters.** AWS recommends each selected subnet have a CIDR block of at least `/27` (giving at least 8 free IP addresses) — the load balancer reserves IPs in each subnet to scale itself, and can enter a degraded state if it runs out.
4. **Internet-facing vs internal changes which subnets are valid:**
   - **Internet-facing** load balancer → needs subnets with a route to an **Internet Gateway** (public subnets).
   - **Internal** load balancer → needs subnets **without** a direct IGW route (private subnets) — clients must already be inside the VPC (or connected via VPN/peering/Transit Gateway) to reach it.

🎯 **Exam tip:** "Highly available load balancer" on the exam always means **2+ AZs, 2+ subnets** — a design that only enables one AZ for the ALB is a guaranteed wrong answer on an HA question, and the console won't even let you build it that way.

---

## 2. Internet-facing vs internal — which subnets apply

| Load balancer scheme | Needs subnets with... |
|---|---|
| **Internet-facing** (clients from the public internet) | A route table with `0.0.0.0/0 → your Internet Gateway` |
| **Internal** (clients only from inside the VPC / peered VPC / on-prem via VPN) | No direct IGW route — routed only via `local` (+ NAT for outbound, if needed) |

`demo-alb` (built in Note 05) is **internet-facing**, so it goes into your VPC's two public subnets — even though the actual application instances it forwards to live in the **private** application subnets. The load balancer's own subnet placement and its targets' subnet placement are two separate decisions.

---

## 3. Hands-on: verify your VPC's subnets satisfy these requirements

We are **not** creating anything new here — just confirming, via the VPC console, that your existing network is ready for Note 05. Do this against whichever VPC you intend to use for this folder's demo — it doesn't matter which tool or note built it.

### Step 1 — Confirm 2+ AZs exist with public subnets

1. **VPC console** → left nav → **Subnets**.
2. Filter/search for your public subnets.
3. Confirm you have exactly two public subnets, and that their **Availability Zone** column shows two **different** AZs (e.g. one in AZ-a, one in AZ-b) — if both show the same AZ, that's a problem (see troubleshooting below).

### Step 2 — Confirm the public subnets' route tables point to the IGW

1. Select the first public subnet → **Route table** tab.
2. Confirm the associated route table has a route: `0.0.0.0/0 → your Internet Gateway`.
3. Repeat for the second public subnet — it should be associated with the **same** public route table (or an equivalent one with the same IGW route).

### Step 3 — Confirm the private subnets (for reference — targets live here, the LB itself does not)

1. Filter/search for your private application subnets.
2. Confirm you have two private subnets, one per Availability Zone, each associated with a route table that sends outbound internet traffic via a **NAT Gateway** — **not** a direct IGW route.
3. This confirms your application instances (which will launch into these subnets) are correctly unreachable from the internet directly.

### Step 4 — Confirm subnet size (CIDR)

Each of the four subnets should be at least a `/27` (8 free IP addresses) — a `/24` (256 addresses) or similar is comfortably larger than the AWS-recommended minimum, so there's normally no capacity concern here.

If all four checks pass, your VPC is ready for the ALB build in Note 05 — no further networking changes are needed.

---

## 4. Diagram: subnet layout annotated for load balancer eligibility

```mermaid
flowchart TD
    INTERNET(("Internet")) <--> IGW["Internet Gateway"]

    subgraph VPC["Your VPC"]
        IGW --> RT_PUB["Public route table<br/>0.0.0.0/0 -> igw"]
        RT_PRIV["Private route table<br/>0.0.0.0/0 -> nat-gw"]

        subgraph AZ_A["AZ-a"]
            PUB1["Public subnet 1<br/>VALID for internet-facing LB"]
            PRIV1["Private subnet 1<br/>VALID for internal LB<br/>(targets: app instances)"]
        end

        subgraph AZ_B["AZ-b"]
            PUB2["Public subnet 2<br/>VALID for internet-facing LB"]
            PRIV2["Private subnet 2<br/>VALID for internal LB<br/>(targets: app instances)"]
        end

        RT_PUB -.assoc.- PUB1
        RT_PUB -.assoc.- PUB2
        RT_PRIV -.assoc.- PRIV1
        RT_PRIV -.assoc.- PRIV2
    end

    style PUB1 fill:#1f6feb,color:#fff
    style PUB2 fill:#1f6feb,color:#fff
    style PRIV1 fill:#8957e5,color:#fff
    style PRIV2 fill:#8957e5,color:#fff
```

`demo-alb` (internet-facing) will be deployed across the two **blue** subnets. If we were instead building an **internal** load balancer, it would use the two **purple** subnets.

---

## 5. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Only one subnet shows up as selectable when creating the load balancer | Only one AZ actually has a subnet available, or you picked the wrong VPC in the wizard | Check the **VPC** dropdown at the top of the create-LB wizard matches your intended VPC; check **Subnets** page for a second AZ's subnet |
| Two public subnets both show the same AZ | Subnets were created with "No preference" for AZ instead of pinning it explicitly | Edit/recreate one subnet, explicitly choosing the other AZ |
| Console won't let you select a private subnet for an internet-facing LB | Internet-facing LBs still let you pick any subnet, but traffic won't reach clients correctly without an IGW route — the ALB will provision but be unreachable | Re-select the public subnets that have the `0.0.0.0/0 → igw` route |
| ALB creation succeeds but shows `provisioning` then `failed` | A selected subnet has too few free IPs (violates the `/27`, 8-free-IP guidance) | Free up IPs in that subnet, or use a larger/different subnet |
| Load balancer created but clients can't reach it at all | Selected private subnets for an internet-facing LB, or the public route table is missing the IGW route | Re-check Steps 1-2 above; confirm subnet-to-route-table association |

---

## 6. Recap

- An ALB/NLB requires **at least 2 AZs** (2+ subnets, one per AZ) — this is enforced, not optional.
- **Internet-facing** load balancers need subnets routed to an **IGW** (your public subnets); **internal** ones need subnets without a direct IGW route (your private subnets).
- You can never select two subnets from the **same** AZ for one load balancer.
- Verified your own VPC's existing subnets already satisfy all of this — no new subnets needed for `demo-alb`.
- Next: Note 04 — Load Balancer Security Group Design (Hands-On).

---

### Sources
- [Application Load Balancers – Subnets for your load balancer – AWS docs](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html#subnets-load-balancer)
- [Availability Zones for your Application Load Balancer – AWS docs](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-subnets.html)
- [What is Amazon VPC? – AWS docs](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
