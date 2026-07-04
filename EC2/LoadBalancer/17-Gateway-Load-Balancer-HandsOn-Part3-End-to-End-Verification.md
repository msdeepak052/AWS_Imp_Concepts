# 17 - Gateway Load Balancer Hands-On, Part 3: End-to-End Verification

> Goal: flip the switch. Everything built across the previous two hands-on notes (`demo-gwlb`, `demo-gwlb-tg`, `demo-firewall-1/2`, `demo-gwlb-endpoint-service`, `demo-gwlbe-1`) exists but carries zero real traffic so far. This note edits the three route tables that actually redirect internet-bound traffic for `demo-alb` through the firewall appliances, then walks through verifying the full round trip. This is the VPC ingress routing concept from earlier in this chapter, made real.

---

## 1. The three route tables that must change

AWS's documented procedure for this exact scenario ("configure routing" for a GWLB endpoint) touches **three** route tables, not one — this is the detail worth getting precisely right rather than guessing:

| # | Route table | New/changed route | Purpose |
|---|---|---|---|
| 1 | **IGW edge-associated route table** (associated with your VPC's Internet Gateway itself, not a subnet) | `10.0.1.0/24` → `demo-gwlbe-1` | Intercepts internet traffic addressed to the ALB's subnet (where `demo-alb` lives) **before** it ever reaches ordinary VPC routing, and detours it to the endpoint. |
| 2 | **The ALB's own subnet route table** | `0.0.0.0/0` → `demo-gwlbe-1` (replacing the direct `0.0.0.0/0 → IGW` route) | Return path: once the appliance has inspected inbound traffic and it's delivered into the subnet, *outbound* replies (and any subnet-initiated egress) must also detour back through the endpoint — otherwise replies leave directly via the IGW and you get **asymmetric routing**, which most stateful appliances silently break on. |
| 3 | **`gwlbe-subnet-1`'s own route table** | `0.0.0.0/0` → IGW | Lets traffic that has passed through the endpoint (post-inspection, heading back out) actually reach the internet. |

> ⚠️ This is not a "the endpoint handles the return path automatically" situation — AWS's own routing procedure explicitly requires **all three** of these routes to be configured by hand (or via the console's "middlebox routing wizard," which automates exactly this). Skipping row 2 or row 3 is the single most common reason a GWLB ingress-inspection build "sort of works" for inbound but breaks replies.

---

## 2. Step 1 — Edit the IGW edge-associated route table

1. VPC console → **Route Tables** → **Create route table** (or select an existing one already edge-associated with your VPC's IGW, if the previous hands-on note created it as part of the ingress-routing preview).
2. **Name**: `demo-igw-edge-rt`. **VPC**: your VPC.
3. **Edge associations** tab → **Edit edge associations** → select your VPC's **Internet Gateway** → **Save**. This is what makes it an *edge* route table rather than an ordinary subnet route table — it governs traffic **entering** the VPC through the gateway, before any subnet-level routing applies.
4. **Routes** tab → **Edit routes** → **Add route**:
   - **Destination**: `10.0.1.0/24` (exactly the ALB's subnet CIDR).
   - **Target**: **VPC Endpoint** → `demo-gwlbe-1`.
5. **Save changes.**

Resulting table:

| Destination | Target |
|---|---|
| `10.0.0.0/16` | `local` |
| `10.0.1.0/24` | `demo-gwlbe-1` |

---

## 3. Step 2 — Edit the ALB subnet's route table (return path)

The ALB's subnet currently shares a route table with the other public subnet (AZ-b). Since only the ALB's subnet is in scope for this inspection demo, give it its **own** route table so the other public subnet's routing is untouched:

1. **Route Tables** → **Create route table** → **Name**: `demo-alb-subnet-rt`. **VPC**: your VPC.
2. **Routes** tab → add `10.0.0.0/16 → local` (present by default) and **`0.0.0.0/0` → `demo-gwlbe-1`** (target: VPC Endpoint).
3. **Subnet associations** tab → **Edit subnet associations** → check the ALB's subnet only.

The other public subnet (and anything else still on the shared public route table) keeps its direct `0.0.0.0/0 → IGW` route, unaffected.

> ⚠️ **Production nuance:** a complete two-AZ design would replicate this entire pattern for AZ-b too — a second `demo-gwlbe-2` in an AZ-b endpoint subnet, a second edge route for the AZ-b public subnet's CIDR, and so on. This demo intentionally scopes to AZ-a only, matching the single-AZ appliance-subnet focus established earlier in this chapter; call this out explicitly if this pattern shows up in an exam scenario about *high availability* GWLB inspection.

---

## 4. Step 3 — Edit `gwlbe-subnet-1`'s route table (egress path)

1. **Route Tables** → **Create route table** → **Name**: `demo-gwlbe-subnet-rt`. **VPC**: your VPC.
2. **Routes**: `10.0.0.0/16 → local` plus **`0.0.0.0/0` → IGW**.
3. **Subnet associations** → associate with **`gwlbe-subnet-1`**.

This is what lets traffic that has just emerged from the endpoint (inbound, post-inspection, heading to the ALB subnet's `local` route) and outbound replies (heading back to the internet) actually find their way to the IGW.

---

## 5. End-to-end verification

1. From a browser or `curl`, hit `demo-alb`'s DNS name (`demo-alb-xxxx.elb.<region>.amazonaws.com`) — it should respond **exactly as before**, with no visible change to the client. The entire detour through the firewall fleet is invisible at the HTTP layer.
2. SSH (via Session Manager, since these are demo boxes) into **`demo-firewall-1`** and **`demo-firewall-2`** → check `iptables -L -v -n` counters, or tail whatever logging the user-data script wrote — packet/byte counters should be incrementing on the appliance that's currently handling the flow (only one appliance sees a given flow, per GWLB's flow-hashing/stickiness).
3. Confirm target health in **`demo-gwlb-tg`** stays `Healthy` throughout — a spike in requests without a health dip is a good sign the appliance is keeping up.
4. Optional: temporarily stop the `httpd`/forwarding logic on one firewall instance mid-test and confirm the GWLB fails over new flows to the other appliance without the client noticing (existing flows may still drain to the now-unhealthy target, since GWLB keeps an existing flow pinned to its original appliance until that flow ends).

```mermaid
sequenceDiagram
    participant Client
    participant IGW
    participant EdgeRT as IGW edge-assoc RT
    participant GWLBE as demo-gwlbe-1
    participant GWLB as demo-gwlb
    participant FW as demo-firewall-1
    participant ALB as demo-alb
    participant TG as demo-tg
    participant EC2 as app instance

    Client->>IGW: HTTP request to demo-alb
    IGW->>EdgeRT: match 10.0.1.0/24
    EdgeRT->>GWLBE: redirect (edge route)
    GWLBE->>GWLB: GENEVE-encapsulate, forward
    GWLB->>FW: deliver to healthy target
    FW-->>FW: inspect / decapsulate
    FW->>GWLBE: return decapsulated packet
    GWLBE->>ALB: deliver via normal subnet (local) routing
    ALB->>TG: forward per listener rule
    TG->>EC2: route to healthy instance
    EC2-->>TG: HTTP response
    TG-->>ALB: response
    ALB-->>GWLBE: response (0.0.0.0/0 route)
    GWLBE-->>GWLB: GENEVE-encapsulate
    GWLB-->>FW: same appliance (flow stickiness)
    FW-->>GWLBE: inspected, return
    GWLBE-->>IGW: via demo-gwlbe-subnet-rt (0.0.0.0/0 -> igw)
    IGW-->>Client: HTTP response
```

---

## 6. Troubleshooting: classic GWLB ingress-routing failure modes

| Symptom | Likely cause / fix |
|---|---|
| Client requests time out entirely | Edge route table isn't actually **edge-associated** with your VPC's IGW (check the **Edge associations** tab, not just Routes) — an ordinary route table association does nothing for IGW-ingress traffic. |
| Requests succeed, but appliance logs/counters show nothing | The route destination CIDR doesn't exactly match the ALB's subnet (`10.0.1.0/24`), so traffic bypasses the redirect entirely — double-check the CIDR, not just the subnet name. |
| Requests succeed inbound but responses never arrive back at the client | **Asymmetric routing** — the ALB subnet's own route table still points `0.0.0.0/0` at the IGW directly instead of `demo-gwlbe-1`; the appliance (often stateful) never sees the return leg and many appliances / the flow itself breaks. This is the single most common GWLB misconfiguration. |
| Traffic reaches the appliance but nothing comes out the other side | The appliance is **inspecting and dropping** instead of **inspecting and forwarding/NATing**. A real firewall appliance must actively forward allowed traffic back out — GWLB does not do any forwarding itself; that's entirely the appliance's job. Our demo's `iptables MASQUERADE`+`FORWARD ACCEPT` rules exist precisely to do this. |
| Targets flap unhealthy under load, dropping some flows | Security group gap — confirm `demo-firewall-sg` allows inbound **UDP 6081** (GENEVE) and the health-check port from the appliance subnet CIDRs, not just from "the load balancer" (GWLB has no single SG of its own to reference). |
| `demo-gwlbe-1` shows as the target but nothing routes to it | The endpoint isn't `Available` yet, or the route table you edited isn't the one actually associated with the IGW / the ALB's subnet / `gwlbe-subnet-1` respectively — re-check each **Subnet associations** / **Edge associations** tab. |

---

## 7. ⚠️ Clean up to avoid charges

This three-part build is one of the **more expensive demo environments** in this repo — every piece bills hourly regardless of traffic:

1. **Delete `demo-gwlbe-1`** (VPC console → Endpoints) — GWLB Endpoints bill hourly + per-GB, same as Interface Endpoints. You must first remove any route table entries pointing at it (Sections 2–4 above) or the delete will fail.
2. **Delete `demo-gwlb-endpoint-service`** (VPC console → Endpoint Services).
3. **Delete the Gateway Load Balancer `demo-gwlb`** (EC2 console → Load Balancers) — bills hourly + LCU-hours like any other ELB type.
4. **Delete target group `demo-gwlb-tg`.**
5. **Terminate `demo-firewall-1` and `demo-firewall-2`** — two more EC2 instance-hours running continuously otherwise.
6. Optionally delete `gwlbe-subnet-1`, `gwlb-appliance-subnet-1/2`, and the three route tables created across this chapter's hands-on notes, if you're tearing down the whole scenario rather than just pausing it.

> ⚠️ Unlike a lone NAT Gateway or a single ALB, this scenario stacks **GWLB hourly + LCU + two GWLB Endpoint-hours + two appliance EC2 instances** simultaneously — leaving it running "just for a bit longer" is a fast way to rack up a surprising bill for a learning exercise.

---

## 8. Recap: the GWLB chapter

- **The concept notes** covered what a Gateway Load Balancer is (Layer 3/4 GENEVE-based traffic inspection, transparent to the traffic it forwards) and the **VPC ingress routing** mechanism that makes it transparent (an IGW edge-associated route table redirecting traffic destined for a subnet to a GWLB endpoint before it ever reaches ordinary `local` routing).
- **Hands-on Part 0** created the dedicated appliance subnets `gwlb-appliance-subnet-1/2`.
- **Hands-on Part 1** launched `demo-firewall-1/2`, created `demo-gwlb-tg` (GENEVE:6081) and `demo-gwlb` itself.
- **Hands-on Part 2** built the PrivateLink plumbing: `demo-gwlb-endpoint-service` and the consumer-side `demo-gwlbe-1`.
- **Hands-on Part 3 (this note)** wired the actual ingress redirect across three route tables and verified a real client request genuinely detours through `demo-firewall-1`/`demo-firewall-2` before ever reaching `demo-alb`, invisibly to the client.
- Together this is the standard AWS reference pattern for **centralized traffic inspection using Gateway Load Balancer** — the same shape used in production hub-and-spoke architectures, just scoped down to one VPC and one AZ for learning purposes.
- Next: Note 18 — Classic Load Balancer, closing out the Load Balancer folder with the legacy Classic Load Balancer, comparing it against ALB/NLB/GWLB.

---

### Sources
- [Access an inspection system using a Gateway Load Balancer endpoint (routing configuration) – AWS docs](https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-load-balancer-endpoints.html)
- [Configure middlebox traffic routing and inspection in a VPC – AWS docs](https://docs.aws.amazon.com/vpc/latest/userguide/gwlb-route.html)
- [What is a Gateway Load Balancer? – AWS docs](https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/introduction.html)
- [Gateway Load Balancer pricing – AWS](https://aws.amazon.com/elasticloadbalancing/pricing/)
