# 02 - Create a Windows EC2 Instance (Hands-On)

> Goal: launch your **first EC2 instance** running **Windows Server**, then connect to its desktop using **RDP (Remote Desktop)**. Every step is explained so a complete beginner can follow.

---

## 0. Before you start (prerequisites)

1. An **AWS account** (sign up at <https://aws.amazon.com> — needs a credit/debit card; small instances are Free-Tier eligible).
2. Sign in to the **AWS Management Console**: <https://console.aws.amazon.com>.
3. On your local computer you need a **Remote Desktop client**:
   - **Windows 10/11** → "Remote Desktop Connection" (`mstsc`) is built in.
   - **Mac** → install "Windows App" / "Microsoft Remote Desktop" from the App Store.

---

## 1. Pick your Region

- Top-right of the console shows the current **Region** (e.g. "N. Virginia").
- Choose a Region close to you (e.g. **Asia Pacific (Mumbai) ap-south-1** for India).
- 🧠 Why it matters: instances, key pairs, and security groups are **Region-specific**. If you can't find your instance later, you're probably looking in the wrong Region.

---

## 2. Open the EC2 console and launch

1. In the top search bar, type **EC2** → click **EC2**.
2. On the EC2 Dashboard, click the orange **Launch instance** button.

You now see the **Launch an instance** wizard. We'll go section by section.

---

## 3. Name and tags

- **Name**: type something like `my-first-windows-server`.
- This just creates a tag `Name = my-first-windows-server` so you can identify it. (Tags = key/value labels.)

---

## 4. Application and OS Image (AMI)

- Under **Quick Start**, click the **Windows** tab.
- Choose **Microsoft Windows Server 2022 Base** (or the latest 2025 Base if shown).
- Make sure it says **Free tier eligible** if you want to stay free.
- 🧠 The AMI is the template that installs the OS for you. (More in Note 05.)

---

## 5. Instance type

- Select **`t3.micro`** (or **`t2.micro`**) — marked **Free tier eligible**.
- This gives ~2 vCPU and 1 GiB RAM — enough to log in and explore.

---

## 6. Key pair (login) — IMPORTANT for Windows password

A **key pair** secures your login. For Windows, AWS uses the **private key to decrypt the Administrator password** later.

1. Click **Create new key pair**.
2. **Name**: `windows-key`.
3. **Key pair type**: **RSA**.
4. **Private key file format**: **`.pem`** (works everywhere) — choose `.ppk` only if you use PuTTY.
5. Click **Create key pair** → a file `windows-key.pem` **downloads automatically**.

> ⚠️ **Save this `.pem` file safely.** AWS does NOT keep a copy. Without it you cannot retrieve the Windows password.

---

## 7. Network settings (firewall / Security Group)

Click **Edit** on the Network settings box.

- **VPC** / **Subnet**: leave defaults (the default VPC) for now.
- **Auto-assign public IP**: **Enable** (so you can reach it from the internet).
- **Firewall (security group)**: choose **Create security group**.
  - It will auto-add a rule. For Windows we need **RDP (port 3389)**:
    - **Type**: RDP
    - **Source type**: **My IP** ✅ (this restricts access to *your* current IP only — much safer than "Anywhere").

> ⚠️ Never leave RDP (3389) open to `0.0.0.0/0` (Anywhere) in real life — bots constantly scan for it. "My IP" is the safe beginner choice. (Security groups are covered in depth in Notes 11–14.)

---

## 8. Configure storage

- Default is usually **30 GiB gp3** (or gp2) root volume for Windows — leave as is.
- This is the C: drive of your Windows server.

---

## 9. Launch

1. Review the **Summary** panel on the right.
2. Click **Launch instance**.
3. You'll see "Success". Click the instance ID link, or click **View all instances**.

Wait until:
- **Instance state** = `Running`
- **Status checks** = `2/2 checks passed` (takes a few minutes)

---

## 10. Get the Windows Administrator password

Windows isn't accessed with the key directly — you use the key to **decrypt the auto-generated Administrator password**.

1. Select your instance → click **Connect** (top).
2. Open the **RDP client** tab.
3. Click **Get password**.
4. Click **Upload private key file** → select your `windows-key.pem`.
5. Click **Decrypt password**.
6. You now see:
   - **Public DNS / Public IP** (the address to connect to)
   - **Username**: `Administrator`
   - **Password**: (the decrypted password) — copy it.
7. Also click **Download remote desktop file** (a `.rdp` file).

---

## 11. Connect with Remote Desktop

**On Windows 10/11:**
1. Double-click the downloaded `.rdp` file (or open **Remote Desktop Connection** and paste the **Public IP**).
2. Username: `Administrator`, Password: (paste the decrypted password).
3. Accept the certificate warning → you'll see the **Windows Server desktop**. 🎉

**On Mac:** open Microsoft Remote Desktop → Add PC → enter the Public IP → connect with `Administrator` + password.

---

## 12. You're in — try something

- Open **Server Manager** (opens automatically).
- Open a browser / PowerShell.
- This is a real Windows server running in AWS!

---

## 13. ⚠️ Clean up to avoid charges

When done practicing:
1. EC2 → **Instances** → select your instance.
2. **Instance state** → **Stop instance** → keeps it (you pay only for the 30 GB disk), OR
3. **Instance state** → **Terminate instance** → deletes it permanently (no more charges).

> For learning, **Terminate** if you don't need it again. **Stop** if you'll come back tomorrow.

---

## 14. Common beginner problems

| Problem | Likely cause / fix |
|---|---|
| Can't connect via RDP | Security group RDP rule doesn't include your current IP (your IP changed). Edit the rule → set Source = My IP again. |
| "Get password" not ready | Wait — password is available only a few minutes after launch, after status checks pass. |
| Lost the `.pem` file | You cannot decrypt the password. You'd have to create a new instance (or use EC2 Rescue). Keep keys safe! |
| Can't find the instance | Wrong **Region** selected (top-right). |
| Connection very slow | `t3.micro` is small; fine for learning, not for heavy use. |

---

## 15. Recap

- Launch wizard = Name → AMI (Windows) → Instance type → **Key pair** → Network/Security group (RDP from **My IP**) → Storage → Launch.
- Windows login = decrypt **Administrator password** with your `.pem` key, then RDP to the **Public IP**.
- Always **Stop or Terminate** when finished to control cost.
- Next: connect to a **Linux** instance from a Windows machine (Note 03).

---

### Sources
- [Get started with Amazon EC2 – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html)
- [Connect to your Windows instance – AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/connecting_to_windows_instance.html)
