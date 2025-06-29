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


Sure Deepak! Let’s go over **DynamoDB table settings** in detail—with a **realistic example**, so you understand every option and how to use it in production.

---

## ✅ DynamoDB Table Settings Overview

When you create a table in DynamoDB, you configure the following **table-level settings**:

| Setting Category              | Key Options/Fields                              |
| ----------------------------- | ----------------------------------------------- |
| Primary Key                   | Partition Key, Sort Key (optional)              |
| Table Class                   | Standard or Standard-IA (infrequent access)     |
| Capacity Mode                 | Provisioned or On-Demand                        |
| Encryption                    | AWS managed, customer managed                   |
| Auto Scaling                  | Only for provisioned mode                       |
| TTL (Time to Live)            | Automatically delete expired items              |
| PITR (Point-in-Time Recovery) | Restore to any point in the last 35 days        |
| Streams                       | Track real-time changes (for Lambda, analytics) |
| Tags                          | Metadata (for billing, ownership, etc.)         |
| Global Tables                 | Optional cross-region replication               |
| Secondary Indexes             | GSI (global), LSI (local)                       |

---

## 🧪 Example Scenario: Orders Table for an E-commerce App

Let’s say we’re building a table to store **orders**.
We want to:

* Use **composite keys** (`customer_id` + `order_id`)
* Enable **PITR**, **TTL**, and **DynamoDB Streams**
* Use **On-Demand capacity** to auto-scale
* Add a **Global Secondary Index** for querying by product\_id

---

## ✅ Table Settings in Detail (with Example)

### 1. **Table Name**

```txt
orders
```

---

### 2. **Primary Key**

```plaintext
Partition Key: customer_id (String)
Sort Key: order_id (String)
```

> This lets us query all orders for a customer and sort them by order ID or date.

---

### 3. **Table Class**

```plaintext
Standard (default)
```

> Use `Standard-IA` if access is rare but you want cost savings.

---

### 4. **Capacity Mode**

```plaintext
On-Demand
```

> Automatically scales read/write capacity. Ideal for unpredictable workloads.

---

### 5. **Encryption**

```plaintext
AWS managed key (default)
```

> You can use KMS custom key if needed for compliance.

---

### 6. **TTL (Time to Live)**

```plaintext
Attribute name: expire_at
```

> This attribute must store **UNIX timestamp** after which the item will be deleted.

---

### 7. **Point-in-Time Recovery (PITR)**

```plaintext
Enabled
```

> Enables recovery to any second in the last 35 days.

---

### 8. **Streams**

```plaintext
Enabled (NEW_AND_OLD_IMAGES)
```

> Useful for triggering AWS Lambda on insert/update/delete.

---

### 9. **Global Secondary Index (GSI)**

```plaintext
GSI Name: product-index
Partition Key: product_id
Sort Key: order_date
Projection: ALL attributes
```

> This lets us query orders by product and sort by date.

---

### 10. **Tags**

```plaintext
Environment = dev
Project     = ecommerce
Owner       = deepak
```

---

## ✅ Final Terraform Example

```hcl
resource "aws_dynamodb_table" "orders" {
  name           = "orders"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "customer_id"
  range_key      = "order_id"

  attribute {
    name = "customer_id"
    type = "S"
  }

  attribute {
    name = "order_id"
    type = "S"
  }

  attribute {
    name = "product_id"
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

  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  global_secondary_index {
    name               = "product-index"
    hash_key           = "product_id"
    range_key          = "order_date"
    projection_type    = "ALL"
  }

  tags = {
    Environment = "dev"
    Owner       = "deepak"
    Project     = "ecommerce"
  }
}
```

---

## ✅ Summary Table

| Setting      | Value                           |
| ------------ | ------------------------------- |
| Table Name   | `orders`                        |
| Primary Key  | `customer_id` + `order_id`      |
| Table Class  | `STANDARD`                      |
| Billing Mode | `PAY_PER_REQUEST`               |
| TTL          | Enabled on `expire_at`          |
| PITR         | Enabled                         |
| Streams      | Enabled (NEW\_AND\_OLD\_IMAGES) |
| GSI          | `product_id + order_date`       |
| Tags         | Dev, Owner, Project             |

---

Let’s dive into the **DynamoDB storage architecture** — how data is stored, managed, and scaled behind the scenes. This helps understand **how it achieves high availability, low latency, and virtually infinite scalability**.

---

## ✅ Overview of DynamoDB Storage Architecture

At a high level, DynamoDB is:

* A **distributed, partitioned key-value store**
* Built on **Amazon’s custom SSD-based storage engine**
* Automatically replicates data across **multiple Availability Zones**
* Designed to scale horizontally using **partitions (shards)**

---

## ✅ Key Components of the Architecture

### 1. **Tables**

* Logical containers that hold **items (rows)**.
* Internally divided into **partitions** based on the **Partition Key**.

---

### 2. **Partitions**

* Physical storage units (think of them like shards).
* **Each partition handles a portion of table data**.
* A single partition can handle:

  * Up to **10 GB** of storage
  * **3,000 RCU** (Read Capacity Units)
  * **1,000 WCU** (Write Capacity Units)

---

### 3. **Partition Key Role**

* Partition Key is **hashed using an internal algorithm** to determine which partition an item goes to.
* Ensures even data distribution.

> ⚠️ Poor partition key design can lead to **hot partitions** → uneven load and throttling.

---

### 4. **Storage Engine**

* Data is stored on **SSD-backed infrastructure**
* Replicated across **3 Availability Zones (AZs)**
* **Eventually consistent** or **strongly consistent** reads (user’s choice)

---

### 5. **Replication**

* **Synchronous replication across 3 AZs** for durability and fault tolerance.
* DynamoDB uses **multi-leader replication**, meaning any replica can handle writes.

---

### 6. **Data Model Storage**

* Data is stored in **key-value format** under the hood:

  * Partition Key (PK)
  * Sort Key (optional)
  * Attributes (can be JSON-like flexible structure)
* You can store **strings, numbers, maps, lists, sets**.

---

### 7. **Secondary Index Storage**

* **GSI (Global Secondary Index)** and **LSI (Local Secondary Index)** are stored in **separate partitions** but share the same underlying data model.
* GSIs can span partitions; LSIs cannot.

---

### 8. **Streams and Change Logs**

* DynamoDB Streams maintain a **change log** in separate infrastructure.
* Used for Lambda triggers, CDC, event-driven pipelines.

---

### 9. **Backup and PITR (Point-in-Time Recovery)**

* Snapshots and PITR data are stored outside the live partitions.
* Doesn't affect table performance during backup/restore.

---

## ✅ Architecture Diagram (Textual)

```
             +---------------------------+
             |       DynamoDB Table      |
             +-------------+-------------+
                           |
      +--------------------+--------------------+
      |         Partition (Shard) 1             |
      | - Handles PK hash range A-M             |
      | - 3x replicated across AZs              |
      +----------------+------------------------+
                       |
        +--------------+--------------+
        |  AZ-1       |  AZ-2        |  AZ-3
        |  SSD Store  |  SSD Store   |  SSD Store
        +-------------+--------------+-------------+

      +--------------------+--------------------+
      |         Partition (Shard) 2             |
      | - Handles PK hash range N-Z             |
      | - 3x replicated                          |
      +-----------------------------------------+
```

---

## ✅ Automatic Scaling (Horizontal Scaling)

DynamoDB auto-scales by:

| Scaling Trigger                        | Action                  |
| -------------------------------------- | ----------------------- |
| Item size > 10 GB                      | Creates a new partition |
| WCU or RCU exceed per-partition limits | Splits partition        |
| Table grows rapidly                    | Adds more partitions    |

---

## ✅ Real-World Analogy

Think of DynamoDB like a **massive warehouse (table)** with **bins (partitions)**.

* Each item has a label (Partition Key)
* The label tells which bin to place the item in
* Bins are duplicated across **3 buildings (AZs)** for safety

---

## ✅ Key Takeaways

| Feature          | How DynamoDB Handles It                         |
| ---------------- | ----------------------------------------------- |
| **Durability**   | 3x replication across AZs                       |
| **Scalability**  | Partitions auto-split and scale                 |
| **Performance**  | Low-latency access via SSDs                     |
| **Resilience**   | Multi-AZ fault tolerance                        |
| **Elasticity**   | On-demand or auto-scaling provisioning          |
| **Consistency**  | Tunable (eventual or strong)                    |
| **Multi-tenant** | Each table is isolated in its own storage space |

---



