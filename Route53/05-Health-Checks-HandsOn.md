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

Go to:

**AWS Console → Route 53 → Health checks → Create health check**

### Step 1 — Choose what to monitor

Select:

**Endpoint**

Enter:

```text
Domain name: www.example.com
```

or an IP address.

### Step 2 — Configure

Example:

```text
Protocol : HTTPS
Port     : 443
Path     : /health
```

You can leave most other settings as default for a hands-on exercise.

### Step 3 — Create

Click:

**Create health check**

You will see:

```text
Status: Healthy
```

if the endpoint responds successfully.

---

# 4. Hands-On Example

Suppose your EC2 web server has:

```text
Public IP: 3.x.x.x
Port: 80
```

And accessing:

```text
http://3.x.x.x/
```

returns your webpage.

Create:

```text
Health Check
----------------
Type     : Endpoint
Protocol : HTTP
IP       : 3.x.x.x
Port     : 80
Path     : /
```

Route 53 will periodically check:

```text
Route 53 Health Check
        |
        | HTTP GET /
        ↓
    EC2 :80
        |
        ↓
    HTTP 200
        |
        ↓
     Healthy ✅
```

---

# 5. Important Hands-On Test

After creating the health check:

### Healthy

```text
EC2 running
Web server running
Port 80 open
        ↓
Health Check = Healthy ✅
```

### Make it unhealthy

Stop the web server:

```bash
sudo systemctl stop nginx
```

After some time:

```text
Health Check = Unhealthy ❌
```

Start it again:

```bash
sudo systemctl start nginx
```

It should eventually become:

```text
Healthy ✅
```

---

## ⭐ Important for SAA

Health Check **alone does NOT automatically move DNS traffic somewhere else**.

For actual traffic failover, typically use:

```text
Route 53
   |
   +-- Primary record
   |      |
   |   Health Check
   |
   +-- Secondary record
```

with **Failover Routing**.

**Remember:**

> **Health Check = Is the endpoint healthy?**

> **Failover Routing = Where should traffic go when the primary is unhealthy?**


---

### Sources
- [How Amazon Route 53 determines whether a health check is healthy — AWS docs](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-determining-health-of-endpoints.html)
- [Creating, updating, and deleting health checks — AWS docs](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html)
- [Values that you specify when you create or update health checks — AWS docs](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/health-checks-creating-values.html)
