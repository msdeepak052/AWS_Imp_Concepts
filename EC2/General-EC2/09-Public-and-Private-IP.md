# 09 - Public IP & Private IP (and how EC2 networking addresses work)

> Goal: clearly understand **private IP**, **public IP**, and **how an instance gets onto the internet** — plus the gotchas that confuse every beginner (the public IP that changes on stop/start).

---

## 1. What is an IP address?

An **IP address** is the unique number that identifies a device on a network so traffic can find it. IPv4 looks like `172.31.16.42`. There are two flavors that matter for EC2:

- **Private IP** — usable only **inside** the AWS private network (your VPC).
- **Public IP** — reachable from the **public internet**.

---

## 2. Private IP address

- Comes from your **VPC subnet's CIDR range** (private ranges defined by RFC 1918): `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`.
- Every instance **always** has a private IP (e.g. `172.31.20.5`).
- Used for **internal communication** — instance-to-instance, instance-to-RDS, within the VPC.
- **The private IP stays the same** for the life of the instance (even across stop/start) because it's tied to the instance's network interface.
- Traffic over private IPs stays inside AWS = **free within the same AZ** and cheaper than going over the internet.

---

## 3. Public IP address

- A globally-routable address that lets the **internet reach your instance**.
- **Auto-assigned** at launch **only if** the subnet/instance setting "Auto-assign public IP" is **enabled** (and the instance is in a public subnet).
- ⚠️ **The auto-assigned public IP is NOT permanent:**
  - It **changes** every time you **Stop then Start** the instance.
  - It is **released** when you stop/terminate the instance.
  - You do **not** get to choose it.
- The instance itself never "sees" its public IP on its own OS — AWS maps it via **NAT** at the internet gateway to the private IP.

> 🧠 This is why connecting by public IP "breaks" after a stop/start — the IP changed. The fix for a stable address is an **Elastic IP** — a static public IPv4 address that you allocate to your own AWS account and attach to an instance, which does **not** change across stop/start (unlike the auto-assigned public IP).

---

## 4. Public DNS name

When a public IP is assigned, the instance also gets a **public DNS hostname** like:
```
ec2-13-234-10-20.ap-south-1.compute.amazonaws.com
```
- From the **internet**, this resolves to the **public IP**.
- From **inside the VPC**, AWS resolves it to the **private IP** (smart — keeps internal traffic private and free).

---

## 5. Public vs Private IP — side by side

| | **Private IP** | **Public IP (auto-assigned)** |
|---|---|---|
| Reachable from | Inside VPC only | The internet |
| Source range | Subnet CIDR (10/172/192…) | AWS public pool |
| Always present? | ✅ Yes | Only if enabled + public subnet |
| Survives Stop/Start? | ✅ Yes | ❌ No — it changes |
| Cost | Free internally | Free while attached to a running instance (IPv4 now has small idle charges — see below) |
| You choose it? | You can specify within subnet | ❌ No |

---

## 6. What makes an instance reachable from the internet?

All of these must be true (the "public" path in a VPC):
1. Instance has a **public IP** (or Elastic IP).
2. It is in a **public subnet** → the subnet's **route table** has a route `0.0.0.0/0 → Internet Gateway (IGW)`.
3. An **Internet Gateway** is attached to the VPC.
4. **Security group** allows the inbound port (e.g. 22/80/443).
5. **Network ACL** (subnet-level firewall) allows the traffic (default NACL allows all).

> Private subnet = no route to an IGW. Instances there reach the internet **outbound only** via a **NAT Gateway**, and cannot be reached **inbound** from the internet.

---

## 7. IPv4 cost note (2024+ change — still applies in 2026)

AWS now charges a **small hourly fee for every public IPv4 address**, including auto-assigned public IPs on running instances and idle Elastic IPs. **IPv6** addresses don't carry this charge. For learning this is tiny (cents), but it's why you should release public IPs you don't need.

---

## 8. Quick hands-on observation

1. Launch a Linux instance with **Auto-assign public IP = Enable**.
2. Note its **Public IPv4** and **Private IPv4** (Instances → details).
3. **Stop** then **Start** the instance.
4. Look again → **private IP unchanged**, **public IP is different**. ✅ Proves the lesson.

---

## 9. Recap

- **Private IP** = internal, permanent, from subnet CIDR, free internally.
- **Public IP** = internet-facing, **temporary** (changes on stop/start), auto-assigned only if enabled.
- Public DNS resolves to public IP externally, private IP internally.
- Internet reachability needs: public IP + public subnet (IGW route) + SG + NACL allowing the port.
- Need a **fixed** public address that survives stop/start? → **Elastic IP** (Note 10).

---

### Sources
- [Amazon EC2 instance IP addressing – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-instance-addressing.html)
- [Public IPv4 address charges – AWS](https://aws.amazon.com/blogs/aws/new-aws-public-ipv4-address-charge-public-ip-insights/)
- [VPC internet gateways – AWS docs](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html)
