# 03 - Create & Connect to a Linux EC2 Instance from Windows 10/11 (Hands-On)

> Goal: launch a **Linux** EC2 instance and connect to it over **SSH** from a **Windows 10 or 11** machine using the **built-in OpenSSH client** (no PuTTY needed). Windows 7/8 users → see Note 04.

---

## 1. Why Linux + SSH?

- Most servers in the cloud run **Linux** (cheaper, lightweight, scriptable).
- You connect with **SSH (Secure Shell)** on **port 22**, using your **private key** (`.pem`) — no password.
- Windows 10/11 ships with the **OpenSSH client**, so the `ssh` command just works in PowerShell/CMD.

---

## 2. Launch the Linux instance

In the EC2 console → **Launch instance**:

1. **Name**: `my-first-linux-server`
2. **AMI**: Quick Start → **Amazon Linux 2023** (Free tier eligible). *(Ubuntu works too — just note the username differs, see step 5.)*
3. **Instance type**: `t3.micro` / `t2.micro` (Free tier).
4. **Key pair**: **Create new key pair**
   - Name: `linux-key`, Type: **RSA**, Format: **`.pem`**
   - Click **Create** → `linux-key.pem` downloads. **Keep it safe.**
5. **Network settings** → Edit:
   - **Auto-assign public IP**: **Enable**
   - **Firewall** → Create security group → allow **SSH (port 22)**, **Source = My IP**.
6. **Storage**: leave default (8 GiB gp3).
7. **Launch instance** → wait for **Running** + **2/2 status checks**.

---

## 3. Find the connection details

1. EC2 → **Instances** → select your instance.
2. Note the **Public IPv4 address** (e.g. `13.234.x.x`) and **Public IPv4 DNS** (e.g. `ec2-13-234-x-x.ap-south-1.compute.amazonaws.com`).
3. Note the **username** based on the AMI (next step).

---

## 4. The default login usernames (memorize!)

| AMI | SSH username |
|---|---|
| Amazon Linux 2 / 2023 | `ec2-user` |
| Ubuntu | `ubuntu` |
| CentOS | `centos` or `ec2-user` |
| Debian | `admin` |
| RHEL | `ec2-user` |
| SUSE | `ec2-user` |

> Wrong username is the #1 reason SSH fails with "Permission denied".

---

## 5. Move your key & fix its permissions

Open **PowerShell** and go to where the key downloaded (usually `Downloads`):

```powershell
cd $HOME\Downloads
```

SSH refuses to use a key file that is readable by other users. Lock the file down to **only your user**:

```powershell
# Remove inherited permissions and grant access only to the current user
icacls "linux-key.pem" /inheritance:r
icacls "linux-key.pem" /grant:r "$($env:USERNAME):R"
```

> 🧠 On Linux/Mac the equivalent is `chmod 400 linux-key.pem`. On Windows we use `icacls`.

---

## 6. Connect with SSH

```powershell
ssh -i "linux-key.pem" ec2-user@<PUBLIC_IP>
```

Example:
```powershell
ssh -i "linux-key.pem" ec2-user@13.234.10.20
```

- First time it asks: `Are you sure you want to continue connecting (yes/no)?` → type **yes**.
- You should land on a prompt like:
  ```
  [ec2-user@ip-172-31-x-x ~]$
  ```
  🎉 You're inside your Linux server.

---

## 7. Try some commands

```bash
whoami                 # ec2-user
cat /etc/os-release    # which Linux + version
sudo yum update -y     # update packages (Amazon Linux). Ubuntu: sudo apt update
df -h                  # disk usage
free -m                # memory
```

Install a web server to prove it works:
```bash
sudo yum install -y httpd
sudo systemctl start httpd
echo "Hello from my EC2 instance" | sudo tee /var/www/html/index.html
```
(To view it in a browser you'd need to add an inbound rule to the instance's security group allowing **HTTP, port 80**, from a source like "Anywhere" or your own IP — the security group blocks all inbound traffic by default until you explicitly allow it.)

To leave the server: type `exit`.

---

## 8. ⚠️ Clean up

EC2 → Instances → select → **Instance state → Terminate** (or **Stop** to resume later).

---

## 9. Troubleshooting

| Symptom | Cause / Fix |
|---|---|
| `Permission denied (publickey)` | Wrong username (use `ec2-user` for Amazon Linux) or wrong key file. |
| `Connection timed out` | Security group port 22 doesn't allow your IP, or no public IP. Edit SG → SSH → My IP. |
| `UNPROTECTED PRIVATE KEY FILE` | Run the `icacls` commands in step 5. |
| Works then breaks next day | Your home IP changed → update the SG SSH rule to your new "My IP". |
| `ssh: command not found` | Enable OpenSSH Client: Settings → Apps → Optional features → Add → OpenSSH Client. |

---

## 10. Recap

- Linux instance + SSH on port 22 + `.pem` key.
- Lock key with `icacls`, connect with `ssh -i key.pem ec2-user@<public-ip>`.
- Username depends on the AMI.
- Next (Note 04): same goal but from **Windows 7/8** using **PuTTY** (older Windows lacks the `ssh` command).

---

### Sources
- [Connect to your Linux instance using SSH – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connect-linux-inst-ssh.html)
- [Get information about your instance for connecting – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connection-prereqs.html)
