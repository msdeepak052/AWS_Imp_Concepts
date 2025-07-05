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

## 🔐 Bonus Security Tip

You can also trigger **AWS Lambda or EventBridge automation** from the alarm for:

* Disabling root access keys (if any exist)
* Revoking sessions
* Triggering an incident workflow

---


