# 17 - EC2 Placement Groups

> Goal: understand the three **placement group** strategies — **Cluster**, **Spread**, **Partition** — what physical placement each gives you, and which workload each is for. Includes a hands-on.

---

## 1. What is a Placement Group?

By default AWS decides **where** (which physical hardware/rack) your instances land. A **Placement Group** lets **you influence that placement** to optimize for either **low latency / high throughput** or **fault isolation**.

- Placement groups are **free**.
- They apply within a single **Region** (and a strategy decides the AZ spread).

There are **3 strategies**:

```
Cluster    → pack instances close together  → max network performance
Spread     → keep instances far apart        → max fault isolation (few instances)
Partition  → group into isolated racks       → big distributed systems (many instances)
```

---

## 2. Cluster Placement Group — "pack tightly"

- Places instances **physically close together**, typically on the **same rack** within a **single AZ**.
- Goal: **lowest network latency** and **highest throughput** between instances (up to very high bandwidth, e.g. 10–100+ Gbps, especially with **EFA – Elastic Fabric Adapter**).

✅ **Use for:** tightly-coupled **HPC**, big-data/analytics clusters, MPI workloads, anything needing nodes to talk fast to each other.

⚠️ **Trade-off:** because everything is on the same rack/AZ, a **hardware/rack failure can take out the whole group** → low fault tolerance. All instances should ideally be the **same type**, launched **together**.

---

## 3. Spread Placement Group — "keep apart"

- Places each instance on **distinct underlying hardware (different racks)**, each with its own power and network — can span **multiple AZs**.
- Goal: **maximize fault isolation** — a single hardware failure affects at most **one** instance.

✅ **Use for:** a **small number of critical instances** that must not fail together (e.g. primary + standby, a handful of critical app nodes).

⚠️ **Limit:** **max 7 instances per AZ** per spread group (it's meant for *few, important* instances, not large fleets).

---

## 4. Partition Placement Group — "isolated groups of racks"

- Divides instances into logical **partitions**; each partition sits on a **separate set of racks** (separate power/network). Up to **7 partitions per AZ**, and can span multiple AZs; **hundreds of instances** total.
- A failure in one partition's hardware **does not affect other partitions**.
- AWS exposes **which partition** each instance is in (via metadata), so distributed software can place replicas in different partitions.

✅ **Use for:** large **distributed & replicated** systems that are partition-aware — **HDFS, HBase, Cassandra, Kafka**.

---

## 5. Quick comparison

| Strategy | Placement | Best for | Fault isolation | Scale |
|---|---|---|---|---|
| **Cluster** | Same rack, 1 AZ | Lowest latency / HPC | ❌ Low (single point) | Small, same-type |
| **Spread** | Separate racks (multi-AZ) | Few critical instances | ✅ Highest | **7 per AZ** |
| **Partition** | Separate rack-groups (multi-AZ) | Big distributed/replicated apps | ✅ Per-partition | **7 partitions/AZ**, 100s of instances |

> 🧠 Memory hook: **Cluster = Close (speed), Spread = Separate (safety, few), Partition = Pods (big distributed apps).**

---

## 6. Hands-On

**Create a placement group:**
1. EC2 → **Network & Security → Placement Groups → Create placement group**.
2. **Name**: `demo-cluster`.
3. **Strategy**: choose **Cluster** (or Spread / Partition).
   - For **Partition**, set the number of partitions (1–7).
4. **Create group**.

**Launch an instance into it:**
1. **Launch instance** → **Advanced details** → **Placement group** → select `demo-cluster`.
2. Launch. (For Cluster, launch all instances of the same type **at once** to ensure capacity on the same rack.)

**Verify:** Instances → instance details → **Placement group** field shows the group.

---

## 7. Rules & gotchas

- You **can't merge** placement groups; an instance can be in **only one** at a time.
- **Cluster** works best when instances are launched **simultaneously** and are the **same instance type** (avoids "insufficient capacity" errors on the rack).
- You can **move/add** a running instance to a group via `modify-instance-placement` only when it's **stopped**.
- **Cluster** groups should use instance types that support **enhanced networking / EFA** for full benefit.
- Spreading across many AZs increases resilience but adds **inter-AZ data charges**.

---

## 8. Recap

- Placement groups influence **physical placement** (free).
- **Cluster** = tight = fast (HPC), low fault tolerance.
- **Spread** = far apart = safest, **max 7/AZ**, few critical instances.
- **Partition** = isolated rack-groups = big distributed systems (Cassandra/Kafka/HDFS), **7 partitions/AZ**.
- One instance → one group; launch cluster instances together.
- Next (Note 18): **AWS Tenancy** — shared vs dedicated hardware.

---

### Sources
- [Placement groups – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html)
- [Elastic Fabric Adapter (EFA) – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa.html)
