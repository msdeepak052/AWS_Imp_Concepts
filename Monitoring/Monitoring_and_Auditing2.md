# **AWS CloudTrail** — a foundational service for **security**, **audit**, and **compliance**.

---

## ✅ What is AWS CloudTrail?

**AWS CloudTrail** is a service that:

* **Records all API calls and events** made in your AWS account.
* Captures actions taken through:

  * AWS Console
  * AWS SDK/CLI
  * AWS Services (internal triggers)
* Stores logs in **S3**, optionally integrates with **CloudWatch Logs** for alerting.

It helps you answer:

> ❓ Who did *what*, *when*, *from where*, and *using which service*?

---

## 📦 Key Benefits

| Benefit                 | Description                                                    |
| ----------------------- | -------------------------------------------------------------- |
| **Security auditing**   | Detect unauthorized access or privilege escalation.            |
| **Change tracking**     | Monitor changes to infrastructure (e.g., new EC2, deleted S3). |
| **Compliance**          | Supports PCI-DSS, HIPAA, SOX, and GDPR logging requirements.   |
| **Troubleshooting**     | Understand cause of failures or unexpected behavior.           |
| **Automation triggers** | Trigger Lambda based on specific events.                       |

---

## 🛠️ How It Works

1. **Trail** is created.
2. **Events** are logged (create, modify, delete).
3. Logs are delivered to an **S3 bucket**.
4. Optionally, logs are pushed to **CloudWatch Logs** or **EventBridge**.
5. Use tools like **Athena**, **CloudWatch Insights**, or **SIEM** for analysis.

---

## 🔍 Event Structure Example (JSON)

```json
{
  "eventTime": "2025-07-06T15:00:00Z",
  "eventName": "StartInstances",
  "awsRegion": "us-east-1",
  "sourceIPAddress": "1.2.3.4",
  "userAgent": "aws-cli/2.0",
  "userIdentity": {
    "type": "IAMUser",
    "userName": "deepak"
  },
  "requestParameters": {
    "instanceIds": ["i-0123456789abcdef0"]
  }
}
```

---

## 🎯 Use Cases

| Use Case                      | Example                                                 |
| ----------------------------- | ------------------------------------------------------- |
| **Who deleted an S3 bucket?** | Find `DeleteBucket` event and source IP                 |
| **Track EC2 launches**        | Alert if new EC2 is launched outside approved AMI       |
| **Detect credential abuse**   | Monitor for suspicious IAM access or API brute force    |
| **Compliance reports**        | Show all activity from a specific IAM role              |
| **Cost impact analysis**      | Who triggered a costly AWS service (e.g., EMR, Athena)? |

---

## 🧩 Associated Parameters

| Parameter              | Description                                                                   |
| ---------------------- | ----------------------------------------------------------------------------- |
| **Trail name**         | Name of the CloudTrail (e.g., `org-audit-trail`)                              |
| **S3 bucket**          | Destination for logs                                                          |
| **Log file prefix**    | Optional folder prefix in the bucket (e.g., `cloudtrail-logs/`)               |
| **Multi-region trail** | Capture events from all AWS regions                                           |
| **Organization trail** | Capture activity across all accounts in AWS Organizations                     |
| **Insight events**     | Detect unusual activity (e.g., API spikes)                                    |
| **CloudWatch Logs**    | Real-time analysis and alerts                                                 |
| **Event selectors**    | Filter by management events (control plane) or data events (e.g., S3, Lambda) |

---

## ⚙️ How to Set Up (AWS Console)

1. Go to **AWS CloudTrail → Trails → Create trail**
2. Enter **Trail name**
3. Choose:

   * **Management Events**: Track control plane operations (default: All)
   * **Data Events**: Deeper tracking for S3, Lambda (e.g., `GetObject`, `Invoke`)
   * **Insight Events** *(optional)*: Detect unusual activity (enabled per trail)
4. Choose S3 bucket or create a new one
5. (Optional) Enable CloudWatch Logs for real-time monitoring
6. Click **Create**

---

## 🧪 Example: Monitor for EC2 Launch Events

### EventSelector Config:

```json
{
  "ReadWriteType": "All",
  "IncludeManagementEvents": true,
  "DataResources": [
    {
      "Type": "AWS::EC2::Instance",
      "Values": ["arn:aws:ec2:region:account-id:instance/*"]
    }
  ]
}
```

Use this for:

* Triggering a Lambda function via EventBridge when someone launches an EC2.
* Enforce compliance or log tags.

---

## 📊 Viewing CloudTrail Logs

| Option                 | Description                                           |
| ---------------------- | ----------------------------------------------------- |
| **S3**                 | Raw JSON files (partitioned by time, region, account) |
| **CloudTrail Console** | Search UI                                             |
| **Athena**             | Query logs using SQL                                  |
| **CloudWatch Logs**    | Stream events for dashboards or alerts                |
| **EventBridge**        | Real-time trigger pipelines                           |

---

## 🔐 Example Alert: IAM Policy Changed

1. In **EventBridge**, create a rule:

   * Event pattern:

     ```json
     {
       "source": ["aws.iam"],
       "detail-type": ["AWS API Call via CloudTrail"],
       "detail": {
         "eventName": ["PutUserPolicy", "PutRolePolicy"]
       }
     }
     ```
2. Target: SNS, Lambda, or Slack webhook

---

## 🧠 Extra from ChatGPT

* **CloudTrail Lake** (2022+ feature): Centralized event log analytics without exporting to S3. Use SQL to query directly.
* **Retention**: S3 logs stored as long as you want; Event history (last 90 days) is available by default for free.
* Use **Control Tower** to auto-enable CloudTrail org-wide.
* Integrate CloudTrail with **GuardDuty** and **Security Hub** for threat detection.

---

## 📘 Optional: CLI Commands

### Create a trail:

```bash
aws cloudtrail create-trail \
  --name my-audit-trail \
  --s3-bucket-name my-trail-logs-bucket
```

### Enable logging:

```bash
aws cloudtrail start-logging --name my-audit-trail
```

### List events (last 90 days):

```bash
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=RunInstances
```

---

