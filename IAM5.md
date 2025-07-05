# **AWS Organizations** 

---

## 🏢 What is **AWS Organizations**?

**AWS Organizations** is a **centralized account management service** that enables you to:

* **Centrally manage** billing, policies, and access
* **Group accounts** into organizational units (OUs)
* Apply **Service Control Policies (SCPs)** across multiple AWS accounts
* Set up a **multi-account strategy** with centralized governance

---

## 🧠 Why Use AWS Organizations?

| 🔍 Use Case                           | ✅ Benefit                                     |
| ------------------------------------- | --------------------------------------------- |
| Multi-team or multi-project isolation | Separate workloads/account-level blast radius |
| Centralized billing                   | Aggregate usage and use consolidated billing  |
| Policy control                        | Set guardrails using SCPs                     |
| Automate account creation             | With Account Factory or APIs                  |
| Enable governance and compliance      | Enforce security controls across all accounts |

---

## 🛠️ AWS Organizations Architecture

```
AWS Organization (Root)
│
├── Organizational Unit: Security
│   ├── Account: Audit
│   └── Account: SecurityTools
│
├── Organizational Unit: Development
│   ├── Account: Dev1
│   └── Account: Dev2
│
└── Organizational Unit: Production
    ├── Account: Prod1
    └── Account: Prod2
```

---

## 🧱 Core Concepts

| Concept                          | Description                                                         |
| -------------------------------- | ------------------------------------------------------------------- |
| **Root**                         | The top node of your Org; created when you enable AWS Organizations |
| **Account**                      | A standard AWS account (child or management)                        |
| **OU (Organizational Unit)**     | Logical grouping of accounts                                        |
| **SCP (Service Control Policy)** | Guardrails that define maximum permissions an account/OUs can have  |
| **Management Account**           | Formerly "Master"; central account to create/manage others          |
| **Member Account**               | An account under the Org hierarchy managed via Organizations        |

---

## ✅ Options and Features Available in AWS Organizations

| Feature                               | Description                                                            |
| ------------------------------------- | ---------------------------------------------------------------------- |
| ✔️ Consolidated Billing               | View & manage all linked accounts' bills from management account       |
| ✔️ OU Hierarchies                     | Organize accounts logically (Dev, Test, Prod)                          |
| ✔️ SCPs                               | Restrict services/regions/actions at org, OU, or account level         |
| ✔️ Account Invitation                 | Add existing accounts                                                  |
| ✔️ Account Creation                   | Create accounts programmatically or manually                           |
| ✔️ Trusted Access                     | Enable integration with AWS services like AWS Config, CloudTrail, etc. |
| ✔️ Integration with AWS Control Tower | For automated landing zone setup                                       |
| ✔️ Tagging                            | Assign tags for cost tracking & management                             |

---

## 🎯 Step-by-Step: Set Up AWS Organizations from Console

### 🔹 Step 1: Enable AWS Organizations

1. Sign in to your **primary account**
2. Go to **AWS Organizations** service
3. Click **“Create organization”**
4. Choose:

   * **Consolidated billing only** ✅
   * OR **All features** (to use OUs and SCPs — recommended)

---

### 🔹 Step 2: Create Organizational Units (OUs)

1. Click **Organize accounts**
2. Choose **“Create organizational unit”**
3. Name it (e.g., `Development`, `Security`, `Production`)
4. Drag/drop existing accounts or create new ones into the OU

---

### 🔹 Step 3: Invite Existing Accounts (optional)

1. Go to **Accounts**
2. Click **“Add account” → Invite account**
3. Enter the email or account ID of the AWS account
4. The other account owner will receive an invite email

---

### 🔹 Step 4: Create a New AWS Account

1. Click **“Add account” → Create account**
2. Fill:

   * Email ID
   * Account name
   * IAM role name (for management access)
3. Account gets created and added under the Org

---

### 🔹 Step 5: Apply SCPs (Service Control Policies)

1. Go to **Policies → Service control policies**
2. Click **“Create policy”**
3. Example SCP: Deny access to `us-west-1`

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Action": "*",
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:RequestedRegion": "us-west-1"
        }
      }
    }
  ]
}
```

4. Attach this policy to an **OU or account**

---

## 💡 Example: Real-World OU Structure

```
Root
├── OU: Security
│   └── Account: audit@example.com
├── OU: Sandbox
│   ├── Account: dev1@example.com
│   └── Account: dev2@example.com
├── OU: Prod
│   ├── Account: app1@example.com
│   └── Account: database@example.com
```

* Sandbox OU: SCP to **deny access to production services**
* Security OU: SCP to **enforce CloudTrail, GuardDuty**
* Prod OU: SCP to **deny use of non-approved regions**

---

## 🔐 SCP Enforcement Model

> 🧠 **IAM + SCP = Effective Permissions**

If:

* IAM allows something ✅
* SCP denies it ❌

➡️ The action is **DENIED**

> SCPs are always **deny-first** unless explicitly allowed and not denied.

---

## 📈 Monitoring & Auditing

| Tool                           | Use                                |
| ------------------------------ | ---------------------------------- |
| **CloudTrail**                 | Logs Org changes                   |
| **AWS Config**                 | Track compliance with policies     |
| **Access Analyzer (Org-wide)** | Monitor external access across Org |
| **Cost Explorer**              | View costs per account             |
| **Service Quotas**             | Monitor limits centrally           |

---

## 🧰 CLI Examples

### List all accounts:

```bash
aws organizations list-accounts
```

### Create an OU:

```bash
aws organizations create-organizational-unit \
  --parent-id <root-id> \
  --name "Dev"
```

---

## 🧠 Best Practices

| Best Practice                                            | Reason                                           |
| -------------------------------------------------------- | ------------------------------------------------ |
| Use **OUs by environment or business unit**              | Logical separation                               |
| Enable **all features** in Organizations                 | Full control (OUs, SCPs, etc.)                   |
| Apply **least-privilege SCPs**                           | Reduce risk of misconfiguration                  |
| Use **audit and security accounts**                      | Separate accounts for logging & security tooling |
| Use **Control Tower** for large-scale landing zone setup | Faster setup and governance                      |
| Enable **trusted access** with AWS services              | Centralized config, guardrails                   |

---

## ✅ Summary

| Feature                     | Description                         |
| --------------------------- | ----------------------------------- |
| Multi-account mgmt          | ✅ Centralized                       |
| Consolidated billing        | ✅ Included                          |
| SCPs                        | ✅ Guardrails across Org             |
| OU hierarchy                | ✅ Logical account structure         |
| Account creation/invitation | ✅ Manual or automated               |
| Integration with services   | ✅ CloudTrail, Config, Control Tower |

---

Would you like:

* 🛠️ A Terraform setup to create an Organization with OUs and SCPs?
* 📊 A cost breakdown per account via AWS Organizations + Cost Explorer?
* 🚀 A visual diagram of an ideal AWS Org for DevOps projects?

Let me know and I’ll help you set that up!
