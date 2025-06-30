## 📘 What are **Secondary Indexes** in DynamoDB?

Secondary indexes in DynamoDB allow you to **query the data using alternate keys** (other than the primary key). This improves flexibility in querying without duplicating tables.

---

## 🔸 Types of Secondary Indexes

| Type                             | Description                                                                                                                       |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **Global Secondary Index (GSI)** | Uses **different partition & sort keys** from the base table. Can include any attributes.                                         |
| **Local Secondary Index (LSI)**  | Shares the **same partition key** as the base table but uses a **different sort key**. Can only be created at **table creation**. |

---

## 🔧 Primary Table Example

```text
Table: Orders
Partition Key: OrderID (string)
Sort Key: OrderDate (string)
```

This structure is great for querying by `OrderID` and `OrderDate`, but what if you want to query by `CustomerID` or `OrderStatus`?

➡️ You need **secondary indexes**!

---

## 🔹 Global Secondary Index (GSI) Example

### Use Case: Query orders by CustomerID and OrderStatus

```hcl
Global Secondary Index:
  IndexName: GSI_CustomerOrderStatus
  Partition Key: CustomerID
  Sort Key: OrderStatus
```

Now, you can query:

```sql
SELECT * FROM Orders WHERE CustomerID = 'C123' AND OrderStatus = 'Pending';
```

---

## 🔹 Local Secondary Index (LSI) Example

### Use Case: Query orders by OrderDate and OrderAmount

```hcl
Local Secondary Index:
  IndexName: LSI_OrderAmount
  Partition Key: OrderID
  Sort Key: OrderAmount
```

Now, you can query:

```sql
SELECT * FROM Orders WHERE OrderID = 'O789' AND OrderAmount > 500;
```

✅ *Note: LSI can only be created at table creation time.*

---

## ✅ Use Cases

| Use Case                                      | Recommended Index Type   | Notes                                         |
| --------------------------------------------- | ------------------------ | --------------------------------------------- |
| Querying by alternate attribute (e.g., email) | **GSI**                  | Can use any attribute as partition key        |
| Range queries with same partition key         | **LSI**                  | Ideal for time-based logs, events, etc.       |
| Analytics-style access patterns               | **GSI with projections** | Use `ALL`, `KEYS_ONLY`, or `INCLUDE` settings |
| Accessing multiple views of the same data     | **GSI + LSI combo**      | Advanced querying scenarios                   |

---

## 🔍 Projections in Indexes

When creating an index, you define what attributes to copy from the base table:

* `ALL` – All attributes (costly)
* `KEYS_ONLY` – Only primary and index keys
* `INCLUDE` – Only specific attributes you need

---

## 🛠️ Terraform Example: GSI

```hcl
resource "aws_dynamodb_table" "orders" {
  name           = "Orders"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "OrderID"
  range_key      = "OrderDate"

  attribute {
    name = "OrderID"
    type = "S"
  }

  attribute {
    name = "OrderDate"
    type = "S"
  }

  attribute {
    name = "CustomerID"
    type = "S"
  }

  attribute {
    name = "OrderStatus"
    type = "S"
  }

  global_secondary_index {
    name               = "GSI_CustomerOrderStatus"
    hash_key           = "CustomerID"
    range_key          = "OrderStatus"
    projection_type    = "INCLUDE"
    non_key_attributes = ["OrderDate"]
  }
}
```

---

## 🚨 Best Practices

* Use **narrow projections** to reduce cost and improve performance.
* GSIs **consume separate RCUs/WCUs** or request units in on-demand mode.
* **Monitor index usage** via CloudWatch metrics (e.g., `ConsumedReadCapacityUnits` per GSI).
* Avoid too many indexes — they increase storage and write costs.

---
Here’s a **concise and practical comparison** of **LSI (Local Secondary Index)** vs **GSI (Global Secondary Index)** in Amazon DynamoDB:

---

## 📊 LSI vs GSI Comparison Table

| Feature                        | **LSI (Local Secondary Index)**                          | **GSI (Global Secondary Index)**                  |
| ------------------------------ | -------------------------------------------------------- | ------------------------------------------------- |
| **Partition Key**              | **Same** as base table                                   | **Different** from base table                     |
| **Sort Key**                   | **Different** from base table                            | Customizable                                      |
| **Creation Time**              | Must be created **at table creation**                    | Can be created **anytime** after table creation   |
| **Max per table**              | Up to **5 LSIs** per table                               | Up to **20 GSIs** per table                       |
| **Storage**                    | **Shares storage** with base table (affects size limits) | **Separate storage** from base table              |
| **RCU/WCU (Provisioned Mode)** | Shares **RCU/WCU with base table**                       | Has **separate RCU/WCU provisioning or billing**  |
| **Consistency**                | Supports **strongly consistent** reads                   | Only **eventually consistent** reads (by default) |
| **Use Case**                   | Same user (partition) with different sorting/filtering   | Accessing data with **different partition key**   |

---

## 🔧 Real-World Use Cases

| Scenario                                                               | Use LSI or GSI? | Reason                                                    |
| ---------------------------------------------------------------------- | --------------- | --------------------------------------------------------- |
| Fetching all user logins sorted by timestamp                           | **LSI**         | Same partition key (user), different sort key (timestamp) |
| Querying all orders by `CustomerID` (not in base PK)                   | **GSI**         | Requires a new partition key                              |
| Need strong consistency in secondary index queries                     | **LSI**         | Only LSIs support strongly consistent reads               |
| Adding new index after table is live                                   | **GSI**         | LSIs must be defined during table creation                |
| Filtering invoices for the same `InvoiceID` by `Status` or `Amount`    | **LSI**         | Same partition key, additional sort keys                  |
| Creating dashboard with metrics filtered by `Region` and `ProductType` | **GSI**         | Needs querying with new partition key combinations        |

---

## 🧠 Summary

| Use **LSI** when:                                      |
| ------------------------------------------------------ |
| - You want **range queries** on the same partition key |
| - You need **strongly consistent reads**               |
| - You define indexes **at table creation**             |

| Use **GSI** when:                                    |
| ---------------------------------------------------- |
| - You need **different partition keys** for querying |
| - You want to **add indexes later**                  |
| - You can work with **eventual consistency**         |

---

