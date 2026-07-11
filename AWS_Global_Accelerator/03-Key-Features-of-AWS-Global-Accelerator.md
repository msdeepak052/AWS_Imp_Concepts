# 03 - Key Features Of AWS Global Accelerator

> Goal: cover the configuration knobs that actually differentiate Global Accelerator on the exam — traffic dial, endpoint weights, health checks, client affinity, and the Standard vs. Custom Routing accelerator split.

---

## 1. Traffic dial — controlling how much traffic a Region gets

Each **endpoint group** (i.e., each Region) has a **traffic dial**, a percentage (0-100%) of the traffic that Global Accelerator is *allowed* to send there.

- Dialing a Region down to **0%** stops new traffic to it entirely, without deleting any configuration — useful for taking a Region out of rotation for maintenance.
- Dialing gradually (e.g. 10% → 50% → 100%) enables **blue/green deployments** or **regional canary testing** — send a small slice of real production traffic to a newly deployed Region before committing fully.

> 🧠 **Mental model:** the traffic dial is Global Accelerator's version of a **weighted routing policy**, but applied at the network layer per Region, rather than as a Route 53 DNS weighted record.

---

## 2. Endpoint weights — controlling distribution *within* a Region

Within a single endpoint group, each individual **endpoint** (an ALB, NLB, EC2 instance, or EIP) has its own **weight**, controlling its relative share of the traffic dial'd into that group — e.g., two ALBs in the same Region with weights 128 and 64 split roughly 2:1.

---

## 3. Health checks and automatic failover

- Global Accelerator continuously runs **TCP, HTTP, or HTTPS health checks** against endpoints.
- The moment an endpoint (or an entire endpoint group/Region) is found unhealthy, Global Accelerator **automatically reroutes traffic** to the next-healthiest option — **within seconds**, since this happens at the network layer with no DNS caching/TTL to wait out.
- This is the concrete mechanism behind Note 01's claim that Global Accelerator fails over **faster** than Route 53 DNS-based failover routing, where clients can keep using a stale cached DNS answer until its TTL expires.

> ⚠️ Health checks operate **per endpoint group (Region)** and **per endpoint** — a single unhealthy EC2 instance behind an ALB doesn't necessarily pull the whole Region out of rotation if the ALB itself (and its other targets) remain healthy; it's the ALB's own target group health check that handles that layer, same as in any `EC2/LoadBalancer` design.

---

## 4. Client affinity

By default (`NONE`), Global Accelerator uses a flow hash across multiple packet header fields, meaning **a single client can be routed to different endpoints across different connections**.

Setting client affinity to **`SOURCE_IP`** forces Global Accelerator to hash on **source + destination IP only**, so **the same client IP consistently reaches the same endpoint** across separate connections — needed for stateful, non-HTTP protocols (e.g. UDP-based gaming or real-time protocols) where session state lives on one specific backend instance and cookies/HTTP mechanisms aren't available to maintain that stickiness.

---

## 5. Standard vs. Custom Routing accelerators

| | **Standard accelerator** | **Custom Routing accelerator** |
|---|---|---|
| Endpoint granularity | ALB, NLB, EC2 instance, or EIP — GA picks the endpoint | Specific **EC2 instance + port**, chosen by *your own application logic* |
| Port mapping | Listener port range maps generically to endpoints | Deterministic **static port mappings** from accelerator ports to EC2 destinations, which your app retrieves via API |
| Typical use case | General multi-Region HA/DR, fixed IP + fast failover needs | Multiplayer gaming, real-time communications — workloads needing session-level control over exactly which instance a specific user lands on |

---

## 6. Security and pricing

- The two fixed static IPs double as an implicit **DDoS-resilient front door** — combined with **AWS Shield** integration, attack traffic is absorbed at the edge before it consumes backend capacity.
- Pricing has two parts: a **fixed hourly fee per accelerator**, plus a **per-GB data transfer premium** on top of the destination Region's standard transfer rate.

> 🎯 **Exam tip:** "needs a fixed IP for firewall allow-listing," "non-HTTP protocol," "fast automatic failover between Regions without DNS TTL delay," and "gaming workload needing users pinned to a specific game server instance" are the four recurring Global Accelerator scenario signatures — the last one specifically points at **Custom Routing**, not Standard.

---

## 7. Recap

- **Traffic dial** (per Region) and **endpoint weight** (per endpoint within a Region) are the two levers controlling traffic distribution.
- **Health checks** trigger **fast, network-layer failover** — the key advantage over Route 53's DNS/TTL-bound failover.
- **Client affinity** (`NONE` vs `SOURCE_IP`) controls whether the same client consistently reaches the same endpoint — relevant for stateful non-HTTP workloads.
- **Standard** accelerators route to load balancers/instances generically; **Custom Routing** accelerators give the application deterministic control over exact EC2+port destinations — built for gaming/real-time use cases.
- Next: Note 04 — hands-on lab building a real multi-Region EC2 traffic routing setup with Global Accelerator.

### Sources
- [AWS Global Accelerator features](https://aws.amazon.com/global-accelerator/features/)
- [How client affinity works — AWS docs](https://docs.aws.amazon.com/global-accelerator/latest/dg/about-listeners-client-affinity.html)
- [Introducing AWS Global Accelerator custom routing accelerators — AWS blog](https://aws.amazon.com/blogs/networking-and-content-delivery/introducing-aws-global-accelerator-custom-routing-accelerators/)
- [AWS Global Accelerator FAQs](https://aws.amazon.com/global-accelerator/faqs/)
