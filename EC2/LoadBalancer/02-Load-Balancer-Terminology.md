# 02 - Load Balancer Terminology

> Goal: nail down the core vocabulary before touching the console. Every hands-on note from here on assumes you know these terms cold. Continues Note 01 (the "why"); Note 03 starts the actual `demo-alb` build with the network prerequisites.

---

## 1. Listener

A **listener** is a process that checks for connection requests on a **protocol + port you configure** — e.g. `HTTP:80`, `HTTPS:443` on an ALB, or `TCP:5000` on an NLB. A load balancer with **no listener** cannot receive any traffic at all — you must add at least one before it's usable.

Each listener has:
- A **protocol and port** it listens on.
- A **default action** (the "default rule" — see below), which every listener must have.
- Zero or more additional **listener rules** you add on top.

`demo-alb` (built in Note 05) gets one listener: **HTTP:80**.

---

## 2. Listener Rule

A **listener rule** is evaluated by the load balancer to decide *which target group* a given request goes to. Each rule has:

- A **priority** (a number — lower number is evaluated first).
- One or more **conditions** (e.g. path pattern `/api/*`, host header `admin.example.internal`, HTTP method, query string, source IP).
- One or more **actions** (e.g. `forward` to a target group, `redirect`, `fixed-response`, or **authenticate**).

Every listener automatically has a **default rule** — it can't be deleted, has no conditions, and is **always evaluated last**, acting as the catch-all for anything that didn't match a more specific rule above it. Rules are evaluated **in priority order, lowest number first; the first matching rule wins** and no further rules are checked after that.

> This is only a preview — full detail on writing rules (path-based and host-based routing, priority ordering in practice) is covered in Notes 06-08. For now: `demo-alb`'s Note-05 build uses only the default rule, forwarding everything to `demo-tg`.

---

## 3. Target Group

A **target group** is the pool of backend destinations the load balancer routes to, plus its own **health check configuration**. It defines:

- **Target type**: `instance` (register by EC2 instance ID), `ip` (register by IP address — works across peered VPCs, on-prem via VPN/Direct Connect, etc.), `lambda` (a single Lambda function), or (ALB only) another **Application Load Balancer** as a target.
- **Protocol and port** used to route traffic to targets (e.g. HTTP:80).
- **Health check settings** (see below).

`demo-tg` (built in Note 05) uses target type **instance**, protocol/port **HTTP:80**.

> ⚠️ You can register one target with **multiple** target groups, and a target group's target type **cannot be changed after creation** — pick it carefully.

---

## 4. Target

A **target** is one individual registered destination inside a target group — a specific EC2 instance ID, a specific IP address, or a specific Lambda function, depending on the target group's target type.

---

## 5. Health Check

The load balancer periodically sends a request (TCP ping, HTTP GET, etc.) to each registered target to check if it's still able to serve traffic. Key settings:

| Setting | Meaning | Typical/default (ALB, instance/ip target) |
|---|---|---|
| **Interval** | How often a health check is sent to each target | 30 seconds (range 5-300) |
| **Timeout** | How long to wait for a response before counting it as a failure | 5 seconds (range 2-120) |
| **Healthy threshold** | Consecutive **successful** checks needed to mark an unhealthy target healthy again | 5 (range 2-10) |
| **Unhealthy threshold** | Consecutive **failed** checks needed to mark a target unhealthy | 2 (range 2-10) |
| **Path** | (HTTP/HTTPS) the URI the health check requests | `/` by default — `demo-tg` uses `/health` |

**What happens to a target that fails its health check?** It is marked `unhealthy` and the load balancer **stops routing new requests to it** — it's taken out of rotation. Critically, **the load balancer does not terminate or restart anything** — it has no such power. It only controls whether *it* sends traffic there.

> 🧠 **Contrast with an Auto Scaling group's job:** an unhealthy target sitting in a target group is only "parked" by the load balancer. If that target group is attached to an Auto Scaling group with ELB health checks enabled, it's the ASG that actually notices the target-group-reported unhealthy status and **replaces the instance** — launching a new one and terminating the bad one. The load balancer diagnoses; the ASG cures.

---

## 6. Cross-Zone Load Balancing

Controls whether each load balancer node distributes requests **only to targets in its own AZ**, or **evenly across targets in all enabled AZs**, regardless of how many targets are actually in each AZ.

- **ALB**: cross-zone load balancing is **always on** and cannot be turned off at the load balancer level (only per target group, as an override).
- **NLB**: cross-zone load balancing is **off by default** and can be enabled per target group; enabling it may incur a **cross-AZ data transfer charge**.

This is just the definition you need now — a full worked comparison (uneven vs. even per-instance traffic share) belongs to a deeper networking discussion beyond this note's scope.

---

## 7. Idle Timeout

The maximum time a connection can stay **open with no data flowing** before the load balancer closes it. Default is **60 seconds** on an ALB. If your application needs long-lived idle connections (e.g. long-polling), you may need to raise this — but raising it also means idle client connections tie up load balancer resources longer.

---

## 8. Connection Draining / Deregistration Delay

When a target is being **removed** from a target group (deregistered) — because it failed a health check, because an ASG is scaling in, or because you manually deregister it — the load balancer doesn't just cut it off mid-request. Instead:

1. The target's state changes to **`draining`**.
2. The load balancer stops sending it **new** requests immediately.
3. **In-flight requests already sent to that target are allowed to finish**, up to a configurable **deregistration delay** (the modern name for what Classic Load Balancers called "connection draining") — default **300 seconds**.
4. After the delay expires (or all in-flight requests complete, whichever is first), the target moves to `unused` and is fully removed.

> ⚠️ **Lowering the deregistration delay** (e.g. to 30-60s) makes deployments/scale-in **faster**, since AWS doesn't have to wait 5 minutes per instance being cycled out — but it risks **cutting off genuinely slow requests** that haven't finished by the time the delay expires. There's a real trade-off: fast deployments vs. never truncating a slow client request. Tune it to match your application's realistic longest request time, not just to "make it faster."

---

## 9. Sticky Sessions

By default, a load balancer distributes each **new** request independently, with no memory of which target served a client's previous request — which is ideal for horizontal scaling (any target can serve any request). **Sticky sessions** override this: once a client is routed to a target, **subsequent requests from that same client are pinned to the same target**, using a cookie.

Two ALB cookie types:

| Type | Cookie name | Who sets it | Default duration |
|---|---|---|---|
| **Duration-based** | `AWSALB` | The load balancer itself | 1 day (configurable 1s-7 days) |
| **Application-based** | `AWSALBAPP` (app-set cookie) / `AWSALBTG` (target-group-specific) | Your application | Controlled by the app's own cookie expiry |

**When it's needed:** legacy or stateful applications that store session data (e.g. shopping cart, login session) **locally on one server** instead of in a shared store (Redis/DynamoDB/ElastiCache), and therefore need every request from a given user to keep landing on that same server.

**Why it works against horizontal scaling ideals:** sticky sessions defeat the whole point of a load balancer's even distribution — a target that happens to get "stuck" with many long-lived sticky clients can become overloaded while others sit idle, and if that target fails, every session pinned to it is lost. The preferred modern pattern is to make your application **stateless** (store session state externally) so sticky sessions aren't needed at all.

---

## 10. Which concepts apply to which load balancer type

| Concept | ALB | NLB | GWLB |
|---|---|---|---|
| Listener | Yes (HTTP/HTTPS) | Yes (TCP/UDP/TLS) | **One fixed listener**, GENEVE:6081, not user-configurable |
| Listener rules (path/host routing) | **Yes** — ALB-only feature | No | No — GWLB has no listener rules at all |
| Target group health checks | Yes | Yes | Yes (separate configurable protocol/port from the GENEVE data path) |
| Cross-zone load balancing | Always on | Off by default, togglable | Always on, not configurable |
| Idle timeout | Yes (default 60s) | N/A (connection-based, different model) | N/A |
| Deregistration delay | Yes (default 300s) | Yes (default 300s) | Yes (default 300s) |
| Sticky sessions | **Yes** (app/duration cookie) | No | No |

🎯 **Exam tip:** "path-based routing" and "host-based routing" are **ALB-only** — if a question needs that and mentions NLB or GWLB, the answer is wrong; route it through ALB instead (or put an ALB behind/in front as appropriate).

🎯 **Exam tip:** cross-zone load balancing is **always-on and free at the load balancer level for ALB**, but **off-by-default and potentially chargeable for NLB** — a classic exam contrast.

---

## 11. Recap

- **Listener** = protocol+port the LB listens on; **Listener rule** = priority-ordered conditions+actions, default rule is the catch-all.
- **Target group** = pool of targets + health check config + target type; **Target** = one registered instance/IP/Lambda.
- **Health check** failure takes a target out of rotation — it does **not** terminate anything; that's the ASG's job when the target group is attached to one.
- **Cross-zone load balancing**, **idle timeout**, **deregistration delay** (the modern name for connection draining), and **sticky sessions** each have different defaults and applicability across ALB/NLB/GWLB — memorize the table in Section 10.
- Next: Note 03 — Load Balancer VPC Design (Hands-On).

---

### Sources
- [Listeners for your Application Load Balancers – AWS docs](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html)
- [Target groups for your Application Load Balancers – AWS docs](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-target-groups.html)
- [Health checks for your Application Load Balancer target groups – AWS docs](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html)
- [Sticky sessions for your Application Load Balancer – AWS docs](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/sticky-sessions.html)
