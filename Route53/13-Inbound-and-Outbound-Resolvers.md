# Route 53 Resolver — Inbound vs Outbound

This topic is mainly about **hybrid DNS**: when you have DNS names in **AWS VPCs** and DNS names in an **on-premises data center**, and both sides need to resolve each other's names.

AWS Route 53 Resolver provides **inbound and outbound endpoints** for this purpose. ([AWS Documentation][1])

---

# 1. First understand the problem

Imagine your company has:

```text
                 AWS
        +-------------------+
        |       VPC         |
        |                   |
        | EC2               |
        | app.aws.local     |
        +-------------------+
                 |
              VPN / DX
                 |
        +-------------------+
        |    On-Premises    |
        |                    |
        | DNS Server         |
        |                    |
        | app.bank.local     |
        +-------------------+
```

Now there are **two DNS requirements**.

### Requirement 1 — AWS → On-Prem

An EC2 instance needs to resolve:

```text
db.bank.local
```

But this DNS record exists only on the **on-premises DNS server**.

### Requirement 2 — On-Prem → AWS

An on-premises server needs to resolve:

```text
app.aws.local
```

But this record exists in an **AWS Route 53 Private Hosted Zone**.

These are solved using:

```text
AWS → On-Prem       = OUTBOUND Resolver
On-Prem → AWS       = INBOUND Resolver
```

That's the most important thing to remember.

---

# 2. The Big Picture

```text
                         AWS VPC
              +---------------------------+
              |                           |
              |        EC2 Instance       |
              |             |             |
              |             v             |
              |      Route 53 Resolver    |
              |             |             |
              |      Outbound Endpoint     |
              |             |             |
              +-------------|-------------+
                            |
                      VPN / Direct Connect
                            |
              +-------------|-------------+
              |             v             |
              |     On-Prem DNS Server    |
              |                           |
              +---------------------------+

                       ↑
                       |
              Inbound Endpoint
                       |
                  Route 53 Resolver
                       |
                  Private Hosted Zone
                       |
                    AWS resources
```

Think of the endpoints as **DNS doors** between AWS and your corporate network.

---

# 3. OUTBOUND Resolver Endpoint

## What does Outbound mean?

**Outbound = DNS query is leaving AWS.**

```text
AWS
 |
 | DNS query
 v
On-Premises
```

Suppose EC2 wants:

```text
db.corp.example.com
```

and that DNS name is managed by your on-premises DNS server.

The flow is:

```text
EC2
 |
 | "What is db.corp.example.com?"
 v
Route 53 VPC Resolver
 |
 | Matching forwarding rule
 v
Outbound Resolver Endpoint
 |
 | VPN / Direct Connect
 v
On-Prem DNS
 |
 | Answer: 10.20.10.50
 v
EC2
```

AWS officially describes an outbound endpoint as forwarding DNS queries **from the VPC to your network**. ([AWS Documentation][2])

---

# 4. Why do we need a Resolver Rule?

This is where **conditional forwarding** comes in.

Suppose your on-premises DNS owns:

```text
corp.example.com
```

You don't want every DNS query from AWS to go to on-premises.

You only want:

```text
*.corp.example.com
```

to go there.

So you create a Resolver forwarding rule:

```text
Domain:
corp.example.com

Forward to:
10.20.1.10
10.20.1.11

Through:
Outbound Endpoint
```

Meaning:

```text
Query: db.corp.example.com
              ↓
Matches corp.example.com
              ↓
Forward to On-Prem DNS
```

But:

```text
Query: www.google.com
              ↓
Doesn't match rule
              ↓
Normal DNS resolution
```

That's what **conditional forwarding** means:

> **Only DNS queries matching a particular domain are forwarded to the specified DNS servers.** ([AWS Documentation][3])

---

# 5. OUTBOUND Architecture

```text
                         AWS VPC
┌────────────────────────────────────────────────┐
│                                                │
│   EC2                                         │
│    │                                           │
│    │ DNS: db.corp.example.com                 │
│    ↓                                           │
│ Route 53 VPC Resolver                         │
│    │                                           │
│    │ Resolver Rule                            │
│    │ corp.example.com                         │
│    ↓                                           │
│ Outbound Resolver Endpoint                    │
│    │                                           │
└────|───────────────────────────────────────────┘
     |
     | VPN / Direct Connect
     |
┌────|───────────────────────────────────────────┐
│    ↓                                           │
│ On-Prem DNS                                   │
│ 10.20.1.10                                    │
│                                                │
│ db.corp.example.com → 10.20.10.50             │
└────────────────────────────────────────────────┘
```

---

# 6. INBOUND Resolver Endpoint

Now reverse the direction.

**Inbound = DNS query is entering AWS.**

```text
On-Premises
     |
     | DNS query
     v
AWS
```

Suppose your AWS Private Hosted Zone contains:

```text
app.aws.example.com
```

with:

```text
app.aws.example.com → 10.0.10.50
```

An on-premises server wants to resolve it.

Flow:

```text
On-Prem Server
      |
      | "What is app.aws.example.com?"
      v
On-Prem DNS
      |
      | Forward this domain to AWS
      v
Route 53 Resolver
Inbound Endpoint
      |
      v
VPC Resolver
      |
      v
Private Hosted Zone
      |
      | 10.0.10.50
      v
On-Prem Server
```

AWS describes an inbound endpoint as allowing DNS queries **from your network into the VPC**. ([AWS Documentation][1])

---

# 7. INBOUND Architecture

```text
                   ON-PREMISES
┌────────────────────────────────────────────┐
│                                            │
│ Server                                      │
│   │                                        │
│   ↓                                        │
│ On-Prem DNS                                │
│   │                                        │
│   │ Forward aws.example.com                │
│   ↓                                        │
└───|────────────────────────────────────────┘
    |
    | VPN / Direct Connect
    |
┌───|────────────────────────────────────────┐
│   ↓                                        │
│ Route 53 Resolver                         │
│ Inbound Endpoint                           │
│   │                                        │
│   ↓                                        │
│ VPC Resolver                               │
│   │                                        │
│   ↓                                        │
│ Private Hosted Zone                        │
│                                            │
│ app.aws.example.com → 10.0.10.50           │
│                                            │
└────────────────────────────────────────────┘
```

For an inbound endpoint, your on-premises DNS server is configured to forward the relevant domain to the **IP addresses of the inbound endpoint**. AWS creates ENIs for the endpoint in the subnets you select. ([AWS Documentation][4])

---

# 8. Complete Hybrid DNS Architecture

This is the architecture you should remember for interviews and SAA-C03.

```text
                       AWS CLOUD
┌───────────────────────────────────────────────────────┐
│                                                       │
│                       VPC                             │
│                                                       │
│   EC2                                               │
│    │                                                  │
│    │ DNS query for corp.example.com                  │
│    ↓                                                  │
│ Route 53 Resolver                                    │
│    │                                                  │
│    ↓                                                  │
│ OUTBOUND ENDPOINT                                     │
│    │                                                  │
│    │                                                  │
│    │ VPN / Direct Connect                            │
│    │                                                  │
│    ↑                                                  │
│ INBOUND ENDPOINT                                      │
│    │                                                  │
│    ↓                                                  │
│ Route 53 Private Hosted Zone                         │
│                                                       │
│ app.aws.example.com → 10.0.10.50                     │
│                                                       │
└───────────────────────┬───────────────────────────────┘
                        │
                        │ VPN / Direct Connect
                        │
┌───────────────────────┴───────────────────────────────┐
│                  ON-PREMISES                          │
│                                                       │
│             Corporate DNS Server                      │
│                                                       │
│ corp.example.com                                      │
│ db.corp.example.com → 10.20.10.50                    │
│                                                       │
└───────────────────────────────────────────────────────┘
```

---

# 9. Two Demo Examples

## Demo 1 — AWS → On-Prem

### Requirement

EC2 needs:

```text
db.corp.example.com
```

On-prem DNS owns the record.

### Configuration

Create:

**Outbound Resolver Endpoint**

Then create:

**Forwarding Rule**

```text
Domain:
corp.example.com

Target DNS:
10.20.1.10
10.20.1.11

Endpoint:
Outbound Endpoint
```

### Test

From EC2:

```bash
nslookup db.corp.example.com
```

Flow:

```text
EC2
 ↓
Route 53 Resolver
 ↓
Rule matches corp.example.com
 ↓
Outbound Endpoint
 ↓
VPN/DX
 ↓
On-Prem DNS
 ↓
IP address
```

---

# 10. Demo 2 — On-Prem → AWS

### Requirement

On-prem server needs:

```text
app.aws.example.com
```

AWS Private Hosted Zone contains:

```text
app.aws.example.com → 10.0.10.50
```

### Configuration

Create:

**Inbound Resolver Endpoint**

For example:

```text
Inbound Endpoint IPs:

10.0.1.50
10.0.2.50
```

Then configure the on-prem DNS server:

```text
aws.example.com
       ↓
Forward to
       ↓
10.0.1.50
10.0.2.50
```

Now:

```bash
nslookup app.aws.example.com
```

Flow:

```text
On-Prem Server
 ↓
On-Prem DNS
 ↓
Inbound Endpoint
 ↓
Route 53 Resolver
 ↓
Private Hosted Zone
 ↓
10.0.10.50
```

---

# 11. Why use two IP addresses?

For production, Resolver endpoints should be deployed across multiple Availability Zones for resilience.

Conceptually:

```text
                 VPC
        ┌───────────────────┐
        │                   │
        │ AZ-1       AZ-2   │
        │  │           │    │
        │  ▼           ▼    │
        │ ENI         ENI   │
        │ 10.0.1.10  10.0.2.10
        │                   │
        └───────────────────┘
```

So your DNS service isn't dependent on one AZ.

---

# 12. Inbound vs Outbound — The Easy Table

|                              | **Inbound**                            | **Outbound**                   |
| ---------------------------- | -------------------------------------- | ------------------------------ |
| Direction                    | On-Prem → AWS                          | AWS → On-Prem                  |
| DNS query enters/leaves      | **Enters AWS**                         | **Leaves AWS**                 |
| Endpoint receives query from | On-Prem DNS                            | AWS Resolver                   |
| Endpoint sends query toward  | AWS VPC Resolver                       | On-Prem DNS                    |
| Typical use                  | Resolve AWS private names from on-prem | Resolve on-prem names from AWS |
| Needs Resolver Rule?         | Usually no AWS outbound rule           | **Yes, forwarding rule**       |
| Example                      | `app.aws.local`                        | `db.corp.local`                |

### Memory trick

> **INBOUND = DNS comes IN to AWS**

> **OUTBOUND = DNS goes OUT of AWS**

---

# 13. Don't confuse Resolver with Route 53 Hosted Zones

This is another important distinction.

### Private Hosted Zone

Stores DNS records:

```text
app.internal.example.com
        ↓
10.0.10.50
```

### Resolver Endpoint

Provides the **connection/path for DNS queries** between AWS and your external network.

```text
Private Hosted Zone
       ↑
Route 53 Resolver
       ↑
Inbound Endpoint
       ↑
VPN/DX
       ↑
On-Prem
```

So:

> **Hosted Zone = Where DNS records live**

> **Resolver Endpoint = How DNS queries cross between networks**

---

# 14. SAA-C03 Exam Memory 🧠

If the question says:

### "EC2 needs to resolve on-premises DNS names"

Think:

**Outbound Resolver Endpoint + Resolver Rule**

```text
AWS → On-Prem
     OUTBOUND
```

### "On-premises servers need to resolve Route 53 private hosted zone names"

Think:

**Inbound Resolver Endpoint**

```text
On-Prem → AWS
         INBOUND
```

### If they need BOTH:

```text
                    Hybrid DNS
                        |
              +---------+---------+
              |                   |
           OUTBOUND            INBOUND
              |                   |
         AWS → On-Prem        On-Prem → AWS
              |                   |
       Resolver Rule        Private Hosted Zone
```

AWS specifically recommends Resolver endpoints and conditional forwarding for DNS resolution between VPCs and connected networks such as on-premises environments over VPN or Direct Connect. ([AWS Documentation][1])

[1]: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver.html?utm_source=chatgpt.com "What is Route 53 VPC Resolver? - Amazon Route 53"
[2]: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-forwarding-outbound-queries.html?utm_source=chatgpt.com "Forwarding outbound DNS queries to your network - Amazon Route 53"
[3]: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-forwarding-outbound-queries-rule-values.html?utm_source=chatgpt.com "Values that you specify when you create or edit rules - Amazon Route 53"
[4]: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-overview-forward-network-to-vpc.html?utm_source=chatgpt.com "How DNS resolvers on your network forward DNS queries to Resolver endpoints - Amazon Route 53"
