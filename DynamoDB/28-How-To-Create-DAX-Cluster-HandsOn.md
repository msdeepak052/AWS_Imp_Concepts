# 28 - How To Create DAX Cluster?

> Goal: a hands-on walkthrough creating a real DAX cluster in front of an existing table, and confirming the latency improvement directly.

---

## 1. Prerequisites

- An existing DynamoDB table (e.g. `Orders`).
- An **IAM role** for DAX granting it permission to access the target table(s) on your behalf.
- A **subnet group** (DAX runs inside a VPC, similar to RDS's DB subnet groups, `RDS/16`).

---

## 2. Create the cluster

1. **DynamoDB console** → **DAX** → **Create cluster**.
2. Name it, choose a **node type**, and a **cluster size** (at least 3 nodes across multiple AZs recommended for production HA — a single node has no failover).
3. Attach the **IAM role** and **subnet group** from Section 1.
4. **Create** — provisioning takes a few minutes.

---

## 3. Point the application at DAX

Using the DAX SDK client (a thin wrapper around the standard DynamoDB SDK client) instead of the standard DynamoDB client:

```python
import amazondax
import boto3

dax = amazondax.AmazonDaxClient(endpoint_url="dax-cluster-endpoint:8111")
table = dax.Table("Orders")
response = table.get_item(Key={"OrderId": "101"})
```

- Note the API call itself (`get_item`, `Key=...`) is **identical** to the standard DynamoDB SDK call — only the client construction changes, confirming Note 27's "minimal code change" claim directly.

---

## 4. Observe the latency difference

- First read of a given key: a **cache miss**, DAX fetches from DynamoDB and populates its cache — latency similar to a normal DynamoDB read.
- Subsequent reads of the **same key** within the cache's TTL: served directly from DAX's in-memory cache — **microsecond**-scale latency, a clear, measurable improvement over DynamoDB's own single-digit-millisecond baseline.

---

## 5. Recap

- Creating a DAX cluster requires an IAM role and a subnet group, similar in shape to RDS's networking prerequisites; pointing an application at DAX is a minimal, client-endpoint-only code change.
- The latency improvement between a first (cache miss) and subsequent (cache hit) read of the same key is directly observable, confirming DAX's value proposition hands-on.
- Next: Note 29 — AWS Certified Solutions Architect - Associate SAA-C03 DynamoDB Cheat Sheet, closing out this folder.

### Sources
- [Creating a DAX cluster — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.create-cluster.html)
- [In-memory acceleration with DAX — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.html)
