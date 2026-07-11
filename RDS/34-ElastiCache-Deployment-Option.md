# 34 - ElastiCache For RDS Deployment Option

> Goal: cover how Redis and Memcached are each actually deployed for availability and scale.

---

## 1. Redis deployment options

- **Single node**: no replication, no failover — cache loss on any restart/failure, cheapest option.
- **Replication group (Cluster Mode Disabled)**: one primary + up to 5 read replicas, all holding the **full dataset** — scales reads, and supports **Multi-AZ with automatic failover** to a replica if the primary fails.
- **Replication group (Cluster Mode Enabled)**: data **sharded** across multiple node groups (each with its own primary + replicas) — scales **both reads and writes** horizontally, since each shard only holds a portion of the data (Note 35 covers this in depth).

---

## 2. Memcached deployment

- Memcached has **no replication concept at all** — a Memcached "cluster" is just multiple **independent nodes**, each with a portion of cached data (partitioned client-side via consistent hashing in the client library), providing horizontal scale-out but **no HA** — losing a node loses that portion of the cache, with requests simply falling back to a cache miss (re-fetching from RDS) rather than any failover.

---

## 3. Recap

- Redis has a spectrum of options from single-node (no HA) up to sharded, Multi-AZ, replicated Cluster Mode; Memcached is always just independent, unreplicated nodes with client-side partitioning and no failover.
- Next: Note 35 — AWS RDS ElastiCache For RDS Cluster Mode, going deeper on Redis's Cluster Mode Enabled sharding.

### Sources
- [Replication: Redis OSS (Cluster Mode Disabled vs. Enabled) — AWS docs](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/Replication.html)
- [Which nodes/clusters are right for me? — AWS docs](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/nodes-select-size.html)
