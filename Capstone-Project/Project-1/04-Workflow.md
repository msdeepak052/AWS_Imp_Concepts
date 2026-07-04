# 04 - Workflow

> Goal: walk through CloudMart's behavior over time as four separate diagrams — a single request, the order the infrastructure gets built in, what happens when an instance fails, and what happens when load rises. Note 02 showed the static architecture; this note shows it in motion.

---

## 1. A single user request, start to finish

```mermaid
sequenceDiagram
    participant U as Browser
    participant R as Route 53
    participant P as Public ALB
    participant W as Web ASG instance (Nginx)
    participant I as Internal ALB
    participant A as App ASG instance (Flask)
    participant D as cloudmart-db-1 (MariaDB)

    U->>R: Resolve www.cloudmart.example
    R-->>U: IP of cloudmart-public-alb
    U->>P: GET /
    P->>W: forward (healthy target)
    W-->>U: index.html
    U->>W: fetch('/api/products')
    W->>I: proxy_pass :8080/api/products
    I->>A: forward (healthy target)
    A->>D: SELECT * FROM products
    D-->>A: 5 rows
    A-->>I: JSON
    I-->>W: JSON
    W-->>U: JSON
    Note over U: Browser renders product list
```

Two load balancers sit in this path, but the browser only ever sees one hop — everything past `cloudmart-public-alb` is invisible to it, exactly as the security design in Note 02 intends.

---

## 2. Build order — why Parts 1 through 6 happen in this sequence

```mermaid
flowchart TD
    P1["Part 1 — VPC and Networking<br/>(05)"] --> P2["Part 2 — Security Groups and IAM<br/>(06)"]
    P2 --> P3["Part 3 — Database Tier<br/>(07)"]
    P3 --> P4["Part 4 — Backend Tier<br/>(08)"]
    P4 --> P5["Part 5 — Frontend Tier<br/>(09)"]
    P5 --> P6["Part 6 — Route 53 DNS<br/>(10)"]
    P6 --> P7["Testing, HA Validation, Cleanup<br/>(11)"]
```

Each part exists as a **hard prerequisite** for the next, not just a suggested order:

| Part | Can't start until... | Because... |
|---|---|---|
| 2 (Security Groups) | Part 1's subnets exist | Security groups belong to the VPC, and later launch templates need them |
| 3 (Database) | Part 2's `cloudmart-db-sg` exists | The DB instance must launch with a security group already in place |
| 4 (Backend) | Part 3's DB instance has a private IP | The backend's user data hardcodes `DB_HOST` to that IP |
| 5 (Frontend) | Part 4's Internal ALB has a DNS name | The frontend's Nginx config hardcodes the `proxy_pass` target to that DNS name |
| 6 (Route 53) | Part 5's Public ALB exists | The DNS Alias record and health check both target the Public ALB |

🎯 **Exam tip:** this "each tier's config bakes in the previous tier's endpoint" pattern is exactly why real infrastructure-as-code tools (CloudFormation, Terraform) express these as explicit resource dependencies — doing it by hand in the console, as this capstone does, makes that dependency chain very concrete and easy to feel.

---

## 3. Auto-healing — one instance fails

This same sequence applies to **either** compute tier (web or app) — only the specific target group and ASG differ.

```mermaid
stateDiagram-v2
    [*] --> Healthy
    Healthy --> FailingChecks: Instance stops responding (crash, patch reboot, host retirement)
    FailingChecks --> Unhealthy: Target group marks it Unhealthy after threshold failures
    Unhealthy --> RemovedFromRotation: ALB stops sending it traffic immediately
    RemovedFromRotation --> Replacing: ASG detects failed health check, terminates instance
    Replacing --> Launching: ASG launches a replacement from the launch template
    Launching --> RegisteringWithTG: New instance boots, registers with target group
    RegisteringWithTG --> Healthy: Passes health checks, rejoins rotation
```

Because both `cloudmart-web-asg` and `cloudmart-app-asg` run with **minimum capacity 2, one per AZ**, losing a single instance never drops that tier to zero — the other AZ's instance keeps serving every request while the failed one is replaced. Note 11 exercises this exact sequence manually to prove it.

---

## 4. Scaling — load rises and falls

```mermaid
flowchart LR
    A[CPU rises<br/>above 50% average] --> B[Target-tracking<br/>alarm triggers]
    B --> C[ASG launches<br/>additional instance]
    C --> D[New instance passes<br/>health checks]
    D --> E[ALB registers it,<br/>load spreads thinner]
    E --> F[CPU falls<br/>back toward 50%]
    F --> G[ASG scales back in<br/>toward desired=2]
```

Both `cloudmart-web-asg` and `cloudmart-app-asg` carry an identical **target-tracking scaling policy** keyed on average CPU utilization at 50%, each capped at a maximum of 4 instances. Because the two ASGs scale independently, a frontend-heavy spike (lots of static page loads) and a backend-heavy spike (lots of API calls) each get absorbed by the tier that's actually under load, without over-provisioning the tier that isn't.

---

## 5. Recap

- One request crosses two load balancers but only one hop is ever visible to the browser.
- The 6-part build order isn't arbitrary — each part's launch template or DNS record literally hardcodes an endpoint value produced by the part before it.
- Auto-healing and scaling both rely on the same underlying mechanism: an ALB target group's health checks feeding into an ASG's replace/launch decisions.
- Next: Note 05 — Build Part 1: VPC and Networking, where the actual console build begins.

### Sources
- [How Elastic Load Balancing works with Auto Scaling — AWS docs](https://docs.aws.amazon.com/autoscaling/ec2/userguide/autoscaling-load-balancer.html)
- [Target tracking scaling policies — AWS docs](https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-target-tracking.html)
- [Health checks for your target groups — AWS docs](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html)
