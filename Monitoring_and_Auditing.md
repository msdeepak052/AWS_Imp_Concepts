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

## 🧠 Extra

* AWS Config works very well with **CloudTrail**: You can correlate config changes with API calls.
* Combine with **AWS Control Tower**, **AWS Organizations**, and **Service Control Policies (SCPs)** for enterprise-level governance.
* You can **query past configurations** using **AWS Config advanced queries** with SQL-like syntax.

---

# **AWS Config Conformance Packs**


## ✅ What is a **Conformance Pack**?

An **AWS Config Conformance Pack** is a **collection of AWS Config rules** and **remediation actions** in a **single YAML/JSON template**. You use this to **standardize compliance checks** across your organization.

Think of it like **CloudFormation for compliance** — a way to **bundle rules** together and **deploy them as a unit**.

---

## 📦 Why Use a Conformance Pack?

| Benefit                      | Description                                             |
| ---------------------------- | ------------------------------------------------------- |
| **Bulk deployment**          | Deploy multiple config rules with one template          |
| **Compliance as code**       | Write and version compliance rules in YAML              |
| **Multi-account governance** | Use AWS Organizations and StackSets                     |
| **Automatic remediation**    | Include remediation actions for non-compliant resources |
| **Auditing & reporting**     | Standardize compliance reporting across environments    |

---

## 🧪 Example Use Case

Let’s say your organization needs to:

* Ensure **EC2 instances don’t have public IPs**
* Ensure **S3 buckets block public access**
* Ensure **CloudTrail is enabled**

You can **combine these into a conformance pack**.

---

## 📁 Sample Conformance Pack (YAML)

```yaml
template:
  name: my-org-security-pack
  description: Ensure critical resources meet security standards

  rules:
    - name: ec2-instance-no-public-ip
      type: AWS::Config::ConfigRule
      properties:
        ConfigRuleName: ec2-instance-no-public-ip
        SourceIdentifier: EC2_INSTANCE_NO_PUBLIC_IP
        Scope:
          ComplianceResourceTypes:
            - AWS::EC2::Instance

    - name: s3-bucket-public-read-prohibited
      type: AWS::Config::ConfigRule
      properties:
        ConfigRuleName: s3-bucket-public-read-prohibited
        SourceIdentifier: S3_BUCKET_PUBLIC_READ_PROHIBITED

    - name: cloudtrail-enabled
      type: AWS::Config::ConfigRule
      properties:
        ConfigRuleName: cloudtrail-enabled
        SourceIdentifier: CLOUD_TRAIL_ENABLED
```

You can optionally add **remediation actions** using `AWS::Config::RemediationConfiguration`.

---

## 🛠️ How to Deploy a Conformance Pack (via Console)

1. **Go to AWS Config Console**
2. Choose **Conformance Packs** → **Deploy conformance pack**
3. Give it a name (e.g., `org-security-pack`)
4. Upload the YAML file or write inline
5. Choose S3 bucket to store evaluation results
6. Deploy 🚀

---

## 🛠️ How to Deploy via CLI

```bash
aws configservice put-conformance-pack \
  --conformance-pack-name org-security-pack \
  --template-body file://security-pack.yaml \
  --delivery-s3-bucket my-config-results-bucket
```

---

## 📊 View Results

After deployment:

* Go to **AWS Config > Conformance Packs**
* View **compliance summary per rule**
* Drill down into **non-compliant resources**
* Optional: Export results to S3 for auditing

---

## 🧠 Best Practices

| Practice                                    | Why It Matters                                 |
| ------------------------------------------- | ---------------------------------------------- |
| Use with **AWS Organizations**              | Centralized control across accounts            |
| Store templates in **CodeCommit or GitHub** | Version control for compliance-as-code         |
| Include **remediation actions**             | Automate fixing non-compliant resources        |
| Monitor with **AWS Security Hub**           | Integrate security posture with other services |
| Schedule **automated reports**              | For compliance audits and governance reviews   |

---

## 📘 Real-World Example: PCI-DSS Conformance Pack

AWS provides **predefined conformance packs** like:

* `Operational Best Practices for PCI-DSS`
* `HIPAA Security & Privacy`
* `NIST 800-53`
* `CIS AWS Foundations Benchmark`

Deploy them directly:

```bash
aws configservice put-conformance-pack \
  --conformance-pack-name pci-dss \
  --template-s3-uri https://s3.amazonaws.com/aws-config-conformance-pack-templates/us-east-1/PciDss.yml \
  --delivery-s3-bucket my-config-audit-logs
```

---

## 🧠 Extra

* You can **integrate conformance packs with AWS Service Catalog** to ensure only compliant stacks are deployed.
* Combine with **AWS Control Tower** to enforce compliance on account creation.
* Use **CloudFormation StackSets** to deploy conformance packs across all Org accounts in one go.

---


