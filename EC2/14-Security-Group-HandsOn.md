# 14 - Security Group (Hands-On)

> Goal: practically **create a security group, add/edit/delete rules, attach it to an instance, and actually observe traffic being allowed vs blocked.** This cements Parts 1–3.

---

## 0. Setup

Have one **Linux instance running** (Amazon Linux, `t3.micro`) with a web server installed so we have something to test:

```bash
ssh -i linux-key.pem ec2-user@<PUBLIC_IP>
sudo yum install -y httpd
echo "<h1>SG Test Page</h1>" | sudo tee /var/www/html/index.html
sudo systemctl enable --now httpd
```

---

## 1. Create a Security Group

1. EC2 console → **Network & Security → Security Groups** → **Create security group**.
2. **Basic details:**
   - **Name**: `web-sg`
   - **Description**: `Web + SSH access for demo`
   - **VPC**: leave the default VPC.
3. **Inbound rules → Add rule** (add these two):
   | Type | Port | Source | Description |
   |---|---|---|---|
   | SSH | 22 | **My IP** | admin access |
   | HTTP | 80 | **Anywhere-IPv4** (0.0.0.0/0) | public website |
4. **Outbound rules:** leave the default **All traffic → 0.0.0.0/0**.
5. Click **Create security group**.

---

## 2. Attach the SG to your instance

1. EC2 → **Instances** → select your instance.
2. **Actions → Security → Change security groups**.
3. Remove the old one if you like, **add `web-sg`** → **Save**.

> Changes apply **immediately** — no reboot needed.

---

## 3. Test: HTTP should work, SSH should work

- Browser → `http://<PUBLIC_IP>` → you see **"SG Test Page"**. ✅ (port 80 from Anywhere)
- Terminal → `ssh -i linux-key.pem ec2-user@<PUBLIC_IP>` → logs in. ✅ (port 22 from My IP)

---

## 4. Experiment A — remove the HTTP rule (observe a block)

1. Security Groups → `web-sg` → **Inbound rules → Edit inbound rules**.
2. **Delete** the HTTP (80) rule → **Save rules**.
3. Refresh `http://<PUBLIC_IP>` in the browser → it **hangs / times out**. ❌
   - The page is blocked because no inbound rule allows port 80 anymore (default deny).
4. **Re-add** the HTTP 80 / Anywhere rule → **Save** → refresh → page loads again. ✅

> 🧠 This proves the **allow-only / default-deny** behavior from Part 1.

---

## 5. Experiment B — break SSH by changing the source

1. Edit inbound rules → change the **SSH source** from **My IP** to a **fake IP** like `1.2.3.4/32` → Save.
2. Try `ssh ...` again → **Connection timed out**. ❌ (your IP no longer matches the allowed source).
3. Change it back to **My IP** → Save → SSH works again. ✅

> This is exactly why SSH "stops working" when your home IP changes — the rule no longer includes your address.

---

## 6. Experiment C — allow ping (ICMP)

1. From your computer: `ping <PUBLIC_IP>` → currently **no reply** (ICMP not allowed).
2. Edit inbound rules → **Add rule** → Type: **All ICMP - IPv4**, Source: **My IP** → Save.
3. `ping <PUBLIC_IP>` again → **replies now arrive**. ✅
> Lesson: ping is **ICMP**, not a TCP port — you allow it with the ICMP type, not port 80/22.

---

## 7. Experiment D — Security Group reference (two instances)

Simulate "only web servers may reach the DB":

1. Create `db-sg` (Description: "DB tier").
2. In `db-sg` add inbound rule: **MySQL/Aurora (3306)**, **Source = `web-sg`** (start typing `sg-` and pick web-sg).
3. Now any instance in `web-sg` can reach port 3306 of any instance in `db-sg`, **without hard-coding IPs**.
4. (If you launch a DB-like instance with `db-sg`, only your web instance — being in `web-sg` — could connect to 3306.)

> This is the real-world multi-tier pattern from Part 3.

---

## 8. View the effect of multiple SGs

1. Attach **both** `web-sg` and `db-sg` to your instance (Actions → Security → Change security groups).
2. Inbound is now the **union**: 22, 80, ICMP (from web-sg) **plus** 3306 (from db-sg).
> Rules are additive — attaching more groups only **adds** allowed traffic.

---

## 9. ⚠️ Clean up

- You can't delete a security group while it's **attached** to an instance — first change the instance's SGs, **then** delete.
- Security Groups → select `web-sg`/`db-sg` → **Actions → Delete security groups**.
- Terminate the test instance if you're done.

---

## 10. Troubleshooting recap (seen during this lab)

| Symptom | Cause |
|---|---|
| Website times out | No inbound port-80 rule (default deny). |
| SSH times out after working | Source no longer matches your IP (IP changed / wrong source). |
| Ping no reply | ICMP rule missing (it's not a TCP port). |
| Can't delete SG | Still attached to an instance/ENI. |

---

## 11. Recap

- Created `web-sg`, attached it, watched **allow vs deny** live.
- Removing a rule = traffic instantly blocked (default deny proven).
- SSH source must match **your current IP**.
- ICMP/ping needs its own rule.
- **SG references** wire tiers together; **multiple SGs = additive**.
- Next (Note 15): **User Data scripts** — auto-configure an instance at first boot.

---

### Sources
- [Work with security groups – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/working-with-security-groups.html)
- [Add rules to a security group – AWS docs](https://docs.aws.amazon.com/vpc/latest/userguide/security-group-rules.html)
