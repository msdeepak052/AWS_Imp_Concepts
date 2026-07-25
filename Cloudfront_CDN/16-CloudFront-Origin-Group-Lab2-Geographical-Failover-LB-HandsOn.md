# 16 - AWS CloudFront Origin Group Lab 2: Geographical Failover with Load Balancer

> Goal: extend the [Origin Group Failover Lab, EC2/S3](15-CloudFront-Origin-Group-Lab1-EC2-S3-Failover-HandsOn.md) note's Origin Group pattern to **two full, independently-running application deployments** behind load balancers in **different Regions** — real multi-Region disaster recovery, not just a static fallback page.

---

## 1. How this differs from Lab 1

The [Origin Group Failover Lab, EC2/S3](15-CloudFront-Origin-Group-Lab1-EC2-S3-Failover-HandsOn.md) note's secondary origin was a **static S3 fallback** — good for graceful degradation, but not a substitute for the real application. This lab's secondary origin is a **second, fully-functional ALB**, fronting its **own EC2/ASG fleet in a different AWS Region** — so failover here means genuinely continuing to serve the **live application**, not a degraded static page.

> 🧠 **Mental model:** this is the CloudFront-edge equivalent of Route 53 failover routing (covered in this repo's `Route53` folder) — both solve "keep serving traffic if an entire Region goes down" — but this pattern operates at the **CDN/edge layer**, evaluated per-request against real-time origin responses, rather than at the **DNS layer** with its own health-check cadence and TTL-bound propagation delay.

---

## 2. Architecture

```mermaid
flowchart TB
    U((Viewer — e.g. India))

    subgraph EDGE["CloudFront Edge Location — e.g. Mumbai"]
        CK["Cache Key check — Cache Key and Origin Requests note, Leg 1"]
        OG{"Origin Group — try Primary first"}
    end

    subgraph PRIMARY["Primary Region — ap-south-1"]
        ALB1["ALB fronting its own ASG"]
    end

    subgraph SECONDARY["Secondary Region — ap-southeast-1 (DR)"]
        ALB2["ALB fronting its own ASG"]
    end

    U --> CK
    CK -->|"Miss"| OG
    OG -->|"Primary request"| ALB1
    ALB1 -->|"5xx, matches failover criteria"| OG
    OG -.->|"Failover retry, same request"| ALB2
    ALB1 -->|"Healthy — served directly"| U
    ALB2 -->|"200 — live application, full functionality"| U
```

Both Regions run a **complete, independent copy** of the application stack — this is meaningfully more expensive and operationally heavier than the [Origin Group Failover Lab, EC2/S3](15-CloudFront-Origin-Group-Lab1-EC2-S3-Failover-HandsOn.md) note's pattern (two full environments to deploy, patch, and keep in sync), which is exactly why it's reserved for workloads where a true multi-Region active/standby posture is actually justified.

---

## 3. Configure it

1. Deploy (or assume already deployed) two independent ALB + ASG stacks, one in each Region — e.g. `ap-south-1` (primary) and `ap-southeast-1` (secondary/DR).
2. **CloudFront console** → distribution → **Origins** → add both ALBs as **custom origins** (the [CloudFront Origin Settings](03-CloudFront-Origin-Settings.md) note).
3. **Origin groups** → **Create origin group** → add both ALBs via the **Choose origins to add to group** dropdown + **Add**. Role is determined by **list position**, not a separate field — use the **▲/▼** arrows so the `ap-south-1` ALB is listed at position **1** (the console labels it **"(primary)"**) and the `ap-southeast-1` ALB is at position **2**. **Failover criteria**: `500`, `502`, `503`, `504`. **Origin selection criteria**: leave at **Default**.
4. Cache behavior → **Origin or origin group** → select the origin group → **Save changes**.

---

## 4. Test cross-Region failover

1. Confirm normal traffic serves from the `ap-south-1` primary.
2. Simulate a full Regional outage of the primary (e.g. scale the primary ASG to 0, or detach the ALB's target group) so requests to it fail with a matching status code.
3. Request the distribution again — traffic now serves from the **`ap-southeast-1`** ALB's live application, fully functional, not a static page.
4. Restore the primary and confirm traffic naturally returns to it on the next request (same per-request evaluation behavior as the [Origin Group Failover Lab, EC2/S3](15-CloudFront-Origin-Group-Lab1-EC2-S3-Failover-HandsOn.md) note — no persistent "stuck on secondary" state).

---

## 5. Real-world walkthrough: applying this to the Cache Key and Origin Requests Netflix-style session

The India-based Netflix-style session from the [Cache Key and Origin Requests](09-Default-Cache-Behavior-Cache-Key-and-Origin-Requests.md) note's Section 3 assumed a single US backend — this lab makes that backend properly redundant. Picture the same session continuing during a full `ap-south-1` outage:

```mermaid
sequenceDiagram
    participant U as Viewer (India)
    participant E as CloudFront Edge — Mumbai
    participant P as Primary ALB — ap-south-1
    participant S as Secondary ALB — ap-southeast-1 (DR)

    Note over U,S: Stage 2 — Login, mid-session, ap-south-1 suffers a full Regional outage
    U->>E: POST /api/login
    E->>P: Origin Group tries primary first
    P--xE: Timeout / 503 — entire Region unreachable
    E->>S: Automatic failover retry, same request
    S-->>E: 200 OK — auth token issued from the DR Region
    E-->>U: Login succeeds, viewer never sees the outage

    Note over U,S: Stage 3 — Search, next request, same failed-over path
    U->>E: GET /api/search?q=Inception&lang=hi
    E->>S: Origin Group already knows ap-south-1 failed this specific request type — but retries primary first again, per-request, not sticky
    Note over E,P: If ap-south-1 is still down, this fails again and falls through to ap-southeast-1 as before
    S-->>E: 200 OK — personalized results from the DR Region
    E-->>U: Search results served normally
```

The viewer experiences **zero visible disruption** beyond, at most, a slightly slower individual request during the failover retry itself — a meaningfully stronger guarantee than the [Origin Group Failover Lab, EC2/S3](15-CloudFront-Origin-Group-Lab1-EC2-S3-Failover-HandsOn.md) note's static fallback, which could only ever hand back a generic "try again later" page for genuinely dynamic stages like login and search.

---

## 6. When this pattern is worth the cost, vs. Route 53 failover

| | CloudFront Origin Group failover (this note) | Route 53 failover routing (`Route53` folder) |
|---|---|---|
| Layer | CDN/edge, per-request | DNS, resolved once per TTL |
| Failover speed | Immediate — the very next request after a failing response | Bound by DNS TTL and health-check interval — visitors with a cached DNS resolution may keep hitting the failed endpoint until their resolver re-queries |
| Best combined with | Static or dynamic secondary content served through the *same* distribution | Any architecture, including non-CloudFront-fronted ones (e.g. failing over directly between two ALBs with no CDN at all) |

> 🎯 **Exam tip:** "failover must happen as fast as possible, on a per-request basis, for content served through CloudFront" points to **Origin Group failover**; "failover for an architecture that isn't necessarily behind CloudFront at all, or where DNS-level redirection is the natural mechanism" points to **Route 53 failover routing** instead — the two are complementary, and real production DR architectures often use both together.

---

## 7. Recap

- This lab's Origin Group uses **two full, independently-running ALB-backed environments** in different Regions — genuine multi-Region DR, not a static fallback (the [Origin Group Failover Lab, EC2/S3](15-CloudFront-Origin-Group-Lab1-EC2-S3-Failover-HandsOn.md) note's simpler pattern).
- The failover retry happens **within the same edge-location request**, per-request, with no sticky state — the primary is tried again first on the very next request regardless of the last outcome (Section 5).
- CloudFront's per-request, immediate failover (bound to actual response status codes) contrasts with Route 53 failover routing's DNS-TTL-bound cadence — the two operate at different layers and are often combined.
- This closes the two-lab Origin Group series (the [Origin Group Failover Lab, EC2/S3](15-CloudFront-Origin-Group-Lab1-EC2-S3-Failover-HandsOn.md) note and this note). Next: the [CloudFront Error Pages](17-CloudFront-Error-Pages.md) note, customizing what viewers actually see when even failover doesn't resolve an error.

### Sources
- [Optimizing high availability with CloudFront origin failover — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/high_availability_origin_failover.html)
- [Choosing a routing policy — Amazon Route 53 — AWS docs](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html)
