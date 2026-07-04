# 06 - Customize / Create Your Own AMI (Hands-On)

> Goal: take a base Linux instance, **install software on it**, then **bake it into your own custom AMI**, and finally **launch a new instance from that AMI** to prove the software is already there. This is the real-world pattern behind Auto Scaling and golden images.

---

## 1. The idea (why do this?)

Instead of installing the same software on every new server, you:
1. Set up **one** instance exactly how you want.
2. **Create an AMI** from it.
3. Launch all future instances from that AMI → they come **pre-configured** in seconds.

This is called a **"golden image"**.

---

## 2. Step 1 — Launch a base instance

1. EC2 → **Launch instance**.
2. Name: `ami-source`; AMI: **Amazon Linux 2023**; Type: `t3.micro`.
3. Key pair: reuse `linux-key` (or create one).
4. Security group: allow **SSH (22)** from **My IP**, and **HTTP (80)** from **Anywhere** (so we can test the web server).
5. Launch → wait for **Running + 2/2 checks**.

---

## 3. Step 2 — Connect and customize it

SSH in using your key pair and the instance's public IP (`ssh -i linux-key.pem ec2-user@<PUBLIC_IP>`), then install and configure a web server:

```bash
# Become root-ish with sudo for installs
sudo yum update -y
sudo yum install -y httpd

# Create a custom home page so we can recognize THIS image later
echo "<h1>Hello from my CUSTOM AMI</h1>" | sudo tee /var/www/html/index.html

# Start the web server now AND on every future boot
sudo systemctl enable --now httpd
```

Verify: open `http://<PUBLIC_IP>` in a browser → you should see **"Hello from my CUSTOM AMI"**.

> 🧠 `systemctl enable` makes httpd auto-start on boot — important, because new instances launched from the AMI must start the web server automatically.

---

## 4. Step 3 — Create the AMI

1. EC2 → **Instances** → select `ami-source`.
2. **Actions → Image and templates → Create image**.
3. Fill in:
   - **Image name**: `my-webserver-ami`
   - **Image description**: `Amazon Linux + httpd + custom index page`
   - **No reboot**: leave **unchecked** (default). 🧠 Letting AWS reboot ensures a clean, consistent image. Checking "No reboot" risks an inconsistent filesystem.
4. Click **Create image**.

Watch progress: **EC2 → AMIs** (left menu). Status goes `pending` → `available` (a few minutes). Behind the scenes an **EBS snapshot** is created (visible under **Snapshots**).

---

## 5. Step 4 — Launch a NEW instance from your AMI

1. EC2 → **AMIs** → select `my-webserver-ami` → **Launch instance from image**.
   *(Or: Launch instance wizard → My AMIs tab → pick it.)*
2. Name: `from-custom-ami`; Type: `t3.micro`.
3. Key pair: `linux-key`.
4. Security group: allow **HTTP (80)** from Anywhere (and SSH from My IP if you want to log in).
5. Launch → wait for **Running + 2/2 checks**.

---

## 6. Step 5 — Prove it worked

- Copy the **Public IP** of `from-custom-ami`.
- Open `http://<PUBLIC_IP>` → you should immediately see **"Hello from my CUSTOM AMI"** — **without installing anything**. 🎉
- The web server was baked into the image and auto-started on boot.

---

## 7. (Optional) Copy the AMI to another Region

1. EC2 → **AMIs** → select `my-webserver-ami` → **Actions → Copy AMI**.
2. Choose **Destination Region** (e.g. another Region) → **Copy AMI**.
3. Switch to that Region → the copied AMI appears with a **new AMI ID**, ready to launch there.

> Use case: deploy the same image globally, or build cross-Region disaster recovery.

---

## 8. ⚠️ Clean up (avoid silent charges)

AMIs rely on **snapshots** that keep costing money even after you delete instances. Clean up fully:

1. **Terminate** both instances (`ami-source`, `from-custom-ami`).
2. EC2 → **AMIs** → select `my-webserver-ami` → **Actions → Deregister AMI**.
3. EC2 → **Snapshots** → find the snapshot that belonged to that AMI → **Delete**.

> Order matters: you usually must **deregister the AMI first**, then delete its snapshot.

---

## 9. Troubleshooting

| Symptom | Cause / Fix |
|---|---|
| New instance shows default page, not your page | You edited the file but didn't save it into the image, or launched from the wrong AMI. Re-check. |
| Web page not loading | Security group missing **HTTP 80** rule, or httpd not enabled. Run `sudo systemctl enable --now httpd` in the source before imaging. |
| AMI stuck in `pending` | Just wait — large volumes take longer to snapshot. |
| Charges after deleting instances | Leftover **AMI + snapshot**. Deregister AMI, delete snapshot. |

---

## 10. Recap

- Customize one instance → **Create image** → get a reusable **custom AMI** (a golden image).
- Always `systemctl enable` services so they auto-start in new instances.
- Launch new instances from **My AMIs** → pre-configured instantly.
- **Copy AMI** to use in other Regions.
- Clean up = **terminate instances + deregister AMI + delete snapshots**.
- Next (Note 07): **EC2 Instance Types** — choosing the right hardware size/family.

---

### Sources
- [Create an Amazon EBS-backed AMI – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/creating-an-ami-ebs.html)
- [Copy an AMI – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/CopyingAMIs.html)
- [Deregister your AMI – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/deregister-ami.html)
