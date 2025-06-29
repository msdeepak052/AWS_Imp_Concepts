## ✅ What is **Read Consistency** in DynamoDB?

**Read consistency** refers to **how fresh and accurate** the data returned by a read operation is, especially in distributed systems where data is replicated across multiple servers/AZs.

---

## ✅ Types of Read Consistency in DynamoDB

| Type                            | Description                              | Latency            | Cost                  | Use Case                          |
| ------------------------------- | ---------------------------------------- | ------------------ | --------------------- | --------------------------------- |
| **Eventually Consistent Reads** | May return stale data temporarily        | ✅ Fastest          | 💲 Cheapest (default) | Most general use cases            |
| **Strongly Consistent Reads**   | Always returns the latest data           | ❗ Slightly slower  | 💲 Doubles read cost  | When accuracy is critical         |
| **Transactional Reads**         | ACID-compliant reads inside transactions | 🚫 Highest latency | 💲 More expensive     | Financial and critical operations |

---

### 🔄 1. **Eventually Consistent Reads** (default)

* Data is replicated to **multiple AZs**.
* A read might return **stale data** for a short time (usually milliseconds).
* Use for **read-heavy applications** where **absolute accuracy isn’t critical**.

#### ✅ Use Cases:

* Product catalog
* User profile info
* Search features
* Real-time leaderboards (if near-real-time is okay)

#### 🧪 Example:

```python
table.get_item(
    Key={'user_id': 'u001'}
)  # Eventually consistent (default)
```

---

### 🛡️ 2. **Strongly Consistent Reads**

* Guarantees the read returns **the most recent committed write**.
* Ensures **read-after-write consistency**.
* **Doubles the read capacity cost** compared to eventually consistent.

#### ✅ Use Cases:

* Banking/account balance
* Inventory systems
* Booking/reservation systems (flight seats, tickets)
* Auditing/logging

#### 🧪 Example:

```python
table.get_item(
    Key={'user_id': 'u001'},
    ConsistentRead=True  # Strongly consistent
)
```

---

### 🔐 3. **Transactional Reads** (`TransactGetItems`)

* Part of DynamoDB Transactions.
* ACID-compliant (Atomicity, Consistency, Isolation, Durability).
* Reads multiple items **as a single unit**.

#### ✅ Use Cases:

* Financial transactions (withdraw and deposit)
* Inventory + purchase together
* Multi-table or multi-item workflows

#### 🧪 Example:

```python
dynamodb.transact_get_items(
    TransactItems=[
        {'Get': {'Key': {'user_id': 'u001'}, 'TableName': 'users'}},
        {'Get': {'Key': {'order_id': 'o1001'}, 'TableName': 'orders'}}
    ]
)
```

---

## ✅ Read Capacity Implications

| Read Type             | Capacity Cost                        |
| --------------------- | ------------------------------------ |
| Eventually Consistent | 1 RCU = 2 reads/sec (4 KB each)      |
| Strongly Consistent   | 1 RCU = 1 read/sec (4 KB each)       |
| Transactional Read    | Multiple RCUs + transaction overhead |

---

## ✅ Best Practices

| Scenario                                   | Recommendation                                      |
| ------------------------------------------ | --------------------------------------------------- |
| You just wrote an item and want to read it | Use **Strongly Consistent**                         |
| You need the latest values always          | Use **Strongly Consistent** or **Transactional**    |
| Most reads are general, non-critical       | Use **Eventually Consistent**                       |
| Reads are part of ACID workflow            | Use **Transactional**                               |
| Optimize cost for large-scale reads        | Stick with **Eventually Consistent** where possible |

---

## ✅ Summary Table

| Read Type             | Fresh?               | Latency           | Cost             | Use Case             |
| --------------------- | -------------------- | ----------------- | ---------------- | -------------------- |
| Eventually Consistent | Maybe slightly stale | ✅ Lowest          | 💲 Cheapest      | General apps         |
| Strongly Consistent   | ✅ Always fresh       | ❗ Slightly higher | 💲💲 Double RCU  | Banking, inventory   |
| Transactional         | ✅ Always fresh       | 🚫 Highest        | 💲💲💲 Expensive | Multi-item ACID apps |

---
