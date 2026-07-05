# 05 - Build Part 1: VPC and Networking (Hands-On)

> Goal: build the network foundation every other part of this capstone sits on — the VPC, all 8 subnets, the Internet Gateway, the single shared NAT Gateway, and the route tables that tie them together. Nothing in this part costs much beyond the NAT Gateway's hourly charge, and nothing here is application-specific — it's pure networking, matching the design from Note 02.

---

## 1. Create the VPC

1. Open the **VPC console** → **Your VPCs** → **Create VPC**.
2. Choose **VPC only** (not "VPC and more" — building it by hand makes every later piece of this capstone easier to follow).
3. **Name tag**: `cloudmart-vpc`
4. **IPv4 CIDR block**: `10.20.0.0/16`
5. Leave IPv6 and tenancy at their defaults → **Create VPC**.
6. Select `cloudmart-vpc` → **Actions** → **Edit VPC settings** → enable **DNS resolution** and **DNS hostnames** (both required — the backend and frontend instances need working DNS to resolve package repositories and, later, the internal ALB's DNS name).

---

## 2. Create the eight subnets

Go to **Subnets** → **Create subnet**, select `cloudmart-vpc`, and add all eight in one wizard (use **Add new subnet** to add rows before creating):

| Name | Availability Zone | IPv4 CIDR |
|---|---|---|
| `cloudmart-web-subnet-1` | `ap-south-1a` | `10.20.1.0/24` |
| `cloudmart-web-subnet-2` | `ap-south-1b` | `10.20.2.0/24` |
| `cloudmart-web-private-1` | `ap-south-1a` | `10.20.31.0/24` |
| `cloudmart-web-private-2` | `ap-south-1b` | `10.20.32.0/24` |
| `cloudmart-app-subnet-1` | `ap-south-1a` | `10.20.11.0/24` |
| `cloudmart-app-subnet-2` | `ap-south-1b` | `10.20.12.0/24` |
| `cloudmart-db-subnet-1` | `ap-south-1a` | `10.20.21.0/24` |
| `cloudmart-db-subnet-2` | `ap-south-1b` | `10.20.22.0/24` |

Click **Create subnet** once all eight rows are filled in.

For the two `cloudmart-web-subnet-*` subnets only: select each → **Actions** → **Edit subnet settings** → enable **Auto-assign public IPv4 address**. Leave this disabled for all six other subnets (`web-private-1/2`, `app-subnet-1/2`, `db-subnet-1/2`) — they must never hand out a public IP. Note that `cloudmart-web-subnet-1/2` end up holding only the ALBs' nodes and the NAT Gateway — no EC2 instance is ever launched directly into them; the frontend's actual compute lives in `cloudmart-web-private-1/2` instead (Note 02, Section 1).

> ⚠️ `cloudmart-db-subnet-2` is created now but stays empty for this entire capstone — it exists so the network layout is already Multi-AZ-ready if this project is later extended to a real RDS Multi-AZ database (Note 02's named HA gap), without having to re-architect the VPC.

---

## 3. Create and attach the Internet Gateway

1. **Internet Gateways** → **Create internet gateway** → name it `cloudmart-igw` → **Create**.
2. Select it → **Actions** → **Attach to VPC** → choose `cloudmart-vpc` → **Attach internet gateway**.

---

## 4. Create the single shared NAT Gateway

A NAT Gateway needs its own Elastic IP and must sit in a **public** subnet (it needs a route to the internet itself, to translate outbound traffic from the private subnets).

1. **Elastic IPs** → **Allocate Elastic IP address** → **Allocate**.
2. **NAT Gateways** → **Create NAT gateway**:
   - Name: `cloudmart-nat-gw-1`, Subnet: `cloudmart-web-subnet-1`, Connectivity type: **Public**, Elastic IP: pick the allocated EIP → **Create NAT gateway**.
3. Wait until it shows **Available** (usually a few minutes) before continuing.

> 🎯 **Exam tip:** a NAT Gateway is scoped to a single Availability Zone — it is not itself a multi-AZ resource. The textbook HA answer is **one NAT Gateway per AZ**, so that one AZ's NAT failing never strands another AZ's outbound traffic. This capstone deliberately deviates from that textbook answer: it uses **one shared NAT Gateway** for all six private subnets across both AZs, to halve the always-on NAT cost, and names the resulting single point of failure explicitly (Note 02, Section 4) rather than hiding it. A route table in one AZ (e.g. `ap-south-1b`) pointing at a NAT Gateway that physically lives in another AZ (`ap-south-1a`) is completely valid — AWS routes across the AZ boundary transparently, at a small per-GB inter-AZ data charge. Know both the "textbook HA" answer and this cost-optimized variant; the exam tests the textbook answer, but real-world architecture regularly makes this exact trade-off.

---

## 5. Create the two route tables

1. **Route Tables** → **Create route table**:
   - `cloudmart-web-rt`, VPC: `cloudmart-vpc` → **Create**.
   - Select it → **Routes** tab → **Edit routes** → **Add route**: destination `0.0.0.0/0`, target **Internet Gateway** → `cloudmart-igw` → **Save**.
   - **Subnet associations** tab → **Edit subnet associations** → select `cloudmart-web-subnet-1` and `cloudmart-web-subnet-2` → **Save**.
2. `cloudmart-private-rt`, VPC: `cloudmart-vpc` → **Create**.
   - **Edit routes** → add `0.0.0.0/0` → target **NAT Gateway** → `cloudmart-nat-gw-1` → **Save**.
   - **Edit subnet associations** → select all six private subnets: `cloudmart-web-private-1`, `cloudmart-web-private-2`, `cloudmart-app-subnet-1`, `cloudmart-app-subnet-2`, `cloudmart-db-subnet-1`, `cloudmart-db-subnet-2` → **Save**. All six share the same single route (`0.0.0.0/0 → cloudmart-nat-gw-1`), so one route table is enough — there's no per-AZ split anymore since there's only one NAT Gateway to point at.

Every subnet also automatically keeps its `10.20.0.0/16 → local` route — that's implicit and lets every subnet in the VPC reach every other subnet directly, regardless of which route table it's associated with.

---

## 6. End state

```mermaid
flowchart TB
    subgraph VPC["cloudmart-vpc — 10.20.0.0/16"]
        IGW[cloudmart-igw]
        N1[cloudmart-nat-gw-1<br/>single shared NAT]
        subgraph AZA["ap-south-1a"]
            WS1["cloudmart-web-subnet-1<br/>10.20.1.0/24 (public)"]
            WP1["cloudmart-web-private-1<br/>10.20.31.0/24 (private)"]
            AS1["cloudmart-app-subnet-1<br/>10.20.11.0/24 (private)"]
            DS1["cloudmart-db-subnet-1<br/>10.20.21.0/24 (private)"]
            WS1 --- N1
        end
        subgraph AZB["ap-south-1b"]
            WS2["cloudmart-web-subnet-2<br/>10.20.2.0/24 (public)"]
            WP2["cloudmart-web-private-2<br/>10.20.32.0/24 (private)"]
            AS2["cloudmart-app-subnet-2<br/>10.20.12.0/24 (private)"]
            DS2["cloudmart-db-subnet-2<br/>10.20.22.0/24 (private, unused)"]
        end
        WS1 & WS2 --> IGW
        WP1 & AS1 & DS1 & WP2 & AS2 & DS2 -.route via cloudmart-private-rt.-> N1
    end
```

No compute or load balancers exist yet — that starts in Part 2 (security groups) and Part 3 (the database instance). This part is purely the network shell.

---

## 7. Troubleshooting

| Symptom | Likely cause |
|---|---|
| Can't select a subnet when creating the NAT Gateway | You're looking at a private subnet — a NAT Gateway must launch in a **public** subnet (one with an IGW route) |
| Subnet CIDR error on creation | Overlap with an already-created subnet — double check the octets in the table above, none of `1`, `2`, `11`, `12`, `21`, `22`, `31`, `32` should repeat |
| An instance later can't reach the internet | Check which route table its subnet is associated with, and that route table's `0.0.0.0/0` target — a common mistake is leaving a subnet on the VPC's default **main** route table instead of `cloudmart-private-rt` |

---

## 8. Recap

- `cloudmart-vpc` (`10.20.0.0/16`) now has 8 subnets across 2 AZs, one Internet Gateway, one shared NAT Gateway, and 2 route tables wiring it all together.
- Only the two public web subnets have a direct route to the internet; all six private subnets (including the new `cloudmart-web-private-1/2`) route outbound-only through the single `cloudmart-nat-gw-1` via `cloudmart-private-rt`.
- Next: Note 06 — Build Part 2: Security Groups and IAM, where the SG chain from Note 02 gets created for real.

### Sources
- [Create a VPC — AWS docs](https://docs.aws.amazon.com/vpc/latest/userguide/create-vpc.html)
- [NAT gateways — AWS docs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)
- [Route tables — AWS docs](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html)
