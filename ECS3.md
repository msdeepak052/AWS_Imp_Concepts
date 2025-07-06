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


# **Amazon ECS Task**
---

## 🔍 What is an **ECS Task**?

An **ECS Task** is the **running instance of a Task Definition** in a specific ECS cluster.

* It's like a **pod in Kubernetes**.
* A Task can contain **1 or more containers** that run together.
* You **cannot run a task** without first defining a **Task Definition**.

---

## 📦 Components of an ECS Task

| Component           | Description                                                      |
| ------------------- | ---------------------------------------------------------------- |
| **Task Definition** | Blueprint: container image, CPU, memory, env vars, volumes, etc. |
| **Task**            | Live copy (runtime instance) of a Task Definition                |
| **Launch Type**     | Fargate (serverless) or EC2 (your own infra)                     |
| **Networking**      | VPC, subnets, security groups, IAM roles                         |
| **Logs & Secrets**  | Logs to CloudWatch, inject secrets via SSM or Secrets Manager    |

---

## 💡 Real Example Use Case

> You want to run a Node.js web API on ECS using Fargate.
> You will:

* Create a Task Definition pointing to a Docker image like `node:18-alpine`
* Run it as a Task using the `FARGATE` launch type

---

## 🔧 PART A: Setup via **AWS Console**

---

### 1️⃣ Create Task Definition

1. Go to **ECS → Task Definitions → Create new Task Definition**

2. Select **FARGATE** (or EC2 if you use EC2 cluster)

3. Fill the following:

   * **Task Definition Name**: `deepak-task`
   * **Task Role**: (optional unless using IAM)
   * **Network Mode**: `awsvpc` (required for Fargate)

4. Under **Container Definitions**:

   * Click **Add container**
   * **Container name**: `deepak-app`
   * **Image**: `nginx` (or your app image)
   * **Port mappings**: `80`

5. Optional:

   * Logging (CloudWatch)
   * Secrets (from SSM or Secrets Manager)
   * Env variables

6. Click **Create**

✅ Your task definition is ready!

---

### 2️⃣ Run the Task

1. Go to **ECS → Clusters → YourCluster → Tasks → Run new Task**
2. Select:

   * Launch Type: `FARGATE` or `EC2`
   * Task Definition: `deepak-task`
   * Cluster: `deepak-cluster`
   * Platform version: `LATEST`
3. Configure **Networking**:

   * VPC
   * Subnet (public for internet)
   * Assign public IP ✅
   * Security group (allow port 80)
4. Click **Run Task**

⏳ Wait a few seconds — go to **Tasks tab** to see it running!

---

### 🔍 Check It Works

If it’s using public IP and running NGINX:

* Copy public IP → open in browser → you’ll see default **Welcome to nginx!**

---

## 🖥️ PART B: Setup via **AWS CLI**

---

### ✅ 1. Register Task Definition

Create a JSON file `deepak-task-def.json`:

```json
{
  "family": "deepak-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "deepak-container",
      "image": "nginx",
      "portMappings": [
        {
          "containerPort": 80,
          "protocol": "tcp"
        }
      ],
      "essential": true
    }
  ]
}
```

Register the task definition:

```bash
aws ecs register-task-definition \
  --cli-input-json file://deepak-task-def.json
```

---

### ✅ 2. Run Task (FARGATE Launch Type)

```bash
aws ecs run-task \
  --cluster deepak-cluster \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-abc123],securityGroups=[sg-xyz456],assignPublicIp=ENABLED}" \
  --task-definition deepak-task
```

> Replace `subnet-abc123` and `sg-xyz456` with real subnet ID and security group ID.

---

### 🔍 Monitor Task

```bash
aws ecs list-tasks --cluster deepak-cluster
```

To describe:

```bash
aws ecs describe-tasks --cluster deepak-cluster --tasks <task-id>
```

---

## 📌 Summary Table

| Task                   | Console                              | CLI                                |
| ---------------------- | ------------------------------------ | ---------------------------------- |
| Create Task Definition | ECS → Task Definitions → Create      | `aws ecs register-task-definition` |
| Run Task               | ECS → Cluster → Tasks → Run new task | `aws ecs run-task`                 |
| Networking             | VPC + Subnet + Public IP             | `--network-configuration`          |
| Logs                   | CloudWatch (via UI)                  | Part of task definition JSON       |
| Image                  | `nginx`, `node`, etc.                | `image: "nginx"`                   |

---
# **Amazon ECS Services**


---

## 🔍 What is an **ECS Service**?

An **ECS Service** is a **long-running controller** that:

| Feature                      | Description                                     |
| ---------------------------- | ----------------------------------------------- |
| 👷 Keeps tasks running       | Automatically restarts tasks if they stop/crash |
| 📈 Scales automatically      | Can scale task count based on demand            |
| 🌍 Load Balancer integration | Can register tasks with ALB, NLB                |
| 🧠 Works with Fargate or EC2 | Supports both launch types                      |

A service **wraps around your Task Definition** to ensure it's always running as expected.

---

## 📦 ECS Architecture (Service + Task)

```
[ ECS Cluster ]
     │
┌────┴────────┐
│ ECS Service │  → Manages long-running Tasks
└────┬────────┘
     │
┌────▼──────────────────────┐
│ Task (from Task Definition) │
│ └─ Container: nginx/node   │
└──────────────────────────┘
```

---

## 🎯 Real Use Case

> You're running a production **Node.js web API** that must always stay online with 2 replicas behind a Load Balancer.

* You’ll create a **Task Definition** that defines the container.
* Then, launch an **ECS Service** that:

  * Runs 2 tasks
  * Registers them to ALB target group

---

## 🔧 PART A: Step-by-Step via **AWS Console**

---

### ✅ 1. Pre-setup Checklist

* ✅ Existing ECS cluster (`deepak-cluster`)
* ✅ A registered Task Definition (`deepak-task`)
* ✅ VPC, public subnets
* ✅ (Optional) Application Load Balancer created

---

### ✅ 2. Create an ECS Service

1. Go to **ECS → Clusters → deepak-cluster → Services → Create**

2. Choose:

* **Launch type**: `FARGATE` or `EC2`
* **Task Definition**: `deepak-task:1`
* **Service Name**: `deepak-service`
* **Number of Tasks**: e.g. `2`

3. **Networking**:

   * VPC: your existing VPC
   * Subnets: public (for internet-facing)
   * Security group: allow ports `80`, `443`

4. **Auto-assign public IP**: ✅ Enabled (for Fargate)

5. **Load Balancing (Optional but Recommended)**:

   * Select **Application Load Balancer**
   * Choose target group (create one if needed)
   * Map container port (e.g. 80) to LB

6. Logging and Auto Scaling (optional)

7. Click **Create Service**

⏳ ECS will now launch and manage 2 tasks behind the load balancer.

---

### 🔍 Verify

* Go to the Service → Tasks → You’ll see tasks running
* Copy the Load Balancer DNS → Open in browser → You should see your app (e.g., NGINX page)

---

## 🖥️ PART B: Step-by-Step via **AWS CLI**

---

### ✅ 1. Ensure Task Definition Is Registered

If not already:

```bash
aws ecs register-task-definition \
  --cli-input-json file://deepak-task-def.json
```

(See earlier response for JSON example)

---

### ✅ 2. Create ECS Service (No Load Balancer)

```bash
aws ecs create-service \
  --cluster deepak-cluster \
  --service-name deepak-service \
  --task-definition deepak-task \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-abc123],securityGroups=[sg-xyz456],assignPublicIp=ENABLED}"
```

---

### ✅ 3. Create ECS Service (WITH Load Balancer)

If using an ALB:

```bash
aws ecs create-service \
  --cluster deepak-cluster \
  --service-name deepak-service \
  --task-definition deepak-task \
  --desired-count 2 \
  --launch-type FARGATE \
  --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:...,containerName=deepak-container,containerPort=80" \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-abc123],securityGroups=[sg-xyz456],assignPublicIp=ENABLED}" \
  --health-check-grace-period-seconds 60
```

Replace the `targetGroupArn` with your ALB’s target group ARN.

---

### 🔍 Monitor Service

List services:

```bash
aws ecs list-services --cluster deepak-cluster
```

Describe service:

```bash
aws ecs describe-services \
  --cluster deepak-cluster \
  --services deepak-service
```

---

## 🧠 Summary: Tasks vs Services

| Feature       | ECS Task                     | ECS Service                          |
| ------------- | ---------------------------- | ------------------------------------ |
| Lifetime      | One-time (runs and exits)    | Long-running (managed lifecycle)     |
| Restart       | No                           | Yes (auto-restarts on failure)       |
| Scaling       | Manual                       | Auto-scaling supported               |
| Load Balancer | Not supported                | Fully supported                      |
| Use Case      | Scripts, batch jobs, testing | Production apps, APIs, microservices |

---

## ✅ Best Practices

* Use ECS Services for **stable applications** that should always be up
* Use **Application Load Balancer** for HTTP/S workloads
* Add **auto-scaling** to scale tasks based on CPU or memory
* Use **Fargate** if you don’t want to manage EC2 infra

---

# Hands-On

If your **Flask app is stored on Docker Hub**, and you want to **deploy it fully using AWS Console**, here's the **complete step-by-step guide** to deploy the app on **Amazon ECS Fargate using ECS Task + ECS Service + Load Balancer**, **100% via AWS Console**.

---

## 🧾 Assumptions

* Docker image: `devopsdktraining/tic-tac-toe-deepak:1` (from Docker Hub)
* Simple Flask app listens on port 80
* You want a load-balanced, highly available service

---

## 🔧 High-Level Flow

1. ✅ Create a VPC (if not existing)
2. ✅ Create a Security Group
3. ✅ Create an **ECS Cluster (Fargate)**
4. ✅ Create a **Task Definition**
5. ✅ Create a **Load Balancer (ALB)**
6. ✅ Create an **ECS Service** that runs the task
7. ✅ Access the app via ALB DNS name

---

## 🔄 Step-by-Step: AWS Console Only

---

### ✅ 1. Create VPC (Skip if already exists)

* Go to **VPC → Create VPC**
* Choose “**VPC + 2 public subnets**”
* Name it: `flask-ecs-vpc`
* Enable **DNS Hostnames**
* Done ✅

---

### ✅ 2. Create Security Group

* Go to **EC2 → Security Groups → Create**
* Name: `flask-ecs-sg`
* VPC: `flask-ecs-vpc`
* Inbound Rules:

  * Type: HTTP, Port 80, Source: Anywhere (0.0.0.0/0)
  * Type: SSH (optional, if needed for EC2 debugging)

---

### ✅ 3. Create ECS Cluster (Fargate)

* Go to **ECS → Clusters → Create Cluster**
* Choose: **Networking only (Fargate)**
* Name: `flask-ecs-cluster`
* Click **Create**

---

### ✅ 4. Create Task Definition

* Go to **ECS → Task Definitions → Create new task definition**
* Choose **FARGATE**
* Name: `flask-task`
* Task Role: (leave blank or create if needed)
* Task size:

  * CPU: `256 (.25 vCPU)`
  * Memory: `512 (MiB)`
* **Add container**

  * Name: `flask-container`
  * Image: `deepakyadav/flask-ecs-app:latest`
  * Port mappings: `80`

💡 Optional:

* Enable logging (CloudWatch)
* Set environment variables

Click **Create**

---

### ✅ 5. Create Application Load Balancer (ALB)

* Go to **EC2 → Load Balancers → Create**

* Choose: **Application Load Balancer**

* Name: `flask-ecs-alb`

* Scheme: **Internet-facing**

* Listeners: HTTP, Port 80

* Select your VPC

* Select 2 public subnets

* **Security Group**: Select `flask-ecs-sg`

* Target Group:

  * Name: `flask-tg`
  * Target Type: **IP**
  * Protocol: **HTTP**
  * Port: **80**
  * Health Check Path: `/`

Click **Create**

---

### ✅ 6. Create ECS Service

* Go to **ECS → Clusters → flask-ecs-cluster → Services → Create**
* Launch type: **FARGATE**
* Task Definition: `flask-task`
* Service name: `flask-service`
* Desired count: `1` (you can scale later)
* Networking:

  * VPC: `flask-ecs-vpc`
  * Subnets: choose 2 public subnets
  * Security Group: `flask-ecs-sg`
  * Auto-assign public IP: ✅ enabled

**Load Balancing:**

* Enable Application Load Balancer ✅
* Choose: `flask-ecs-alb`
* Listener: Port 80: default
* Target group: `flask-tg`
* Container to register: `flask-container`
* Port: `80`

Click **Next** and **Create Service**

---

## 🔍 Step 7: Verify

* Go to **ECS → Cluster → flask-ecs-cluster → Services**
* Check task status is **RUNNING**
* Go to **EC2 → Load Balancer → flask-ecs-alb**
* Copy **DNS name**
* Open in browser

➡️ You should see:

```bash
🚀 Hello from Flask App on ECS Fargate!
```

---

## 🧠 Summary

| Component       | Value                              |
| --------------- | ---------------------------------- |
| ECS Cluster     | flask-ecs-cluster                  |
| Task Definition | flask-task                         |
| Container Image | `deepakyadav/flask-ecs-app:latest` |
| ECS Service     | flask-service                      |
| Load Balancer   | flask-ecs-alb                      |
| Target Group    | flask-tg                           |
| VPC/Subnets     | Public VPC                         |
| Security Group  | Allows HTTP (80)                   |
| Result          | Public URL running your Flask app  |

---






