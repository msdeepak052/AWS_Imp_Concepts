# AWS Identity and Access Management (IAM)
---

## 🛡️ **What is AWS IAM?**

**AWS Identity and Access Management (IAM)** is a service that enables **secure access control** to AWS services and resources. IAM lets you:

* **Create and manage users, groups, and roles**
* **Define permissions** using policies (fine-grained access)
* **Control access** to AWS APIs, resources, or services

---

## 🔐 **Core IAM Components**

| Component                     | Description                                                 |
| ----------------------------- | ----------------------------------------------------------- |
| **IAM Users**                 | Human users (developers, admins) with login credentials     |
| **IAM Groups**                | Collection of users with shared permissions                 |
| **IAM Roles**                 | Temporary identity for trusted AWS services, users, or apps |
| **IAM Policies**              | JSON-based permissions attached to users, groups, or roles  |
| **Identity Providers (IdPs)** | Integrate with SAML, OIDC, AD for SSO (federated access)    |

---

## ✅ **IAM Identity Types**

| Identity               | Use Case                                                         |
| ---------------------- | ---------------------------------------------------------------- |
| **IAM User**           | Login to AWS Console or use CLI/SDK                              |
| **IAM Group**          | Assign same policy to multiple users                             |
| **IAM Role**           | Used by AWS services (e.g., EC2, Lambda) or cross-account access |
| **Federated Identity** | External login via Google, Okta, SAML, etc.                      |

---

## 🧾 **IAM Policies**

### 🔹 Types of Policies:

| Type                                | Description                                             |
| ----------------------------------- | ------------------------------------------------------- |
| **AWS Managed Policies**            | Predefined by AWS (e.g., `AmazonEC2FullAccess`)         |
| **Customer Managed Policies**       | Custom JSON policies you create                         |
| **Inline Policies**                 | Directly attached to one user/role/group (not reusable) |
| **Permissions Boundaries**          | Limit the max permissions a user/role can have          |
| **Service Control Policies (SCPs)** | Used with AWS Organizations for account-level control   |
| **Session Policies**                | Temporary permissions with assumed roles                |

---

### 🧪 Example Policy – Allow EC2 Start/Stop

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["ec2:StartInstances", "ec2:StopInstances"],
      "Resource": "*"
    }
  ]
}
```

---

## 🧭 **Step-by-Step: Create IAM User with Limited Permissions**

### 🧱 Step 1: Create a User

1. Go to **IAM Console** → Users → **Add user**
2. Enter name (e.g., `developer-user`)
3. Select **Programmatic access** and/or **AWS Management Console access**
4. Set password if Console access selected

### 🧱 Step 2: Assign Permissions

* **Attach existing policies**: Choose AWS managed (e.g., `AmazonEC2ReadOnlyAccess`)
* Or **Create a new custom policy** (e.g., limit EC2 access to one region)

### 🧱 Step 3: Tags and Review

* Optionally add tags (e.g., `Team: DevOps`)
* Click **Create user**

---

## 🧭 **Step-by-Step: Create IAM Role for EC2**

1. IAM Console → **Roles** → **Create role**
2. **Trusted Entity:** Choose **EC2**
3. Attach a policy (e.g., `AmazonS3ReadOnlyAccess`)
4. Name the role: `EC2-S3ReadOnly`
5. Launch an EC2 instance → under **IAM Role**, attach `EC2-S3ReadOnly`

---

## 🧭 **Step-by-Step: Create IAM Group for Developers**

1. IAM Console → **Groups** → Create group
2. Name: `DevGroup`
3. Attach `AmazonEC2ReadOnlyAccess`
4. Add users (e.g., `developer-user`) to the group

---

## 🔐 **IAM Best Practices**

| Practice                                           | Why?                                                |
| -------------------------------------------------- | --------------------------------------------------- |
| ✅ **Use roles for EC2, Lambda, etc.**              | More secure than embedding credentials              |
| ✅ **Enable MFA for root & users**                  | Prevent unauthorized access                         |
| ✅ **Use least privilege**                          | Grant only necessary permissions                    |
| ✅ **Rotate access keys**                           | Avoid compromised static credentials                |
| ✅ **Use IAM Access Analyzer**                      | Identify resources shared publicly or cross-account |
| ✅ **Monitor with CloudTrail & IAM Access Advisor** | Track usage of permissions                          |

---

## 🎓 Real-World Use Cases

| Use Case                    | Solution                                         |
| --------------------------- | ------------------------------------------------ |
| DevOps needs EC2 access     | IAM group + EC2-specific policy                  |
| App on EC2 needs S3 read    | Attach IAM role to EC2                           |
| Users log in with Google    | Use IAM Identity Provider with SAML/OIDC         |
| Jenkins or Terraform access | Create IAM user with limited programmatic access |

---

## 📜 Policy Evaluation Flow

1. Start with **Deny by default**
2. Apply all **Allow statements**
3. Apply any **Explicit Deny** (overrides all Allows)
4. Final decision: **Allow or Deny**

---

## 🔚 Summary

| IAM Component | Purpose                      |
| ------------- | ---------------------------- |
| **User**      | Login & CLI access           |
| **Group**     | Group permissions            |
| **Role**      | Temp access or service roles |
| **Policy**    | Fine-grained control         |
| **IdP**       | SSO with third-party         |

---
# **IAM Policies**

---

## 🔐 **What are IAM Policies?**

IAM **policies** are JSON documents that define **permissions** — what actions are allowed or denied on which AWS resources and under what conditions.

---

## 📘 **What Are AWS Managed Policies?**

**AWS Managed Policies** are pre-created, maintained, and updated by **AWS** to help you quickly assign **common sets of permissions** without writing your own JSON policies.

---

## ✅ **Why Use AWS Managed Policies?**

* 🧠 **No need to write custom JSON**
* 🔄 **Auto-updated by AWS** with best practices
* ⚡ **Easy to attach** to users, groups, or roles
* 🔒 Generally safe, designed with least privilege in mind (but some are broad)

---

## 🔍 **Types of AWS Managed Policies**

AWS provides managed policies in 3 categories:

| Type                             | Description                                   | Examples                                               |
| -------------------------------- | --------------------------------------------- | ------------------------------------------------------ |
| **Service-specific full access** | Full permissions to use a service             | `AmazonS3FullAccess`, `AmazonEC2FullAccess`            |
| **Service-specific read-only**   | Read-only permissions for auditing or viewing | `AmazonS3ReadOnlyAccess`, `AmazonEC2ReadOnlyAccess`    |
| **Job function policies**        | Permissions based on roles or job types       | `AdministratorAccess`, `PowerUserAccess`, `Billing`    |
| **Service-linked role policies** | Used internally for service-linked roles      | `AWSServiceRoleForEC2SpotFleet` (auto-attached by AWS) |

---

## 🔑 **Examples of Popular AWS Managed Policies**

| Policy Name                | Description                                            |
| -------------------------- | ------------------------------------------------------ |
| `AmazonEC2FullAccess`      | Full control over EC2 resources                        |
| `AmazonS3ReadOnlyAccess`   | Can only list and read S3 bucket objects               |
| `AmazonDynamoDBFullAccess` | Full access to DynamoDB tables                         |
| `CloudWatchLogsFullAccess` | Full access to CloudWatch Logs                         |
| `IAMReadOnlyAccess`        | View IAM users, groups, roles, but can’t change        |
| `AdministratorAccess`      | Full root-like access to all services                  |
| `PowerUserAccess`          | Full access to services **except** IAM & Organizations |

---

## 🧭 **How to Attach AWS Managed Policy via Console**

### 🎯 Example: Attach `AmazonEC2ReadOnlyAccess` to a User

### 🛠 Step-by-Step

1. Go to **IAM Console** → **Users**
2. Select the user (e.g., `deepak-user`)
3. Click **Add permissions**
4. Choose **Attach policies directly**
5. Search for `AmazonEC2ReadOnlyAccess`
6. Select the checkbox and click **Next**
7. Review and click **Add permissions**

✅ This user can now **view EC2 instances**, but **not create, stop, or terminate them**.

---

## 🔁 **How AWS Keeps Managed Policies Updated**

* AWS updates managed policies when services or APIs change
* You don’t need to modify or redeploy them — **changes are automatic**
* AWS includes **change logs** in IAM documentation

---

## 🧠 Real Use Case Examples

| Team/Use Case                    | Policy to Use                                         |
| -------------------------------- | ----------------------------------------------------- |
| Developer needing S3 access      | `AmazonS3FullAccess`                                  |
| DevOps needing CloudWatch access | `CloudWatchFullAccess`                                |
| Read-only access for auditors    | `ReadOnlyAccess`                                      |
| Billing access only              | `AWSBillingReadOnlyAccess`                            |
| EC2 startup automation role      | `AmazonEC2FullAccess`, `AmazonSSMManagedInstanceCore` |

---

## ⚠️ When *Not* to Use AWS Managed Policies

| Reason                                              | Solution                                                  |
| --------------------------------------------------- | --------------------------------------------------------- |
| Too broad for your security model                   | Use **customer-managed policy** with narrowed permissions |
| Needs condition keys (e.g., specific bucket or tag) | Create a **custom JSON policy**                           |
| Needs permission boundaries or service control      | Use **permissions boundaries** or **SCPs**                |

---

## 📘 AWS Managed Policy Naming Convention

* `Amazon<Service>FullAccess`
* `Amazon<Service>ReadOnlyAccess`
* `AWS<Service>RolePolicy` (for service-linked roles)
* `AWS<Function>Access` (for job roles, like billing)

---

## 🧠 Pro Tips

* Start with **AWS Managed ReadOnlyAccess** for new users.
* Always use **roles instead of users** for services like EC2, Lambda, ECS.
* Use **IAM Access Analyzer** to see what resources users can access.
* Use **Access Advisor tab** in IAM Console to check unused permissions.

---

## 🔚 Summary

| Feature    | AWS Managed Policies                              |
| ---------- | ------------------------------------------------- |
| Ownership  | Created & managed by AWS                          |
| Updates    | Auto-updated                                      |
| Use case   | Rapid, secure permission assignments              |
| Limitation | Not customizable                                  |
| Best for   | Common service access (e.g., EC2, S3, CloudWatch) |

---

# **IAM Policies – Customer Managed Policies**

## 🔐 **What are Customer Managed IAM Policies?**

**Customer Managed Policies** are IAM policies **created and maintained by you** (the AWS account admin). Unlike AWS Managed Policies, they give you **full control** over permissions, resources, and conditions.

---

## 🧩 Why Use Customer Managed Policies?

| ✅ Benefit            | 💡 Description                                                  |
| -------------------- | --------------------------------------------------------------- |
| 🔧 Customization     | You can define very specific actions, resources, and conditions |
| 🔒 Least Privilege   | Tailor access precisely to what’s needed                        |
| 📁 Versioning & Tags | You can manage, tag, and version your policies                  |
| 🔁 Reusable          | Can be attached to multiple users, roles, or groups             |

---

## 🧭 Step-by-Step: Create a Customer Managed Policy (AWS Console)

### 🎯 Use Case: Allow only **S3 List and Read access** to a specific bucket

---

### 🛠 Steps:

1. Go to **IAM Console → Policies**
2. Click **Create Policy**
3. Choose **JSON** tab
4. Paste the following policy:

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
        "arn:aws:s3:::my-bucket-name",
        "arn:aws:s3:::my-bucket-name/*"
      ]
    }
  ]
}
```

5. Click **Next: Tags** → (Optional)
6. Click **Next: Review**
7. Name it: `CustomS3ReadOnly`
8. Click **Create Policy**

---

### 🧲 Attach the Custom Policy

1. IAM Console → **Users** (or **Roles** or **Groups**)
2. Select a user (e.g., `dev-user`)
3. Go to **Permissions** → **Add permissions**
4. Choose **Attach policies directly**
5. Search for `CustomS3ReadOnly`
6. Select → Click **Add permissions**

✅ Now this user can only list and read from a specific S3 bucket.

---

## 🧠 Examples of Common Customer Managed Policies

| Use Case                       | Policy Example                            |
| ------------------------------ | ----------------------------------------- |
| Allow EC2 start/stop only      | `ec2:StartInstances`, `ec2:StopInstances` |
| Restrict access to 1 S3 bucket | `s3:*` for a specific ARN                 |
| Allow full DynamoDB access     | `dynamodb:*`                              |
| Allow read/write to SQS queues | `sqs:SendMessage`, `sqs:ReceiveMessage`   |

---

### 🛠 Another JSON Example – Start/Stop EC2 only

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "StartStopInstances",
      "Effect": "Allow",
      "Action": [
        "ec2:StartInstances",
        "ec2:StopInstances"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## 🔁 Versions & Tags (Advanced Feature)

* Customer Managed Policies support **versioning**
* You can track changes and roll back if needed
* Tag policies for environments, projects, or auditing

---

## 🆚 **AWS Managed vs. Customer Managed Policies**

| Feature            | AWS Managed Policies                    | Customer Managed Policies              |
| ------------------ | --------------------------------------- | -------------------------------------- |
| 🛠 Created By      | AWS                                     | You (account admin)                    |
| ✏️ Editable        | ❌ No                                    | ✅ Yes                                  |
| 🔧 Customizable    | ❌ No                                    | ✅ Fully customizable                   |
| 🆙 Updated         | ✅ Automatically by AWS                  | ❌ You maintain                         |
| 🏷 Taggable        | ❌ No                                    | ✅ Yes                                  |
| 💾 Versioning      | ❌ No                                    | ✅ Yes                                  |
| 🔐 Least Privilege | ❌ Often too broad                       | ✅ Precise control                      |
| 📦 Examples        | `AmazonEC2FullAccess`, `ReadOnlyAccess` | `CustomEC2StartStop`, `CustomS3Access` |

---

## 🔍 When to Use Which?

| Scenario                                    | Best Option        |
| ------------------------------------------- | ------------------ |
| Quick setup or testing                      | ✅ AWS Managed      |
| Production access with fine-grained control | ✅ Customer Managed |
| Need tag/resource-level conditions          | ✅ Customer Managed |
| One-size-fits-all team access               | ✅ AWS Managed      |
| Compliance or security auditing             | ✅ Customer Managed |

---

## 🧠 Best Practices for Customer Managed Policies

* 🔒 Follow **least privilege** principle
* 📑 Use **naming conventions** (e.g., `DevTeam-S3Access`)
* 📁 Group reusable permissions into one policy
* 🔍 Audit permissions regularly with IAM **Access Advisor**
* 🧪 Test with **Access Analyzer** to see effective permissions

---

## ✅ Summary

| Feature      | Description                                                   |
| ------------ | ------------------------------------------------------------- |
| Policy Type  | Customer Managed                                              |
| Customizable | ✅ Yes (full control)                                          |
| Common Use   | Restrict access, tag-based permissions, resource-scoped roles |
| Where to Use | IAM users, roles, groups                                      |
| Example      | Limit EC2 to Start/Stop only                                  |

---

 Here are **realistic IAM policy use cases tailored specifically for DevOps and Site Reliability Engineering (SRE) teams**, aligned with **best practices** in cloud-native environments.

---

## 🧰 **IAM Policy Use Cases for DevOps/SRE Teams**

| 🧑‍💻 Role | 🎯 Use Case | ✅ IAM Permissions Required |
| ---------- | ----------- | -------------------------- |

### 1. 🏗 **Provision EC2, EBS, VPC resources**

DevOps engineers commonly need to launch infrastructure.

```json
{
  "Action": [
    "ec2:*",
    "elasticloadbalancing:*",
    "autoscaling:*",
    "cloudwatch:*",
    "iam:PassRole"
  ],
  "Resource": "*",
  "Effect": "Allow"
}
```

> 🔐 **Restrict `iam:PassRole`** to only trusted roles (e.g., Terraform EC2 role).

---

### 2. 🚀 **Deploy code using CodePipeline, CodeBuild, CodeDeploy**

Enable CI/CD tool access for pipelines.

```json
{
  "Action": [
    "codecommit:*",
    "codepipeline:*",
    "codedeploy:*",
    "codebuild:*",
    "s3:GetObject",
    "s3:PutObject",
    "iam:PassRole"
  ],
  "Resource": "*",
  "Effect": "Allow"
}
```

> ✅ Attach this to Jenkins/CodePipeline/Deploy role.

---

### 3. 📦 **Docker Registry Access (ECR)**

Allow Docker image push/pull.

```json
{
  "Action": [
    "ecr:GetAuthorizationToken",
    "ecr:BatchCheckLayerAvailability",
    "ecr:GetDownloadUrlForLayer",
    "ecr:PutImage",
    "ecr:InitiateLayerUpload",
    "ecr:UploadLayerPart",
    "ecr:CompleteLayerUpload"
  ],
  "Resource": "*",
  "Effect": "Allow"
}
```

> 🎯 Attach this to the CI/CD agent (e.g., GitLab Runner, Jenkins agent).

---

### 4. 📊 **Access CloudWatch for Monitoring & Logs**

Enable DevOps to view logs, metrics, alarms.

```json
{
  "Action": [
    "cloudwatch:DescribeAlarms",
    "cloudwatch:GetMetricData",
    "logs:DescribeLogGroups",
    "logs:GetLogEvents",
    "logs:FilterLogEvents"
  ],
  "Resource": "*",
  "Effect": "Allow"
}
```

> ✅ Ideal for SRE dashboards or observability teams.

---

### 5. ☁️ **EKS Cluster Access for Kubernetes DevOps**

Used by DevOps to interact with Kubernetes.

```json
{
  "Action": [
    "eks:DescribeCluster",
    "eks:ListClusters",
    "eks:UpdateClusterConfig",
    "eks:AccessKubernetesApi"
  ],
  "Resource": "*",
  "Effect": "Allow"
}
```

> 🔧 Combine this with **RBAC mapping inside the EKS cluster**.

---

### 6. 📚 **Manage Terraform State (S3 + DynamoDB)**

Enable S3 and DynamoDB backend access.

```json
{
  "Action": [
    "s3:GetObject",
    "s3:PutObject",
    "s3:ListBucket",
    "dynamodb:PutItem",
    "dynamodb:GetItem",
    "dynamodb:DeleteItem",
    "dynamodb:UpdateItem"
  ],
  "Resource": [
    "arn:aws:s3:::my-terraform-backend/*",
    "arn:aws:dynamodb:ap-south-1:123456789012:table/terraform-locks"
  ],
  "Effect": "Allow"
}
```

> 💡 Replace ARNs with your actual backend bucket and table.

---

### 7. 🔐 **Temporary EC2 Access for Debugging**

Allow starting/stopping/debugging instances, not termination.

```json
{
  "Action": [
    "ec2:StartInstances",
    "ec2:StopInstances",
    "ec2:DescribeInstances",
    "ssm:StartSession",
    "ssm:DescribeSessions",
    "ssm:TerminateSession"
  ],
  "Resource": "*",
  "Effect": "Allow"
}
```

> ✅ Use SSM Session Manager for secure, auditable access instead of SSH.

---

### 8. 📤 **Manage Route 53 for DNS Automation**

Let DevOps update DNS records (for ingress or ALB changes).

```json
{
  "Action": [
    "route53:ChangeResourceRecordSets",
    "route53:GetHostedZone",
    "route53:ListResourceRecordSets"
  ],
  "Resource": "*",
  "Effect": "Allow"
}
```

---

### 9. 🧪 **Lambda Function Deployment**

Grant permissions to deploy or update Lambda functions.

```json
{
  "Action": [
    "lambda:CreateFunction",
    "lambda:UpdateFunctionCode",
    "lambda:UpdateFunctionConfiguration",
    "lambda:GetFunction",
    "iam:PassRole"
  ],
  "Resource": "*",
  "Effect": "Allow"
}
```

> 🔐 Use `iam:PassRole` with a condition limiting allowed roles.

---

### 10. 📋 **Read-Only View for Audit or Compliance**

Allow SRE to audit configurations and logs.

```json
{
  "Action": "*",
  "Resource": "*",
  "Effect": "Allow",
  "Condition": {
    "StringEquals": {
      "aws:RequestedRegion": "ap-south-1"
    }
  }
}
```

> ✅ Or just attach `ReadOnlyAccess` AWS Managed Policy.

---

## ⚙️ How It Works

Pick your **DevOps task** below. I’ll give you:

* ✅ JSON IAM policy (least privilege)
* 🧾 Description of what it does
* 💡 What to customize (like ARNs or tags)

---

### 🧪 1. **Start/Stop EC2 Instances**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:StartInstances",
        "ec2:StopInstances",
        "ec2:DescribeInstances"
      ],
      "Resource": "*"
    }
  ]
}
```

🔎 *Use for: On-demand dev server management*

---

### 📦 2. **Push/Pull Images to Amazon ECR**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:InitiateLayerUpload",
        "ecr:PutImage",
        "ecr:CompleteLayerUpload"
      ],
      "Resource": "*"
    }
  ]
}
```

🔎 *Use for: Docker build and push from CI/CD*

---

### 📦 3. **Read/Write S3 Bucket (Scoped)**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-devops-artifacts",
        "arn:aws:s3:::my-devops-artifacts/*"
      ]
    }
  ]
}
```

🔧 Replace `my-devops-artifacts` with your bucket name.

---

### 🔍 4. **View CloudWatch Logs and Metrics**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudwatch:GetMetricData",
        "cloudwatch:ListMetrics",
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams",
        "logs:GetLogEvents",
        "logs:FilterLogEvents"
      ],
      "Resource": "*"
    }
  ]
}
```

🔎 *Use for: Monitoring or observability dashboards*

---

### ⚙️ 5. **Deploy Lambda Functions**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "lambda:UpdateFunctionCode",
        "lambda:UpdateFunctionConfiguration",
        "lambda:GetFunction",
        "iam:PassRole"
      ],
      "Resource": "*"
    }
  ]
}
```

💡 Scope `iam:PassRole` using `Condition` (optional):

```json
"Condition": {
  "StringEquals": {
    "iam:PassedToService": "lambda.amazonaws.com"
  }
}
```

---

### 🛠 6. **Run Terraform (S3 + DynamoDB for State)**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:GetObject",
        "s3:PutObject",
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:DeleteItem",
        "dynamodb:UpdateItem"
      ],
      "Resource": [
        "arn:aws:s3:::my-terraform-state/*",
        "arn:aws:s3:::my-terraform-state",
        "arn:aws:dynamodb:ap-south-1:123456789012:table/terraform-lock"
      ]
    }
  ]
}
```

📝 Replace with your actual bucket/table ARNs.

---

### 📤 7. **Update DNS in Route 53**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "route53:ChangeResourceRecordSets",
        "route53:ListResourceRecordSets",
        "route53:GetHostedZone"
      ],
      "Resource": "*"
    }
  ]
}
```

🔎 *Use for: Ingress/DNS automation during deployments*

---

### 🧾 8. **CloudFormation Stack Deployment**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudformation:CreateStack",
        "cloudformation:UpdateStack",
        "cloudformation:DescribeStacks",
        "cloudformation:DeleteStack"
      ],
      "Resource": "*"
    }
  ]
}
```

🔧 Scope to stack ARNs if needed.

---

## 💡 Add-on Options

You can combine these base policies with:

### ✅ MFA Enforcement (Optional)

```json
"Condition": {
  "Bool": {
    "aws:MultiFactorAuthPresent": "true"
  }
}
```

### ✅ Tag-Based Access Control (Optional)

```json
"Condition": {
  "StringEquals": {
    "aws:ResourceTag/Environment": "dev"
  }
}
```

---

## 📦 Want Terraform Output?

Here’s how to wrap any of the above JSON into a **Terraform IAM Policy**:

```hcl
resource "aws_iam_policy" "devops_s3_access" {
  name        = "DevOpsS3Access"
  description = "Access to DevOps S3 bucket"
  policy      = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = [
          "arn:aws:s3:::my-devops-artifacts/*"
        ]
      }
    ]
  })
}
```

---

## ✅ Summary

| Task                   | Use IAM Policy           |
| ---------------------- | ------------------------ |
| EC2 management         | Start/Stop/Describe only |
| CI/CD image push       | ECR push/pull            |
| S3 backend (Terraform) | Scoped S3 + DynamoDB     |
| Logs monitoring        | CloudWatch read-only     |
| Lambda deploy          | UpdateCode + PassRole    |
| DNS updates            | Route53 scoped access    |

---


## 🧠 IAM Strategy Tips for DevOps/SRE

* 🔐 Use **IAM Roles** instead of Users wherever possible (especially for automation)
* ✅ Use **Customer Managed Policies** with **least privilege**
* 💡 Use **tag-based access control** to isolate by environment (e.g., only access `Environment:Dev`)
* 🔎 Use **IAM Access Analyzer** to validate policy scope
* 🔁 Rotate access keys and **enable MFA**

---

## 🔐 **Best Practices for IAM Policies in a Multi-Account AWS Setup**

---

### 1. 🏢 **Use AWS Organizations with Service Control Policies (SCPs)**

| ✅ Best Practice                                  | 💡 Why It Matters                                                                                   |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| Use **SCPs** to set **permission guardrails**    | Prevent users in child accounts from performing restricted actions (e.g., `ec2:TerminateInstances`) |
| Apply SCPs **at OU (Organizational Unit)** level | Different accounts (e.g., Dev, Prod, Audit) can have different controls                             |

📌 **Example**: Deny all actions outside `ap-south-1`

```json
{
  "Effect": "Deny",
  "Action": "*",
  "Resource": "*",
  "Condition": {
    "StringNotEquals": {
      "aws:RequestedRegion": "ap-south-1"
    }
  }
}
```

---

### 2. 🧭 **Centralize Identity with AWS IAM Identity Center (SSO)**

| ✅ Strategy                                                                           | 🔒 Benefit                                                     |
| ------------------------------------------------------------------------------------ | -------------------------------------------------------------- |
| Use **IAM Identity Center (formerly AWS SSO)** for centralized user/group management | Avoid managing users in every account                          |
| Assign **Permission Sets** per account/OU                                            | Scalable and role-based access (DevOps, Viewer, Billing, etc.) |
| Integrate with **Azure AD/Okta/Gsuite**                                              | Use existing identity providers (via SAML or OIDC)             |

---

### 3. 🔐 **Use IAM Roles Instead of IAM Users in Member Accounts**

| Practice                                                                      | Reason                                                  |
| ----------------------------------------------------------------------------- | ------------------------------------------------------- |
| Use IAM roles for humans and automation                                       | IAM users are harder to govern across accounts          |
| Federate users via Identity Center → assume roles                             | Easier auditing and better temporary credential hygiene |
| Use `sts:AssumeRole` to access member accounts from a central tooling account | Allows **centralized access with cross-account trust**  |

---

### 4. 🧩 **Define and Attach Fine-Grained IAM Policies**

| ✅ Use Case                                    | IAM Strategy                                                   |
| --------------------------------------------- | -------------------------------------------------------------- |
| DevOps can launch EC2 but not delete VPCs     | Create scoped **customer-managed policies** and attach to role |
| SRE can access CloudWatch, but only read logs | Grant `logs:GetLogEvents`, `cloudwatch:GetMetricData` etc.     |
| Developers only access `dev` prefixed buckets | Use **condition keys** like `s3:prefix` or resource ARNs       |

---

### 5. 🛡️ **Set Up Permission Boundaries**

Use **permission boundaries** to control **max permissions** even if a user or automation tries to overreach.

📌 Example: Bound all developer-created roles to only manage `dev` resources

```json
{
  "Effect": "Allow",
  "Action": "*",
  "Resource": "arn:aws:s3:::dev-*"
}
```

---

### 6. 🏷️ **Use Tags for IAM Access Control**

| Best Practice                                                                 | Use                                                                    |
| ----------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Tag AWS resources (e.g., EC2, S3, Lambda) with `Environment`, `Team`, `Owner` | Enables **tag-based IAM policies**                                     |
| Tag IAM roles and users for visibility                                        | Use conditions in policies like `"aws:ResourceTag/Environment": "dev"` |

---

### 7. 📑 **Logging & Auditing with CloudTrail and Access Analyzer**

| Tool                    | Purpose                                                            |
| ----------------------- | ------------------------------------------------------------------ |
| **CloudTrail**          | Tracks all IAM-related changes across all accounts                 |
| **IAM Access Analyzer** | Detects public, cross-account, or third-party access               |
| **Config Rules**        | Monitor changes to IAM roles, policies, or account root user usage |

---

### 8. 🧪 **Use ReadOnlyAccess for Auditors and Exploratory Users**

Avoid giving write access unless needed. AWS Managed `ReadOnlyAccess` policy is great for:

* Security auditors
* Finance/Billing teams
* External consultants

---

### 9. 🧬 **Follow the Least Privilege Model**

| Practice                                                                           | Why                                                                 |
| ---------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Grant only the permissions needed, and nothing more                                | Reduces blast radius                                                |
| Use job-role-based policies like `DevOpsRole`, `ObserverRole`, `SecurityAdminRole` | Maps well to real org structure                                     |
| Periodically **review and remove unused permissions**                              | Use **IAM Access Advisor** or **CloudTrail insights** for reference |

---

### 10. 🛠️ **Implement Automation (CI/CD) with Scoped IAM Roles**

| Component                | IAM Strategy                                                      |
| ------------------------ | ----------------------------------------------------------------- |
| Jenkins / GitHub Actions | Create scoped IAM role with `sts:AssumeRole` from central account |
| Terraform                | Use `iam:PassRole` + resource-level access for VPC, EC2, S3, etc. |
| Lambda Functions         | Attach **execution roles** with only required permissions         |

---

## 🧾 Example: Multi-Account Role Trust for Central DevOps Account

In **target account** (e.g., prod), define a role `ProdReadOnlyRole`:

```json
{
  "Effect": "Allow",
  "Principal": {
    "AWS": "arn:aws:iam::123456789012:root"  // Central DevOps account ID
  },
  "Action": "sts:AssumeRole"
}
```

Then allow DevOps users in the central account to assume this role for read-only tasks.

---

## ✅ Summary Table

| Strategy              | Benefit                            |
| --------------------- | ---------------------------------- |
| SCPs                  | Account-level control (deny/allow) |
| IAM Identity Center   | Central user/group-based access    |
| IAM Roles             | Temporary, secure, scalable        |
| Fine-grained policies | Restrict per environment/resource  |
| Permission boundaries | Cap delegated permissions          |
| Tags                  | Dynamic access control             |
| Audit tools           | Ensure visibility and governance   |

---





