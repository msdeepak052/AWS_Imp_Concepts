# 23 - AWS Command Line Interface (CLI) — Hands-On

> Goal: install and configure the **AWS CLI**, then **manage EC2 from the command line** — list, launch, stop, and terminate instances. The CLI is the gateway to **automation and scripting**.

---

## 1. Why the CLI?

The console is great for learning, but the **AWS CLI** lets you:
- **Automate** repetitive tasks and put them in **scripts**.
- Do things **faster** and **reproducibly**.
- Use it in **CI/CD pipelines** and **User Data** scripts.
- Manage **every** AWS service from one tool.

> The CLI calls the same AWS APIs the console uses — anything you can click, you can script.

---

## 2. Install the AWS CLI (v2)

**Windows:**
- Download and run the MSI: <https://awscli.amazonaws.com/AWSCLIV2.msi>
- Verify in PowerShell:
  ```powershell
  aws --version
  # aws-cli/2.x.x Python/3.x Windows/10 ...
  ```

**macOS:** `brew install awscli` (or the official `.pkg`).
**Linux:**
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip && sudo ./aws/install
aws --version
```

> Amazon Linux EC2 instances often have the CLI **pre-installed**.

---

## 3. Create access keys (for your IAM user)

⚠️ **Never use root account keys.** Create an **IAM user** with appropriate permissions first (see the IAM notes).

1. Console → **IAM → Users → (your user) → Security credentials**.
2. **Create access key** → choose **Command Line Interface (CLI)** → Next → **Create**.
3. Copy the **Access key ID** and **Secret access key** (the secret is shown **once** — save it safely).

> 🔒 Treat keys like passwords. Don't commit them to Git. Rotate/delete unused keys. For real automation on EC2, prefer **IAM roles** (no stored keys) over access keys.

---

## 4. Configure the CLI

```powershell
aws configure
```
You'll be prompted for:
```
AWS Access Key ID    : AKIA....................
AWS Secret Access Key: ****************************************
Default region name  : ap-south-1        # your Region
Default output format: json              # json | table | text
```
This writes `~/.aws/credentials` and `~/.aws/config`.

**Test it:**
```powershell
aws sts get-caller-identity
# Shows your account ID + user ARN = you're authenticated
```

> Tip: use **named profiles** for multiple accounts: `aws configure --profile dev`, then add `--profile dev` to commands.

---

## 5. EC2 from the CLI — core commands

### 5.1 List instances (readable table)
```bash
aws ec2 describe-instances \
  --query "Reservations[].Instances[].{ID:InstanceId,State:State.Name,Type:InstanceType,IP:PublicIpAddress}" \
  --output table
```

### 5.2 List available AMIs (Amazon Linux 2023, owned by Amazon)
```bash
aws ec2 describe-images --owners amazon \
  --filters "Name=name,Values=al2023-ami-*-x86_64" "Name=state,Values=available" \
  --query "reverse(sort_by(Images,&CreationDate))[:5].{ID:ImageId,Name:Name}" \
  --output table
```

### 5.3 Launch an instance
```bash
aws ec2 run-instances \
  --image-id ami-xxxxxxxxxxxxxxxxx \
  --instance-type t3.micro \
  --key-name linux-key \
  --security-group-ids sg-xxxxxxxx \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=cli-demo}]' \
  --count 1
```
> Replace `ami-...`, `sg-...`, and `--key-name` with your real values. The output JSON includes the new **InstanceId**.

### 5.4 Stop / Start / Reboot / Terminate
```bash
aws ec2 stop-instances      --instance-ids i-0123456789abcdef0
aws ec2 start-instances     --instance-ids i-0123456789abcdef0
aws ec2 reboot-instances    --instance-ids i-0123456789abcdef0
aws ec2 terminate-instances --instance-ids i-0123456789abcdef0
```

### 5.5 Wait for a state (great in scripts)
```bash
aws ec2 wait instance-running --instance-ids i-0123456789abcdef0
echo "Instance is now running."
```

---

## 6. Handy CLI features

- **`--query`** uses **JMESPath** to filter/shape JSON output (as shown above).
- **`--output`**: `table` (human), `json` (default), `text` (for `grep`/scripts).
- **`--dry-run`** on many EC2 commands checks permissions **without** performing the action.
- **`help`**: `aws ec2 help`, `aws ec2 run-instances help`.
- **`--filters`** to narrow `describe-*` results (e.g. by tag, state).

---

## 7. Mini end-to-end script (launch → wait → show IP → terminate)

```bash
#!/bin/bash
AMI=ami-xxxxxxxxxxxxxxxxx
SG=sg-xxxxxxxx
KEY=linux-key

ID=$(aws ec2 run-instances --image-id $AMI --instance-type t3.micro \
      --key-name $KEY --security-group-ids $SG --count 1 \
      --query "Instances[0].InstanceId" --output text)
echo "Launched $ID"

aws ec2 wait instance-running --instance-ids $ID
IP=$(aws ec2 describe-instances --instance-ids $ID \
      --query "Reservations[0].Instances[0].PublicIpAddress" --output text)
echo "Public IP: $IP"

# ... do work ...

aws ec2 terminate-instances --instance-ids $ID
echo "Terminated $ID"
```

---

## 8. Troubleshooting

| Error | Cause / Fix |
|---|---|
| `Unable to locate credentials` | Run `aws configure` (keys not set). |
| `AccessDenied` / `UnauthorizedOperation` | IAM user lacks the permission for that action. |
| `InvalidAMIID.NotFound` | AMI ID is for a different **Region**; AMIs are Region-specific. |
| `Could not connect to the endpoint URL` | Wrong/typo Region, or no internet. |
| Wrong Region results | CLI uses your **default region** unless you pass `--region`. |

---

## 9. Security best practices

- Use **IAM users with least privilege**, never root.
- On EC2 itself, attach an **IAM role** to the instance instead of storing keys.
- **Rotate** access keys; delete unused ones.
- Never hard-code keys in scripts or commit them to Git; consider **AWS SSO / IAM Identity Center** for human access.

---

## 10. Recap

- AWS CLI v2 = automate/script every AWS service from the terminal.
- Configure with `aws configure` (Access key + Secret + Region + output); verify with `aws sts get-caller-identity`.
- Core EC2: `describe-instances`, `run-instances`, `stop/start/reboot/terminate-instances`, `wait`.
- Use `--query`, `--output`, `--filters`, `--dry-run` to work efficiently.
- Prefer **IAM roles** on EC2; protect access keys.
- 🎉 This completes the EC2 deep-dive (Notes 01–23).

---

### Sources
- [Install or update the AWS CLI – AWS docs](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [Configure the AWS CLI – AWS docs](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
- [Use Amazon EC2 with the AWS CLI – AWS docs](https://docs.aws.amazon.com/cli/latest/userguide/cli-services-ec2.html)
