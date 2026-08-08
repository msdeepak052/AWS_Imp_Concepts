# 06 - AWS Route 53 — Geolocation Routing

![Image](https://images.openai.com/static-rsc-4/0t6eYjFMtDDXhZXglN2wxm3GcAYuPv7BhfhAzAIJ3UGVOzhS0jTXp2-tnCEkDLeYTunAcc2ub8fPy2gtgxDzqL87zOa2Zx7ILizs1wmpdoK24wNXiHhZs-CsP1nDK4IJWbLMrRjlYF3lmFmLLsRW9aKfoK0uG8SbCPPlIdzoLgwOusSQDHVIqJ76BHlZMIeB?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/4HOvpY8NtZCDedWrOBEvVa1_U4wzbvKABCeTJvvmJC-qFcjh19USA6y4cpDffpsS7rLulCZU8ZlKwEBSPVgcllwX6Th6qxolVZ1GWhfuNXQyhMAOCkLysR2WmgqtQX5bMhBHnaXm6n4Eq9KNg7xFxaqNMTTsCSmkNMPD69r9xDUFHVeVWnicHGLLdUXL-x_-?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/sATBgkq6afYcyxhcX1ECde7TEhtW5L3ugWeVDUxK9hG5_QAYFAC-n8YbezrMvqrMZQ2R4HeeOK2gvly_fQhWq8sucopArgdO-Co2yurccA4abiBET1t4ema0b3dRhrV0u8iPg2L82bC0_YyaFY4_qxRx3o-dPz_5dKtpMiV0ivbubEc9cl3sALwPJ5b1Q5tO?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/uX31EdlZgkgoVFhGJOZiLG5EuGh4WJAESA7HYg9jkqa-DD99XKYLID6rSigM-f6YPFQJbAYzCN7JadU2i7yCXvFxqes7Vkd-5W7v94iM774yJnKXmiEySOemY5tNASwugwuHR88zrlOAaeHuoemnUdEWpOstlNPZws25bJ0Sn6tSKsl0qCnQRsBBGPR_OUCI?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/kRagt4_s4CzYXlf8ybcWliO1rLideoxnu0Phy4vWCYwo277u7iI_Z9b4kd2gE2Mhp1dncuWcZULbwUq-VhBEYJenJ2E8yka6L9FtPe-9koduOhKWuo3PfLV2kkgoAM6LhTo5uyMCNbduqsevLaSwM_wtVOntwhbqPuftnC0lqyPT7QiPv0O-kY9kcN-dEje9?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/ocHBC6FDEGROo4gqXHQdXrQXewVhZyNlSiTtkoE35RPGFL1_wH-70AwznXKuJNrXO5Ahitl4vs04J8X4-8DvTdJ26c_4CPfqW1u0x3jjOlhWwGSK7rY05sAcfo4ER5DdcHVBWRET1MBPJyqwbQSP4v7ZOZp-FK-pRIPjQPjjRmyft8xz6dL3ovODNGqzKuGj?purpose=fullsize)

## 1. What is Geolocation Routing?

**Geolocation Routing** in Amazon Route 53 routes users to different resources based on **where the user is geographically located**.

In simple terms:

> **"Send users to a specific AWS resource based on the user's country, continent, or geographic location."**

For example:

```text
                    Users
                      |
                      v
                Route 53 DNS
                      |
          +-----------+-----------+
          |           |           |
       India       USA         Europe
          |           |           |
          v           v           v
       ALB-IND     ALB-USA     ALB-EU
```

A user from:

* 🇮🇳 India → India application
* 🇺🇸 USA → US application
* 🇩🇪 Germany → Europe application

---

# 2. Why would we use Geolocation Routing?

Suppose your company has applications deployed in three regions:

```text
India
ap-south-1

USA
us-east-1

Europe
eu-west-1
```

You want:

```text
Indian users  → India application
US users      → US application
European users → Europe application
```

Route 53 Geolocation Routing can implement this.

### Example

```text
                    www.example.com
                           |
                           v
                     Route 53
                           |
             "Where is the user?"
                           |
          +----------------+----------------+
          |                |                |
       India              USA            Europe
          |                |                |
          v                v                v
      ap-south-1       us-east-1        eu-west-1
```

---

# 3. How does Route 53 know the user's location?

Route 53 determines the **geographic location of the DNS resolver/client** and uses that information to select the appropriate record.

The important idea for the exam is:

```text
User Location
      ↓
Route 53
      ↓
Geolocation rule
      ↓
Corresponding DNS record
      ↓
Application endpoint
```

It does **not** mean Route 53 is measuring which AWS region has the lowest network latency.

That's a different routing policy.

---

# 4. Geolocation vs Latency-Based Routing

This is one of the most important distinctions.

### Geolocation Routing

Question:

> **"Where is the user?"**

Example:

```text
User in India
      ↓
Route 53
      ↓
India endpoint
```

### Latency-Based Routing

Question:

> **"Which AWS region gives this user the lowest latency?"**

Example:

```text
User in India
      ↓
Route 53
      ↓
Measure/select lowest-latency AWS region
      ↓
Maybe Mumbai
```

The selected region isn't necessarily based on your desired geographic boundary.

---

## Quick comparison

| Routing Policy | Decision based on          |
| -------------- | -------------------------- |
| Simple         | Single resource            |
| Weighted       | Percentage/weight          |
| Latency        | Lowest network latency     |
| Geolocation    | User's geographic location |
| Geoproximity   | Geographic distance + bias |
| Failover       | Health/failover state      |
| Multi-value    | Multiple healthy resources |
| IP-based       | Client IP mapping          |

### Remember:

**Geolocation = Location**

**Latency = Network performance**

---

# 5. Geolocation hierarchy

Route 53 allows you to define locations such as:

```text
Continent
   ↓
Country
   ↓
US State
```

For example:

```text
North America
    |
    +--- USA
    |     |
    |     +--- California
    |     +--- Texas
    |
    +--- Canada
```

You can create records based on these geographic boundaries.

---

# 6. Example — Country-Based Routing

Suppose you have:

```text
Application India
ALB DNS:
india-alb.example.com

Application USA
ALB DNS:
usa-alb.example.com

Application Germany
ALB DNS:
germany-alb.example.com
```

Route 53 can have:

```text
www.example.com
        |
        v
    Route 53
        |
        +---- India ----> india-alb.example.com
        |
        +---- USA ------> usa-alb.example.com
        |
        +---- Germany --> germany-alb.example.com
```

### User 1

User is in India:

```text
www.example.com
      ↓
Route 53
      ↓
India rule
      ↓
India ALB
```

### User 2

User is in USA:

```text
www.example.com
      ↓
Route 53
      ↓
USA rule
      ↓
USA ALB
```

### User 3

User is in Germany:

```text
www.example.com
      ↓
Route 53
      ↓
Germany rule
      ↓
Germany ALB
```

---

# 7. Real-world example — Banking application

Imagine a bank operates in:

* India
* UK
* USA

The architecture is:

```text
                         Internet
                            |
                            v
                     Route 53 DNS
                            |
            +---------------+---------------+
            |               |               |
          India             UK             USA
            |               |               |
            v               v               v
        ALB India        ALB UK         ALB USA
            |               |               |
          EKS             EKS             EKS
            |               |               |
           DB              DB              DB
```

You could configure:

```text
India users → India application
UK users    → UK application
USA users   → USA application
```

This can be useful when applications need to follow **regional data residency or business requirements**.

---

# 8. Very Important — Default Location

What happens if Route 53 doesn't have a specific record for the user's location?

You should configure a **Default** geolocation record.

Example:

```text
India → India ALB
USA → USA ALB
Europe → Europe ALB
Default → Global/Backup ALB
```

Why?

Because not every possible location may have an explicitly configured record.

For example:

```text
User from Brazil
      ↓
Route 53
      ↓
No Brazil-specific rule
      ↓
Default
      ↓
Default application
```

### Exam tip

> **Always consider a Default geolocation record when designing geolocation routing.**

---

# 9. Example with Continent + Country

Suppose you want:

```text
India → India application

Rest of Asia → Singapore application

Europe → Frankfurt application

USA → Virginia application

Rest of world → Global application
```

You could configure:

```text
Route 53
   |
   +--- India
   |      ↓
   |   Mumbai
   |
   +--- Asia
   |      ↓
   |   Singapore
   |
   +--- Europe
   |      ↓
   |   Frankfurt
   |
   +--- USA
   |      ↓
   |   Virginia
   |
   +--- Default
          ↓
       Global
```

The more specific geographic rule can take precedence over a broader geographic rule.

So:

```text
India
```

can have its own rule even though India is part of:

```text
Asia
```

---

# 10. Geolocation Routing is NOT traffic distribution

This is a common misunderstanding.

Suppose:

```text
India → Mumbai
USA   → Virginia
```

Geolocation routing does **not** mean:

```text
50% → Mumbai
50% → Virginia
```

It means:

```text
India users → Mumbai
USA users   → Virginia
```

The routing decision is based on **geographic location**, not percentage.

If you want:

```text
70% → Application A
30% → Application B
```

use **Weighted Routing**.

---

# 11. Geolocation vs Geoproximity

These two are easy to confuse.

### Geolocation

You explicitly define geographic boundaries.

```text
India → Mumbai
USA → Virginia
Europe → Frankfurt
```

Think:

> **"Users from this location should go here."**

---

### Geoproximity

Geoproximity routes traffic based on the **geographic location of users and resources**, with an optional **bias**.

Think:

> **"Route users toward the closest resource, but let me shift more traffic toward one resource."**

For example:

```text
                 Users
                   |
          +--------+--------+
          |                 |
       Mumbai            Singapore
        AWS                 AWS
       Region              Region
```

You can use bias to expand or shrink the geographic area served by a resource.

### Easy memory trick

```text
Geolocation
    ↓
"Where are my USERS?"

Geoproximity
    ↓
"How geographically CLOSE are users to RESOURCES?"
```

---

# 12. Geolocation with Health Checks

You can also combine geolocation routing with Route 53 health checks.

Example:

```text
India users
     |
     v
India ALB
     |
   Healthy?
   /     \
 Yes      No
 |         |
 v         v
India     Backup
```

This allows you to build more resilient architectures.

For example:

```text
India users
     |
     v
India endpoint
     |
  unhealthy
     |
     v
Default/backup endpoint
```

---

# 13. Important limitation

Geolocation routing is based on **geographic location**, not exact physical GPS location.

For example:

```text
User
 ↓
DNS query
 ↓
Route 53 determines geographic source
 ↓
Geolocation rule
```

So don't think of it as:

```text
"User is exactly 12 km from Mumbai."
```

That's not what this routing policy is designed for.

---

# 14. Complete Example

Imagine you own:

```text
example.com
```

You have:

```text
🇮🇳 India
ap-south-1
ALB → india.example.com

🇺🇸 USA
us-east-1
ALB → usa.example.com

🇬🇧 UK
eu-west-2
ALB → uk.example.com
```

Route 53:

```text
                    example.com
                         |
                         v
                    Route 53
                         |
       +-----------------+-----------------+
       |                 |                 |
     India              USA               UK
       |                 |                 |
       v                 v                 v
   India ALB          USA ALB           UK ALB
       |                 |                 |
      EKS               EKS               EKS
```

Requests:

```text
User in Bangalore
       ↓
example.com
       ↓
Route 53
       ↓
India
       ↓
India ALB
```

```text
User in New York
       ↓
example.com
       ↓
Route 53
       ↓
USA
       ↓
USA ALB
```

```text
User in London
       ↓
example.com
       ↓
Route 53
       ↓
UK
       ↓
UK ALB
```

---

# 15. SAA-C03 Exam Perspective

If the question says:

> A company wants users from different countries to access different endpoints based on their geographic location.

Think immediately:

### ✅ Route 53 Geolocation Routing

If it says:

> Send users to the AWS Region that provides the lowest latency.

Think:

### ✅ Latency-Based Routing

If it says:

> Send 80% of traffic to one endpoint and 20% to another.

Think:

### ✅ Weighted Routing

If it says:

> Route users to resources based on geographic distance and allow administrators to shift traffic using bias.

Think:

### ✅ Geoproximity Routing

---

## 🧠 One-page memory notes

```text
ROUTE 53 GEOLOCATION ROUTING
────────────────────────────────────────

Purpose:
Route DNS requests based on USER LOCATION.

Decision:
"Where is the user?"

Examples:
India → Mumbai
USA → Virginia
Europe → Frankfurt

Can route based on:
✓ Country
✓ Continent
✓ US state
✓ Default location

Important:
Configure a DEFAULT record for locations
that don't have a specific rule.

NOT based on:
✗ Percentage
✗ Lowest latency
✗ Health alone
✗ Geographic distance to AWS resource

Compare:

Geolocation
→ User's geographic location

Latency
→ Lowest network latency

Weighted
→ Traffic percentage

Geoproximity
→ Geographic distance + bias

Failover
→ Primary/secondary based on health

Multi-value
→ Return multiple healthy IPs
```

### The easiest way to remember it

> **Geolocation = "WHERE is the USER?"**

> **Latency = "WHERE is the FASTEST AWS REGION?"**

> **Weighted = "HOW MUCH TRAFFIC should each endpoint receive?"**

> **Geoproximity = "HOW CLOSE is the USER to the RESOURCE, and can I shift the boundary?"**

### Sources
- [Geolocation routing — AWS docs](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy-geo.html)
- [Values specific for geolocation records — AWS docs](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-values-geo.html)
- [How Amazon Route 53 uses EDNS0 to estimate the location of a user — AWS docs](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy-edns0.html)
