# **IAM Roles for AWS Account-to-Account AssumeRole**
---

## 🔁 What is “AssumeRole” Between AWS Accounts?

This allows a **user or role in one AWS account** (Account A) to **assume a role in another AWS account** (Account B) and **temporarily gain its permissions** using `sts:AssumeRole`.

🔐 It is **secure**, **auditable**, and avoids creating long-term credentials across accounts.

![image](https://github.com/user-attachments/assets/8f8ed9be-94ff-4c4e-889c-dc44e16c92d1)

![image](https://github.com/user-attachments/assets/6840b83e-5449-4216-8a27-f265dd2803d0)

---

## 🧠 When is it used?

| Use Case                        | Description                                                 |
| ------------------------------- | ----------------------------------------------------------- |
| 🛠 DevOps CI/CD                 | CI system in Account A deploys to EKS in Account B          |
| 🔍 Centralized Logging          | Logging tools in Account A pull logs from multiple accounts |
| 💼 Central Security/Audit Teams | Access all other accounts via read-only role                |
| 💳 Shared Billing Access        | Finance team accesses billing data from child accounts      |
| 🚀 Shared S3 Access             | Upload/download to S3 buckets in another account            |

---

## 🛠 Step-by-Step Setup: Cross-Account Role Access

### Scenario:

* **Account A** (ID: `111111111111`) has a user `deepak.dev`
* **Account B** (ID: `222222222222`) has an S3 bucket and you want to allow Account A to access it
* You’ll **create a role in Account B** that Account A can assume

---

### 🧾 Step 1: Create IAM Role in Account B

1. Login to **Account B**

2. Go to **IAM → Roles → Create role**

3. Select **Trusted entity**:
   ✅ Choose **Another AWS Account**

4. Enter **Account A's ID**: `111111111111`

---

### 🔐 Trust Policy Created Behind the Scenes:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::111111111111:root"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

✅ This means: “Any IAM user or role in Account A can assume this role”

---

### 📝 Step 2: Attach Permissions to the Role

For example, to allow access to an S3 bucket:

```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject"],
  "Resource": ["arn:aws:s3:::my-shared-bucket/*"]
}
```

Name the role: `CrossAccountS3ReadOnly`
Click **Create Role**

---

### 🔑 Step 3: Allow User in Account A to Assume the Role

In **Account A**, attach this policy to the IAM user `deepak.dev` or an IAM Role used by a service:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sts:AssumeRole",
      "Resource": "arn:aws:iam::222222222222:role/CrossAccountS3ReadOnly"
    }
  ]
}
```

✅ This allows the user to call `sts:AssumeRole` on that specific role in Account B.

---

### 🔄 Step 4: Assume Role (From AWS CLI or SDK)

```bash
aws sts assume-role \
  --role-arn arn:aws:iam::222222222222:role/CrossAccountS3ReadOnly \
  --role-session-name deepakSession
```

You’ll receive:

* Temporary credentials (Access Key ID, Secret Access Key, Session Token)

Set them via environment variables or use `aws configure` to test access.

---

### ✅ Now Try Accessing S3 in Account B

```bash
aws s3 ls s3://my-shared-bucket/ --profile assumed-role
```

---

## 📦 Options When Creating Role for Cross-Account AssumeRole

| Option                                           | Purpose                                     |
| ------------------------------------------------ | ------------------------------------------- |
| ✅ Specify Account ID                             | Only allow a specific AWS account           |
| 🔄 Use `ExternalId` condition                    | Protect against confused deputy attacks     |
| ⛔ Use `Condition` to restrict services, IP, tags | Fine-grained control                        |
| 🔐 `sts:ExternalId` for 3rd parties              | Required when you share access with vendors |
| 🔀 Session name, duration                        | Customize session time (max 12 hrs default) |

---

### 🔐 Example: Trust Policy with External ID

Used when giving 3rd party access (e.g., CI/CD tools or vendor accounts)

```json
{
  "Effect": "Allow",
  "Principal": {
    "AWS": "arn:aws:iam::111111111111:root"
  },
  "Action": "sts:AssumeRole",
  "Condition": {
    "StringEquals": {
      "sts:ExternalId": "my-secret-external-id-1234"
    }
  }
}
```

---

## ✅ Best Practices

| Best Practice                          | Reason                                         |
| -------------------------------------- | ---------------------------------------------- |
| 🔐 Use ExternalId                      | Prevent misuse of AssumeRole (confused deputy) |
| 🔎 Enable CloudTrail                   | Monitor role assumptions                       |
| ⏳ Limit session duration               | Avoid long-lived credentials                   |
| 🔄 Use Role Chaining wisely            | Don’t exceed 1-hour limit with chained roles   |
| 📂 Use SCP + IAM + Conditions together | Granular control in AWS Organizations          |

---

## 🧠 Summary

| Component                                     | Description                         |
| --------------------------------------------- | ----------------------------------- |
| **Trust policy** (in Account B)               | Allows Account A to assume the role |
| **Permissions policy** (on role in Account B) | Grants access to AWS resources      |
| **IAM User/Role in Account A**                | Needs permission to assume role     |
| **`sts:AssumeRole` call**                     | Establishes temporary session       |

---
### **IAM Roles for AssumeRole within the same AWS account** — often referred to as **Intra-Account Assume Role**.

---

## 🔁 What is Intra-Account AssumeRole?

This allows an **IAM user** or **IAM role** in an AWS account to **assume another role in the same account** using the `sts:AssumeRole` API.

---

## ✅ Why Use AssumeRole Within the Same Account?

| Use Case                                        | Description                                                                    |
| ----------------------------------------------- | ------------------------------------------------------------------------------ |
| 🔐 **Privileged access escalation**             | Allow users to switch into an admin or elevated role temporarily               |
| 🧪 **Different permission contexts**            | Developers assume roles for specific environments (DevOps, ReadOnly, Auditing) |
| 🔍 **Session tagging for logging and cost**     | Use `sts:AssumeRole` with tags                                                 |
| 👨‍👩‍👧‍👦 **Break-glass roles**               | Emergency access roles with approval workflow                                  |
| 🧱 **Temporary elevated access via automation** | E.g., via AWS SSO, CLI, SDK, or federated access                               |

---

## 🛠️ Step-by-Step Setup

### 🎯 Example:

IAM user `deepak.dev` in Account `123456789012` should assume a role `AdminAccessRole` with elevated permissions.

---

### 🔹 Step 1: Create IAM Role

1. Go to **IAM → Roles → Create Role**
2. Select **Trusted entity** → **Custom trust policy**
3. Use this **Trust Policy**:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:user/deepak.dev"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

✅ This means:

> The IAM user `deepak.dev` in **this same account** is allowed to assume this role.

---

### 🔹 Step 2: Attach a Permissions Policy to the Role

Let’s say you want this role to have **Admin access**:

Choose managed policy: `AdministratorAccess`
Or use a custom one:

```json
{
  "Effect": "Allow",
  "Action": "*",
  "Resource": "*"
}
```

* Name the role: `AdminAccessRole`
* Create ✅

---

### 🔹 Step 3: Allow `deepak.dev` to Assume the Role

Add a policy to the user `deepak.dev` (inline or attached):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sts:AssumeRole",
      "Resource": "arn:aws:iam::123456789012:role/AdminAccessRole"
    }
  ]
}
```

✅ Now, `deepak.dev` can call `sts:AssumeRole` for `AdminAccessRole`.

---

## 🔄 Step 4: How to Use the Role (Assume)

### a) 🧪 Using AWS CLI:

```bash
aws sts assume-role \
  --role-arn arn:aws:iam::123456789012:role/AdminAccessRole \
  --role-session-name elevated-access
```

This returns:

* Access key
* Secret key
* Session token

You can export them to environment variables and use temporary elevated access:

```bash
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_SESSION_TOKEN=...
```

---

### b) 🧑‍💻 Using AWS Console (Switch Role):

1. Click username on the top bar → **Switch Role**
2. Enter:

   * Account ID: `123456789012`
   * Role name: `AdminAccessRole`
3. Switch ✅

Now you’re working under the assumed role in the same account.

---

## 🧩 Optional: Add ExternalId, MFA, or Conditions

You can enhance security by requiring:

* ✅ **MFA authentication**
* 🎯 **Session tags** for audit and cost tracking
* 🔒 **IP or time-based conditions**
* 🧩 **ExternalId** (not typical for same-account)

### 🔐 Example: Require MFA to Assume Role

```json
{
  "Effect": "Allow",
  "Principal": {
    "AWS": "arn:aws:iam::123456789012:user/deepak.dev"
  },
  "Action": "sts:AssumeRole",
  "Condition": {
    "Bool": {
      "aws:MultiFactorAuthPresent": "true"
    }
  }
}
```

---

## ✅ Summary

| Component          | Purpose                                     |
| ------------------ | ------------------------------------------- |
| Trust Policy       | Who can assume the role                     |
| Permissions Policy | What the role can do                        |
| sts\:AssumeRole    | Action to trigger temporary credentials     |
| Session Duration   | By default 1 hour (can go up to 12 hours)   |
| Session Tags       | Optional metadata (e.g., environment, team) |

---

## 🛡️ Best Practices

| Practice                     | Why                                         |
| ---------------------------- | ------------------------------------------- |
| 🔐 Enforce MFA               | Prevent misuse of privilege escalation      |
| 🔎 Use CloudTrail            | Log all `AssumeRole` actions                |
| 🧪 Limit permissions         | Avoid `*:*` unless necessary                |
| 🏷 Use session tags          | Track usage and cost by team/user           |
| 🔄 Rotate session frequently | Reduce risk exposure from compromised creds |

---

## 🧠 Real-World Use Case

Let’s say your **developers** have regular user permissions. When they need to troubleshoot a production issue:

* They **switch roles** into a temporary `ProdSupportRole`
* That role has read-only access to logs and metrics
* After work is done, they switch back to default context

No need for 24/7 elevated access ✅

---


