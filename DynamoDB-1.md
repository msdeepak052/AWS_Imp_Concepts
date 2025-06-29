## ✅ What is **Amazon DynamoDB**?

**Amazon DynamoDB** is a **fully managed NoSQL database service** offered by AWS. It provides **single-digit millisecond performance at any scale** with **built-in high availability, security, backup, and in-memory caching**.

> ⚡️ It is ideal for applications that require **high throughput and low latency**, like IoT, gaming, serverless apps, and real-time analytics.

---

## ✅ DynamoDB Core Concepts

| Concept                          | Description                                                                      |
| -------------------------------- | -------------------------------------------------------------------------------- |
| **Table**                        | Collection of items (like a table in SQL)                                        |
| **Item**                         | A single record (like a row)                                                     |
| **Attribute**                    | A field within an item (like a column)                                           |
| **Primary Key**                  | Uniquely identifies each item in a table (Partition Key or Partition + Sort Key) |
| **Provisioned / On-Demand**      | Controls how capacity is allocated                                               |
| **Global Secondary Index (GSI)** | Additional queryable indexes                                                     |
| **Local Secondary Index (LSI)**  | Alternate sort key on the same partition key                                     |
| **Streams**                      | Real-time change log of table operations                                         |
| **DAX (DynamoDB Accelerator)**   | In-memory caching layer (like Redis)                                             |
| **TTL (Time to Live)**           | Auto-expire records after a set time                                             |
| **Backup/Restore**               | Point-in-time recovery and snapshot backups                                      |

---

## ✅ DynamoDB Modes

| Mode              | Description                                                                                                                                  |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **On-Demand**     | Auto-scales read/write instantly. Pay-per-request. Great for unpredictable workloads.                                                        |
| **Provisioned**   | You predefine **Read Capacity Units (RCU)** and **Write Capacity Units (WCU)**. More control, more cost-effective for predictable workloads. |
| **DAX**           | Optional in-memory cache for faster reads                                                                                                    |
| **Global Tables** | Multi-region replication of DynamoDB tables                                                                                                  |
| **Streams**       | Log every data change for integration or replay                                                                                              |

---

## ✅ Key Features of DynamoDB

| Feature                   | Description                                                               |
| ------------------------- | ------------------------------------------------------------------------- |
| ⚡ **Performance**         | Single-digit millisecond latency, even at millions of requests per second |
| 🌍 **Global Tables**      | Cross-region replication and HA                                           |
| 🚀 **Serverless**         | No need to provision or manage infrastructure                             |
| 🔐 **Security**           | IAM integration, KMS encryption at rest, VPC endpoints                    |
| ♻️ **Auto Scaling**       | Dynamically adjusts capacity (for provisioned tables)                     |
| 📦 **Durability**         | Multi-AZ replication by default                                           |
| 🧼 **Streams**            | Event sourcing & change tracking for Lambda or analytics                  |
| 🧠 **DAX**                | 10x read speed via in-memory cache                                        |
| 🔁 **Time to Live (TTL)** | Automatically delete old or stale data                                    |
| 🕐 **Backup & PITR**      | Point-in-time recovery for up to 35 days                                  |
| 🧩 **Flexible Schema**    | No need to define schema beforehand (schemaless NoSQL)                    |

---

## ✅ Important Parameters (You Define per Table)

| Parameter                             | Description                                                |
| ------------------------------------- | ---------------------------------------------------------- |
| `table_name`                          | Name of the table                                          |
| `hash_key` / `partition_key`          | The primary partition key                                  |
| `range_key` / `sort_key`              | (Optional) Enables composite primary key                   |
| `read_capacity`                       | For provisioned mode, defines max reads per second         |
| `write_capacity`                      | For provisioned mode, defines max writes per second        |
| `billing_mode`                        | `PROVISIONED` or `PAY_PER_REQUEST`                         |
| `ttl_attribute_name`                  | Defines which attribute holds expiry timestamps            |
| `point_in_time_recovery`              | Enables PITR for table                                     |
| `stream_enabled` / `stream_view_type` | Enables change data capture (NEW\_IMAGE, OLD\_IMAGE, etc.) |
| `global_secondary_indexes`            | Adds GSI definitions                                       |
| `local_secondary_indexes`             | Adds LSI definitions                                       |

---

## ✅ Use Cases for DynamoDB

| Use Case                     | Description                                          |
| ---------------------------- | ---------------------------------------------------- |
| **Serverless applications**  | Integrates natively with AWS Lambda and API Gateway  |
| **IoT data ingestion**       | Real-time telemetry at scale                         |
| **Gaming leaderboards**      | Low-latency access with sort key on scores           |
| **E-commerce shopping cart** | Stores session-specific data                         |
| **Chat applications**        | Messages with partition key as user or channel       |
| **Mobile app backend**       | Real-time sync and updates with DynamoDB Streams     |
| **Event sourcing**           | Use DynamoDB + Streams to record every state change  |
| **Microservices**            | Easily decouples services with a single table design |

---

## ✅ Example Terraform Configuration

```hcl
resource "aws_dynamodb_table" "users" {
  name           = "users"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "user_id"

  attribute {
    name = "user_id"
    type = "S"
  }

  ttl {
    attribute_name = "expire_at"
    enabled        = true
  }

  point_in_time_recovery {
    enabled = true
  }

  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"
}
```

---

## ✅ Monitoring and Alerts

* **CloudWatch Metrics**: `ConsumedReadCapacityUnits`, `ThrottledRequests`, `ReadThrottleEvents`, etc.
* **Alarms**: Set CloudWatch alarms on capacity usage
* **DynamoDB Console**: View performance graphs and table status
* **AWS X-Ray**: Trace DynamoDB calls inside Lambda/API Gateway

---

## ✅ Best Practices

| Tip                                                | Why?                                            |
| -------------------------------------------------- | ----------------------------------------------- |
| Use **on-demand** for unpredictable traffic        | Avoid over/under-provisioning                   |
| Design keys carefully                              | Poor key design leads to "hot partitions"       |
| Use **DAX** for read-heavy workloads               | Improves performance significantly              |
| Enable **TTL** to clean up old items automatically | Saves storage costs                             |
| Use **Streams** for CDC (Change Data Capture)      | For analytics, triggering workflows             |
| Use **Global Tables** for global apps              | Ensures low-latency access globally             |
| Leverage **single-table design** for microservices | Reduces number of tables and simplifies scaling |

---

## ✅ DynamoDB vs RDS vs Aurora (Quick View)

| Feature        | DynamoDB                                   | RDS                               | Aurora                             |
| -------------- | ------------------------------------------ | --------------------------------- | ---------------------------------- |
| Type           | NoSQL                                      | Relational                        | Relational                         |
| Schema         | Schema-less                                | Fixed schema                      | Fixed schema                       |
| Scaling        | Auto                                       | Manual (except Aurora Serverless) | Auto (storage), Manual (compute)   |
| Availability   | Multi-AZ, no downtime                      | Multi-AZ                          | Highly available, 6-way replicated |
| Best For       | High throughput, low-latency key-value use | Traditional relational apps       | Cloud-native relational apps       |
| Query Language | NoSQL API (not SQL)                        | SQL                               | SQL                                |
| Pricing        | Pay-per-request or provisioned             | Instance-based                    | Instance-based or Serverless       |

---

Let’s break down the **Primary Key**, **Partition Key**, and **Sort Key** in **Amazon DynamoDB**, using **clear examples** to make everything crystal clear.

---

## ✅ 1. What is a **Primary Key** in DynamoDB?

In DynamoDB, the **Primary Key uniquely identifies each item** in a table.

It can be of two types:

| Type                      | Description                                   |
| ------------------------- | --------------------------------------------- |
| **Simple Primary Key**    | Only the **Partition Key**                    |
| **Composite Primary Key** | A combination of **Partition Key + Sort Key** |

---

## ✅ 2. What is a **Partition Key**?

* It's used to **determine the partition** where the data will be stored.
* Think of it like a "hash key" — items with the same partition key are stored together.
* Must be **unique** if there's **no sort key**.

---

## ✅ 3. What is a **Sort Key**?

* Optional but powerful.
* Allows **multiple items to share the same Partition Key** but be **distinguished by the Sort Key**.
* Allows **range queries**, sorting, and filtering within a partition.

---

## ✅ Example 1: **Simple Primary Key (Only Partition Key)**

```plaintext
Table: Users
Primary Key = user_id (Partition Key)
```

| user\_id | name   | email                                       |
| -------- | ------ | ------------------------------------------- |
| u001     | Deepak | [deepak@email.com](mailto:deepak@email.com) |
| u002     | Ramesh | [ramesh@email.com](mailto:ramesh@email.com) |
| u003     | Sita   | [sita@email.com](mailto:sita@email.com)     |

* Each `user_id` is **unique**
* You can **get item** using `user_id`

---

## ✅ Example 2: **Composite Primary Key (Partition Key + Sort Key)**

```plaintext
Table: Orders
Partition Key = customer_id  
Sort Key = order_date
```

| customer\_id | order\_date | order\_id | total\_amount |
| ------------ | ----------- | --------- | ------------- |
| c001         | 2024-01-01  | o1001     | ₹1,200        |
| c001         | 2024-02-01  | o1002     | ₹2,100        |
| c002         | 2024-01-01  | o1003     | ₹1,800        |

### ✅ How it works:

* Partition key groups all orders for a customer
* Sort key **orders data within the partition**
* You can query:

  * All orders for customer `c001`
  * All orders after `2024-01-15` for customer `c001`
  * Order placed on exact date

---

## ✅ Querying by Key Types

| Operation          | Key Type      | Query Pattern                                             |
| ------------------ | ------------- | --------------------------------------------------------- |
| Get one item       | Simple key    | Get by Partition Key only                                 |
| Get multiple items | Composite key | Query by Partition Key and filter on Sort Key             |
| Range queries      | Composite key | Query all items where Sort Key is between two dates, etc. |

---

## ✅ Terraform Example: Table with Composite Key

```hcl
resource "aws_dynamodb_table" "orders" {
  name           = "orders"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "customer_id"
  range_key      = "order_date"

  attribute {
    name = "customer_id"
    type = "S"
  }

  attribute {
    name = "order_date"
    type = "S"
  }

  ttl {
    attribute_name = "expire_at"
    enabled        = true
  }

  point_in_time_recovery {
    enabled = true
  }
}
```

---

## ✅ Summary Table

| Term              | Description                                          | Required?  |
| ----------------- | ---------------------------------------------------- | ---------- |
| **Partition Key** | Determines the partition (physical storage location) | ✅ Yes      |
| **Sort Key**      | Optional – allows multiple items per partition       | ❌ Optional |
| **Primary Key**   | Either Partition Key alone or Partition + Sort Key   | ✅ Yes      |

---


