# 07 - EC2 Instance Types

> Goal: understand how to **read an instance type name**, the **families** (general purpose, compute, memory, storage, accelerated, HPC), and **how to pick the right one**. Updated for 2026 (Graviton4/Graviton5).

---

## 1. What is an "instance type"?

An **instance type** defines the **hardware** of your virtual server:
- **vCPUs** (virtual CPUs)
- **Memory (RAM)** in GiB
- **Networking** bandwidth
- **Storage** options (EBS-only or local NVMe)
- The **processor** (Intel, AMD, or AWS Graviton ARM)

The **AMI** decides the software; the **instance type** decides the muscle.

---

## 2. How to read an instance type name

Example: **`m5.xlarge`** or **`c8g.2xlarge`**

```
   m        5        g        .       xlarge
   │        │        │                │
 family   generation attributes      size
```

- **Family letter** → workload category (`t`, `m`, `c`, `r`, `x`, `i`, `g`, `p`, `hpc`…).
- **Generation number** → newer = better price/performance (`m5` < `m6` < `m7` < `m8`).
- **Attribute letters** (after the number) → special capabilities:
  - `g` = AWS **Graviton** (ARM) processor
  - `a` = AMD processor
  - `i` = Intel processor (when distinguishing) or `d` = local NVMe disk
  - `n` = network-optimized; `d` = instance store; `b` = high EBS bandwidth; `e` = extra storage/memory; `z` = high frequency; `q` = … (combine, e.g. `c8gd`, `m8id`)
- **Size** → `nano, micro, small, medium, large, xlarge, 2xlarge … 48xlarge, metal`. Each step roughly **doubles** vCPU + RAM.

> 🧠 Example reading: `c8g.2xlarge` = **C**ompute family, **8th** gen, **G**raviton (ARM), **2xlarge** size.

---

## 3. The instance families (the big six)

### a) General Purpose — balanced CPU/RAM
- Letters: **`t`** (burstable), **`m`** (steady), **`mac`** (Apple).
- Use for: web servers, small/medium databases, dev/test, microservices.
- **`t` (burstable)**: cheap; accumulate **CPU credits** when idle, spend them on bursts. Great for low-traffic apps. Examples: `t2.micro`, `t3.micro`, `t4g.micro` (Graviton). **`t3.micro`/`t2.micro` are the Free-Tier instances.**
- **`m`**: consistent performance. Examples: `m7g`, `m8g`, **`m9g`** (Graviton5, GA June 2026).

### b) Compute Optimized — high CPU per RAM
- Letter: **`c`** (e.g. `c7g`, `c8g`).
- Use for: batch processing, gaming servers, video encoding, HPC, scientific modeling, ML inference, high-traffic web/app servers.

### c) Memory Optimized — lots of RAM
- Letters: **`r`** (RAM), **`x`** (extra-large memory), **`u`/high-memory** (huge in-memory DBs), **`z`** (high freq + memory).
- Use for: in-memory databases (Redis), large relational DBs, real-time big-data analytics, SAP HANA. `X8g` offers up to **3 TiB** RAM.

### d) Storage Optimized — high local disk IOPS/throughput
- Letters: **`i`** (high IOPS NVMe, e.g. `i4i`, `i8g`), **`d`** (dense HDD), **`h`** (HDD throughput).
- Use for: NoSQL DBs (Cassandra, MongoDB), data warehouses, Elasticsearch, large transactional DBs.

### e) Accelerated Computing — GPUs / special chips
- Letters: **`p`** (GPU for ML training, e.g. `p5`), **`g`** as a GPU-graphics family (`g6`), **`inf`** (Inferentia, ML inference), **`trn`** (Trainium, ML training), **`f`** (FPGA).
- Use for: deep learning, graphics rendering, generative AI.
> ⚠️ Don't confuse the **`g` GPU families** (e.g. `g6`) with the **`g` suffix = Graviton** (e.g. `m7g`). Context matters.

### f) HPC Optimized — tightly-coupled clusters
- Prefix: **`hpc`** (e.g. `hpc7g`).
- Use for: weather simulation, computational fluid dynamics, large-scale HPC. Pairs with **cluster placement groups** (a placement strategy that packs instances physically close together on the same underlying hardware/network to minimize inter-instance latency) and **EFA** (Elastic Fabric Adapter — a network interface that gives applications very low-latency, high-throughput, OS-bypass communication between instances, used for tightly-coupled HPC and distributed ML training).

---

## 4. Processor choices (2026)

| Processor | Suffix | Why |
|---|---|---|
| **AWS Graviton (ARM)** | `g` (e.g. `m8g`, `c8g`) | Best **price-performance** & energy efficiency. **Graviton4** powers `*8g`; **Graviton5** (`m9g`) GA June 2026 (~25% faster than M8g). Needs ARM-compatible software. |
| **Intel Xeon** | (often `i`) | Broad software compatibility; some workloads tuned for Intel. Latest = Xeon 6 "Granite Rapids". |
| **AMD EPYC** | `a` (e.g. `m7a`) | Often cheaper than Intel for x86 workloads. Latest = EPYC "Turin". |

> 🧠 Rule of thumb in 2026: **try Graviton first** for cost savings if your software supports ARM (most Linux apps, Java, Python, .NET do).

---

## 5. EC2 Instance "metal" (bare metal)

- Sizes ending in **`.metal`** give your workload **direct access to the physical processor** (no hypervisor) — for software that needs it (licensing, low-latency, nested virtualization).

---

## 6. How to choose — a simple decision guide

1. **Just learning / low traffic?** → `t3.micro` / `t4g.micro` (burstable, cheap, Free Tier).
2. **Balanced general app?** → `m`-family (`m7g`/`m8g`).
3. **CPU-bound (encoding, batch, HPC)?** → `c`-family.
4. **RAM-bound (caches, big DBs)?** → `r` / `x`-family.
5. **Local disk-heavy (NoSQL, analytics)?** → `i` / `d`-family.
6. **ML / GPU / rendering?** → `p` / `g` / `inf` / `trn`.
7. **Save money?** → choose **Graviton (`g`)** where software allows.

> You can **change instance type later**: Stop the instance → Actions → Instance settings → **Change instance type** → Start. (Only when stopped; root volume must be EBS.)

---

## 7. Quick recap

- Name = **family + generation + attributes + size** (e.g. `c8g.2xlarge`).
- Six families: **General (t/m)**, **Compute (c)**, **Memory (r/x)**, **Storage (i/d)**, **Accelerated (p/g/inf/trn)**, **HPC (hpc)**.
- `g` suffix = **Graviton** ARM = best price-performance (Graviton4 = `*8g`; Graviton5 = `m9g`, 2026).
- Bigger size = roughly double resources per step.
- You can resize later by stopping the instance.
- Next (Note 08): **Multi-AZ** — placing instances across Availability Zones for resilience.

---

### Sources
- [Amazon EC2 instance types – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html)
- [Amazon EC2 C8g instances – AWS](https://aws.amazon.com/ec2/instance-types/c8g/)
- [Amazon EC2 R8g instances – AWS](https://aws.amazon.com/ec2/instance-types/r8g/)
- [Amazon EC2 M9g instances (Graviton5) – AWS](https://aws.amazon.com/ec2/instance-types/m9g/)
- [AWS Graviton – Wikipedia](https://en.wikipedia.org/wiki/AWS_Graviton)
