# **AWS IAM Policy Generator**

* 🔍 What it is
* 🛠 How to use it (step-by-step)
* 📘 All options explained
* ✅ Examples for real-world use cases
* ⚠️ Limitations & Best Practices

---

## 🧰 What is the **IAM Policy Generator**?

The **AWS IAM Policy Generator** is a **web-based tool** provided by AWS that helps you **create JSON policies** for IAM users, groups, and roles without needing to write raw JSON.

📍 Available here:
👉 [https://awspolicygen.s3.amazonaws.com/policygen.html](https://awspolicygen.s3.amazonaws.com/policygen.html)

---

## 🎯 What Can You Generate?

You can generate **three types** of policies:

| Type                    | Description                              |
| ----------------------- | ---------------------------------------- |
| ✅ IAM Policy            | Identity-based (users, groups, roles)    |
| ✅ S3 Bucket Policy      | Resource-based for S3                    |
| ✅ SNS/SQS Access Policy | Resource policies for messaging services |

---

## 🛠 How to Use IAM Policy Generator (Step-by-Step)

### ▶️ Step-by-Step: IAM Policy Example (Read EC2 & S3 access)

1. Go to the [IAM Policy Generator](https://awspolicygen.s3.amazonaws.com/policygen.html)
2. Select **Policy Type** → `IAM Policy`
3. Choose **Effect** → `Allow`
4. Select **AWS Service** → `Amazon EC2`, then again `Amazon S3`
5. Choose **Actions**:

   * For EC2: `DescribeInstances`
   * For S3: `GetObject`, `ListBucket`
6. Add **Resource ARN** (or `*` to allow all)

   * Example: `arn:aws:s3:::my-bucket/*`
7. Click **Add Statement**
8. Add more statements if needed
9. Click **Generate Policy**
10. Copy the JSON output or save it

---

## 🧩 Policy Generator Options Explained

| Option           | Description                            | Example                    |
| ---------------- | -------------------------------------- | -------------------------- |
| **Policy Type**  | IAM, S3, SNS, SQS                      | IAM Policy                 |
| **Effect**       | Allow or Deny                          | Allow                      |
| **Service**      | AWS service name                       | `Amazon S3`                |
| **Actions**      | Operations (read, write, delete, etc.) | `s3:PutObject`             |
| **Resource ARN** | Restrict to specific resources         | `arn:aws:s3:::my-bucket/*` |

---

## 🔍 Real-World Examples

---

### 📦 Example 1: **Allow read-only access to a specific S3 bucket**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-app-bucket",
        "arn:aws:s3:::my-app-bucket/*"
      ]
    }
  ]
}
```

---

### 🚀 Example 2: **Allow EC2 Describe only**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:DescribeVolumes"
      ],
      "Resource": "*"
    }
  ]
}
```

---

### 🔐 Example 3: **Deny deleting any S3 object**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Action": [
        "s3:DeleteObject"
      ],
      "Resource": "*"
    }
  ]
}
```

---

### 🧑‍💻 Example 4: **Allow Lambda deployment + IAM PassRole**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "lambda:UpdateFunctionCode",
        "lambda:GetFunction",
        "iam:PassRole"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## ⚠️ Limitations of IAM Policy Generator

| Limitation                                  | Note                                                  |
| ------------------------------------------- | ----------------------------------------------------- |
| 🧾 No SCP or permission boundary generation | Use AWS Organizations or manual JSON                  |
| ❌ No condition key builder                  | You have to add `Condition` manually after generation |
| ❌ No tag-based access builder               | Must modify policy post-generation                    |
| 🧑‍🍳 Not ideal for complex policies        | Use custom JSON or Terraform/CDK instead              |

---

## ✅ Best Practices

* Always follow **least privilege** — allow only what's needed
* Use **resource ARNs** instead of wildcards where possible
* **Review generated policy** in IAM Policy Simulator
* Add **explicit denies** when needed for critical actions
* Test with **temporary credentials** (roles, not users)

---

## 🔎 **What is Policy Evaluation in AWS?**

**Policy Evaluation** is the logic AWS IAM uses to determine whether a request is **allowed or denied** based on all applicable policies. The **IAM Policy Simulator** lets you test and evaluate this logic **before deploying policies**, reducing errors and misconfigurations.

---

## ⚙️ **Core Evaluation Principles**

AWS follows a **default-deny** model. Here's the flow:

### 🔄 Evaluation Flow:

1. **Start with Deny** (implicit)
2. **Evaluate policies** (IAM, resource-based, SCPs, etc.)
3. **If any explicit `Deny` matches → Final Decision is DENY**
4. **If no Deny and at least one matching `Allow` → ALLOW**
5. **Otherwise → DENY**

---

## 📋 **Sources of Policies Considered**

| Policy Type                       | Description                                    |
| --------------------------------- | ---------------------------------------------- |
| ✅ IAM Identity-based              | Policies attached to Users, Groups, Roles      |
| ✅ Resource-based                  | e.g., S3 Bucket Policy, Lambda Resource Policy |
| ✅ SCPs (Service Control Policies) | Org-level policy boundaries                    |
| ✅ Permissions boundaries          | Optional IAM boundaries for roles              |
| ✅ Session policies                | Temporary session constraints (e.g., via STS)  |

> IAM Policy Simulator **only evaluates identity-based and resource-based policies** in your account — it doesn't simulate SCPs or session policies.

---

## 📌 **Key Decision Rules**

| Rule                          | Result                 |
| ----------------------------- | ---------------------- |
| ❌ Explicit Deny               | Overrides everything   |
| ✅ Allow with no explicit Deny | Allowed                |
| ❌ No matching Allow           | Denied (Implicit Deny) |

---

## 🧪 **Using Policy Simulator - Step-by-Step**

1. Go to [IAM Policy Simulator](https://policysim.aws.amazon.com)
2. Select **User**, **Group**, or **Role**
3. Choose **Service** (e.g., S3, EC2)
4. Select **Actions** (e.g., `s3:PutObject`)
5. Provide **Resource ARN** (optional)
6. Click **Run Simulation**

---

### 🧾 Example:

Let's say:

* You have an S3 bucket policy denying all deletes
* Your IAM policy allows full S3 access

Then you simulate `s3:DeleteObject`:

```json
{
  "Effect": "Deny",
  "Action": "s3:DeleteObject",
  "Resource": "*"
}
```

🎯 **Result**: `Deny` ✅ — because explicit deny in resource policy **overrides** allow in IAM.

---

## 🎯 Common Evaluation Scenarios

| Scenario                        | Evaluation Result | Why                                     |
| ------------------------------- | ----------------- | --------------------------------------- |
| Only Allow present              | ✅ Allow           | Matching action/resource                |
| No policy matches               | ❌ Deny            | Implicit deny                           |
| Allow + Deny                    | ❌ Deny            | Explicit deny overrides                 |
| Wildcard action (`*`) in Allow  | ✅ Allow           | If not denied                           |
| Resource-based Deny + IAM Allow | ❌ Deny            | Deny overrides IAM policy               |
| SCP blocks action               | ❌ Deny            | But Policy Simulator won’t detect this! |

---

## 🧠 Extra from ChatGPT

### 🔍 Pro Tips for Using Policy Simulator:

* Use **"Expand all services"** to simulate multiple permissions at once
* Check **missing resources** — many failures are due to missing or wrong ARNs
* Use it to **test new custom policies** before rollout
* Run simulations in **multiple environments (Dev/Test/Prod)**

---

## ✅ Summary

| Concept                        | Description                                   |
| ------------------------------ | --------------------------------------------- |
| **Default behavior**           | Deny                                          |
| **Explicit Allow**             | Grants permission unless denied elsewhere     |
| **Explicit Deny**              | Always wins                                   |
| **Simulator evaluates**        | Identity-based + Resource-based policies      |
| **Not evaluated by simulator** | SCPs, session policies, permission boundaries |

---

Let's build a **CLI-based IAM Policy Generator** you can use to quickly create custom IAM policies **from your terminal**. This is great for scripting, automation, and DevOps workflows.

---

## 🚀 CLI-Based IAM Policy Generator – Overview

We’ll create a **Python CLI tool** that:

* Accepts service, action(s), and resource(s) as arguments
* Outputs a valid IAM policy JSON
* Optional: Adds tags, conditions, or output to a file

---

### 🛠️ Prerequisites

* Python 3.x
* `argparse` (default)
* `json` (default)

---

## 📦 Script: `iam_policy_generator.py`

```python
#!/usr/bin/env python3

import argparse
import json
from datetime import datetime

def generate_policy(service, actions, resources, effect):
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": effect,
                "Action": [f"{service}:{action.strip()}" for action in actions],
                "Resource": resources
            }
        ]
    }

def main():
    parser = argparse.ArgumentParser(description="CLI-based IAM Policy Generator")

    parser.add_argument("-s", "--service", required=True, help="AWS service name (e.g., s3, ec2, lambda)")
    parser.add_argument("-a", "--actions", required=True, nargs='+', help="List of actions (e.g., GetObject PutObject)")
    parser.add_argument("-r", "--resources", required=True, nargs='+', help="List of resource ARNs or *")
    parser.add_argument("-e", "--effect", default="Allow", choices=["Allow", "Deny"], help="Policy effect (Allow or Deny)")
    parser.add_argument("-o", "--output", help="Output file to save the policy (optional)")

    args = parser.parse_args()

    policy = generate_policy(args.service, args.actions, args.resources, args.effect)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(policy, f, indent=2)
        print(f"[✓] Policy written to {args.output}")
    else:
        print(json.dumps(policy, indent=2))

if __name__ == "__main__":
    main()
```

---

## 🧪 Example Usage

### 1. 🚀 Generate read-only S3 policy (output to terminal)

```bash
python3 iam_policy_generator.py \
  -s s3 \
  -a GetObject ListBucket \
  -r arn:aws:s3:::my-bucket arn:aws:s3:::my-bucket/* \
  -e Allow
```

### 2. 📁 Save EC2 Start/Stop policy to file

```bash
python3 iam_policy_generator.py \
  -s ec2 \
  -a StartInstances StopInstances DescribeInstances \
  -r "*" \
  -e Allow \
  -o ec2-start-stop-policy.json
```

---

## 📘 Sample Output

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-bucket",
        "arn:aws:s3:::my-bucket/*"
      ]
    }
  ]
}
```

---

## ✅ Features You Can Extend

| Feature                        | How to Add                                                                  |
| ------------------------------ | --------------------------------------------------------------------------- |
| 🔐 Conditions                  | Add a `Condition` block in `generate_policy()`                              |
| 🏷 Tags (for tag-based access) | Add `"Condition": {"StringEquals": {"aws:ResourceTag/Environment": "dev"}}` |
| 📂 SCP support                 | Add `PolicyType` switch for organizational SCP logic                        |
| 🧪 Test Mode                   | Integrate with AWS CLI + `simulate-custom-policy`                           |
| 🛠 Role attachment             | Combine with `aws iam put-role-policy` script                               |

---

## 💡 Tip: Turn into an Executable

```bash
chmod +x iam_policy_generator.py
sudo mv iam_policy_generator.py /usr/local/bin/iamgen
```

Now run with:

```bash
iamgen -s s3 -a GetObject -r arn:aws:s3:::my-bucket/*
```

---


Let's **package your IAM Policy Generator as a proper CLI tool** with:

✅ Installation as a command-line utility (`iamgen`)
✅ Auto-completion for **bash/zsh/fish**
✅ Help, subcommands, and a professional CLI experience
✅ Ready-to-extend plugin-based architecture

We'll use [**Click**](https://click.palletsprojects.com/) – a powerful Python CLI framework.

---

## 🧰 Step-by-Step: Package `iamgen` as a CLI with Autocomplete

---

### 🔧 Step 1: Install Dependencies

```bash
pip install click
```

---

### 📦 Step 2: Full Tool – `iamgen.py`

```python
#!/usr/bin/env python3

import click
import json

@click.command()
@click.option('--service', '-s', required=True, help='AWS service (e.g., ec2, s3, lambda)')
@click.option('--action', '-a', multiple=True, required=True, help='Action(s) (e.g., GetObject, StartInstances)')
@click.option('--resource', '-r', multiple=True, required=True, help='Resource ARN(s) or *')
@click.option('--effect', '-e', default='Allow', type=click.Choice(['Allow', 'Deny']), help='Effect: Allow or Deny')
@click.option('--output', '-o', type=click.Path(), help='Output file to save policy')
def generate_policy(service, action, resource, effect, output):
    """🔐 IAM Policy Generator - Create AWS IAM policy JSON via CLI"""
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": effect,
                "Action": [f"{service}:{a}" for a in action],
                "Resource": list(resource)
            }
        ]
    }

    policy_json = json.dumps(policy, indent=2)
    
    if output:
        with open(output, 'w') as f:
            f.write(policy_json)
        click.echo(f"✅ Policy saved to: {output}")
    else:
        click.echo(policy_json)

if __name__ == '__main__':
    generate_policy()
```

---

### 📁 Step 3: Make It Executable

```bash
chmod +x iamgen.py
mv iamgen.py /usr/local/bin/iamgen
```

Test it:

```bash
iamgen -s s3 -a GetObject -a ListBucket -r arn:aws:s3:::my-bucket -r arn:aws:s3:::my-bucket/* --effect Allow
```

---

### ⚙️ Step 4: Enable Shell Autocompletion

#### 🐚 Bash:

Add to your `~/.bashrc` or `~/.bash_profile`:

```bash
eval "$(_IAMGEN_COMPLETE=bash_source iamgen)"
```

Then run:

```bash
source ~/.bashrc
```

#### 🐟 Fish:

```bash
eval (env _IAMGEN_COMPLETE=fish_source iamgen)
```

#### 🐚 Zsh:

Add to your `~/.zshrc`:

```bash
eval "$(_IAMGEN_COMPLETE=zsh_source iamgen)"
```

Then:

```bash
source ~/.zshrc
```

Now you’ll get **tab-completion** for options like `--service`, `--effect`, etc.

---

### ✅ Example CLI Usage

```bash
iamgen -s ec2 -a StartInstances -a StopInstances -r "*" -e Allow -o ec2-policy.json
```

---

## 📁 Optional: Turn into a PIP-installable Package

Create a `setup.py`:

```python
from setuptools import setup

setup(
    name='iamgen',
    version='1.0',
    py_modules=['iamgen'],
    install_requires=['Click'],
    entry_points={
        'console_scripts': [
            'iamgen = iamgen:generate_policy',
        ],
    },
)
```

Then install with:

```bash
pip install .
```

---

## ✅ Bonus Features You Can Add Later

| Feature            | Description                        |
| ------------------ | ---------------------------------- |
| 🔐 `--condition`   | Add MFA, tag-based conditions      |
| 🎯 `--policy-type` | Choose IAM/S3/SNS policy formats   |
| 🧪 `--simulate`    | Integrate with AWS CLI to simulate |
| 📂 `--template`    | Use predefined policy templates    |

---

Would you like me to:

* ✅ Add **template presets** (e.g., "read-s3", "deploy-lambda")?
* ✅ Include **auto-generate ARNs** from resource names?
* ✅ Package this as a GitHub repo + README?

---

# **Inline IAM Policies**

* 📘 What Inline Policies are
* 🛠 How to create them via the AWS Console
* 📊 Comparison: Inline vs AWS Managed vs Customer Managed
* ✅ Use cases & examples

---

## 🔐 What are **Inline IAM Policies**?

An **inline policy** is a **directly embedded policy** within a single IAM user, role, or group.

Unlike managed policies, inline policies are **tied to one principal** and **deleted** if the principal is deleted.

---

## 🧠 Key Characteristics

| Attribute   | Inline Policy                                              |
| ----------- | ---------------------------------------------------------- |
| Scope       | One IAM user, group, or role only                          |
| Reusability | ❌ Not reusable across identities                           |
| Lifecycle   | **Tied** to the identity                                   |
| Visibility  | Harder to audit at scale                                   |
| Purpose     | **Tightly coupled permission** model for specific identity |

---

## 🛠 How to Create an Inline Policy (AWS Console)

### 📍 Example: Allow a role to read-only access to S3 bucket

#### 👉 Steps:

1. Go to **IAM → Roles**
2. Click on the **role name** (e.g., `DevOpsEngineerRole`)
3. Scroll down → Under **Permissions**, click `Add inline policy`
4. Use **Visual editor** or **JSON**
5. Select **Service**: `S3`
6. Select **Actions**: `ListBucket`, `GetObject`
7. Specify **Resources**:

   * Bucket: `arn:aws:s3:::my-dev-bucket`
   * Objects: `arn:aws:s3:::my-dev-bucket/*`
8. Click **Review policy**
9. Give it a name: `InlineS3ReadPolicy`
10. Click **Create policy**

🔍 The inline policy will now appear **only under that role**.

---

## 📘 Example JSON for Inline Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-dev-bucket",
        "arn:aws:s3:::my-dev-bucket/*"
      ]
    }
  ]
}
```

---

## ⚖️ Comparison: IAM Policy Types

| Feature                | AWS Managed Policy             | Customer Managed Policy  | Inline Policy                          |
| ---------------------- | ------------------------------ | ------------------------ | -------------------------------------- |
| ✅ **Reusable**         | ✅ Across roles/users           | ✅ Across identities      | ❌ One identity only                    |
| 🛠 **Customizable**    | ❌ Predefined by AWS            | ✅ Full control           | ✅ Full control                         |
| 🔄 **Version control** | ❌ (AWS updates it)             | ✅ You manage it          | ❌ Tied to principal                    |
| 🔍 **Auditing**        | ✅ Easy to track                | ✅ Easy to track          | ❌ Hard to manage at scale              |
| 📌 **Use case**        | Common roles (ReadOnly, Admin) | Org-wide custom policies | Tight control for a specific role/user |
| 🗑️ **Lifecycle**      | Independent                    | Independent              | Deletes with identity                  |

---

## ✅ Use Cases for Inline Policies

| Use Case                            | Why Inline Works                                                                 |
| ----------------------------------- | -------------------------------------------------------------------------------- |
| **Highly specific access**          | E.g., a Lambda function that can access only a single SQS queue                  |
| **Tightly coupled identity-policy** | When the policy shouldn’t apply to any other role/user                           |
| **Temporary or test setups**        | Quick test with scoped permissions                                               |
| **Compliance requirement**          | Example: inline policies for break-glass access roles that are tightly monitored |

---

## ❌ When to Avoid Inline Policies

* When you **need reuse** (use Customer Managed instead)
* When you want **centralized permission management**
* When **auditing and consistency** is important

---

## 📦 When to Use Which?

| Scenario                              | Recommended Policy Type |
| ------------------------------------- | ----------------------- |
| Standard AWS use (e.g., EC2 ReadOnly) | **AWS Managed**         |
| Organization-wide custom roles        | **Customer Managed**    |
| One-off, tightly coupled permission   | **Inline Policy**       |
| Least privilege with versioning       | **Customer Managed**    |

---

## 👥 What Are **IAM Groups**?

An **IAM Group** is a **collection of IAM users** that you manage as a single unit. You **attach policies** (AWS Managed or Customer Managed) to the group, and all users in that group automatically inherit those permissions.

📌 You **can’t log in as a group** — groups are just **permission containers**.

---

## ✅ Why Use IAM Groups?

| Benefit                             | Description                                        |
| ----------------------------------- | -------------------------------------------------- |
| 🔄 Centralized Permissions          | Attach policy once — applies to all users in group |
| ⏱️ Time-Saving                      | Add/remove users without updating permissions      |
| 📘 Role-Based Access Control (RBAC) | Map groups to DevOps, QA, Admin, Audit, etc.       |
| 🔒 Enforce Least Privilege          | Easier to audit and manage who can do what         |

---

## 🛠️ Steps to Create and Use IAM Groups (From AWS Console)

---

### 🎯 Example Use Case: DevOps group with access to EC2 and S3

#### 👉 Step 1: Go to IAM Console

* Open [https://console.aws.amazon.com/iam](https://console.aws.amazon.com/iam)

---

### 👉 Step 2: Create Group

1. Click **Groups** → **Create group**
2. Name it: `DevOpsTeam`

---

### 👉 Step 3: Attach Permissions (Policy)

You can either:

* Attach **AWS Managed Policies** (e.g., `AmazonEC2ReadOnlyAccess`)
* Attach **Customer Managed Policies** (your own)
* Skip and attach later

✅ Example:

* Attach `AmazonEC2FullAccess`
* Attach `AmazonS3ReadOnlyAccess`

Click **Next** → **Create group**

---

### 👉 Step 4: Add Users to Group

1. Go to **IAM → Users**
2. Select a user (e.g., `deepak.dev`)
3. Go to **Groups** tab
4. Click **Add user to groups**
5. Choose `DevOpsTeam`

Now the user inherits the group's permissions.

---

## 📘 JSON Example (Customer Managed Policy for DevOps)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:*",
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": "*"
    }
  ]
}
```

You could attach this policy to your `DevOpsTeam` group.

---

## 📊 IAM Group Options & Features

| Feature                    | Description                          |
| -------------------------- | ------------------------------------ |
| ✅ Add/Remove users         | Easily manage group membership       |
| ✅ Attach multiple policies | Combine multiple permission sets     |
| ✅ List users in group      | See who inherits access              |
| ✅ Nested groups            | ❌ Not supported (no group of groups) |
| ✅ Tag groups               | Add metadata for automation/auditing |

---

## 📦 Example Grouping Strategy

| Group Name     | Permissions                             |
| -------------- | --------------------------------------- |
| `DevOpsTeam`   | EC2 full, S3 read-only, CloudWatch logs |
| `FinanceUsers` | Billing and Cost Explorer               |
| `Developers`   | Read/write to CodeCommit, S3, Lambda    |
| `Auditors`     | Read-only to CloudTrail, S3, IAM        |

---

## 🛡️ Best Practices

| Best Practice                               | Why                                                    |
| ------------------------------------------- | ------------------------------------------------------ |
| 🔒 Follow least privilege                   | Avoid attaching `AdministratorAccess` unless necessary |
| 🧠 Use clear group names                    | e.g., `QA_ReadOnly`, `Dev_Admin`                       |
| 📦 Combine with tagging                     | For automation and auditing (`Environment`, `Team`)    |
| 🔁 Review group memberships                 | Remove ex-employees or rotated roles                   |
| ❌ Don’t use groups for cross-account access | Use **roles** for that purpose                         |

---


# **IAM Roles**

---

## 🔐 What is an IAM Role?

An **IAM Role** is an **identity with a set of permissions** that **can be assumed by trusted entities**, such as:

* IAM Users
* AWS Services (like EC2, Lambda, ECS, etc.)
* Other AWS accounts
* Federated users (SSO, OIDC, SAML)
* Applications (via AssumeRole API)

✅ Unlike IAM users, **roles do not have long-term credentials**. They issue **temporary credentials** via **STS (Security Token Service)**.

---

## 🔄 When to Use IAM Roles?

| Use Case                             | Example                                 |
| ------------------------------------ | --------------------------------------- |
| ✅ Grant permissions to EC2 instances | EC2 accessing S3, CloudWatch, DynamoDB  |
| ✅ Cross-account access               | Role in Prod assumed from Dev account   |
| ✅ Service-to-service access          | Lambda calling DynamoDB                 |
| ✅ Temporary access                   | Security audit with 12-hour credentials |
| ✅ Federated identity access          | IAM Identity Center (AWS SSO), AD       |

---

## 🛠 How to Create and Use IAM Roles via AWS Console

---

### 🧑‍💻 **Example**: EC2 instance uploads files to S3

### 🔹 Step 1: Go to IAM → **Roles** → Click **Create role**

---

### 🔹 Step 2: Select **Trusted Entity**

Choose:

* `AWS service` (for EC2, Lambda, etc.)
* `Another AWS account`
* `Web identity` (OIDC)
* `SAML 2.0 federation`

For this example, choose:
➡️ **AWS Service** → **EC2**

---

### 🔹 Step 3: Attach Permissions Policy

Attach a policy like:

* `AmazonS3FullAccess`
* Or a **custom policy** (example below)

---

### 🔹 Step 4: Name the Role

* Name: `EC2ToS3Role`
* Add tags (optional)
* Create role ✅

---

### 🔹 Step 5: Attach Role to EC2

1. Go to **EC2 Console**
2. Select your EC2 instance
3. Actions → Security → Modify IAM Role
4. Attach `EC2ToS3Role`

Now the EC2 instance has the S3 permissions you defined.

---

## 📘 Example: JSON Policy for IAM Role (S3 Read/Write)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject", "s3:GetObject"],
      "Resource": ["arn:aws:s3:::my-dev-bucket/*"]
    }
  ]
}
```

---

## 🛡 Trust Policy (for EC2 or Lambda)

Each role has a **trust policy** that defines **who can assume it**:

### ▶️ Trust Policy for EC2

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

---

## 🧑‍🤝‍🧑 Trust Policy for Cross-Account Access

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:root"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Use this when an IAM user or role from **another account** needs to assume this role.

---

## ⚙️ Types of Roles in AWS

| Role Type                | Description                                           | Example                    |
| ------------------------ | ----------------------------------------------------- | -------------------------- |
| Service role             | Used by AWS services (EC2, Lambda, ECS)               | EC2 uploads to S3          |
| Service-linked role      | Managed by AWS, linked to a service                   | `AWSServiceRoleForEC2Spot` |
| Cross-account role       | Assumed by a user or role in another AWS account      | Prod team accesses Dev     |
| Identity Federation role | Used by external identity providers (SSO, SAML, OIDC) | Google or AD logins        |
| Role chaining            | Temporary role assumes another role                   | Lambda assumes admin role  |

---

## 📊 IAM Role Options in Console

| Option               | Description                           |
| -------------------- | ------------------------------------- |
| Trusted entities     | Defines who can assume the role       |
| Permissions policies | Attached policies (inline or managed) |
| Tags                 | Metadata for tracking/auditing        |
| Inline policies      | Unique to this role only              |
| Session duration     | Up to 12 hours (default 1 hour)       |
| Role last used       | Tracks usage for auditing             |

---

## ✅ Best Practices for IAM Roles

| Best Practice                                     | Reason                            |
| ------------------------------------------------- | --------------------------------- |
| 🧠 Use roles over users for services              | No long-term keys                 |
| 🔒 Follow least privilege                         | Only needed actions and resources |
| 📍 Add session tags                               | For audit and access controls     |
| ⏳ Set session timeout appropriately               | Prevent token abuse               |
| 🧪 Test with IAM Policy Simulator                 | Validate access before using      |
| 🧼 Rotate credentials if using AssumeRole via SDK | Handle STS limits properly        |

---

## 🧠 Extra

* Use **IAM roles with EC2 Instance Profiles** for app-level permissions instead of storing secrets in code
* For **multi-account organizations**, roles + AWS Organizations + SCPs provide scalable security
* Integrate **CloudTrail** to monitor who assumed which role and when

---

#### Let’s now explore the **three other IAM Role trusted entity types** in AWS IAM:

1. 🧑‍🤝‍🧑 **Another AWS Account**
2. 🌐 **Web Identity Federation (OIDC – Google, Cognito, etc.)**
3. 🔐 **SAML 2.0 Federation (Corporate SSO like Azure AD, Okta)**

We’ll follow the **same format** as before: explanation, use case, trust policy example, how to create via Console, and real-world scenario.

---

## 🧑‍🤝‍🧑 1. IAM Role Trusted by **Another AWS Account**

### 📘 What It Means:

Allows users/roles in **Account A** to assume a role in **Account B** using `sts:AssumeRole`.

### 📦 Common Use Case:

* Centralized security access (audit/account team accessing prod)
* Shared DevOps roles
* Cross-account CI/CD pipelines

---

### 🎯 Example: Account A (DevOps) assumes a role in Account B (Prod)

#### 👉 Step-by-Step: In Account B (where role is created)

1. Go to **IAM → Roles → Create role**
2. Choose **Trusted entity type** → `Another AWS Account`
3. Enter the AWS Account ID of Account A (e.g., `123456789012`)
4. Attach policy (e.g., `AmazonEC2FullAccess`)
5. Name the role: `CrossAccountEC2Access`
6. Create role ✅

---

### 🔐 Trust Policy Example:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:root"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

---

### 🔄 In Account A (caller):

1. IAM user or role uses AWS CLI:

```bash
aws sts assume-role \
  --role-arn arn:aws:iam::098765432109:role/CrossAccountEC2Access \
  --role-session-name DevOpsAccess
```

---

## 🌐 2. IAM Role for **Web Identity Federation (OIDC)**

### 📘 What It Means:

Allows **external identities (like Google, Facebook, GitHub, Cognito)** to assume an IAM role using **OpenID Connect (OIDC)**.

### 📦 Common Use Cases:

* Cognito-authenticated mobile/web apps accessing AWS resources
* GitHub Actions deploying to AWS using GitHub’s OIDC provider

---

### 🎯 Example: A mobile app authenticated with Cognito uploads to S3

#### 👉 Step-by-Step:

1. Go to **IAM → Roles → Create role**
2. Choose **Web identity** → Choose `Cognito`, `Google`, etc.
3. Select Identity Pool or Provider
4. Choose OIDC Condition (e.g., `aud` or `sub`)
5. Attach policy (e.g., `AmazonS3PutObject`)
6. Name the role: `CognitoS3Uploader`
7. Create role ✅

---

### 🔐 Trust Policy for Cognito:

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
          "cognito-identity.amazonaws.com:aud": "us-east-1:pool-id",
          "cognito-identity.amazonaws.com:amr": "authenticated"
        }
      }
    }
  ]
}
```

✅ This role is assumed using `AssumeRoleWithWebIdentity` API via the app.

---

## 🔐 3. IAM Role for **SAML 2.0 Federation**

### 📘 What It Means:

Allows enterprise users to authenticate into AWS using a **SAML 2.0-compatible identity provider** like:

* Azure Active Directory
* Okta
* ADFS
* Google Workspace

This enables **Single Sign-On (SSO)** into AWS Console or STS APIs.

---

### 📦 Common Use Cases:

* Enabling SSO for internal teams
* Temporary access for contractors via ADFS/Okta

---

### 🎯 Example: Azure AD user signs into AWS console

#### 👉 Step-by-Step:

### 🔹 In IAM Console (AWS):

1. Go to **IAM → Identity Providers**
2. Click **Add provider**

   * Provider type: `SAML`
   * Provider name: `AzureADProvider`
   * Upload **SAML metadata XML** from Azure AD
3. Create IAM **role for SAML 2.0 Federation**

   * Trusted entity: `SAML 2.0 Federation`
   * Choose `AzureADProvider`
   * Specify SAML condition (`SAML:aud` = `https://signin.aws.amazon.com/saml`)
4. Attach permissions (e.g., `ReadOnlyAccess`)
5. Name it: `AzureADSSORole`

---

### 🔐 Trust Policy for SAML Federation:

```json
{
  "Version": "2012-10-17",
  "Statement": [
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
  ]
}
```

---

### 🧑‍💼 End User Flow (SSO Login):

1. Go to the corporate identity provider (e.g., Okta or Azure AD)
2. Click the **AWS application tile**
3. SAML assertion is sent → AWS STS issues temporary credentials
4. User is logged into AWS Console with assigned role

---

## 🧠 Summary Table: IAM Role Trusted Entity Types

| Trusted Entity Type          | Method                          | Example                |
| ---------------------------- | ------------------------------- | ---------------------- |
| 🧑‍🤝‍🧑 Another AWS Account | `sts:AssumeRole`                | Cross-account CI/CD    |
| 🌐 Web Identity (OIDC)       | `sts:AssumeRoleWithWebIdentity` | Cognito, GitHub OIDC   |
| 🔐 SAML Federation           | `sts:AssumeRoleWithSAML`        | Azure AD, Okta, ADFS   |
| 🤖 AWS Services              | `sts:AssumeRole` by service     | EC2, Lambda            |
| 🧑 Federated Users           | Via SSO/STS                     | Login without IAM user |


---

## 📜 The Two Policies You Shared:

---

### **1. Permissions Policy (Identity Policy or Inline Policy)**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject", "s3:GetObject"],
      "Resource": ["arn:aws:s3:::my-dev-bucket/*"]
    }
  ]
}
```

✅ **Purpose**:
Grants permissions to **perform specific actions** on AWS resources (in this case, S3).

✅ **Attached To**:
An IAM **user, role, or group**.

✅ **Use Case**:
A role or user needs **access to an S3 bucket** — this policy defines **what actions** (`PutObject`, `GetObject`) they can do **on what resources** (objects in the bucket).

🧑‍💻 **Example**:
You attach this policy to an EC2 role called `EC2ToS3Uploader`, so when an EC2 instance uses this role, it can upload/download files to `my-dev-bucket`.

---

### **2. Trust Policy (Assume Role Policy / Role Trust Relationship)**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

✅ **Purpose**:
Defines **who (which trusted entity)** is allowed to **assume the role** — it **does not grant access to AWS resources** directly.

✅ **Attached To**:
Always part of an **IAM Role definition**.

✅ **Use Case**:
Allows **EC2 instances** to assume the IAM role that has this trust policy.

🧑‍💻 **Example**:
You create a role `EC2ToS3Uploader` and define this trust policy. This tells AWS,

> "Only EC2 instances (via EC2 service) are allowed to use this role."

---

## 🔁 How These Work Together in a Role

Let’s combine both in one flow:

### 🚀 Scenario:

You want EC2 instances to upload logs to S3 (`my-dev-bucket`).

---

### ✅ Step-by-Step:

#### 1. **Create IAM Role**: `EC2ToS3Uploader`

#### 2. **Attach Permissions Policy**:

Gives permission to interact with S3:

```json
{
  "Effect": "Allow",
  "Action": ["s3:PutObject", "s3:GetObject"],
  "Resource": ["arn:aws:s3:::my-dev-bucket/*"]
}
```

#### 3. **Attach Trust Policy**:

Allows EC2 instances to assume the role:

```json
{
  "Effect": "Allow",
  "Principal": {
    "Service": "ec2.amazonaws.com"
  },
  "Action": "sts:AssumeRole"
}
```

#### 4. **Assign Role to EC2 Instance**:

Go to EC2 → Actions → Modify IAM Role → Select `EC2ToS3Uploader`

---

## 🧠 Summary Table: Key Differences

| Feature                         | Permissions Policy                      | Trust Policy                |
| ------------------------------- | --------------------------------------- | --------------------------- |
| 🔐 Grants Permissions           | ✅ Yes                                   | ❌ No                        |
| 🔓 Controls Who Can Assume Role | ❌ No                                    | ✅ Yes                       |
| 📦 Attached To                  | IAM Role/User/Group                     | IAM Role only               |
| 🎯 Example Action               | `s3:GetObject`, `ec2:DescribeInstances` | `sts:AssumeRole`            |
| 👥 Principal                    | None (implicit)                         | Required                    |
| 🧑 Use Case                     | Define what a role can do               | Define who can use the role |

---

## ✅ Real-World Analogy

> Think of a **trust policy** as the **door policy** of a secure room — who’s allowed to enter.
>
> Think of a **permissions policy** as **what actions someone can do** inside the room once they’re in.

---


## ✅ Scenario

**Goal:**
You want your EC2 instance to **upload files to an S3 bucket** named `my-dev-bucket`.

---

### ❓ Problem

By default, **EC2 instances have no permissions to access S3**.
You cannot give IAM user credentials directly to EC2 for security reasons.

🔐 Solution: Use an **IAM Role** with:

1. A **Trust Policy** → Allows EC2 to assume the role
2. A **Permissions Policy** → Allows the role to access S3

---

## 🛠️ Step-by-Step Example (with Explanations)

---

### **Step 1: Create IAM Role**

* Go to AWS Console → IAM → Roles → Create role

#### 🔸 Select Trusted Entity

* Select **AWS service**
* Choose **EC2**
* ✅ This automatically adds the **trust policy**:

```json
{
  "Effect": "Allow",
  "Principal": {
    "Service": "ec2.amazonaws.com"
  },
  "Action": "sts:AssumeRole"
}
```

📌 **Why this is needed?**
This tells AWS:

> “Only EC2 instances can use (assume) this role.”

✅ \*\*This is the **trust policy**.

---

### **Step 2: Attach Permissions Policy**

Next screen: **Attach Permissions**

* Choose: **Create inline policy** (or pick from AWS Managed policies)
* Use this **permissions policy**:

```json
{
  "Effect": "Allow",
  "Action": ["s3:PutObject", "s3:GetObject"],
  "Resource": ["arn:aws:s3:::my-dev-bucket/*"]
}
```

📌 **Why this is needed?**
This defines **what the role is allowed to do**:

> "This role can read/write to `my-dev-bucket` in S3."

✅ This is the **permissions policy**.

---

### **Step 3: Name and Create the Role**

* Name: `EC2S3UploadRole`
* Click **Create role**

---

### **Step 4: Attach the Role to an EC2 Instance**

1. Go to **EC2 → Instances**
2. Select your EC2 instance
3. Click **Actions → Security → Modify IAM Role**
4. Select `EC2S3UploadRole`
5. Save ✅

📌 Now your EC2 instance can **assume this role automatically** when it starts.

---

### ✅ Final Result:

| Layer                    | What It Does                                                  |
| ------------------------ | ------------------------------------------------------------- |
| **Trust Policy**         | Allows EC2 to **assume the role**                             |
| **Permissions Policy**   | Allows the role (and thus EC2) to **put/get objects** from S3 |
| **IAM Role**             | Acts as the **identity** that glues both together             |
| **EC2 Instance Profile** | Automatically **injects the role** into the EC2 instance      |

---

## 🔄 What Happens at Runtime?

1. EC2 instance boots up.
2. Instance metadata service gives it **temporary credentials** from the role.
3. The app/script inside EC2 calls S3 using SDK/CLI (no hardcoded keys).
4. S3 checks:

   * 🟢 "Is this a valid session from a trusted principal (EC2)?"
   * 🟢 "Does the session have permission to put/get objects?"

✅ If both are YES → Access granted.

---

## 📦 Diagram Summary

```plaintext
[EC2 Instance]
     |
     |----> IAM Role: EC2S3UploadRole
                 |           |
     Trust Policy    Permissions Policy
     (Who can use?)   (What can they do?)
         |                   |
     ec2.amazonaws.com   s3:PutObject, GetObject
                           on my-dev-bucket/*
```

---

## 🧪 Test the setup

SSH into EC2:

```bash
aws s3 cp testfile.txt s3://my-dev-bucket/
```

🎉 If configured correctly, this will succeed — with **no AWS credentials stored on the EC2**.

---






