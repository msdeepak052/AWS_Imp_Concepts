# 04 - Connect to a Linux EC2 Instance from Windows 7 & 8 using PuTTY (Hands-On)

> Goal: connect to a **Linux** EC2 instance from **older Windows (7 / 8 / 8.1)** that does **not** include the built-in `ssh` command. We use **PuTTY**. The trick: PuTTY can't read AWS's `.pem` file directly — we convert it to `.ppk` first using **PuTTYgen**.

> Already on Windows 10/11? Use Note 03 instead (simpler — no PuTTY needed).

---

## 1. Why PuTTY?

- Windows 7/8 has **no OpenSSH client**, so you can't run `ssh -i key.pem ...`.
- **PuTTY** is a free SSH client for Windows.
- PuTTY uses its own key format **`.ppk`**, not AWS's **`.pem`**, so we convert with **PuTTYgen** (ships with PuTTY).

---

## 2. Launch a Linux instance (quick recap of the launch steps)

1. EC2 → **Launch instance**.
2. Name: `linux-putty-demo`; AMI: **Amazon Linux 2023**; Type: `t3.micro`.
3. **Key pair** → Create new → `linux-key` → RSA → **.pem** → download `linux-key.pem`.
4. Network → **Enable** public IP; Security group → allow **SSH (22)**, Source **My IP**.
5. Launch → wait for **Running + 2/2 checks**.
6. Copy the **Public IPv4 address**. Username will be **`ec2-user`** (Amazon Linux).

---

## 3. Install PuTTY

- Download the installer from <https://www.putty.org> (the MSI gives you **PuTTY** + **PuTTYgen** + **Pageant**).
- Install with defaults.

---

## 4. Convert `.pem` → `.ppk` with PuTTYgen

1. Open **PuTTYgen** (Start menu).
2. Top menu: **Conversions → Import key**.
3. Select your `linux-key.pem`.
4. (Optional) add a passphrase for extra security, or leave blank.
5. Click **Save private key** → save as `linux-key.ppk`.

> 🧠 You only do this once per key. From now on use the `.ppk` in PuTTY.

---

## 5. Configure PuTTY to connect

1. Open **PuTTY**.
2. **Session** category (left):
   - **Host Name**: `ec2-user@<PUBLIC_IP>`  (e.g. `ec2-user@13.234.10.20`)
   - **Port**: `22`
   - **Connection type**: SSH
3. Left tree → **Connection → SSH → Auth → Credentials** (older PuTTY: **Connection → SSH → Auth**):
   - **Private key file for authentication** → **Browse** → select `linux-key.ppk`.
4. (Recommended) go back to **Session**, type a name under **Saved Sessions** (e.g. `my-linux`) → **Save**, so you can reload it next time.
5. Click **Open**.

---

## 6. First connection

- A security alert about the host key appears the first time → click **Accept**.
- You should see the Linux shell prompt:
  ```
  [ec2-user@ip-172-31-x-x ~]$
  ```
  🎉 Connected via PuTTY.

If you didn't put `ec2-user@` in the Host Name, PuTTY will ask **"login as:"** → type `ec2-user`.

---

## 7. Try commands

```bash
whoami
sudo yum update -y
cat /etc/os-release
```

To disconnect: type `exit` or just close the window.

---

## 8. (Optional) Pageant — avoid re-selecting the key

**Pageant** is PuTTY's key agent that holds your `.ppk` in memory:
1. Open **Pageant** (runs in the system tray).
2. **Add Key** → select `linux-key.ppk`.
3. Now PuTTY sessions authenticate automatically (no need to point to the key each time).

---

## 9. Troubleshooting

| Symptom | Cause / Fix |
|---|---|
| `Server refused our key` | You pointed PuTTY at the `.pem` instead of `.ppk`, or wrong key. Use the converted `.ppk`. |
| `Network error: Connection timed out` | Security group port 22 doesn't allow your IP / no public IP. Fix SG → SSH → My IP. |
| `Access denied` / wrong login | Use the right username (`ec2-user` for Amazon Linux, `ubuntu` for Ubuntu). |
| PuTTYgen won't import | Make sure you chose **Conversions → Import key**, not "Load" of a `.ppk`. |
| Key works then fails next day | Home IP changed → update SG SSH rule. |

---

## 10. `.pem` vs `.ppk` — remember this

| | `.pem` | `.ppk` |
|---|---|---|
| Made by | AWS (download at launch) | PuTTYgen (you convert) |
| Used by | OpenSSH (`ssh` on Win10/Mac/Linux) | PuTTY (Windows) |
| Conversion | — | `pem → ppk` via PuTTYgen |

---

## 11. Recap

- Old Windows → no `ssh` command → use **PuTTY**.
- Convert `.pem` to `.ppk` with **PuTTYgen** (Conversions → Import key → Save private key).
- Connect: Host `ec2-user@public-ip`, port 22, key = `.ppk`.
- Next (Note 05): **Amazon Machine Images (AMI)** — the templates behind every instance.

---

### Sources
- [Connect to your Linux instance from Windows using PuTTY – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html)
- [PuTTY download](https://www.putty.org/)
