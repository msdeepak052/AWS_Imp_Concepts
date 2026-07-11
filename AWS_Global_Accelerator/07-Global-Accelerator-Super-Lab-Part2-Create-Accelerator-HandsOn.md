# 07 - AWS Global Accelerator - Super Lab Part 2

> Goal: create the actual Global Accelerator on top of Part 1's two independent regional ALB/ASG stacks — listener, two endpoint groups, and each Region's ALB attached as its endpoint.

---

## 1. Prerequisites

- Both Regional stacks from Note 06 up and independently verified (each ALB DNS name responding with its Region-identifying page).

---

## 2. Create the accelerator

1. **Global Accelerator console** → **Create accelerator**.
2. Name it (e.g. `super-lab-accelerator`), keep **IP address type: IPv4** (dual-stack optional), choose **Standard accelerator** (Note 03 — endpoints here are ALBs, not per-instance gaming-style routing, so Custom Routing doesn't apply).
3. **Add listener**: protocol **TCP**, port **80** (matching the ALB listener from Note 06, Section 5).

---

## 3. Add the two endpoint groups

1. **Add endpoint group** → Region A → **traffic dial: 100%** → health check settings: leave defaults (HTTP health check against the ALB's own listener/target group health, same check the ALB itself already performs).
2. **Add endpoint** within this group → select **Application Load Balancer** as the endpoint type → choose Region A's ALB → weight **128** (default, single endpoint per group here).
3. Repeat identically for **Region B's endpoint group**, attaching **Region B's ALB**.

---

## 4. Confirm deployment

1. Wait for the accelerator's status to show **Deployed**.
2. Note the **2 static anycast IP addresses** assigned to the accelerator (Note 02) — these are now the single, permanent entry point for the entire two-Region architecture, regardless of which Region actually ends up serving any given request.

---

## 5. Why attach the ALB, not the ASG or instances directly

Global Accelerator's standard endpoint types are **ALB, NLB, EC2 instance, or EIP** — not an Auto Scaling Group directly. Attaching the **ALB** is the correct choice here because:

- The ALB already tracks the ASG's actual healthy instance set via its own **target group health checks** (Note 06) — Global Accelerator only needs to health-check the **ALB** itself, one stable endpoint, rather than trying to track a constantly-scaling fleet of individual instances.
- This cleanly separates concerns: **ASG** handles instance-level elasticity and health within a Region; **ALB** distributes across those instances and exposes one stable health signal; **Global Accelerator** operates one layer up, choosing *between Regions* based on that ALB-level signal.

> 🧠 **Mental model:** this is the same "delegate health to the layer that actually owns it" pattern as an ALB delegating instance health to its target group instead of pinging every instance itself — Global Accelerator does the same one layer higher, delegating regional health to each Region's ALB.

---

## 6. Recap

- The accelerator's **listener** (TCP/80) and **two endpoint groups** (one per Region, each at 100% traffic dial) are now wired to each Region's **ALB** as the endpoint — not the ASG or raw instances directly.
- The **2 static anycast IPs** are now the single permanent front door for the whole two-Region architecture.
- Attaching the **ALB** (not individual instances) lets Global Accelerator delegate instance-level health tracking to the layer that already owns it.
- Next: Note 08 — Super Lab Part 3, end-to-end verification: normal routing, forced Regional failover, comparison against Route 53, and cleanup.

### Sources
- [Endpoint groups — AWS Global Accelerator docs](https://docs.aws.amazon.com/global-accelerator/latest/dg/about-endpoint-groups.html)
- [Endpoints — AWS Global Accelerator docs](https://docs.aws.amazon.com/global-accelerator/latest/dg/about-endpoints.html)
- [Getting started with AWS Global Accelerator — AWS docs](https://docs.aws.amazon.com/global-accelerator/latest/dg/getting-started.html)
