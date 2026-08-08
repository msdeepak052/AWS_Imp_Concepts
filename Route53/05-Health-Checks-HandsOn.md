# 05 - Route 53 Health Checks 

## 1. What is a Health Check?

A **Route 53 Health Check** monitors whether an endpoint is healthy or unhealthy.

Example:

```text
Route 53
    |
    v
Health Check
    |
    v
ALB / EC2 / Website
    |
    +--- Healthy   → Traffic allowed
    |
    +--- Unhealthy → Failover to backup
```

### Example

You have:

```text
Primary   → ALB-1
Secondary → ALB-2
```

If ALB-1 becomes unhealthy:

```text
User
 ↓
Route 53
 ↓
ALB-1 ❌
 ↓
ALB-2 ✅
```

---

# 2. What is Required?

For a basic health check, you need:

* **Endpoint** — IP address, domain name, or URL
* **Protocol** — HTTP / HTTPS / TCP
* **Port** — e.g. `80` or `443`
* **Path** — e.g. `/health` or `/`
* **Failure threshold** — how many failures before unhealthy

Example:

```text
Protocol : HTTP
IP/Domain: myapp.example.com
Port     : 80
Path     : /health
```

---

# 3. AWS Console — Create Health Check

The best demo is to create **2 EC2 web servers**, give each a **Weighted Route 53 record**, and attach a **separate health check to each record**.

## 1. What are we building?

```text
                         User
                           |
                           v
                     Route 53
                  www.example.com
                           |
              +------------+------------+
              |                         |
        Weight = 70                Weight = 30
              |                         |
          Health Check 1            Health Check 2
              |                         |
              v                         v
          EC2-Server-1             EC2-Server-2
           70% traffic              30% traffic
```

So normally:

```text
EC2-1 → ~70% traffic
EC2-2 → ~30% traffic
```

If **EC2-1 becomes unhealthy**, Route 53 can stop returning its record and route traffic to the healthy endpoint.

---

# 2. Prerequisites

You need:

* 2 EC2 instances
* Apache/Nginx running on both
* Public connectivity for the health checks
* A Route 53 hosted zone, e.g. `example.com`
* Two public DNS endpoints/IPs

For the demo, make the webpages different:

### EC2-1

```html
<h1>SERVER 1</h1>
```

### EC2-2

```html
<h1>SERVER 2</h1>
```

This makes it easy to see which server received the request.

---

# 3. Create Health Check for Server 1

Go to:

**Route 53 → Health checks → Create health check**

Choose:

```text
What to monitor: Endpoint
Protocol: HTTP
IP address: <EC2-1-PUBLIC-IP>
Port: 80
Path: /
```

Create it.

You should eventually see:

```text
Health Check 1
Status: Healthy ✅
```

---

# 4. Create Health Check for Server 2

Create another health check:

```text
What to monitor: Endpoint
Protocol: HTTP
IP address: <EC2-2-PUBLIC-IP>
Port: 80
Path: /
```

You should have:

```text
Health Check 1 → EC2-1 → Healthy ✅

Health Check 2 → EC2-2 → Healthy ✅
```

---

# 5. Create Weighted Record for Server 1

Go to:

**Route 53 → Hosted zones → your domain → Create record**

Example:

```text
Record name: app
Record type: A
Routing policy: Weighted
Weight: 70
Value: <EC2-1-PUBLIC-IP>
```

Then enable:

**Evaluate Target Health**

But for a standalone endpoint, the important part for this demo is associating the record with the health check.

Select:

```text
Health check → Health Check 1
```

Create the record.

---

# 6. Create Weighted Record for Server 2

Create another record with the **same name**:

```text
Record name: app
Record type: A
Routing policy: Weighted
Weight: 30
Value: <EC2-2-PUBLIC-IP>

Health check → Health Check 2
```

Now Route 53 has:

```text
app.example.com

        |
        +---- Weight 70 ----> EC2-1
        |                     Health Check 1
        |
        +---- Weight 30 ----> EC2-2
                              Health Check 2
```

---

# 7. Test the Weighted Routing

Run:

```bash
for i in {1..20}; do
    curl http://app.example.com
done
```

You should see approximately:

```text
SERVER 1
SERVER 1
SERVER 2
SERVER 1
SERVER 1
SERVER 1
SERVER 2
...
```

Over a sufficiently large number of DNS responses, traffic should approximately follow:

```text
EC2-1 → 70%
EC2-2 → 30%
```

**Important:** Don't expect exactly 14/6 requests out of 20. DNS caching/resolvers can make small samples look uneven.

---

# 8. Test Health Check Failure

Now stop the web server on EC2-1:

```bash
sudo systemctl stop nginx
```

or Apache:

```bash
sudo systemctl stop apache2
```

Health Check 1 eventually becomes:

```text
EC2-1 → Unhealthy ❌
```

Now Route 53 will stop using the unhealthy weighted record when selecting an answer, leaving the healthy EC2-2 record.

Conceptually:

```text
Before:

Route 53
   |
   +--- 70% → EC2-1 ✅
   |
   +--- 30% → EC2-2 ✅


After EC2-1 failure:

Route 53
   |
   +--- EC2-1 ❌  (removed from eligible answers)
   |
   +--- EC2-2 ✅
              |
              v
          Traffic
```

---

# 9. Start Server 1 Again

```bash
sudo systemctl start nginx
```

After the health check detects it as healthy:

```text
EC2-1 → Healthy ✅
EC2-2 → Healthy ✅
```

The weighted distribution becomes approximately:

```text
70% → EC2-1
30% → EC2-2
```

---

## 🧠 Final Notes

### Weighted Routing

> **Controls how traffic is distributed.**

```text
70 + 30 = 100
```

### Health Check

> **Determines whether an endpoint is healthy enough to receive traffic.**

### Combined

```text
Weighted Routing
       +
Health Checks
       ↓
Traffic distribution
with unhealthy endpoints excluded
```

### Your hands-on architecture

```text
                app.example.com
                       |
                    Route 53
                       |
             Weighted Routing
                 /         \
             Weight 70    Weight 30
                |            |
             HC-1           HC-2
                |            |
               EC2-1       EC2-2
                |            |
              :80           :80
                |            |
             Healthy       Healthy
```

**This is a very good SAA-C03 hands-on because it demonstrates two concepts together: *Weighted Routing* + *Route 53 Health Checks*.**

---

### Sources
- [How Amazon Route 53 determines whether a health check is healthy — AWS docs](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-determining-health-of-endpoints.html)
- [Creating, updating, and deleting health checks — AWS docs](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html)
- [Values that you specify when you create or update health checks — AWS docs](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/health-checks-creating-values.html)
