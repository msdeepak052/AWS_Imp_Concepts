# **AWS Config**

---

## ✅ What is **AWS Config**?

**AWS Config** is a service that enables you to:

* **Track** AWS resource configurations over time.
* **Audit** and **record** changes.
* **Evaluate** those configurations against desired settings using **Config Rules**.
* Helps with **compliance**, **security auditing**, **troubleshooting**, and **resource change tracking**.

---

## 🧠 Key Concepts in AWS Config

| Concept                    | Explanation                                                                                                                |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| **Configuration Item**     | Snapshot of resource metadata (e.g., EC2 instance type, security group settings).                                          |
| **Configuration Recorder** | Records changes in supported resources. Must be enabled.                                                                   |
| **Delivery Channel**       | Sends snapshots and compliance reports to an S3 bucket. Optionally, SNS for notifications.                                 |
| **Rules**                  | Conditions that AWS Config evaluates. Determines if resources comply with your organization’s standards.                   |
| **Compliance**             | Shows whether a resource configuration complies with a rule. Values: **Compliant**, **Non-compliant**, **Not applicable**. |

---

## 🎯 Use Cases for AWS Config

| Use Case                | Description                                                                            |
| ----------------------- | -------------------------------------------------------------------------------------- |
| **Security Compliance** | Ensure all EC2 instances have encrypted volumes or all S3 buckets block public access. |
| **Resource Inventory**  | Track and list all AWS resources in your environment with configuration changes.       |
| **Change Management**   | Troubleshoot changes like “Why was this security group altered?”                       |
| **Auditing**            | Generate historical configuration reports for audits (e.g., for SOC 2, HIPAA).         |
| **Governance**          | Prevent resources from being configured against best practices.                        |

---

## 📘 Example: Use AWS Config to ensure S3 Buckets are not publicly accessible

### Step 1: Enable AWS Config

Go to AWS Console → Config → “Set up”:

1. Select the region and resources to track (default: all).
2. Choose an S3 bucket to store logs.
3. Optionally configure SNS for alerts.
4. Enable recording.

---

### Step 2: Create a Rule – **s3-bucket-public-read-prohibited**

AWS provides **managed rules**. Use this rule to ensure no bucket allows public read access.

#### Rule: `s3-bucket-public-read-prohibited`

| Parameter               | Value                                                 |
| ----------------------- | ----------------------------------------------------- |
| **Rule Type**           | AWS Managed                                           |
| **Trigger**             | Periodic or Configuration change                      |
| **Compliance Criteria** | Buckets with public read access are **non-compliant** |

---

### Step 3: Check Compliance

Once enabled:

* AWS Config evaluates all your S3 buckets.
* If any bucket allows public access, it's marked **non-compliant**.
* You can **remediate** or automate remediation using **SSM Automation**.

---

## 🔧 Sample Project: Enforce EC2 Instances to Use Approved AMIs

Let’s say you want to ensure all EC2 instances are launched only using company-approved AMIs.

### Step-by-step

#### Step 1: Create a Custom Rule (Lambda-backed)

1. Create a Lambda function that:

   * Checks instance AMI against an approved list (e.g., stored in SSM Parameter Store).
2. Create an AWS Config custom rule and associate it with the Lambda.

#### Lambda Sample (Python):

```python
import boto3

def lambda_handler(event, context):
    invoking_event = json.loads(event['invokingEvent'])
    configuration_item = invoking_event['configurationItem']
    resource_type = configuration_item['resourceType']
    
    if resource_type != 'AWS::EC2::Instance':
        return build_response('NOT_APPLICABLE')

    ami_id = configuration_item['configuration']['imageId']
    approved_amis = ['ami-12345678', 'ami-87654321']

    if ami_id in approved_amis:
        return build_response('COMPLIANT')
    else:
        return build_response('NON_COMPLIANT')

def build_response(compliance_type):
    return {
        'compliance_type': compliance_type,
        'annotation': 'Checked against approved AMIs'
    }
```

---

## 🧩 Types of Rules in AWS Config

| Rule Type                          | Description                      | Example                                           |
| ---------------------------------- | -------------------------------- | ------------------------------------------------- |
| **Managed Rules**                  | Prebuilt by AWS                  | `ec2-instance-no-public-ip`, `cloudtrail-enabled` |
| **Custom Rules**                   | Written using Lambda             | Check EC2 tags, validate AMIs                     |
| **Periodic**                       | Runs at fixed interval           | Daily enforcement of encryption                   |
| **Configuration Change Triggered** | Runs when a resource is modified | S3 bucket ACL changed                             |

---

## 📝 How to View Config Output

* Go to AWS Config Console
* Select **“Rules”** tab → View rule evaluation results
* Click on **non-compliant** → see why and when a resource became non-compliant
* Check **Timeline** tab of resource → View config changes over time

---

## 💡 Best Practices

* Use **managed rules** first before writing custom logic.
* Use **tags** and **AWS Config Aggregators** to manage multi-account compliance.
* Combine with **AWS Systems Manager Automation** for auto-remediation.
* Enable **SNS notifications** for real-time compliance changes.

---

## 🧠 Extra from ChatGPT

* AWS Config works very well with **CloudTrail**: You can correlate config changes with API calls.
* Combine with **AWS Control Tower**, **AWS Organizations**, and **Service Control Policies (SCPs)** for enterprise-level governance.
* You can **query past configurations** using **AWS Config advanced queries** with SQL-like syntax.

---

Would you like me to:

* Share a CloudFormation template to set this up?
* Guide you through creating a custom rule end-to-end?
* Or integrate this into a CI/CD pipeline for compliance checks?

Let me know what you want to do next!
