# 35 - AWS RDS ElastiCache For RDS Cluster Mode

> Goal: go deeper on Redis's Cluster Mode Enabled — sharding a dataset across multiple node groups for horizontal scale beyond what a single primary can hold or write.

---

## 1. Cluster Mode Disabled vs. Enabled

| | Cluster Mode Disabled | Cluster Mode Enabled |
|---|---|---|
| Data placement | **Full dataset** copied to primary and every replica | Dataset **sharded** across up to 500 node groups (shards) |
| Write scaling | No — all writes go to the one primary | Yes — writes spread across multiple shard primaries |
| Read scaling | Yes — via replicas of the single primary | Yes — via replicas within each shard |
| Max dataset size | Limited by a single node's memory | Scales with number of shards — much larger total capacity |
| Client complexity | Simple — one primary endpoint | Client (or a Redis-cluster-aware library) must route keys to the correct shard |

---

## 2. How sharding works

Keys are distributed across shards using **hash slots** (16,384 total) — each shard owns a range of slots, and a cluster-aware client computes which shard owns a given key before routing the request there directly.

> 🧠 **Mental model:** this is the same idea as DynamoDB's partitioning (this repo's `DynamoDB` folder covers this for DynamoDB specifically) — spreading both storage and request load across multiple independent nodes by hashing a key to a fixed range of "buckets."

---

## 3. When Cluster Mode Enabled is worth the added complexity

- The full dataset **no longer fits comfortably in a single node's memory**.
- **Write throughput** to a single primary has become the bottleneck (Cluster Mode Disabled can only scale reads, never writes).

> 🎯 **Exam tip:** "dataset too large for one node" or "need to scale write throughput on the cache layer itself" signals **Cluster Mode Enabled**; simple read-scaling on a modest dataset stays with **Cluster Mode Disabled**, keeping full-dataset replicas and a simpler single-primary-endpoint client model.

---

## 4. Recap

- Cluster Mode Enabled shards Redis data across multiple node groups using hash slots, scaling both reads and writes and total dataset size — at the cost of client-side complexity; Cluster Mode Disabled keeps a full-dataset replica set behind one primary, simpler but read-scaling-only.
- Next: Note 36 — AWS RDS ElastiCache Exam SAA-C03 Cheat Sheet, consolidating Notes 32-35.

### Sources
- [Redis OSS cluster mode — AWS docs](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/Replication.Redis-RedisCluster.html)
