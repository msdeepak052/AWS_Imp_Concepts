# 05 - Amazon Machine Image (AMI)

> Goal: understand what an **AMI** is, what it contains, the different **types/sources** of AMIs, and why AMIs are the key to **fast, consistent, repeatable** instance launches. Hands-on (building your own) is in Note 06.

---

## 1. What is an AMI?

An **Amazon Machine Image (AMI)** is a **template** that contains everything needed to **boot and run an EC2 instance**:

- The **operating system** (Amazon Linux, Ubuntu, Windows, RHEL…).
- **Pre-installed software / configuration** (e.g. a web server, your app, patches).
- **Block device mapping** — which EBS volumes/snapshots to attach and their sizes.
- **Launch permissions** — who is allowed to use this AMI.

> 🧠 **Analogy:** An AMI is like a **"golden master" disk image** or a phone "factory image". You launch many identical instances from one AMI — like stamping copies from a mould.

---

## 2. Why AMIs matter

1. **Speed** — boot a ready-to-go server in ~1 minute instead of installing software each time.
2. **Consistency** — every instance from the same AMI is identical (no "works on my machine" drift).
3. **Scalability** — Auto Scaling launches new instances from an AMI automatically during traffic spikes.
4. **Disaster recovery / backup** — an AMI is a restorable snapshot of a known-good server.

---

## 3. What an AMI is made of (the components)

| Component | Description |
|---|---|
| **Root volume template** | An **EBS snapshot** (or instance-store template) containing the OS + software. |
| **Launch permissions** | Controls which AWS accounts can launch from this AMI (private / shared / public). |
| **Block device mapping** | Defines the volumes attached at launch (root + any extra data volumes). |

**Key fact:** An EBS-backed AMI is built **on top of EBS snapshots**. When you create an AMI, AWS creates snapshot(s) behind the scenes; deleting the AMI alone may leave snapshots that still cost money.

---

## 4. Where AMIs come from (sources)

When you launch an instance, the AMI selector has these categories:

1. **Quick Start AMIs** — official, ready-made images by AWS and OS vendors (Amazon Linux, Ubuntu, Windows, etc.). Best for beginners.
2. **My AMIs** — AMIs **you created** (your customized images — Note 06).
3. **AWS Marketplace AMIs** — third-party images, often pre-loaded with commercial software (some have extra hourly software fees).
4. **Community AMIs** — images shared publicly by other users (use with caution — verify the source).

---

## 5. AMI storage type: EBS-backed vs Instance Store-backed

| | **EBS-backed AMI** (common) | **Instance store-backed AMI** (rare) |
|---|---|---|
| Root device | EBS volume (network disk) | Ephemeral local disk |
| Can **stop** the instance? | ✅ Yes | ❌ No (only run/terminate) |
| Data persists on stop? | ✅ Yes | ❌ Lost when instance stops/terminates |
| Boot time | Fast | Slower |
| Most modern AMIs | ✅ | Legacy |

> For the SAA exam and real life, you'll almost always use **EBS-backed** AMIs.

---

## 6. AMIs are Region-specific (very important!)

- An AMI **belongs to the Region where it was created** and has a Region-specific **AMI ID** (e.g. `ami-0abcd1234` in `us-east-1`).
- To use the same AMI in another Region, you **copy the AMI** to that Region (which copies the underlying snapshots). It gets a **new AMI ID** there.
- This is how you deploy a consistent image globally or set up **cross-Region disaster recovery**.

---

## 7. Sharing AMIs

- **Private** (default) — only your account.
- **Shared with specific AWS accounts** — grant launch permission to a partner account.
- **Public** — anyone can launch it (be careful: never leave secrets/keys baked into a public AMI).
- You can also publish to **AWS Marketplace**.

---

## 8. AMI lifecycle (the typical flow)

```
Launch base AMI → customize instance (install apps, configure) →
Create Image (AMI)  → (optional) Copy AMI to other Regions →
Launch new instances from your AMI → Deregister AMI + delete snapshots when done
```

- **Create Image** = make an AMI from a running/stopped instance.
- **Deregister** = delete the AMI. ⚠️ Remember to also **delete the leftover EBS snapshots** to stop paying for them.
- **EC2 Image Builder** is an AWS service that automates building, patching, and testing AMIs on a schedule.

---

## 9. Cost of AMIs

- An AMI itself has no charge, **but** the **EBS snapshots** it relies on are billed by GB-month of snapshot storage.
- Many AMIs sharing snapshots only pay for unique stored blocks (incremental).
- Marketplace AMIs may add a **per-hour software fee** on top of EC2 costs.

---

## 10. Quick recap

- AMI = **template** (OS + software + config + block device mapping + permissions) used to launch instances.
- Benefits: **speed, consistency, scaling, recovery**.
- Sources: **Quick Start, My AMIs, Marketplace, Community**.
- AMIs are **Region-specific** → **copy** to use elsewhere.
- EBS-backed AMIs (can stop instance) are the norm; built on **EBS snapshots** — clean those up to avoid cost.
- Next (Note 06): **build your own custom AMI** hands-on.

---

### Sources
- [Amazon Machine Images (AMI) – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html)
- [AMI types (EBS vs instance store) – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ComponentsAMIs.html)
- [Copy an AMI – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/CopyingAMIs.html)
