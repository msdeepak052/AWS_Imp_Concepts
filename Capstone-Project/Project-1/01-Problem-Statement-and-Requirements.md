# 01 - Problem Statement and Requirements

> Goal: establish the client brief for **CloudMart** — the single capstone project this whole `Project-1` folder builds, end to end, using only VPC, EC2, Auto Scaling Groups, Elastic Load Balancing, and Route 53. Every later file in this folder (concept notes 02-04, then the hands-on builds 05-11) implements the requirements captured here. Read this file first — it's the "why" behind every design decision made downstream.

---

## 1. The client brief

> *"CloudMart is a small e-commerce startup that currently sells branded merchandise (t-shirts, mugs, stickers, hoodies, caps) through a single, manually-managed EC2 instance running everything — web server, application logic, and database — on one box. It's cheap, but it's also a single point of failure: the last time that instance rebooted for a patch, the storefront was down for twenty minutes, and the founders are worried about a bigger outage during a marketing push. They've asked for a rebuilt architecture that is highly available across multiple data centers, doesn't expose their application or database directly to the internet, can automatically absorb a traffic spike without manual intervention, and is reachable through a friendly domain name instead of a raw load balancer hostname. They are a small team, so they want to stay within a small, well-understood set of AWS services rather than adopting a large managed-services bill on day one."*

This becomes the CloudMart 3-tier web application: a frontend (product catalog page), a backend (a small REST API), and a database (the product catalog itself), deployed across two Availability Zones in **ap-south-1** (Asia Pacific — Mumbai), fronted by Route 53 under the illustrative domain `cloudmart.example`.

🧠 **Mental model:** every requirement below maps to exactly one AWS service from the five in scope. HA and scaling → EC2 + Auto Scaling Groups + Elastic Load Balancing. Isolation → VPC subnetting and security groups. Friendly DNS → Route 53. Nothing here needs VPN, Direct Connect, or a managed database — which is precisely why those are called out as out of scope in Section 4.

---

## 2. Functional requirements

| # | Requirement |
|---|---|
| F1 | A visitor browsing to the CloudMart domain must see a product catalog page listing the current items for sale (name, price, stock level). |
| F2 | The product catalog must be served dynamically from a backing database, not hardcoded into the web page — the frontend calls a backend API to fetch live data. |
| F3 | The backend must expose a REST API capable of both reading the catalog (`GET /api/products`) and adding a new product (`POST /api/products`), so the write path can be exercised as part of end-to-end testing later in this capstone. |
| F4 | The system must be reachable over a human-friendly domain name (`www.cloudmart.example`), not a raw load balancer DNS name. |
| F5 | The backend must never be reachable directly from the public internet — all traffic to it must pass through the frontend tier first. |

---

## 3. Non-functional requirements

### 3.1 High availability

- The application must survive the loss of a single Availability Zone without full downtime: every compute tier (frontend, backend) is deployed across **two AZs** (`ap-south-1a` and `ap-south-1b`), never one.
- Losing a single EC2 instance (crash, patching reboot, underlying host retirement) must be self-healing — an unhealthy instance is detected and replaced automatically, with no human paging a phone.
- Outbound internet access from the private tiers uses a single, shared NAT Gateway rather than one per AZ — a deliberate cost trade-off, not an oversight. It means both AZs' outbound package-update traffic depends on one AZ's NAT infrastructure staying up; inbound traffic to the app (via the load balancers, across both AZs) is completely unaffected if that NAT Gateway fails. Note 02 names this gap explicitly.

### 3.2 Security

- No security group in this project may open inbound port 22 (SSH) from anywhere. Administrative access to any instance happens through **AWS Systems Manager Session Manager**, not SSH keys or a bastion host.
- All three tiers — frontend, backend, and database — must live in **private subnets** with no route to the internet other than outbound-only via NAT; none of them is directly reachable from a public IP. Only the load balancers themselves sit in public subnets.
- Each tier must only accept inbound traffic from the specific tier immediately in front of it (a chained security-group model), never from a broad CIDR range.

### 3.3 Scalability

- The frontend and backend tiers must scale independently of one another, since a traffic spike doesn't necessarily load both tiers equally (e.g., cached static assets vs. API-heavy requests).
- Scaling must be automatic, triggered by a measurable load signal (CPU utilization), not a manual "add another instance" console click during a traffic spike.

### 3.4 DNS

- The application must be reachable under a friendly domain name, with the DNS layer aware of the load balancer's health so it can, in principle, support failover routing later.

### 3.5 Cost-awareness

- The founders explicitly want a small, well-understood service footprint. Every additional always-on resource is a recurring cost: one NAT Gateway, two Application Load Balancers, and a Route 53 health check all bill continuously (hourly plus usage-based charges) whether or not a single customer visits the site that hour. Using a single shared NAT Gateway instead of one per AZ is itself a cost-awareness decision — half the hourly NAT charge, accepted in exchange for the named HA gap in Section 3.1. This capstone accepts that remaining cost as the price of the HA/security requirements above, but it should be stated plainly rather than discovered later on a bill — Note 11 (End-to-End Testing, HA Validation, and Cleanup) closes the loop by tearing every one of these resources back down in the correct order once the capstone is complete.

---

## 4. Out of scope for this capstone

| Excluded | Reason |
|---|---|
| **AWS Site-to-Site VPN** | CloudMart is a pure public-internet storefront with no on-premises network to connect back to. VPN is an enterprise/hybrid-connectivity topic — solving "connect our office network to our VPC," which isn't a problem CloudMart has. |
| **AWS Direct Connect** | Same reasoning as VPN, one level up in scale and cost: Direct Connect exists for sustained, high-bandwidth, private connectivity between an existing data center and AWS. CloudMart has no data center to connect from — this is an industry/enterprise-scale topic, not needed for a single-region public web app. |
| **Amazon RDS** | The brief limits this build to exactly five services: VPC, EC2, Auto Scaling Groups, Elastic Load Balancing, and Route 53. To stay strictly inside that scope, the database tier is a **self-managed MariaDB instance on a plain EC2 instance** rather than a managed RDS instance. This is a deliberate, named simplification — Note 02 calls out explicitly that this means the database tier has no Multi-AZ high availability, and that a real production build would use **RDS Multi-AZ** (or Aurora) instead. |
| **Multi-region disaster recovery** | Running a second, full copy of this stack in a second AWS Region (with Route 53 failover routing between them) is a legitimate next step for a business that outgrows single-region availability, but it doubles the infrastructure and cost described above. It's mentioned in Note 02 and Note 10 as "the next step up" from what's built here, but this capstone deliberately stops at single-region, multi-AZ availability. |

🎯 **Exam tip:** SAA-C03 loves scenario questions that describe a business problem and ask you to pick the *right-sized* service — not the most powerful one available. "Small team, single region, wants HA and auto-recovery" points at ASG + ELB + Multi-AZ subnetting, not at Direct Connect or a multi-region active-active design. Recognizing when a fancier service is over-engineering for the stated problem is exactly what's being tested.

---

## 5. Recap

- CloudMart is a startup outgrowing a single manually-managed EC2 instance; it needs HA, security isolation, independent auto scaling per tier, and friendly DNS — using only VPC, EC2, ASG, ELB, and Route 53.
- Functional requirements center on a working 3-tier product catalog app (frontend page, backend REST API, database) reachable under `www.cloudmart.example`.
- Non-functional requirements cover HA (2 AZs everywhere, self-healing, one named NAT gap), security (no SSH, private subnets for all three tiers, chained security groups), scalability (independent per-tier auto scaling), DNS (health-check-aware), and honest cost-awareness (a shared NAT Gateway/ALBs/health checks bill continuously).
- VPN, Direct Connect, RDS, and multi-region DR are explicitly out of scope, each for a stated reason — not oversights.
- Next: Note 02 — Architecture and Design, where these requirements become concrete named resources: the VPC, subnets, security group chain, load balancers, and Auto Scaling Groups.

### Sources
- [AWS Well-Architected Framework — Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html)
- [Amazon VPC User Guide — VPCs and subnets](https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html)
- [AWS Direct Connect — What Is AWS Direct Connect?](https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html)
- [Amazon RDS — Multi-AZ deployments](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html)
