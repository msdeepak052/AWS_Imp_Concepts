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

![image](https://github.com/user-attachments/assets/97e4c9c8-a807-4c31-9739-30cc91934c32)



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

## **IAM Roles with Web Identity Federation and SAML 2.0 Federation**

These roles allow **external users** (such as mobile app users or corporate employees) to **access AWS services** securely **without needing IAM users** or long-term credentials.

![image](https://github.com/user-attachments/assets/1fba70bc-d38a-4ead-8746-c30d1018c8ad)

![image](https://github.com/user-attachments/assets/af3495e3-fffb-42d6-965d-026996a57ba7)

![image](https://github.com/user-attachments/assets/ecabb44c-0ff2-483a-bcbe-d089c5d262cd)

![image](https://github.com/user-attachments/assets/d49624da-d6eb-4d78-84eb-e03ce7e3d557)

---

## 🔷 Part 1: IAM Roles with **Web Identity Federation (OIDC)**

---

### ✅ Use Case:

Allow users **authenticated via Amazon Cognito, Google, or GitHub** to access AWS services **(e.g., S3)** via temporary credentials.

---

### 🧠 Key Concepts:

| Term                       | Description                                          |
| -------------------------- | ---------------------------------------------------- |
| Web identity provider      | OIDC-compatible (e.g., Cognito, Google, GitHub)      |
| IAM Role with Web Identity | Role assumed via `sts:AssumeRoleWithWebIdentity`     |
| Temporary credentials      | No long-term access keys needed                      |
| Condition                  | Restrict access to only specific user groups or apps |

---

### 🎯 Scenario:

You want users authenticated via **Amazon Cognito** to **upload objects to an S3 bucket**.

---

### 🛠 Hands-On Steps from AWS Console:

---

#### 🔹 Step 1: Create Cognito Identity Pool

1. Go to **Amazon Cognito** → Identity Pools

2. Click **Create new identity pool**

   * Name: `MyWebAppIdentityPool`
   * Enable **unauthenticated identities** (optional)

3. Choose authentication provider (e.g., Cognito User Pool, Google OIDC)

4. Click **Create Pool**
   Cognito **automatically creates IAM roles**:

   * `Cognito_MyWebAppIdentityPoolAuth_Role` (for signed-in users)
   * `Cognito_MyWebAppIdentityPoolUnauth_Role` (optional)

---

#### 🔹 Step 2: Modify IAM Role (Trust Policy)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "cognito-identity.amazonaws.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "cognito-identity.amazonaws.com:aud": "REGION:POOL-ID",
          "cognito-identity.amazonaws.com:amr": "authenticated"
        }
      }
    }
  ]
}
```

---

#### 🔹 Step 3: Attach Permissions Policy to Role

Example: Allow upload to specific S3 bucket

```json
{
  "Effect": "Allow",
  "Action": ["s3:PutObject"],
  "Resource": ["arn:aws:s3:::webapp-user-data/*"]
}
```

---

#### 🔹 Step 4: Access AWS via Temporary Credentials

On the client-side (JavaScript, Android, iOS), use AWS SDK to **exchange the identity token for temporary credentials**. Then call AWS services like this:

```js
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
  IdentityPoolId: 'REGION:POOL-ID',
  Logins: {
    'cognito-idp.REGION.amazonaws.com/USER_POOL_ID': ID_TOKEN
  }
});
```

---

### 🔐 Output:

* App users don’t need AWS keys
* All access is via secure, short-lived tokens
* Permissions are controlled via IAM Role + Trust Policy

---

## 🔶 Part 2: IAM Role with **SAML 2.0 Federation (SSO)**

---

### ✅ Use Case:

Allow **enterprise users** to sign into AWS Console or CLI using **Azure AD**, **Okta**, or **Google Workspace** via **SAML 2.0 SSO**.

---

### 🧠 Key Concepts:

| Term               | Description                                     |
| ------------------ | ----------------------------------------------- |
| Identity Provider  | SAML 2.0-compliant (Azure AD, Okta, ADFS, etc.) |
| SAML assertion     | Token received from the IdP after login         |
| IAM Role with SAML | Role assumed via `sts:AssumeRoleWithSAML`       |
| Role session       | Temporary AWS session from federated login      |

---

### 🎯 Scenario:

Allow users in Azure AD group `AWS-Admin` to assume `AdminAccessRole` in AWS.

---

### 🛠 Hands-On Steps from AWS Console:

---

#### 🔹 Step 1: Configure Identity Provider in IAM

1. Go to **IAM → Identity Providers → Add Provider**

   * Provider Type: `SAML`
   * Name: `AzureADProvider`
   * Upload **metadata XML** from Azure AD or other IdP

✅ Creates:
`arn:aws:iam::<account_id>:saml-provider/AzureADProvider`

---

#### 🔹 Step 2: Create IAM Role with SAML Trust Policy

1. Go to IAM → Roles → Create Role
2. Choose `SAML 2.0 federation` as trusted entity
3. Select `AzureADProvider`

Choose `Allow programmatic and AWS Management Console access`

4. Add Trust Policy like:

```json
{
  "Effect": "Allow",
  "Principal": {
    "Federated": "arn:aws:iam::123456789012:saml-provider/AzureADProvider"
  },
  "Action": "sts:AssumeRoleWithSAML",
  "Condition": {
    "StringEquals": {
      "SAML:aud": "https://signin.aws.amazon.com/saml"
    }
  }
}
```

---

#### 🔹 Step 3: Attach Permissions Policy

Attach a permission like `AdministratorAccess` or create your own.

---

#### 🔹 Step 4: Configure SAML Application in Azure AD or Okta

1. Add AWS as an enterprise application
2. Upload AWS SAML metadata or enter manually:

   * ACS URL: `https://signin.aws.amazon.com/saml`
   * Entity ID: `urn:amazon:webservices`
3. Map claim:

   * `https://aws.amazon.com/SAML/Attributes/Role`
     → `arn:aws:iam::<account_id>:role/AdminAccessRole,arn:aws:iam::<account_id>:saml-provider/AzureADProvider`

---

### 🔐 Final Flow

```plaintext
[User] --> [Login to Azure AD / Okta]
       --> [Gets SAML assertion]
       --> [Redirect to AWS Sign-in SAML]
       --> [STS:AssumeRoleWithSAML]
       --> [Access Console or AWS APIs]
```

---

## 📊 Summary: Web Identity vs SAML

| Feature            | Web Identity                    | SAML 2.0 Federation              |
| ------------------ | ------------------------------- | -------------------------------- |
| For                | Apps, mobile users              | Corporate employees              |
| Protocol           | OIDC                            | SAML 2.0                         |
| Roles Assumed Via  | `sts:AssumeRoleWithWebIdentity` | `sts:AssumeRoleWithSAML`         |
| Identity Providers | Cognito, Google, GitHub         | Azure AD, Okta, Google Workspace |
| Primary Use Case   | App-level access                | Console/CLI access with SSO      |
| Credential Type    | Temporary STS                   | Temporary STS                    |

---

## ✅ Best Practices

| Practice                                      | Benefit                 |
| --------------------------------------------- | ----------------------- |
| 🔐 Use least privilege                        | Secure scoped access    |
| 🎯 Restrict by `aud`, `sub`, group membership | Fine-grained control    |
| ⏳ Short session durations                     | Better security         |
| 🧪 Test with policy simulator                 | Avoid unintended access |
| 🔎 Monitor with CloudTrail                    | Full traceability       |

---

# **IAM Roles with Custom Trust Policies**

* ✅ What a trust policy is
* ✅ All possible options/fields you can customize
* ✅ Real-world examples
* ✅ Hands-on steps in the AWS Console
* ✅ Use cases and best practices

---

## 🔐 What is a **Trust Policy** in IAM?

A **trust policy** is a JSON document attached to an **IAM role**, which defines ***who is allowed to assume the role*** and ***under what conditions***.

💡 Think of it as the **entry gate rule** – it doesn’t define what you can do (permissions), only **who can enter** the role.

---

## 🧱 Trust Policy Structure

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { ... },
      "Action": "sts:AssumeRole",
      "Condition": { ... }
    }
  ]
}
```

---

## 🧰 Components You Can Customize

| Field       | Purpose                                                                         |
| ----------- | ------------------------------------------------------------------------------- |
| `Principal` | Who can assume the role: a user, service, account, etc.                         |
| `Action`    | Usually `sts:AssumeRole` (or `AssumeRoleWithSAML`, `AssumeRoleWithWebIdentity`) |
| `Condition` | Optional conditions like IP range, MFA, ExternalId, session tags, etc.          |

---

## 🛠️ Example Use Cases with Custom Trust Policies

---

### 🧑‍🤝‍🧑 1. **Allow Only a Specific User in the Same Account**

```json
{
  "Effect": "Allow",
  "Principal": {
    "AWS": "arn:aws:iam::123456789012:user/deepak.dev"
  },
  "Action": "sts:AssumeRole"
}
```

✅ Use case: User `deepak.dev` can assume this role to perform privileged tasks.

---

### 🏢 2. **Allow Users from Another AWS Account**

```json
{
  "Effect": "Allow",
  "Principal": {
    "AWS": "arn:aws:iam::111111111111:root"
  },
  "Action": "sts:AssumeRole"
}
```

✅ Use case: Cross-account access (DevOps role used from a central account).

---

### 🎯 3. **Restrict to Specific IAM Role**

```json
{
  "Effect": "Allow",
  "Principal": {
    "AWS": "arn:aws:iam::111111111111:role/GitHubDeployRole"
  },
  "Action": "sts:AssumeRole"
}
```

✅ Use case: Only GitHub's CI/CD role can assume this role (used with `OIDC` or service integrations).

---

### 🔐 4. **Allow AssumeRole Only with MFA**

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

✅ Use case: Enforce MFA for elevated privilege assumption.

---

### 🔑 5. **Use ExternalId to Protect Against Confused Deputy**

```json
{
  "Effect": "Allow",
  "Principal": {
    "AWS": "arn:aws:iam::987654321098:root"
  },
  "Action": "sts:AssumeRole",
  "Condition": {
    "StringEquals": {
      "sts:ExternalId": "your-external-client-id"
    }
  }
}
```

✅ Use case: 3rd-party tool/service (e.g., Terraform Cloud, Snowflake, Datadog) securely assuming the role.

---

### 🌐 6. **Allow Web Identity (OIDC) Token-based Assumption**

```json
{
  "Effect": "Allow",
  "Principal": {
    "Federated": "cognito-identity.amazonaws.com"
  },
  "Action": "sts:AssumeRoleWithWebIdentity",
  "Condition": {
    "StringEquals": {
      "cognito-identity.amazonaws.com:aud": "identity-pool-id"
    }
  }
}
```

✅ Use case: Authenticated users from Cognito identity pool can assume this role.

---

## 🛠️ Create Custom Trust Policy – AWS Console Steps

### 🔹 Step-by-Step

1. Go to **IAM → Roles → Create role**
2. Choose **Custom trust policy** (bottom option)
3. Paste your custom trust policy JSON
4. Click **Next**
5. Attach permissions (e.g., `AmazonS3FullAccess`)
6. Name the role: `CustomTrustedAccessRole`
7. Click **Create Role**

---

## 🧠 Real-world Example

### 🔧 Scenario:

You want to allow a specific IAM user (`deepak.dev`) to **assume a role for temporary admin access** — but **only with MFA enabled**.

### ✅ Custom Trust Policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
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
  ]
}
```

Then attach an `AdministratorAccess` permission policy to the role.

---

## 🔎 Use `Policy Simulator` to test the trust

Go to **IAM → Policy Simulator**, simulate an `AssumeRole` action for the user/role in question, and ensure it evaluates to `Allowed`.

---

## 🛡️ Best Practices

| Practice                                 | Why                        |
| ---------------------------------------- | -------------------------- |
| ✅ Always restrict Principal              | Avoid wildcards like `"*"` |
| 🔐 Use Conditions like MFA or ExternalId | Adds security              |
| 📜 Tag sessions using `sts:TagSession`   | Track usage                |
| 🔍 Monitor AssumeRole with CloudTrail    | Log role usage             |
| ⛔ Don't use root user in trust policies  | Use named roles or users   |

---

## 🚀 Summary Table: Trust Policy Options

| Feature                          | Example                                                           |
| -------------------------------- | ----------------------------------------------------------------- |
| IAM User (same account)          | `arn:aws:iam::<account>:user/<name>`                              |
| IAM Role (same or cross-account) | `arn:aws:iam::<account>:role/<name>`                              |
| AWS Services (e.g., EC2)         | `"Service": "ec2.amazonaws.com"`                                  |
| ExternalId                       | `Condition → sts:ExternalId`                                      |
| MFA Enforcement                  | `Condition → aws:MultiFactorAuthPresent: true`                    |
| Web Identity                     | `Principal → Federated` + `Action: sts:AssumeRoleWithWebIdentity` |
| SAML                             | `Principal → Federated` + `Action: sts:AssumeRoleWithSAML`        |

---



