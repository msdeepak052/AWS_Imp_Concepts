#  IAM Root User Best Practices Multi Factor Authentication (MFA)

 **AWS root user** is the most powerful entity in your AWS account — it has **full unrestricted access** to all AWS resources. Because of this, AWS **strongly recommends minimizing its use** and securing it properly.

Let’s focus on **best practices** for the **root user**, especially around **Multi-Factor Authentication (MFA)**.

---

## 🔐 What is the AWS Root User?

* The **root user** is created when you first open an AWS account.
* It is associated with the **email address and password** you used to create the account.
* It has **complete control** over all AWS resources and billing information.

---

## ✅ Root User Best Practices (with a focus on MFA)

| 🔒 Practice                                   | ✅ Description                                                                               |
| --------------------------------------------- | ------------------------------------------------------------------------------------------- |
| **1. Enable MFA**                             | Enforce **hardware or virtual MFA** on the root user for added security.                    |
| **2. Do NOT use root user for daily tasks**   | Create an **admin IAM user** and use that instead.                                          |
| **3. Use strong, unique password**            | Use a **long complex password** not shared with any other service.                          |
| **4. Store credentials securely**             | Keep root email and recovery options secure. Use a **password manager**.                    |
| **5. Don’t create access keys for root user** | If already created, **delete them immediately**. Use IAM roles/users instead.               |
| **6. Use AWS Organizations for control**      | Manage permissions via **Service Control Policies (SCP)**, not root user access.            |
| **7. Monitor root user activity**             | Enable **AWS CloudTrail** and set alerts for any root activity using **CloudWatch alarms**. |

---

## ✅ Enable MFA for Root User (Step-by-Step)

### 🔹 Step 1: Sign In as Root

* Go to: [https://aws.amazon.com/console/](https://aws.amazon.com/console/)
* Use **email address and password** (not IAM user)

### 🔹 Step 2: Go to IAM Dashboard

* Search for **IAM** in the AWS Console
* Click **Dashboard**

### 🔹 Step 3: Enable MFA

1. In **Security Status** → Find **“Activate MFA on your root account”**
2. Click **“Activate MFA”**
3. Choose **MFA type**:

   * ✅ **Virtual MFA device** (e.g., Google Authenticator, Authy, 1Password)
   * 🔐 **Hardware MFA device** (like a YubiKey)
4. Follow prompts to scan QR code and enter two OTPs

✅ Once complete, your root account is protected with **MFA**.

---

## 🚨 Important: Never Create Access Keys for Root User

* AWS root **access keys allow full programmatic access**, making them highly dangerous.
* If created, delete them:

  * Go to IAM → Security credentials (root account) → Access keys → Delete

---

## 🔍 Monitor Root Usage

Use **AWS CloudTrail** to detect root user actions:

### Example: CloudTrail Event for Root Sign-in

```json
{
  "eventName": "ConsoleLogin",
  "userIdentity": {
    "type": "Root",
    "principalId": "123456789012"
  },
  ...
}
```

### Set CloudWatch Alarm:

* Filter: `userIdentity.type = "Root"`
* Action: Send email via SNS for any root activity

---

## 🚫 What Root User Should Be Used For Only:

| Task                                                            | Reason              |
| --------------------------------------------------------------- | ------------------- |
| Change AWS support plan                                         | Only root can do it |
| Close AWS account                                               | Root-only           |
| Manage some billing info                                        | e.g., tax settings  |
| Activate IAM access to billing console                          | Initial setup       |
| Enable/Disable AWS services like Organizations or Control Tower | Root-only           |

![image](https://github.com/user-attachments/assets/c9ba2589-5481-4cd7-923b-103c9f04c09d)


---

## 🧠 Summary: Secure Root with MFA

| 🔐 Feature              | Status                  |
| ----------------------- | ----------------------- |
| Strong password         | ✅ Required              |
| MFA enabled             | ✅ Strongly recommended  |
| Access keys deleted     | ✅ Best practice         |
| CloudTrail monitored    | ✅ Essential             |
| IAM used for daily work | ✅ Yes, avoid using root |

---
### Here's a **Terraform example** that sets up **CloudTrail + CloudWatch Logs + Alarm + SNS Notification** to alert you **whenever the AWS Root user performs any action** (e.g., login, API call).

---

## ✅ What We’ll Deploy

| Resource                                       | Purpose                         |
| ---------------------------------------------- | ------------------------------- |
| `aws_cloudtrail`                               | Tracks all AWS account activity |
| `aws_cloudwatch_log_group`                     | Stores CloudTrail logs          |
| `aws_cloudwatch_metric_filter`                 | Looks for root user usage       |
| `aws_cloudwatch_alarm`                         | Triggers on root activity       |
| `aws_sns_topic` + `aws_sns_topic_subscription` | Sends email alert               |

---

## 📦 Terraform Structure

```hcl
provider "aws" {
  region = "us-east-1"
}

# 🔔 SNS Topic
resource "aws_sns_topic" "root_activity_alert" {
  name = "root-activity-alert-topic"
}

# 📧 Email Subscription
resource "aws_sns_topic_subscription" "email_alert" {
  topic_arn = aws_sns_topic.root_activity_alert.arn
  protocol  = "email"
  endpoint  = "your-email@example.com" # Replace with your email
}

# 📂 CloudWatch Log Group for CloudTrail
resource "aws_cloudwatch_log_group" "trail_log_group" {
  name              = "/aws/cloudtrail/root-alerts"
  retention_in_days = 30
}

# 🕵️ CloudTrail Logging
resource "aws_cloudtrail" "root_trail" {
  name                          = "root-activity-trail"
  s3_bucket_name                = aws_s3_bucket.trail_bucket.id
  cloud_watch_logs_group_arn    = "${aws_cloudwatch_log_group.trail_log_group.arn}:*"
  cloud_watch_logs_role_arn     = aws_iam_role.trail_role.arn
  include_global_service_events = true
  is_multi_region_trail         = true
  enable_logging                = true
}

# 🪣 S3 Bucket for CloudTrail logs
resource "aws_s3_bucket" "trail_bucket" {
  bucket = "my-cloudtrail-logs-${random_id.bucket_suffix.hex}"

  lifecycle {
    prevent_destroy = true
  }
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# 🔐 IAM Role for CloudTrail to write logs
resource "aws_iam_role" "trail_role" {
  name = "cloudtrail-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "cloudtrail.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "trail_policy" {
  name = "cloudtrail-logs"
  role = aws_iam_role.trail_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "${aws_cloudwatch_log_group.trail_log_group.arn}:*"
      }
    ]
  })
}

# 🧠 Metric Filter to detect Root usage
resource "aws_cloudwatch_log_metric_filter" "root_activity_filter" {
  name           = "root-user-activity"
  log_group_name = aws_cloudwatch_log_group.trail_log_group.name

  pattern = "{ $.userIdentity.type = \"Root\" }"

  metric_transformation {
    name      = "RootUsageMetric"
    namespace = "RootUsage"
    value     = "1"
  }
}

# 🔔 Alarm for Root activity
resource "aws_cloudwatch_metric_alarm" "root_activity_alarm" {
  alarm_name                = "RootUserActivityAlarm"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = 1
  metric_name               = "RootUsageMetric"
  namespace                 = "RootUsage"
  period                    = 300
  statistic                 = "Sum"
  threshold                 = 1
  alarm_description         = "Triggers when root user is used"
  alarm_actions             = [aws_sns_topic.root_activity_alert.arn]
  treat_missing_data        = "notBreaching"
}
```

---

## 📧 After Terraform Apply

* You will receive a **confirmation email** to the address you used in `aws_sns_topic_subscription`.
* Once you **confirm**, the SNS will be active.
* Any **root login or API call** will trigger the alarm and send you an alert.

---
# **IAM Credential Reports**
---

## 🔍 What is an **IAM Credential Report**?

The **IAM Credential Report** is a downloadable `.csv` file provided by AWS that shows the **age, status, and usage of credentials** (passwords, access keys, MFA) for **all IAM users in your account**.

It helps you **audit security best practices** and identify users who:

* Have old or unused passwords or access keys
* Lack MFA
* Haven't rotated keys recently
* Have enabled credentials that are unused

---

## 📄 What Does the Credential Report Contain?

It contains **one row per IAM user**, and includes the following key columns:

| Column                             | Description                                      |
| ---------------------------------- | ------------------------------------------------ |
| `user`                             | IAM username                                     |
| `arn`                              | Full ARN of the user                             |
| `user_creation_time`               | When the user was created                        |
| `password_enabled`                 | `true` if console login is enabled               |
| `password_last_used`               | Last time password was used                      |
| `password_last_changed`            | When password was last changed                   |
| `password_next_rotation`           | When it must be rotated (if rotation is enabled) |
| `mfa_active`                       | `true` if MFA is enabled                         |
| `access_key_1_active` / `2_active` | `true` if access key is enabled                  |
| `access_key_1_last_used_date`      | Last use of access key                           |
| `cert_1_active`                    | For X.509 certs (legacy, rarely used now)        |

---

## ✅ Use Cases

| 🔐 Scenario                                     | 📈 Value                |
| ----------------------------------------------- | ----------------------- |
| Identify users with stale or unused credentials | Clean up access         |
| Enforce password or key rotation policies       | Improve compliance      |
| Spot users without MFA                          | Enforce MFA as baseline |
| Audit unused accounts                           | Remove or deactivate    |
| Prepare for security assessments or reviews     | Compliance-ready data   |

---

## 🛠️ How to Generate IAM Credential Report (AWS Console)

### 🔹 Step-by-Step

1. **Sign in to AWS Console** as admin/root
2. Go to **IAM → Access reports → Credential report**
3. Click: **“Download Report (CSV)”**

   * If not yet generated, AWS will create one within seconds
4. Open the CSV using Excel, Google Sheets, or CLI tools

---

## 💡 Example Analysis

| user     | password\_enabled | mfa\_active | access\_key\_1\_active | access\_key\_1\_last\_used\_date |
| -------- | ----------------- | ----------- | ---------------------- | -------------------------------- |
| devops   | true              | false       | true                   | 2024-12-01                       |
| auditor  | false             | true        | false                  | N/A                              |
| testuser | true              | false       | true                   | never                            |

🛡️ What we can conclude:

* `devops` needs MFA enabled.
* `testuser`'s access key is stale → disable or delete.
* `auditor` has read-only setup with MFA – good!

---

## 📦 Generate IAM Credential Report via CLI

### 📌 Generate Report

```bash
aws iam generate-credential-report
```

### 📥 Download Report

```bash
aws iam get-credential-report --query 'Content' --output text | base64 --decode > credential-report.csv
```

Then open `credential-report.csv` in your editor.

---

## ✅ Best Practices for IAM Credential Report Usage

| Best Practice                                        | Why                   |
| ---------------------------------------------------- | --------------------- |
| ⏳ Automate report download & audit weekly            | Maintain compliance   |
| 🔐 Disable unused credentials                        | Reduce attack surface |
| 🔁 Rotate access keys regularly (<=90 days)          | Enforce good hygiene  |
| 🚫 Avoid root user access keys                       | Disable if created    |
| 📊 Use Athena or QuickSight for report visualization | Enhance insight       |

---

# **IAM Access Advisor Reports** (part of **IAM Reports**) 
---

## 📘 What Are IAM Access Advisor Reports?

**Access Advisor Reports** help you **analyze which AWS services your IAM users or roles actually use**, and when they last accessed them.

This allows you to:

* Identify **over-provisioned permissions**
* Clean up **unused access**
* Move toward **least-privilege access model**

---

## 🧠 Access Advisor vs Credential Reports

| Report Type        | Focus                              |
| ------------------ | ---------------------------------- |
| Credential Report  | Credential usage (keys, MFA, etc.) |
| **Access Advisor** | **Service-level access history**   |

---

## ✅ Use Cases for IAM Access Advisor

| 🔍 Goal                              | 💡 Value                                 |
| ------------------------------------ | ---------------------------------------- |
| Reduce over-permissioned IAM roles   | Know which services are *not being used* |
| Audit last accessed services         | Check stale/unused permissions           |
| Enforce least privilege              | Only allow what’s actually needed        |
| Role or user permission right-sizing | Clean up policies over time              |
| Compliance & risk reduction          | Reduce blast radius of access            |

---

## 🛠️ How to Use IAM Access Advisor Report (AWS Console)

### 🔹 Step-by-Step for IAM **Users**

1. Go to **IAM → Users**
2. Select a specific **IAM User**
3. Click the **“Access Advisor”** tab
4. You'll see:

   * **Service name**
   * **Last accessed time**
   * **Status: Accessed or Not accessed**

> 🔎 This shows which AWS services this user *has permission to use*, and when (or if) they actually used them.

---

### 🔹 Step-by-Step for IAM **Roles**

1. Go to **IAM → Roles**
2. Select a specific **IAM Role**
3. Click **Access Advisor**
4. Same report is shown: which services were accessed and when

---

## 📊 Report Output Example

| Service    | Last Accessed Time | Accessed |
| ---------- | ------------------ | -------- |
| Amazon S3  | 2025-06-22         | ✅ Yes    |
| Amazon EC2 | None               | ❌ No     |
| IAM        | 2025-06-18         | ✅ Yes    |
| CloudTrail | None               | ❌ No     |

💡 You could then remove EC2 and CloudTrail access if it's not needed.

---

## ⚙️ Filtering or Exporting Reports?

While **not directly downloadable via Console**, you can:

* Use **AWS CLI** to get similar data (see below)
* Use **Access Analyzer + CloudTrail** for deeper analysis

---

## 📦 Access Advisor via AWS CLI (Per User or Role)

```bash
aws iam generate-service-last-accessed-details \
  --arn arn:aws:iam::123456789012:user/Deepak
```

Then fetch the details:

```bash
aws iam get-service-last-accessed-details \
  --job-id <job-id-from-previous-command>
```

Output includes:

* **Services last accessed**
* **Last authenticated time**
* **Actions allowed in each service**

---

## 🧰 Example: Use Case in DevOps

### 🎯 Scenario: You have a role `EKSAdminRole` with full access to EC2, IAM, EKS, S3

Access Advisor shows:

| Service | Last Accessed |
| ------- | ------------- |
| EC2     | 2025-07-01    |
| S3      | Never         |
| IAM     | 2025-06-29    |
| EKS     | 2025-07-01    |

✅ **Action**: Remove `s3:*` permissions from this role — it’s not needed.

---

## 🔐 Best Practices Using Access Advisor

| Practice                                                  | Why                              |
| --------------------------------------------------------- | -------------------------------- |
| Review Access Advisor monthly                             | Keep permissions clean           |
| Pair with CloudTrail logs                                 | Confirm usage patterns           |
| Combine with `aws:LastUsed` condition in policies         | Enforce conditional access       |
| Use with custom scripts or tools like PMapper/CloudMapper | Deeper analysis                  |
| Always test before removing permissions                   | Avoid breaking apps or pipelines |

---
# **IAM Access Analyzer**

---

## 🔍 What is **IAM Access Analyzer**?

**IAM Access Analyzer** helps you **identify resources in your AWS account that are shared externally** (outside your AWS Organization or account).

🔐 It answers questions like:

* "Is this S3 bucket shared with the public?"
* "Is this role assumed by another AWS account?"
* "Is this KMS key shared with external users?"

![image](https://github.com/user-attachments/assets/bd3f7c09-d676-4f56-b7f8-d8123ceea3bd)


---

## 📦 What Can Access Analyzer Analyze?

IAM Access Analyzer reviews **resource-based policies** for the following:

| AWS Resource Type                              | Examples                              |
| ---------------------------------------------- | ------------------------------------- |
| **S3 buckets**                                 | Public buckets, cross-account buckets |
| **IAM roles**                                  | Roles that trust external principals  |
| **KMS keys**                                   | Keys accessible from other accounts   |
| **Lambda functions**                           | Cross-account function access         |
| **SQS queues / SNS topics**                    | Externally accessible queues/topics   |
| **Secrets Manager secrets**                    | With cross-account access policies    |
| **EFS file systems**, **Glue resources**, etc. |                                       |

---

## 🛠️ How It Works

IAM Access Analyzer:

1. **Creates an analyzer** scoped to your AWS account or AWS Organization.
2. **Continuously monitors** supported resources.
3. **Finds findings** where access is allowed to external entities.
4. Allows you to **archive or remediate** findings.

---

## 🧠 Why It Matters (Use Cases)

| Use Case                    | Description                                          |
| --------------------------- | ---------------------------------------------------- |
| 🔍 Detect public access     | Find misconfigured S3 buckets, IAM roles             |
| 🛡️ Enforce least privilege | Verify no resource is shared unless intended         |
| 🧾 Prove compliance         | Show external access is restricted                   |
| 🔄 Automation               | Trigger alerts or remediation via EventBridge/Lambda |

---

## 🛠️ How to Use IAM Access Analyzer (AWS Console)

### 🔹 Step-by-Step: Creating an Analyzer

1. Open **IAM** in AWS Console
2. On left menu, click **“Access Analyzer”**
3. Click **“Create Analyzer”**
4. Choose:

   * **Zone of trust**: `Your AWS Account` or `AWS Organization`
   * **Analyzer name**: e.g., `prod-analyzer`
   * (Optional) Choose **Tags**
5. Click **Create Analyzer**

✅ Done! Access Analyzer will now scan your account for external sharing.

---

### 🔎 Viewing Findings

* Go to **IAM → Access Analyzer → Findings**
* You’ll see a list of all findings:

  * **Resource** (e.g., S3 bucket)
  * **Finding Type**: External access detected
  * **Status**: Active / Archived
  * **Condition**: e.g., Principal `*` has `s3:GetObject`

You can **click on each finding** to:

* View the JSON policy
* Download it
* Archive the finding (if it's known/allowed)
* Remediate the policy from the same screen

---

## 📊 Example: S3 Bucket Exposed

### Detected Finding:

```json
{
  "resourceType": "AWS::S3::Bucket",
  "resource": "arn:aws:s3:::deepak-public-data",
  "principal": "*",
  "action": "s3:GetObject",
  "effect": "Allow"
}
```

🛡️ What it means: **Anyone on the internet** can access this bucket.

✅ Fix: Update bucket policy to limit to a specific IAM principal or remove the `Allow` for `"Principal": "*"`.

---

## 📈 Archive a Finding

Use **Archive** if access is intentional (e.g., sharing with another AWS account).

* Select finding → Click **“Archive”**
* You can **filter out archived findings** later

---

## 🚨 EventBridge Integration (Automation)

Access Analyzer integrates with **Amazon EventBridge**, so you can:

* Send finding notifications to **SNS**, **Slack**, or **email**
* Trigger **Lambda functions** to auto-remediate risky policies

Example EventBridge rule filter:

```json
{
  "source": ["aws.access-analyzer"],
  "detail-type": ["Access Analyzer Finding"]
}
```

---

## ✅ Using Access Analyzer via AWS CLI

### Create Analyzer

```bash
aws accessanalyzer create-analyzer \
  --analyzer-name my-analyzer \
  --type ACCOUNT
```

### List Findings

```bash
aws accessanalyzer list-findings \
  --analyzer-name my-analyzer
```

### Archive Finding

```bash
aws accessanalyzer archive-findings \
  --analyzer-name my-analyzer \
  --ids <finding-id>
```

---

## 🚦 Access Analyzer Modes (Scope Types)

| Mode                      | Description                                             |
| ------------------------- | ------------------------------------------------------- |
| `ACCOUNT`                 | Analyze sharing outside **this AWS account**            |
| `ORGANIZATION`            | Analyze sharing outside **your AWS Org**                |
| `SERVICE_ACCESS_ANALYZER` | Detect unused permissions in policies (new mode in IAM) |

---

## 🔐 Access Analyzer vs IAM Policy Simulator

| Feature        | Access Analyzer         | Policy Simulator             |
| -------------- | ----------------------- | ---------------------------- |
| Purpose        | Detect external access  | Evaluate policies for access |
| Scope          | Resource-based policies | All IAM policies             |
| Real-time scan | ✅ Yes                   | ❌ No                         |
| Automation     | ✅ Yes (EventBridge)     | ❌ Manual                     |

---

## 🧠 Best Practices

| Practice                                         | Why                                    |
| ------------------------------------------------ | -------------------------------------- |
| Enable analyzer per region                       | It’s regional — cover all used regions |
| Use org-wide analyzer if using AWS Organizations | Broader visibility                     |
| Automate finding notifications                   | Don’t miss misconfigurations           |
| Archive only after review                        | Avoid ignoring real threats            |
| Integrate with IAM review processes              | For consistent compliance              |

---

## ✅ Summary

| Feature                        | IAM Access Analyzer          |
| ------------------------------ | ---------------------------- |
| Detects external access        | ✅ Yes                        |
| Real-time analysis             | ✅ Yes                        |
| Integrated with IAM            | ✅ Yes                        |
| Supports multiple AWS services | ✅ S3, IAM, KMS, Lambda, etc. |
| Automation via EventBridge     | ✅ Yes                        |
| CLI/Console support            | ✅ Yes                        |
| Archiving & audit              | ✅ Yes                        |

---


