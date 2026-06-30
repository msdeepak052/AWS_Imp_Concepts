# AWS ElastiCache
---

## ✅ What is ElastiCache?

**Amazon ElastiCache** is an **in-memory data store and cache service** that supports **Redis** and **Memcached**. It helps **reduce load** on RDS databases by **caching frequently accessed data**, thus improving application **performance and latency**.

---

## ✅ Why use ElastiCache with RDS?

Let’s say you have a web application querying RDS for:

* Product listings
* User profile details
* Frequently accessed but rarely updated data

These queries can be **offloaded** to ElastiCache by storing them temporarily in-memory, so repeated requests do **not hit the RDS cluster** every time.

---

## ✅ Architecture Overview

```
Client App
   |
   |--> Check ElastiCache (Redis)
   |       └── Hit? Return data
   |       └── Miss? Query RDS → Store result in Redis → Return data
   |
   └--> Amazon RDS (Aurora/MySQL/PostgreSQL)
```

---

## ✅ Steps to Setup ElastiCache with RDS (Redis + MySQL Example)

---

### **Step 1: Launch Your RDS Cluster (if not already)**

1. Go to AWS Console → RDS → Create database
2. Choose MySQL or PostgreSQL or Aurora
3. Select instance specs, networking (VPC, subnets), and DB name
4. Create and wait for it to be **Available**

---

### **Step 2: Create an ElastiCache Cluster (Redis)**

1. Go to **ElastiCache → Redis → Create**
2. Choose:

   * **Cluster Mode Disabled** (for simple single node) or enabled for high availability
   * Engine: **Redis**
3. Choose the same **VPC** as your RDS
4. Under Subnet Group, create a new **Redis Subnet Group** if needed
5. Set **Security Group** to allow inbound connections from your app server or EC2
6. Launch the cluster and note down the **Primary Endpoint**

---

### **Step 3: Configure Security Groups**

Ensure:

* Your **ElastiCache Security Group** allows **inbound TCP on port 6379** (default Redis port) **from your application EC2** instances or wherever your backend is running.
* Your application server should be in the **same VPC** and **subnet availability zone** ideally, or at least routable.

---

### **Step 4: Integrate Redis with Your App**

Here's a **Python (Flask)** example:

```python
import redis
import pymysql

# Redis cache setup
cache = redis.StrictRedis(host='your-elasticache-endpoint', port=6379, decode_responses=True)

# MySQL RDS setup
conn = pymysql.connect(host='your-rds-endpoint', user='admin', password='password', db='mydb')

def get_user(user_id):
    # Try to get from cache first
    cached = cache.get(f"user:{user_id}")
    if cached:
        return f"From Cache: {cached}"
    
    # If not in cache, query RDS
    with conn.cursor() as cursor:
        cursor.execute("SELECT name FROM users WHERE id=%s", (user_id,))
        result = cursor.fetchone()
        if result:
            cache.setex(f"user:{user_id}", 300, result[0])  # store in Redis for 5 minutes
            return f"From DB: {result[0]}"
    return "User not found"
```

---

## ✅ Optional: Monitoring & Alerts

* Use **CloudWatch** to monitor Redis metrics (memory usage, cache hits/misses)
* Set up **Alarms** for CPU or memory thresholds
* Enable **automatic backups** if using Redis with cluster mode

---

## ✅ Best Practices

* Use Redis TTLs (`setex`) to avoid stale data
* Store serialized data (e.g., JSON) if caching complex queries
* Use consistent key naming (e.g., `user:{id}`, `product:{id}`)

---

## ✅ Summary

| Feature        | RDS             | ElastiCache (Redis)      |
| -------------- | --------------- | ------------------------ |
| Persistent     | ✅ Yes           | ❌ No (in-memory)         |
| Query Language | SQL             | NoSQL (Key-Value)        |
| Access Time    | \~10ms+         | \~1ms                    |
| Use Case       | Source of truth | Caching frequent queries |

---

