# 04 - AWS Global Accelerator - Multi-Region EC2 Traffic Routing (Hands-On)

> Goal: build one real accelerator routing to plain EC2 instances in two separate Regions, then directly observe both normal routing and health-check-driven failover — the simplest possible hands-on proof of Notes 01-03's concepts, before the larger Super Lab (Notes 05-08) adds load balancers and Auto Scaling.

---

## 1. Prerequisites

- Two EC2 instances, each in a **different Region** (e.g. `ap-south-1` and `ap-southeast-1`), each running a minimal web server (e.g. `python3 -m http.server 80` or a tiny Nginx/Apache install) returning a page that identifies **which Region** served the request — this makes routing behavior visible.
- Each instance's security group allows inbound **HTTP (port 80)** from the internet (or at least from Global Accelerator's health-check/data path).

---

## 2. Create the accelerator

1. **Global Accelerator console** → **Create accelerator**.
2. Name it, choose **Standard accelerator** (Note 03 — not Custom Routing, since we're targeting plain EC2 endpoints generically, not per-instance gaming-style port mapping).
3. **Add listener**: protocol **TCP**, port **80**.
4. **Add endpoint groups** — one per Region:
   - Endpoint group 1 → Region `ap-south-1`, traffic dial **100%**.
   - Endpoint group 2 → Region `ap-southeast-1`, traffic dial **100%**.
5. Within each endpoint group, **add endpoint** → select the EC2 instance in that Region, default weight (**128**).
6. **Create accelerator** — note the **2 static anycast IP addresses** assigned once it's deployed.

---

## 3. Test normal routing

```bash
curl http://<static-ip-1>/
```

- The response should come back identifying whichever Region's instance Global Accelerator judged as the best destination — typically the one **closest to where the request originates**, assuming both endpoint groups are healthy and dialed at 100%.
- Run the same `curl` from a different geographic location (or a VPN/proxy) if available, and notice it may route to the *other* Region — direct, hands-on confirmation of Note 02's "nearest edge + best latency" routing behavior.

---

## 4. Observe health-check-driven failover

1. Stop the web server process (or stop the instance entirely) in whichever Region is currently receiving traffic.
2. Wait for Global Accelerator's health check to mark that endpoint **unhealthy** (typically well within a minute).
3. Re-run:
   ```bash
   curl http://<static-ip-1>/
   ```
4. Traffic should now be served by the **other Region's** instance — with **no DNS change, no client-side cache to expire, no static IP change**. The same two anycast IPs simply now route to the surviving healthy Region.

> 🧠 This is the concrete, hands-on version of Note 01's Route 53 comparison: contrast how immediate this failover felt against `Route53`'s DNS failover routing, which is bound by whatever TTL the client (or a resolver in between) has already cached.

---

## 5. Clean up

- Delete the accelerator (disables the listener/endpoint groups; static IPs are released).
- Stop or terminate the EC2 instances in both Regions if not needed further.

---

## 6. Recap

- A Standard accelerator with two Regional endpoint groups, each pointing at a plain EC2 instance, is enough to directly observe Global Accelerator's core value: **fixed static IPs**, **proximity-based routing**, and **fast health-check-driven failover** with no DNS/TTL involved.
- The next lab (Notes 05-08) builds a fuller "Super Lab" — real VPCs, Application Load Balancers, and Auto Scaling Groups in each Region — to see the same routing/failover behavior in a production-shaped architecture.
- Next: Note 05 — Super Lab Introduction, laying out the full multi-Region architecture this next lab builds.

### Sources
- [Getting started with AWS Global Accelerator — AWS docs](https://docs.aws.amazon.com/global-accelerator/latest/dg/getting-started.html)
- [Endpoint groups — AWS Global Accelerator docs](https://docs.aws.amazon.com/global-accelerator/latest/dg/about-endpoint-groups.html)
- [Endpoints — AWS Global Accelerator docs](https://docs.aws.amazon.com/global-accelerator/latest/dg/about-endpoints.html)
