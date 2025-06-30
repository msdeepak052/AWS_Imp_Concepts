## 📘 What is **On-Demand Capacity Mode** in DynamoDB?

**On-Demand Capacity Mode** lets DynamoDB **automatically scale** read and write throughput **based on actual traffic**, without requiring you to manually set Read/Write Capacity Units (RCUs/WCUs).

You pay **per request** instead of provisioning capacity in advance.

---

## 🔹 Key Features

| Feature                    | Description                                                               |
| -------------------------- | ------------------------------------------------------------------------- |
| **No provisioning needed** | DynamoDB manages capacity internally.                                     |
| **Auto-scaling**           | Scales instantly to accommodate sudden spikes or drops in traffic.        |
| **Billing model**          | Pay per request (read/write)                                              |
| **Best for**               | Unpredictable workloads or low-to-medium consistent usage.                |
| **Limitations**            | More expensive than provisioned if traffic is consistent and high volume. |

---

## 🔸 Example: Read and Write Pricing Calculation

### Assume:

* 1 million **eventually consistent reads** (up to 4 KB each)
* 500,000 **standard writes** (up to 1 KB each)

### Pricing (as of AWS 2024, example region: US East):

* Read request unit = \$0.25 per million
* Write request unit = \$1.25 per million

### Cost:

* 1M reads × \$0.25 = **\$0.25**
* 0.5M writes × \$1.25 = **\$0.625**

✅ Total: **\$0.875 for this usage**

---

## ✅ Use Cases for On-Demand Mode

### 🔹 1. **Startups / New Applications**

* Traffic patterns unknown or highly variable.
* Avoid over-provisioning or throttling.

### 🔹 2. **Spiky Workloads**

* E.g., ticket booking systems, Black Friday sales, exam results.
* Handles thousands of requests during a short burst.

### 🔹 3. **Low-Traffic Tables**

* Tables used occasionally (e.g., user feedback, logs).
* Paying per request is cheaper than provisioned minimums.

### 🔹 4. **Development & QA Environments**

* Avoids manual tuning during testing.

---

## 🔸 When **NOT** to Use On-Demand

* **High, steady workloads** (e.g., > 5000 reads/sec consistently):

  * **Provisioned mode** + Auto Scaling is cheaper.

---

## 🔧 Switching Between Modes

You can switch **from provisioned to on-demand** (and vice versa) once every 24 hours **per table**.

---

## 🛠️ Terraform Example

```hcl
resource "aws_dynamodb_table" "example" {
  name           = "MyOnDemandTable"
  billing_mode   = "PAY_PER_REQUEST"  # Enables On-Demand mode

  hash_key       = "UserID"
  attribute {
    name = "UserID"
    type = "S"
  }
}
```

---

## 📘 What is **Provisioned Capacity Mode** in DynamoDB?

In **Provisioned Mode**, you manually specify:

* **Read Capacity Units (RCUs)**
* **Write Capacity Units (WCUs)**

DynamoDB then reserves this throughput for your table, and you’re **billed hourly** for the provisioned capacity — regardless of actual usage.

---

## 🔹 Key Features

| Feature                    | Description                                               |
| -------------------------- | --------------------------------------------------------- |
| **Manual provisioning**    | You specify RCU and WCU limits                            |
| **Predictable cost**       | Cost is based on provisioned capacity, not usage          |
| **Auto Scaling available** | Optional: Automatically adjusts provisioned values        |
| **Best for**               | Predictable workloads or applications with steady traffic |
| **Throttling possible**    | If requests exceed provisioned RCU/WCU limits             |

---

## 🔧 Example: Provisioned Table Setup

Suppose you set:

* **RCU** = 200
* **WCU** = 100

This means your table can:

* Serve **200 strongly consistent reads/sec** for 4KB items
* Handle **100 writes/sec** for 1KB items

### ⚠️ If you exceed this, you'll get:

* `ProvisionedThroughputExceededException` unless auto scaling is enabled.

---

## ✅ Use Cases

### 🔹 1. **E-commerce Site with Predictable Traffic**

* Daily traffic patterns (e.g., peak morning and evening hours).
* Set auto scaling to increase/decrease provisioned throughput.

### 🔹 2. **Gaming Leaderboard**

* Continuous writes for scores and frequent reads.
* Predictable and frequent usage = lower cost than on-demand.

### 🔹 3. **IoT Devices Streaming Data**

* Consistent ingestion from fixed number of sensors.
* Better cost control with fixed WCU allocation.

---

## 🔁 Switching Between Modes

You can switch between **on-demand** and **provisioned** **once per table every 24 hours**.

---

## 🔸 DynamoDB Provisioned Mode Terraform Example

```hcl
resource "aws_dynamodb_table" "my_provisioned_table" {
  name         = "MyProvisionedTable"
  billing_mode = "PROVISIONED"

  read_capacity  = 200
  write_capacity = 100

  hash_key = "UserID"
  attribute {
    name = "UserID"
    type = "S"
  }

  # Optional auto scaling (not shown here)
}
```

---

## 📊 Provisioned vs On-Demand Comparison

| Feature                | **Provisioned Mode**                           | **On-Demand Mode**                      |
| ---------------------- | ---------------------------------------------- | --------------------------------------- |
| **Capacity control**   | You configure RCU and WCU manually             | Auto-managed by DynamoDB                |
| **Billing**            | Pay per provisioned capacity (hourly)          | Pay per request                         |
| **Scaling**            | Optional auto scaling (slower reaction)        | Instant, elastic scaling                |
| **Best for**           | Steady, predictable workloads                  | Spiky, unpredictable workloads          |
| **Risk of throttling** | Yes, if requests > provisioned capacity        | No, unless hard limits are hit          |
| **Cost optimization**  | More cost-effective for high/steady throughput | Better for unpredictable or low traffic |
| **Switching limit**    | Can switch mode once per 24 hours per table    | Same                                    |

---

## ✅ Summary Decision Matrix

| Situation                             | Recommended Mode               |
| ------------------------------------- | ------------------------------ |
| Low traffic, unpredictable            | **On-Demand**                  |
| High, consistent traffic              | **Provisioned**                |
| Startup with unknown usage            | **On-Demand**                  |
| Scheduled burst (e.g., nightly jobs)  | **Provisioned + Auto Scaling** |
| Mission-critical with consistent load | **Provisioned (lower cost)**   |

---


Let’s explore **DynamoDB Warm Throughput** — a lesser-known but critical concept when dealing with performance and scaling in provisioned capacity mode.

---

## 📘 What is **Warm Throughput** in DynamoDB?

**Warm throughput** refers to DynamoDB's ability to **quickly serve traffic at the full provisioned capacity**, **after the table or partition has already been receiving traffic** (i.e., it’s “warm” or active).

### ❄️ Opposite: **Cold Start**

When a table or partition hasn’t received traffic for a while, it may become **cold**, and suddenly ramping up traffic can cause **throttling**, even if you're within your provisioned limits.

---

## 🔥 Warm vs. Cold Throughput Analogy

| Concept  | Behavior                                                               |
| -------- | ---------------------------------------------------------------------- |
| **Warm** | Table is actively being read/written. Traffic is stable and sustained. |
| **Cold** | Table/partition is idle, and suddenly high traffic arrives (burst).    |

---

## 📊 Example

### Scenario:

* You provision 1,000 WCUs for a table.
* It remains **idle** (cold) for 6 hours.
* Suddenly, you send 800 write requests per second.

### What Happens:

* Even though you’re **under the 1,000 WCU limit**, DynamoDB may **throttle** some requests for a short time.
* Reason: AWS **ramps up partitions slowly** when waking from cold state (to prevent abuse and ensure fairness).

---

## ✅ How to Keep Throughput Warm

### 🛠️ Strategies:

1. **Ping the table periodically**:

   * Send dummy reads/writes every few minutes to keep it “warm”.

2. **Auto scaling with minimum capacity**:

   * Set a base threshold (e.g., 200 RCUs and WCUs) to prevent full cold states.

3. **Use On-Demand mode**:

   * Automatically handles cold-to-hot transitions better than provisioned mode.

---

## 📦 Use Cases & Impacts

| Use Case                         | Impact of Warm Throughput                        | Recommendation                       |
| -------------------------------- | ------------------------------------------------ | ------------------------------------ |
| **Retail App** (burst traffic)   | Sudden spikes can hit cold partitions            | Use warm-up writes or on-demand mode |
| **IoT Devices** (stable traffic) | Table remains warm due to consistent input       | Provisioned mode with stable usage   |
| **Scheduled batch jobs**         | May face throttling if table is idle most of day | Send pre-job warm-up requests        |
| **Periodic backup/check**        | Idle table accessed rarely                       | Consider on-demand or warm-up pings  |

---

## 🧠 Summary

* **Warm throughput** means your provisioned table is already active and can serve full RCU/WCU instantly.
* **Cold tables** need time to ramp up, risking throttling.
* To maintain performance:

  * Periodically send small requests.
  * Use **on-demand mode** for unpredictable workloads.
  * Use **auto scaling** with sensible minimums.

---



