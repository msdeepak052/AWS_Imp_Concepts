# 03 - Subnets and CIDR Calculations

> Goal: **actually be able to do the math** — given any CIDR block, calculate subnet ranges, usable host counts, and VLSM splits from scratch. This is the single most exam-tested VPC skill on SAA-C03. Note 02 covered the vocabulary; this note is all arithmetic.

---

## 1. Refresher: what a `/n` prefix means

An IPv4 address is 32 bits, written as 4 octets (e.g. `10.0.1.0` = `00001010.00000000.00000001.00000000`).

- The prefix (`/n`) says: **the first `n` bits are fixed ("network bits")**; the remaining `32-n` bits are free to vary ("host bits").
- **Total addresses in the block** = `2^(32-n)` (every possible combination of the host bits).
- A **smaller prefix number = more host bits = a bigger block**. `/16` (65,536 IPs) is much bigger than `/24` (256 IPs) — easy to get backwards, so always sanity-check with the formula.

| Prefix | Host bits (`32-n`) | Total IPs (`2^(32-n)`) |
|---|---|---|
| `/16` | 16 | 65,536 |
| `/24` | 8 | 256 |
| `/28` | 4 | 16 |

---

## 2. AWS reserves 5 IP addresses in every subnet

This is the #1 gotcha on the exam. **In every AWS subnet — no matter its size — AWS reserves 5 addresses** that you can't assign to instances:

| # | Address (example: `10.0.1.0/24`) | Reason |
|---|---|---|
| 1 | `10.0.1.0` (first) | Network address |
| 2 | `10.0.1.1` | Reserved for the **VPC router** |
| 3 | `10.0.1.2` | Reserved for **DNS** (Amazon-provided DNS server) |
| 4 | `10.0.1.3` | Reserved for **future use** |
| 5 | `10.0.1.255` (last) | Network **broadcast address** (AWS doesn't support broadcast, but still reserves it) |

**Formula: usable IPs = `2^(32-prefix) - 5`.**

### Quick reference table: `/16` through `/28`

| Prefix | Total IPs | Usable IPs (`total - 5`) |
|---|---|---|
| `/16` | 65,536 | 65,531 |
| `/17` | 32,768 | 32,763 |
| `/18` | 16,384 | 16,379 |
| `/19` | 8,192 | 8,187 |
| `/20` | 4,096 | 4,091 |
| `/21` | 2,048 | 2,043 |
| `/22` | 1,024 | 1,019 |
| `/23` | 512 | 507 |
| `/24` | 256 | 251 |
| `/25` | 128 | 123 |
| `/26` | 64 | 59 |
| `/27` | 32 | 27 |
| `/28` | 16 | 11 |

> ⚠️ Every "how many usable hosts" question on the exam needs you to **subtract 5**, not just compute `2^(32-n)`. This is different from classic on-prem subnetting (which only reserves 2: network + broadcast).

---

## 3. Worked Example 1 — split `10.0.0.0/16` into 4 equal subnets

**Step 1 — how many extra bits do we need?** To split one block into 4 *equal* pieces, we need `2^2 = 4`, so we borrow **2 more bits** from the host portion.

**Step 2 — new prefix** = original prefix + borrowed bits = `/16 + 2` = **`/18`**.

**Step 3 — size of each `/18`** = `2^(32-18)` = `2^14` = **16,384 IPs** each (16,384 × 4 = 65,536 ✓, matches the original `/16`).

**Step 4 — where do the boundaries fall?** 16,384 addresses = 64 in the third octet (16,384 ÷ 256 = 64). So each block's third octet jumps in steps of 64: `0, 64, 128, 192`.

| Subnet | CIDR | Range | First usable | Last usable |
|---|---|---|---|---|
| 1 | `10.0.0.0/18` | `10.0.0.0` – `10.0.63.255` | `10.0.0.4` | `10.0.63.254` |
| 2 | `10.0.64.0/18` | `10.0.64.0` – `10.0.127.255` | `10.0.64.4` | `10.0.127.254` |
| 3 | `10.0.128.0/18` | `10.0.128.0` – `10.0.191.255` | `10.0.128.4` | `10.0.191.254` |
| 4 | `10.0.192.0/18` | `10.0.192.0` – `10.0.255.255` | `10.0.192.4` | `10.0.255.254` |

(First usable = network address + 4, skipping the 4 reserved-at-the-start addresses; last usable = broadcast address − 1.)

---

## 4. Worked Example 2 — the actual `myapp-vpc` layout

Recall: `myapp-vpc` (`10.0.0.0/16`) uses four `/24` subnets:

| Subnet | CIDR | Third octet | Usable range |
|---|---|---|---|
| `myapp-public-subnet-1` | `10.0.1.0/24` | `1` | `10.0.1.4` – `10.0.1.254` (251 usable) |
| `myapp-public-subnet-2` | `10.0.2.0/24` | `2` | `10.0.2.4` – `10.0.2.254` (251 usable) |
| `myapp-private-subnet-1` | `10.0.11.0/24` | `11` | `10.0.11.4` – `10.0.11.254` (251 usable) |
| `myapp-private-subnet-2` | `10.0.12.0/24` | `12` | `10.0.12.4` – `10.0.12.254` (251 usable) |

**Why these are valid and non-overlapping:** a `/24` fixes the first three octets and leaves the 4th free (`2^8 = 256` IPs), so **every distinct third-octet value is a separate, non-overlapping block**. `1 ≠ 2 ≠ 11 ≠ 12`, so there's zero overlap — the ranges don't even need to be adjacent.

**How much is left unused?** The `/16` has room for **256 possible `/24` subnets** (third octet `0`–`255`). We've used 4 (`1, 2, 11, 12`). That leaves **252 unused `/24` blocks** — plenty of room for a future database tier (e.g. `10.0.21.0/24`, `10.0.22.0/24`, if we ever split the private tier into a separate app tier and DB tier), more AZs, or entirely new tiers, without ever touching the ranges already in use.

> 🧠 Leaving gaps on purpose (public subnets at `.1`/`.2`, private at `.11`/`.12`, not `.3`/`.4`) is a deliberate real-world habit — it leaves room to insert more subnets per tier later without renumbering everything.

---

## 5. Worked Example 3 — VLSM: sizing subnets for 500, 100, and 30 hosts

**VLSM (Variable Length Subnet Masking)** = giving each subnet only as much space as it needs, instead of forcing every subnet to be the same size. Given a pool like `10.0.0.0/16`, size a subnet for each requirement:

**The method, step by step, for any "N hosts" requirement:**
1. Add AWS's 5 reserved IPs to the requirement: `N + 5`.
2. Round **up** to the next power of 2 — that's your subnet's total IP count.
3. Convert total IPs to a prefix: `prefix = 32 - log2(total IPs)`.

**500 hosts:**
- `500 + 5 = 505`
- Next power of 2 ≥ 505 → `512` (`2^9`)
- Prefix = `32 - 9 = /23`
- Check: `/23` → 512 total, `512 - 5 = 507` usable ≥ 500 ✓

**100 hosts:**
- `100 + 5 = 105`
- Next power of 2 ≥ 105 → `128` (`2^7`)
- Prefix = `32 - 7 = /25`
- Check: `/25` → 128 total, `128 - 5 = 123` usable ≥ 100 ✓

**30 hosts:**
- `30 + 5 = 35`
- Next power of 2 ≥ 35 → `64` (`2^6`)
- Prefix = `32 - 6 = /26`
- Check: `/26` → 64 total, `64 - 5 = 59` usable ≥ 30 ✓ (note: `/27` = 32 total, 27 usable, which is **too small** for 30 — this is exactly the kind of off-by-one trap the exam sets)

**Laying them out without overlap** (example allocation inside `10.0.0.0/16`, separate from the `myapp` production layout — just for this exercise):

| Requirement | CIDR | Range | Usable |
|---|---|---|---|
| 500 hosts | `10.0.64.0/23` | `10.0.64.0` – `10.0.65.255` | 507 |
| 100 hosts | `10.0.66.0/25` | `10.0.66.0` – `10.0.66.127` | 123 |
| 30 hosts | `10.0.66.128/26` | `10.0.66.128` – `10.0.66.191` | 59 |

Each block starts exactly where the previous one ends (or on a valid boundary for its size), so nothing overlaps.

---

## 6. Worked Example 4 — the default VPC, `172.31.0.0/16`, split into `/20`s

This is literally what AWS's **default VPC** (the `172.31.0.0/16` VPC that AWS auto-creates in every Region for every new account) does automatically, one subnet per AZ:

- Block size of a `/20` = `2^(32-20)` = `2^12` = **4,096 total IPs** (usable = `4,091`).
- How many `/20` blocks fit inside a `/16`? `2^(20-16)` = `2^4` = **16 subnets**.
- 4,096 IPs = 16 in the third octet (`4096 ÷ 256 = 16`), so boundaries step by 16: `0, 16, 32, 48, ...`

First 3 default subnets:

| Subnet | CIDR | Range |
|---|---|---|
| 1 | `172.31.0.0/20` | `172.31.0.0` – `172.31.15.255` |
| 2 | `172.31.16.0/20` | `172.31.16.0` – `172.31.31.255` |
| 3 | `172.31.32.0/20` | `172.31.32.0` – `172.31.47.255` |

AWS creates one such `/20` per AZ in the Region (e.g. 3 AZs → 3 of these subnets used, 13 left unused in the default VPC's address space).

---

## 7. Practice problems (self-test)

**Problem 1:** You have `10.20.0.0/16` and need **8 equal-sized subnets**. What prefix should each use, and what's the CIDR of the **3rd** subnet?

<details>
<summary>Show answer</summary>

- 8 subnets = `2^3` → borrow 3 bits → prefix = `/16 + 3` = **`/19`**.
- Block size = `2^(32-19)` = `2^13` = 8,192 IPs = 32 in the third octet (8192 ÷ 256 = 32).
- Boundaries: `10.20.0.0`, `10.20.32.0`, `10.20.64.0`, `10.20.96.0` …
- **3rd subnet = `10.20.64.0/19`**.
</details>

**Problem 2:** How many **usable** IP addresses are in a `/27` subnet on AWS?

<details>
<summary>Show answer</summary>

- Total = `2^(32-27)` = `2^5` = 32.
- Usable = `32 - 5` = **27**.
</details>

**Problem 3:** You need a subnet for **252 EC2 instances**. Why can't you use a `/24`, and what's the smallest CIDR that works?

<details>
<summary>Show answer</summary>

- `/24` gives `256 - 5 = 251` usable — **one short** of 252! A classic reserved-IP trap.
- Next size up: `/23` → `512 - 5 = 507` usable, which comfortably fits 252.
- **Answer: `/23`.**
</details>

---

## 8. Secondary CIDR blocks and a note on IPv6

- A VPC isn't locked to its original CIDR forever — you can **add secondary CIDR blocks** later (up to 5 total per VPC, including the primary) if you run out of address space, e.g. adding `10.1.0.0/16` on top of `myapp-vpc`'s original `10.0.0.0/16`. New subnets can then be created inside the secondary range. The same non-overlap rule applies to secondary blocks too: a secondary CIDR must not overlap the primary block, any other secondary block, or any network you'll ever connect the VPC to (a peered VPC, an on-premises network over VPN, etc.).
- **IPv6 in a VPC works completely differently and needs no math at all**: if you enable IPv6, AWS (or your own BYOIP pool) assigns the **VPC a fixed `/56` block**, and **every subnet gets a fixed `/64` block** carved out of it automatically. There's no VLSM-style sizing decision to make — every subnet is always exactly `/64`, because IPv6's address space is so vast that fixed-size allocation is simply the design. Just remember the two magic numbers: **VPC = `/56`, subnet = `/64`**.

---

## 9. Recap

- Total IPs = `2^(32-prefix)`; **AWS always reserves 5**, so usable = `2^(32-prefix) - 5`.
- Splitting into **N equal subnets** → borrow `log2(N)` bits → new prefix = old prefix + borrowed bits.
- **VLSM** for an exact host count → `(hosts + 5)` → round up to the next power of 2 → derive the prefix.
- `myapp-vpc`'s four `/24`s (`.1`, `.2`, `.11`, `.12`) are valid because different third octets never overlap, leaving 252 `/24` blocks free for growth.
- Default VPC = `172.31.0.0/16` split into `/20`s, one per AZ.
- A VPC can grow via **secondary CIDR blocks**; **IPv6 needs no math** — VPC is always `/56`, subnets are always `/64`.
- Next: **Note 04** — create `myapp-vpc` for real in the console.

---

### Sources
- [IP addressing for your VPCs and subnets – AWS docs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html)
- [Subnet sizing and reserved IP addresses – AWS docs](https://docs.aws.amazon.com/vpc/latest/userguide/subnet-sizing.html)
- [Amazon VPC IP Address Manager (IPAM) – AWS docs](https://docs.aws.amazon.com/vpc/latest/ipam/what-it-is-ipam.html)
