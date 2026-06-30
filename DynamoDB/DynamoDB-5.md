## 🔐 What is **Encryption at Rest** in DynamoDB?

**Encryption at Rest** in DynamoDB means that all your data is **automatically encrypted** when stored on disk (SSD), and decrypted when accessed. This helps protect your data from unauthorized access to the physical storage.

---

## 🔸 Key Features

| Feature                  | Details                                                                     |
| ------------------------ | --------------------------------------------------------------------------- |
| **Default Status**       | **Enabled by default** (since 2017) for all new tables                      |
| **Encryption Algorithm** | **AES-256**                                                                 |
| **Managed By**           | AWS Key Management Service (**KMS**)                                        |
| **Performance Impact**   | **No performance degradation**                                              |
| **Cost**                 | No extra charge for AWS-owned key (default); cost for customer-managed keys |

---

## 🔧 Types of KMS Keys Supported

| Key Type                    | Description                                                                |
| --------------------------- | -------------------------------------------------------------------------- |
| **AWS Owned CMK** (default) | Fully managed by AWS; no customer access                                   |
| **AWS Managed CMK**         | Managed by AWS but visible in your account under KMS                       |
| **Customer Managed CMK**    | You create/manage the key, define policies, enable logging, rotation, etc. |

---

## 🛠️ Example (Terraform - Customer Managed CMK)

```hcl
resource "aws_kms_key" "dynamodb_key" {
  description = "Customer-managed key for DynamoDB"
  enable_key_rotation = true
}

resource "aws_dynamodb_table" "secure_table" {
  name           = "SecureData"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "UserID"

  attribute {
    name = "UserID"
    type = "S"
  }

  server_side_encryption {
    enabled     = true
    kms_key_arn = aws_kms_key.dynamodb_key.arn
  }
}
```

---

## ✅ Use Cases

| Use Case                               | Why Encryption at Rest is Needed                                     |
| -------------------------------------- | -------------------------------------------------------------------- |
| **Financial data (e.g., banking app)** | Protect account info, balances, and transactions                     |
| **Healthcare records**                 | Meet HIPAA compliance                                                |
| **PII/Personal Data Storage**          | Compliance with GDPR, SOC 2, etc.                                    |
| **Enterprise Audit Logs**              | Ensure sensitive logs cannot be exposed if hardware is compromised   |
| **Multi-tenant SaaS apps**             | Use different CMKs per customer to isolate data access and ownership |

---

## 🔎 Monitoring and Auditing

* **CloudTrail** logs all key usage if using **Customer Managed Keys**
* **CloudWatch** can alert on unauthorized access attempts

---

## 🧠 Summary

* DynamoDB encrypts all data at rest using KMS.
* You can choose AWS-owned, AWS-managed, or customer-managed CMKs.
* Use customer-managed keys for better control and compliance requirements.
* **No code changes** needed in your application for encryption.

---


## 📘 What are **DynamoDB Resource Policies**?

A **DynamoDB resource policy** is a **JSON-based IAM policy** attached directly to a DynamoDB table. It defines **who (users, roles, accounts, orgs)** can access the table **from outside the account** and **under what conditions**.

It is most commonly used to enable **cross-account access** to DynamoDB tables.

---

## 🔐 Why Use Resource Policies?

* Allow **cross-account access** to a table without needing to share IAM roles.
* Restrict table access based on **specific conditions** (e.g., IP, VPC, time, etc.).
* Enforce **data governance** and security policies.
* Required when granting access to **AWS Organizations** or **external AWS accounts**.

---

## 🔧 Syntax Example: Resource Policy for Cross-Account Access

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowCrossAccountRead",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::222222222222:role/ReadOnlyRole"
      },
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:Query",
        "dynamodb:Scan"
      ],
      "Resource": "arn:aws:dynamodb:us-east-1:111111111111:table/CustomerData"
    }
  ]
}
```

### 🧾 Explanation:

* Grants read-only access (Query, GetItem, Scan) to the `CustomerData` table
* To a role in **another AWS account** (`222222222222`)
* The table resides in account `111111111111`

---

## ✅ Use Cases

| Use Case                                  | Why Resource Policy Helps                                                           |
| ----------------------------------------- | ----------------------------------------------------------------------------------- |
| **Cross-account analytics pipeline**      | Grant an analytics team in a separate AWS account access to a shared DynamoDB table |
| **Centralized audit logs**                | Multiple apps write logs to a single logging table                                  |
| **Multi-tenant architecture**             | Each tenant in different AWS accounts accesses a shared config table                |
| **AWS Organization-level access control** | Apply policies for all accounts under the same organization                         |
| **Partner integrations**                  | Allow external vendors to read specific records                                     |

---

## 🛠️ How to Attach Resource Policy (via AWS CLI)

```bash
aws dynamodb put-resource-policy \
  --resource-arn arn:aws:dynamodb:us-east-1:111111111111:table/CustomerData \
  --policy file://cross-account-policy.json
```

---

## 🧠 Tips & Best Practices

* Use **least privilege principle**: only allow specific actions like `Query`, `PutItem`, etc.
* Combine with **VPC endpoint policies** or **IAM condition keys** (e.g., `aws:SourceVpc`)
* Monitor access with **CloudTrail** and enable **encryption at rest** for security

---

## 🔄 Difference from IAM Policies

| Feature     | **IAM Policy**                   | **Resource Policy**                           |
| ----------- | -------------------------------- | --------------------------------------------- |
| Attached To | Users, Groups, Roles             | Resources (e.g., DynamoDB table)              |
| Scope       | Within same AWS account          | Enables **cross-account access**              |
| Use Case    | Define what user/role **can do** | Define **who can access** a specific resource |

---

# 🌍 **DynamoDB Global Tables** – Replication Made Simple

### 🔐 Definition:

**Global Tables** in DynamoDB provide **multi-region, active-active replication**. This means:

* Your data is **automatically replicated** across two or more AWS regions.
* You can read and write to **any region**, and DynamoDB handles syncing.

---

## 🚀 Key Features

| Feature                         | Description                                                |
| ------------------------------- | ---------------------------------------------------------- |
| **Multi-region replication**    | Syncs data across multiple AWS regions automatically       |
| **Active-active architecture**  | All replicas are writable; conflict resolution is built-in |
| **Automatic conflict handling** | Latest timestamp wins (last writer wins model)             |
| **Disaster recovery**           | High availability even if one region fails                 |
| **Low-latency access**          | Serve global users from the region closest to them         |

---

## 📦 How It Works

1. You define a **global table** in Region A.
2. You replicate it to Region B (and more).
3. Any change in one region is **eventually replicated** to all others.
4. DynamoDB handles **conflict resolution**, encryption, versioning, and replication automatically.

---

## 🔧 Example: Global Table Definition

### Scenario:

You have a table `UserProfiles` in `us-east-1` and want to replicate it to `eu-west-1`.

```hcl
resource "aws_dynamodb_table" "user_profiles" {
  name           = "UserProfiles"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "UserID"

  attribute {
    name = "UserID"
    type = "S"
  }

  replica {
    region_name = "eu-west-1"
  }

  replica {
    region_name = "ap-southeast-1"
  }
}
```

This config creates a **global table** spanning:

* **us-east-1**
* **eu-west-1**
* **ap-southeast-1**

---

## ✅ Use Cases

| Use Case                                     | How Global Tables Help                                            |
| -------------------------------------------- | ----------------------------------------------------------------- |
| 🌐 **Global user apps (e.g., social media)** | Serve users from their nearest region for low latency             |
| 🛍️ **E-commerce platforms**                 | Ensure cart, order, and profile data is consistent globally       |
| 🎮 **Gaming leaderboards**                   | Real-time updates across game servers worldwide                   |
| 📊 **Multi-region analytics/reporting**      | Enable teams in different regions to work on consistent data sets |
| 🚨 **Disaster Recovery & BCP**               | Continue operations even if one region goes down                  |

---

## ⚠️ Notes & Limitations

| Aspect                  | Detail                                                                           |
| ----------------------- | -------------------------------------------------------------------------------- |
| **Consistency**         | Eventually consistent across regions (not immediate)                             |
| **Conflict resolution** | Based on **last-writer-wins** using timestamps                                   |
| **Pricing**             | Charges apply for each replicated write per region                               |
| **Table schema**        | Must be identical across all replicas                                            |
| **Not editable**        | Once global table is created, adding/removing replicas requires table recreation |

---

## 🧠 Summary

| Benefit                             | Description                                             |
| ----------------------------------- | ------------------------------------------------------- |
| **Multi-region access**             | Low latency for global users                            |
| **Resilient architecture**          | Survive regional outages automatically                  |
| **Fully managed**                   | No manual replication or sync logic needed              |
| **Write anywhere, sync everywhere** | Multi-master write capability with eventual consistency |

---



