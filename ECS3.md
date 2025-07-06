![image](https://github.com/user-attachments/assets/63261f0b-92c6-4da9-8daa-f3c28daf4e71)

![image](https://github.com/user-attachments/assets/556ba8f9-e029-4787-b951-db5515d07cba)

![image](https://github.com/user-attachments/assets/ddf4f20f-9967-4058-9de6-cbe7792c51d9)

---

# **Complete guide to adding EC2 infrastructure to an ECS Cluster** — step-by-step for both:

* ✅ **AWS Console**
* ✅ **AWS CLI**

This lets ECS run containers on **EC2 instances** instead of (or in addition to) Fargate.

---

## 🔍 Why Add EC2 Infrastructure to ECS?

ECS EC2 launch type gives you:

* Full control over the underlying instances (custom AMIs, GPU, EBS, etc.)
* Spot instance usage
* Consistent workloads with fixed cost

---

## 🔧 PART 1: Using **AWS Console**

### ✅ Prerequisites:

* A running **ECS Cluster** (e.g., `deepak-ec2-cluster`)
* A **VPC with public subnet**
* A **Key Pair** (for SSH access to EC2)
* A **Security Group** (allowing ports 22 and 80)

---

### 🧱 Step-by-Step (Console)

---

### 1️⃣ Create or Use an Existing ECS Cluster

* Go to **ECS → Clusters → Create Cluster**
* Select **EC2 Linux + Networking**
* Enter:

  * Cluster name: `deepak-ec2-cluster`
  * Instance type: `t2.micro` or `t3.medium`
  * Number of instances: `1` or more
  * Key Pair: Select your key (for SSH)
  * Networking: Choose your VPC, public subnet
  * Security Group: One that allows port **22**, **80**, **443**
* Click **Create**

ECS will **launch EC2 instances** using the **Amazon ECS-optimized AMI** with ECS agent pre-installed.

Once launched:

* Go to the **cluster → ECS Instances** → You’ll see EC2 registered ✅

---

### 2️⃣ Manually Add EC2 Instance (if needed later)

You can also manually launch an EC2 instance and register it to ECS.

#### EC2 Launch Steps:

* Launch EC2 → Choose **Amazon ECS-optimized Amazon Linux 2 AMI**
* Instance Type: e.g., `t3.micro`
* Network: Choose ECS-compatible VPC and subnet
* IAM Role: Attach an **instance profile with `AmazonEC2ContainerServiceforEC2Role`**
* User data script (register to cluster):

```bash
#!/bin/bash
echo ECS_CLUSTER=deepak-ec2-cluster >> /etc/ecs/ecs.config
```

* Security Group: allow ports **22**, **80**, and **443**

---

## 🖥️ PART 2: Using **AWS CLI**

---

### ✅ Prerequisites:

* IAM Role: `ecsInstanceRole` (create if it doesn’t exist)
* ECS Cluster already created via CLI:

```bash
aws ecs create-cluster --cluster-name deepak-ec2-cluster
```

---

### 1️⃣ Create IAM Instance Profile (Only once)

```bash
aws iam create-role --role-name ecsInstanceRole \
  --assume-role-policy-document file://<(cat <<EOF
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Service": "ec2.amazonaws.com" },
    "Action": "sts:AssumeRole"
  }]
}
EOF
)
```

Attach ECS policy:

```bash
aws iam attach-role-policy \
  --role-name ecsInstanceRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role
```

Create instance profile:

```bash
aws iam create-instance-profile --instance-profile-name ecsInstanceProfile
aws iam add-role-to-instance-profile --instance-profile-name ecsInstanceProfile --role-name ecsInstanceRole
```

---

### 2️⃣ Launch EC2 Instance with ECS Config

```bash
aws ec2 run-instances \
  --image-id ami-0de7ac6a527b6b0a6 \  # ECS Optimized Amazon Linux 2 in ap-south-1
  --instance-type t3.micro \
  --iam-instance-profile Name=ecsInstanceProfile \
  --key-name my-keypair \
  --security-group-ids sg-xxxxxxx \
  --subnet-id subnet-xxxxxxx \
  --user-data file://<(cat <<EOF
#!/bin/bash
echo ECS_CLUSTER=deepak-ec2-cluster >> /etc/ecs/ecs.config
EOF
)
```

✅ The instance will register with ECS after boot (check ECS Console → Cluster → ECS Instances)

---

## 🔎 Verify EC2 is Added to ECS Cluster

In ECS Console:

* Go to `deepak-ec2-cluster`
* Click **"ECS Instances"** tab
* You should see 1 or more EC2s listed as “ACTIVE”

Now you can deploy ECS **EC2 launch type tasks** to this cluster.

---

## 📌 Summary Table

| Step                | Console                                       | CLI                                                   |
| ------------------- | --------------------------------------------- | ----------------------------------------------------- |
| Create Cluster      | ECS → Create Cluster → EC2 Linux + Networking | `aws ecs create-cluster --cluster-name <name>`        |
| Launch EC2 for ECS  | Select ECS-optimized AMI, configure User Data | `aws ec2 run-instances` with userdata and IAM profile |
| Attach IAM Role     | `ecsInstanceRole` via EC2 Console UI          | Create + attach via CLI commands                      |
| Register EC2 to ECS | Automatic via AMI or UserData                 | User data script with `ECS_CLUSTER=name`              |

---

I already have an **ECS cluster** created without EC2 infrastructure. Now I want to **manually add EC2 instances** to that cluster so I can run EC2 launch type tasks.”

Here's how to **explicitly add EC2 instances** to an existing ECS cluster, both via:

---

![image](https://github.com/user-attachments/assets/4b58338e-47d4-4ec4-9996-b08355dcc12b)

![image](https://github.com/user-attachments/assets/a6397723-e29f-448e-b3ee-f83ccd99546b)

![image](https://github.com/user-attachments/assets/f3b108d4-9002-40b0-bacb-428c7eb61f8a)

![image](https://github.com/user-attachments/assets/66e0e4e5-1e62-4964-8b67-a21e58b9e9ae)

![image](https://github.com/user-attachments/assets/6fdcf19d-1070-41a1-807a-8edcd31e144d)



## ✅ Step-by-Step: Add EC2 to Existing ECS Cluster (Console & CLI)

Let’s assume your existing ECS cluster is named: `deepak-ec2-cluster`

---

## 🔷 A. Using **AWS Console**

### 1️⃣ Launch an EC2 Instance

* Go to **EC2 → Launch Instance**
* Name: `ecs-node-deepak`
* **AMI**: Choose **Amazon ECS-Optimized Amazon Linux 2 AMI**

  🔍 To find:

  * Go to **Community AMIs** and search: `ECS-Optimized Amazon Linux 2`

### 2️⃣ Choose Instance Type

* Select `t3.micro` or higher (for basic workloads)

### 3️⃣ Configure Network

* Choose:

  * Your existing **VPC**
  * A **public subnet** if you want public access
* Enable **Auto-assign public IP** ✅

### 4️⃣ Attach IAM Role

* Create or choose IAM Role: `ecsInstanceRole`

  It must have **this policy** attached:

  * `AmazonEC2ContainerServiceforEC2Role`

> If you don’t have it, create a new role in IAM:
>
> * Trusted entity: **EC2**
> * Permission: `AmazonEC2ContainerServiceforEC2Role`

### 5️⃣ Add **User Data** (VERY IMPORTANT)

In **Advanced → User Data**, paste:

```bash
#!/bin/bash
echo ECS_CLUSTER=deepak-ec2-cluster >> /etc/ecs/ecs.config
```

This command registers the EC2 instance with your existing ECS cluster.

### 6️⃣ Configure Storage and Security Group

* Security Group:

  * Allow ports **22 (SSH)**, **80 (HTTP)** if your task is web-based
  * Attach your **key pair**

### 7️⃣ Launch

* Click **Launch Instance**

---

### 🔎 Verify

* Wait 2–3 minutes
* Go to **ECS → Clusters → deepak-ec2-cluster → ECS Instances**
* You should see the EC2 node in “ACTIVE” state ✅

---

## 🔷 B. Using **AWS CLI**

### 1️⃣ Get Latest ECS-Optimized AMI ID (Optional)

```bash
aws ssm get-parameters-by-path \
  --path /aws/service/ecs/optimized-ami/amazon-linux-2/recommended \
  --query "Parameters[?Name=='/aws/service/ecs/optimized-ami/amazon-linux-2/recommended/image_id'].Value" \
  --output text
```

Let’s say AMI = `ami-0de7ac6a527b6b0a6`

---

### 2️⃣ Launch EC2 with Proper Config

```bash
aws ec2 run-instances \
  --image-id ami-0de7ac6a527b6b0a6 \
  --count 1 \
  --instance-type t3.micro \
  --key-name deepak-keypair \
  --subnet-id subnet-xxxxxxx \
  --security-group-ids sg-xxxxxxx \
  --iam-instance-profile Name=ecsInstanceProfile \
  --user-data file://<(cat <<EOF
#!/bin/bash
echo ECS_CLUSTER=deepak-ec2-cluster >> /etc/ecs/ecs.config
EOF
)
```

> Make sure:
>
> * The **IAM instance profile** `ecsInstanceProfile` exists and includes the `ecsInstanceRole`
> * Subnet and SG are correct

---

### 🔎 Verify (Again)

```bash
aws ecs list-container-instances --cluster deepak-ec2-cluster
```

You should see the container instance ID listed.

---

## 📌 Summary

| Task                      | Console                                    | CLI                             |
| ------------------------- | ------------------------------------------ | ------------------------------- |
| Launch EC2                | EC2 → Launch Instance                      | `aws ec2 run-instances`         |
| Use ECS Optimized AMI     | Select from AMI dialog                     | Get AMI via SSM Parameter Store |
| Attach IAM Role           | `ecsInstanceRole` with correct permissions | `--iam-instance-profile`        |
| Add ECS Cluster Name      | Via User Data: `echo ECS_CLUSTER=...`      | Same using `--user-data`        |
| Register with ECS Cluster | ECS Agent auto-registers                   | ECS Agent auto-registers        |

---



You're referring to the **IAM role and instance profile setup** required to allow an **EC2 instance to join an ECS cluster**.

Let’s break it down and explain **both CLI and Console steps**.

---

## 🔍 What is this for?

This process creates an **IAM Role** and an **Instance Profile** so that your EC2 instance can:

* Communicate with ECS
* Register itself to an ECS cluster
* Download and run containers using the ECS Agent

Without this, ECS agent on EC2 **cannot connect** to ECS control plane.

---

## 🔧 CLI Breakdown

### 1️⃣ **Create IAM Role (ecsInstanceRole)**

```bash
aws iam create-role --role-name ecsInstanceRole \
  --assume-role-policy-document file://<(cat <<EOF
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Service": "ec2.amazonaws.com" },
    "Action": "sts:AssumeRole"
  }]
}
EOF
)
```

🧠 This creates a role trusted by EC2 (allows EC2 to "assume" the role).

---

### 2️⃣ **Attach Policy to Role**

```bash
aws iam attach-role-policy \
  --role-name ecsInstanceRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role
```

✅ This gives permission for ECS agent to:

* Connect to ECS
* Pull container images
* Send logs/metrics, etc.

---

### 3️⃣ **Create Instance Profile**

```bash
aws iam create-instance-profile --instance-profile-name ecsInstanceProfile
aws iam add-role-to-instance-profile --instance-profile-name ecsInstanceProfile --role-name ecsInstanceRole
```

🧠 EC2 can only use **Instance Profiles**, not IAM Roles directly — this step binds the role to a usable EC2-compatible profile.

---

## 🖥️ Do the Same via AWS Console

---

### ✅ Steps to Create IAM Role (Console)

#### Step 1: Go to IAM Console

URL: [https://console.aws.amazon.com/iam](https://console.aws.amazon.com/iam)

#### Step 2: Click **Roles** → **Create Role**

* **Trusted Entity**: Choose **AWS service**
* **Use Case**: Choose **EC2**
* Click **Next**

---

#### Step 3: Attach Permissions

* Search for: `AmazonEC2ContainerServiceforEC2Role`
* ✅ Check it
* Click **Next**

---

#### Step 4: Name the Role

* Role Name: `ecsInstanceRole`
* Description: *(optional)*
* Click **Create Role**

---

### 🔄 Behind the scenes:

This automatically creates the **trust relationship**:

```json
{
  "Effect": "Allow",
  "Principal": {
    "Service": "ec2.amazonaws.com"
  },
  "Action": "sts:AssumeRole"
}
```

---

### ✅ Steps to Attach Role to EC2 (via Instance Profile)

When you launch a new EC2 instance:

1. Go to **EC2 → Launch Instance**
2. Under **Advanced Details → IAM Role**
3. Select the `ecsInstanceRole` from dropdown

✔️ That’s your instance profile — AWS automatically binds the role to a usable instance profile when done via Console.

---

### 📝 Bonus: View Trust Relationship (Console)

* IAM → Roles → `ecsInstanceRole` → **Trust relationships** tab
* You’ll see it says EC2 can assume the role

---

## ✅ Summary

| Step                    | CLI Command                       | Console Equivalent                        |
| ----------------------- | --------------------------------- | ----------------------------------------- |
| Create IAM Role         | `aws iam create-role`             | IAM → Roles → Create Role                 |
| Attach ECS Policy       | `aws iam attach-role-policy`      | Add `AmazonEC2ContainerServiceforEC2Role` |
| Create Instance Profile | `aws iam create-instance-profile` | Auto-handled in Console                   |
| Attach Role to EC2      | Use `--iam-instance-profile`      | Select IAM Role during EC2 launch         |

---




