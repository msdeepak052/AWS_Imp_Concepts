# 10 - Elastic IP (EIP)

> Goal: understand the **Elastic IP** — a **static, permanent public IPv4 address** you own and can move between instances — when to use it, when **not** to, and a full hands-on.

---

## 1. The problem Elastic IP solves

Recall: the **auto-assigned public IP changes** every time you stop/start an instance (the old address is released and a new one is handed out). That's bad if:
- DNS records, firewalls, or partners are configured to point at a **fixed** IP.
- You need to **replace** a failed instance but keep the **same** public address.

An **Elastic IP (EIP)** is a **static public IPv4 address** that:
- **Stays the same** until you choose to release it.
- Belongs to **your AWS account** (you "own" it).
- Can be **remapped** from one instance to another in seconds.

---

## 2. How it works

1. You **allocate** an Elastic IP from Amazon's pool (or bring your own — BYOIP).
2. You **associate** it with an instance (technically with the instance's network interface / private IP).
3. The instance is now reachable at that fixed public IP.
4. If the instance dies, you **re-associate** the EIP to a healthy instance → same address, minimal downtime.

> 🧠 Think of an EIP as a **phone number you keep** even when you change phones.

---

## 3. Important rules & gotchas

- An EIP **survives stop/start** of the instance (unlike auto-assigned public IPs).
- **Cost trap:** An EIP is **billed when it is NOT actively in use.** AWS charges an hourly fee for:
  - an EIP that is **allocated but not associated** with anything, or
  - associated with a **stopped** instance, or
  - a second EIP on the same instance.
  - *(Separately, since 2024 all public IPv4 — even in-use EIPs — carry a small hourly charge.)*
  - 👉 **Lesson:** release EIPs you no longer need.
- Default soft limit: **5 Elastic IPs per Region** (can request an increase).
- EIPs are **IPv4 only** (IPv6 doesn't need them — IPv6 addresses are globally routable already).
- An EIP is **Region-scoped** — you can't move it to another Region.

---

## 4. When to use an Elastic IP — and when NOT to

**Use an EIP when:**
- A single instance must keep a **fixed public IP** (legacy systems, whitelisting, NAT instances).
- You need to quickly **failover** an address to a standby instance.

**Avoid an EIP (use something better) when:**
- You have **many** instances → put them behind a **Load Balancer** (it gives a stable DNS name) instead of an EIP each.
- You just need a stable **name** → use **Route 53 DNS** pointing at the LB.
- 🧠 AWS best practice: **EIPs should be the exception, not the default.** Modern designs prefer **ELB + Auto Scaling + Route 53** over pinning EIPs to instances.

---

## 5. Hands-On — allocate and associate an Elastic IP

**Step 1 — Allocate:**
1. EC2 console → left menu **Network & Security → Elastic IPs**.
2. Click **Allocate Elastic IP address** → keep "Amazon's pool of IPv4 addresses" → **Allocate**.
3. A new public IP appears (e.g. `13.235.x.x`). (Optional: add a Name tag.)

**Step 2 — Associate with an instance:**
1. Select the EIP → **Actions → Associate Elastic IP address**.
2. **Resource type**: Instance → choose your instance → choose its private IP.
3. **Associate**.
4. The instance's **Public IPv4** now shows the Elastic IP.

**Step 3 — Prove it's stable:**
1. Connect via the EIP (SSH/RDP/browser).
2. **Stop** then **Start** the instance.
3. The public address is **still the same EIP** (whereas an auto-assigned IP would have changed). ✅

**Step 4 — Remap (failover demo):**
1. Launch a second instance.
2. EIP → **Actions → Associate** → point it at the new instance.
3. Traffic to the same IP now hits the new instance.

---

## 6. ⚠️ Clean up (avoid charges)

1. EIP → **Actions → Disassociate Elastic IP address**.
2. EIP → **Actions → Release Elastic IP address**.
> If you only terminate the instance but **don't release** the EIP, the now-idle EIP keeps charging you.

---

## 7. Troubleshooting

| Symptom | Cause / Fix |
|---|---|
| Surprise small charge | EIP allocated but not associated, or attached to a stopped instance. Release unused EIPs. |
| Can't associate | EIP already in use, or instance in a different Region. EIPs are Region-scoped. |
| Still can't reach instance | EIP fixes the address, but you still need a **security group** rule allowing the port (e.g. 22/80/443) for your source, and the instance's subnet needs a route to an **Internet Gateway** (i.e. it must be a public subnet) — the fixed IP alone doesn't open a path through the firewall or the network. |

---

## 8. Recap

- **Elastic IP = static public IPv4** you own and can **move between instances**.
- Survives stop/start (fixes the changing-IP problem).
- **Charged when idle/unassociated** → release what you don't use; max 5/Region by default.
- Prefer **Load Balancer + Route 53** over EIPs when you have multiple instances.
- Next (Note 11): **Security Groups Part 1** — the instance firewall.

---

### Sources
- [Elastic IP addresses – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html)
- [Elastic IP address pricing – Amazon EC2 pricing](https://aws.amazon.com/ec2/pricing/on-demand/)
- [Public IPv4 address charge – AWS](https://aws.amazon.com/blogs/aws/new-aws-public-ipv4-address-charge-public-ip-insights/)
