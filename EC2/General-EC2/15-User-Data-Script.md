# 15 - EC2 User Data Script (Bootstrapping)

> Goal: use **User Data** to automatically run a script the **first time an instance boots**, so a new server configures itself (installs software, starts services) with **zero manual SSH**. Includes a full hands-on.

---

## 1. What is User Data?

**User Data** is a script (or cloud-init directives) you pass to an instance at launch. EC2 runs it **automatically on first boot** as the **root** user. This process is called **bootstrapping**.

- For **Linux**: typically a **bash script** starting with `#!/bin/bash`.
- For **Windows**: a `<powershell>...</powershell>` or `<script>...</script>` block.

> 🧠 **Why it matters:** combined with an AMI and Auto Scaling, User Data lets brand-new servers come up **fully configured and serving traffic** without anyone logging in. This is the heart of automation/elasticity.

---

## 2. Key rules (memorize)

- Runs **once**, on the **first boot**, as **root** (no `sudo` needed).
- Runs **before** the instance is fully "ready" — there's no logged-in user yet.
- **Size limit: 16 KB** (raw). For bigger setups, have User Data download a larger script from S3 and run it.
- You can **view/edit** User Data only when the instance is **stopped** (Actions → Instance settings → Edit user data). Editing it does **not** re-run it on a normal start — by default it executes only on the very first boot.
- Logs (Linux): `/var/log/cloud-init-output.log` — your go-to for debugging.

---

## 3. AMI + User Data: division of labor

| Approach | What it's good for |
|---|---|
| **Bake into AMI** (an AMI is a saved snapshot/image of a fully configured instance's disk that you can launch new instances from) | Heavy/slow installs done once → fast boot, consistent. |
| **User Data at launch** | Last-mile config, per-environment values, things that change often. |
| **Both (common)** | Golden AMI for the base + small User Data for environment-specific tweaks. |

---

## 4. Hands-On — auto-install a web server with User Data

**Step 1 — Launch with User Data:**
1. EC2 → **Launch instance**.
2. Name `userdata-demo`; AMI **Amazon Linux 2023**; Type `t3.micro`; key pair as usual.
3. Security group: allow **HTTP 80** from Anywhere, **SSH 22** from My IP.
4. Expand **Advanced details** (bottom) → scroll to **User data** box → paste:

```bash
#!/bin/bash
# Update packages
dnf update -y
# Install Apache web server
dnf install -y httpd
# Start now and enable on every boot
systemctl enable --now httpd
# Create a home page that shows THIS instance's ID (via Instance Metadata Service v2)
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 300")
INSTANCE_ID=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/instance-id)
echo "<h1>Hello from User Data</h1><p>Instance: $INSTANCE_ID</p>" > /var/www/html/index.html
```

5. **Launch instance** → wait for **Running + 2/2 checks** (give User Data ~1–2 min to finish).

**Step 2 — Verify:**
- Browser → `http://<PUBLIC_IP>` → you should see **"Hello from User Data"** and the **instance ID**, with **no manual setup**. 🎉

**Step 3 — Debug if needed:**
```bash
ssh -i linux-key.pem ec2-user@<PUBLIC_IP>
sudo cat /var/log/cloud-init-output.log   # see exactly what your script did/failed
```

---

## 5. Windows User Data example

```powershell
<powershell>
# Install IIS web server
Install-WindowsFeature -name Web-Server -IncludeManagementTools
"<h1>Hello from Windows User Data</h1>" | Out-File C:\inetpub\wwwroot\index.html -Encoding utf8
</powershell>
```
- `<powershell>` runs once on first boot. Add `<persist>true</persist>` to run on every boot if needed.

---

## 6. Tips & gotchas

- **Start with `#!/bin/bash`** (Linux) or it won't be treated as a script.
- It runs as **root** → don't add `sudo` (harmless but unnecessary).
- If the script fails halfway, the instance still boots — check `cloud-init-output.log`.
- For long scripts, store the real script in **S3** and have User Data download + execute it (keeps you under 16 KB and lets you update centrally).
- The metadata endpoint `169.254.169.254` (**Instance Metadata Service / IMDS**) is how an instance learns about itself (instance ID, IP, IAM role creds). Prefer **IMDSv2** (token-based, as shown) for security.
- User Data is visible to anyone who can describe the instance — **never put secrets/passwords** in it. Use **Secrets Manager / SSM Parameter Store** instead.

---

## 7. Where User Data fits in the big picture

```
Launch Template (AMI + instance type + User Data)
        │
        ▼
 Auto Scaling Group  → launches N identical, self-configuring instances
        │
        ▼
 Behind a Load Balancer → instantly serving traffic, no human touch
```

---

## 8. Recap

- **User Data** = startup script run **once on first boot as root** = **bootstrapping**.
- Linux: `#!/bin/bash …`; Windows: `<powershell>…</powershell>`.
- **16 KB** limit; debug via `/var/log/cloud-init-output.log`.
- **No secrets** in User Data; use Secrets Manager/SSM.
- Combine **golden AMI + User Data + Auto Scaling** for hands-off elastic fleets.
- Next (Note 16): **Termination Protection** — preventing accidental instance deletion.

---

### Sources
- [Run commands at launch (user data) – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html)
- [Instance metadata and user data (IMDS) – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html)
- [Run commands on your Windows instance at launch – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/ec2-windows-user-data.html)
