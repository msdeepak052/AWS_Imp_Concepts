# 16 - EC2 Termination Protection (and Stop Protection)

> Goal: prevent **accidental deletion** of important instances using **Termination Protection**, understand its limits, and learn the related **Stop Protection** and **Shutdown Behavior** settings. Includes a hands-on.

---

## 1. The problem

**Terminating** an instance is **permanent** — the instance is deleted and (by default) its **root EBS volume is destroyed**. One careless click on "Terminate" can wipe a production server.

**Termination Protection** adds a safety latch: while it's ON, an instance **cannot be terminated** until you explicitly turn the protection off.

---

## 2. What Termination Protection does (and doesn't)

✅ **Protects against:**
- Terminating via the **Console**, **CLI** (`terminate-instances`), or **API** — the request is **rejected** until protection is disabled.

❌ **Does NOT protect against:**
- **Stopping** the instance (use *Stop Protection* for that — see §5).
- **Rebooting**.
- **OS-level shutdown** *if* the instance's **Shutdown behavior = Terminate** (see §4) — in that case an in-OS `shutdown` could still terminate it. Keep Shutdown behavior = **Stop**.
- **Auto Scaling** terminations — ASG manages its own instance lifecycle and can still terminate them (it ignores this flag in scaling actions).
- **Spot Instance** interruptions — Spot instances can't reliably use it; AWS reclaims them.
- Deleting the **EBS volume** directly.

> 🧠 So Termination Protection guards the **manual "Terminate" action** on normal On-Demand instances. It's a guardrail, not a force field.

---

## 3. Hands-On — enable & test

**Enable at launch:**
- Launch wizard → **Advanced details** → **Termination protection** → **Enable**.

**Enable on an existing instance:**
1. EC2 → **Instances** → select instance.
2. **Actions → Instance settings → Change termination protection**.
3. Check **Enable** → **Save**.

**Test it:**
1. Select the instance → **Instance state → Terminate (delete) instance**.
2. You get an error like *"The instance 'i-xxxx' may not be terminated. Modify its 'disableApiTermination' instance attribute and try again."* ✅ Protection works.

**Disable to actually terminate:**
1. **Actions → Instance settings → Change termination protection** → uncheck → Save.
2. Now **Instance state → Terminate** succeeds.

---

## 4. Shutdown Behavior (related setting)

Controls what happens when the OS issues a shutdown (e.g. you run `sudo shutdown` inside the instance):
- **Stop** (default, recommended) → instance just stops, data on EBS preserved.
- **Terminate** → instance is deleted on OS shutdown. ⚠️ Combined with this, an in-OS shutdown could bypass the intent of termination protection.

Set it in **Actions → Instance settings → Change shutdown behavior**. Keep it on **Stop** for important servers.

---

## 5. Stop Protection (the sibling feature)

Termination Protection blocks **terminate**, but not **stop**. If stopping an instance is also disruptive (e.g. it loses its public IP, or interrupts a job), enable **Stop Protection**:
- **Actions → Instance settings → Change stop protection → Enable.**
- Now the instance **can't be stopped** until you disable it.

> Use **both** Termination + Stop protection for truly critical instances.

---

## 6. The `disableApiTermination` attribute (CLI)

Under the hood it's an instance attribute. Via CLI:

```bash
# Enable termination protection
aws ec2 modify-instance-attribute --instance-id i-0123456789abcdef0 \
  --disable-api-termination

# Disable it (allow termination)
aws ec2 modify-instance-attribute --instance-id i-0123456789abcdef0 \
  --no-disable-api-termination
```

Stop protection equivalent: `--disable-api-stop` / `--no-disable-api-stop`.

---

## 7. Best practices

- Turn on **Termination Protection** for all **production / stateful** instances.
- Keep **Shutdown behavior = Stop**.
- For critical data, also rely on **EBS snapshots / backups** — protection prevents accidental *terminate*, not data corruption.
- Use **IAM policies** to restrict *who* can call `TerminateInstances` (defense in depth beyond the per-instance flag).
- Remember it's **ignored by Auto Scaling and Spot** — design accordingly.

---

## 8. Recap

- **Termination Protection** blocks the **manual Terminate** action (console/CLI/API) until disabled.
- Does **not** block stop/reboot, OS-shutdown-to-terminate, ASG, or Spot reclaim.
- **Stop Protection** separately blocks stopping; **Shutdown behavior** should stay **Stop**.
- Pair with **IAM restrictions** and **backups** for real protection.
- Next (Note 17): **EC2 Placement Groups** — controlling how instances are physically placed.

---

### Sources
- [Enable termination protection – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/terminating-instances.html#Using_ChangingDisableAPITermination)
- [Enable stop protection – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Stop_Start.html#enable-stop-protection)
- [Change the instance initiated shutdown behavior – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/terminating-instances.html#Using_ChangingInstanceInitiatedShutdownBehavior)
