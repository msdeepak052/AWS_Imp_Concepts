# 33 - ElastiCache For RDS Cluster Type - Redis & Memcached

> Goal: cover the two ElastiCache engines and the feature gap between them that drives almost every engine-choice exam question.

---

## 1. Side-by-side

| | Redis (Valkey-compatible) | Memcached |
|---|---|---|
| Data structures | Rich — strings, lists, sets, sorted sets, hashes | Simple key-value strings only |
| Persistence | Yes — snapshots (RDB) and/or append-only file (AOF) | No — purely in-memory, gone on restart |
| Replication | Yes — primary/replica, Multi-AZ with automatic failover | No native replication |
| Multi-threading | Single-threaded per shard (scales via sharding/cluster mode) | Multi-threaded per node |
| Pub/Sub, transactions | Yes | No |
| Use case fit | Anything needing durability, HA, or richer data structures | Simple, pure caching, maximum raw throughput per node, horizontal scale-out with no HA requirement |

---

## 2. Why Redis is the default recommendation

For most RDS-caching scenarios, **Redis** is the right default because:

- **Multi-AZ with automatic failover** protects the cache layer itself from becoming a single point of failure.
- **Persistence** means a restart doesn't force every request to become a full cache-miss storm against RDS simultaneously.
- Richer data structures support more sophisticated caching patterns (e.g. sorted sets for leaderboards) beyond simple key-value lookups.

Memcached remains the right choice specifically when the workload is **simple, pure caching**, doesn't need HA/persistence, and benefits from Memcached's **multi-threaded, horizontally-scalable-by-design** architecture for raw throughput.

> 🎯 **Exam tip:** "need Multi-AZ/HA for the cache," "need data structures beyond simple key-value," or "need persistence" → **Redis**. "Simple, pure caching with maximum simplicity and multi-threaded performance, no HA requirement" → **Memcached**.

---

## 3. Recap

- **Redis** offers persistence, replication/HA, and rich data structures; **Memcached** is simpler, multi-threaded, and purely in-memory with no HA — Redis is the more common default, Memcached fits narrower, simpler use cases.
- Next: Note 34 — ElastiCache For RDS Deployment Option, covering how each engine is actually deployed for HA.

### Sources
- [Comparing Memcached and Redis OSS — AWS docs](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/SelectEngine.html)
- [What is Amazon ElastiCache? — AWS docs](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/WhatIs.html)
