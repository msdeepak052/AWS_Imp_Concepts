### ✅ **AWS Auto Scaling – Explained Simply**

**AWS Auto Scaling** is a service that **automatically adjusts the number of Amazon EC2 instances or other resources** based on the demand (traffic, CPU usage, etc.). It helps in maintaining **application availability**, **performance**, and **cost-efficiency**.

---

## 🧠 **Why Use Auto Scaling?**

* Handle **traffic spikes** automatically (scale out).
* Save cost during **low traffic** by reducing resources (scale in).
* Ensure **high availability** and **resilience**.

---

## 🛠️ **How AWS Auto Scaling Works**

Auto Scaling uses:

* **Launch Configuration / Launch Template** – Defines how to create new instances.
* **Auto Scaling Group (ASG)** – Group of EC2 instances managed together.
* **Scaling Policies** – Define when to scale in or out.
* **CloudWatch Alarms** – Triggers scaling actions (based on CPU, memory, etc.).

---

## 📦 **Example Scenario: Web Application Auto Scaling**

Let’s say you have a **web app** hosted on EC2 behind an **Application Load Balancer**.

### 🔧 Step-by-Step Setup:

1. **Create a Launch Template:**

   * Define AMI, instance type, security groups, and key pair.

2. **Create an Auto Scaling Group (ASG):**

   * Minimum: 2 instances
   * Maximum: 6 instances
   * Desired Capacity: 2
   * Attach to ALB

3. **Set Scaling Policies:**

   * Scale Out: If average CPU > 70% for 5 minutes → Add 1 instance
   * Scale In: If average CPU < 30% for 10 minutes → Remove 1 instance

4. **CloudWatch Metrics + Alarm:**

   * Monitors CPU utilization and triggers scaling.

**Result:**
During peak hours, instances increase. During off-peak, instances reduce — automatically.

---
### ✅ Horizontal vs Vertical Scaling

---

### 📌 **Vertical Scaling (Scale Up/Down):**

**Definition:**
Increasing or decreasing the power (CPU, RAM, storage) of a single server or machine.

**Example:**

* You upgrade your EC2 instance from `t2.medium` (2vCPU, 4GB RAM) to `t2.large` (2vCPU, 8GB RAM).

**Pros:**

* Simple to implement.
* No changes needed to application architecture.
* Ideal for monolithic apps.

**Cons:**

* Hardware limits: there's only so much you can upgrade.
* Downtime is often required for upgrade.
* Single point of failure.

---

### 📌 **Horizontal Scaling (Scale Out/In):**

**Definition:**
Adding or removing multiple machines/nodes to handle increased load.

**Example:**

* You add 3 EC2 instances behind a load balancer to serve more users.

**Pros:**

* No theoretical limit on scaling.
* High availability and fault tolerance.
* Ideal for microservices, cloud-native and stateless apps.

**Cons:**

* More complex to implement and manage.
* Requires load balancer or clustering.

---

### ✅ Scale Out vs Scale In

---

### 🔁 **Scale Out (Horizontal Scaling Out):**

**Definition:**
Adding more instances/machines to distribute the load.

**Example:**
Adding more Kubernetes pods when CPU usage exceeds 80%.

🟢 Goal: Handle more traffic by **increasing capacity**.

---

### 🔁 **Scale In (Horizontal Scaling In):**

**Definition:**
Removing instances/machines when load decreases.

**Example:**
Removing pods when average CPU drops below 30%.

🟢 Goal: **Reduce cost** when demand is low.

---

### 🎯 Summary Table:

| Term               | Type       | Meaning                  | Trigger Example               |
| ------------------ | ---------- | ------------------------ | ----------------------------- |
| Vertical Scaling   | Scale Up   | Add CPU/RAM to a machine | Upgrade EC2 type              |
| Vertical Scaling   | Scale Down | Reduce CPU/RAM           | Downgrade instance type       |
| Horizontal Scaling | Scale Out  | Add more machines        | Auto Scaling Group adds EC2s  |
| Horizontal Scaling | Scale In   | Remove machines          | Auto Scaling Group terminates |


![image](https://github.com/user-attachments/assets/b21d0c8e-2c84-4507-9e41-cd2e00e4d56c)

#### Vertical Scaling not supported by AWS

![image](https://github.com/user-attachments/assets/08b1e488-d67f-4375-bccc-e8c1f0a9c781)

#### Horizontal Scaling supported by AWS

![image](https://github.com/user-attachments/assets/66a53b54-b88a-4a47-912a-d8af41b927e5)


---

## 💡 **Real-Time Use Cases of Auto Scaling**

| Use Case                           | Description                                                            |
| ---------------------------------- | ---------------------------------------------------------------------- |
| **E-Commerce Site (Festive Sale)** | Auto Scaling handles sudden user traffic spikes by adding EC2s.        |
| **Dev/Test Environments**          | Scale down resources at night/weekends to save cost.                   |
| **Video Streaming App**            | Based on CPU/GPU/network load, scale in/out streaming servers.         |
| **CI/CD Build System**             | Automatically scale build agents based on queue length.                |
| **Serverless with ECS/Fargate**    | Use Application Auto Scaling to scale services based on request count. |

---

## 🧩 **Auto Scaling Beyond EC2**

AWS Auto Scaling can also scale other services:

* **DynamoDB**: Adjust read/write capacity.
* **ECS Services**: Scale number of tasks.
* **Aurora Read Replicas**: Adjust read instance count.
* **Spot Fleet**: Scale spot instances based on capacity.

---

## 🔐 **Best Practices**

* Use **target tracking policies** for smarter scaling (e.g., maintain 50% CPU).
* Set **cooldown periods** to avoid rapid scaling in/out.
* Use **scaling schedules** for predictable traffic (e.g., 9 AM to 5 PM).
* Combine with **Elastic Load Balancer** and **CloudWatch** for optimal performance.

---

## 🚀 Summary

| Feature                | Benefit                                            |
| ---------------------- | -------------------------------------------------- |
| **Auto Scaling Group** | Defines scaling boundaries and instance management |
| **Scaling Policy**     | Triggers based on metrics or schedule              |
| **Cost Optimization**  | Only run what you need                             |
| **High Availability**  | Replaces unhealthy instances automatically         |

---
---
Let’s walk through a **real-world Terraform module-based example** for **AWS EC2 Auto Scaling with Load Balancer**. This is ideal for production-grade architecture.

---

## ✅ **Scenario:**

You're deploying a **web application** behind an **Application Load Balancer (ALB)**. You want:

* EC2 instances launched using a **Launch Template**
* An **Auto Scaling Group (ASG)** to scale based on CPU usage
* Instances to be automatically registered with the **ALB Target Group**

---

## 📁 Folder Structure (Module Approach)

```
terraform-auto-scaling/
├── main.tf
├── variables.tf
├── outputs.tf
├── terraform.tfvars
└── modules/
    └── ec2-asg/
        ├── main.tf
        ├── variables.tf
        ├── outputs.tf
```

---

## 🧱 Root Module (`main.tf`)

```hcl
provider "aws" {
  region = "ap-south-1"
}

module "ec2_asg" {
  source = "./modules/ec2-asg"

  vpc_id              = "vpc-12345678"
  subnet_ids          = ["subnet-abc123", "subnet-def456"]
  ami_id              = "ami-0abcdef1234567890"
  instance_type       = "t2.micro"
  desired_capacity    = 2
  min_size            = 1
  max_size            = 4
  target_group_arn    = "arn:aws:elasticloadbalancing:ap-south-1:1234567890:targetgroup/mytg/abcd1234efgh5678"
}
```

---

## 📦 Module: `modules/ec2-asg/main.tf`

```hcl
resource "aws_launch_template" "web_lt" {
  name_prefix   = "web-lt-"
  image_id      = var.ami_id
  instance_type = var.instance_type

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "web-app"
    }
  }
}

resource "aws_autoscaling_group" "web_asg" {
  desired_capacity     = var.desired_capacity
  max_size             = var.max_size
  min_size             = var.min_size
  vpc_zone_identifier  = var.subnet_ids
  target_group_arns    = [var.target_group_arn]
  launch_template {
    id      = aws_launch_template.web_lt.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "web-app"
    propagate_at_launch = true
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_policy" "scale_out" {
  name                   = "scale-out-policy"
  autoscaling_group_name = aws_autoscaling_group.web_asg.name
  adjustment_type        = "ChangeInCapacity"
  scaling_adjustment     = 1
  cooldown               = 300
}

resource "aws_autoscaling_policy" "scale_in" {
  name                   = "scale-in-policy"
  autoscaling_group_name = aws_autoscaling_group.web_asg.name
  adjustment_type        = "ChangeInCapacity"
  scaling_adjustment     = -1
  cooldown               = 300
}

resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  alarm_name          = "high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 120
  statistic           = "Average"
  threshold           = 70
  alarm_actions       = [aws_autoscaling_policy.scale_out.arn]
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.web_asg.name
  }
}

resource "aws_cloudwatch_metric_alarm" "low_cpu" {
  alarm_name          = "low-cpu"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 120
  statistic           = "Average"
  threshold           = 30
  alarm_actions       = [aws_autoscaling_policy.scale_in.arn]
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.web_asg.name
  }
}
```

---

## 🔧 `modules/ec2-asg/variables.tf`

```hcl
variable "ami_id" {}
variable "instance_type" {}
variable "subnet_ids" {
  type = list(string)
}
variable "vpc_id" {}
variable "desired_capacity" {}
variable "min_size" {}
variable "max_size" {}
variable "target_group_arn" {}
```

---

## 📤 `modules/ec2-asg/outputs.tf`

```hcl
output "asg_name" {
  value = aws_autoscaling_group.web_asg.name
}
```

---

## 📥 `terraform.tfvars` (Optional)

```hcl
ami_id           = "ami-0abcdef1234567890"
instance_type    = "t2.micro"
desired_capacity = 2
min_size         = 1
max_size         = 4
vpc_id           = "vpc-12345678"
subnet_ids       = ["subnet-abc123", "subnet-def456"]
target_group_arn = "arn:aws:elasticloadbalancing:ap-south-1:1234567890:targetgroup/mytg/abcd1234efgh5678"
```

---

## 🧪 Test the Setup

```bash
terraform init
terraform plan
terraform apply
```

---

## 📌 Real-World Notes

* Use **dynamic blocks** in modules to handle more flexible configs.
* Add **CloudWatch logs** or custom metrics for application-level auto scaling.
* Use **Terraform remote backends** for team collaboration (S3 + DynamoDB).
* Use **lifecycle hooks** to integrate with configuration management tools (Ansible, Chef, etc.).

---

## Practical 
Here's a **step-by-step guide to configure AWS EC2 Auto Scaling with Load Balancer via the AWS Console**, including setting up a **dummy Apache web app** and using `stress` to **test Auto Scaling**.

---

## ✅ **Objective**

* Launch EC2 instances in an **Auto Scaling Group (ASG)**
* Attach them to an **Application Load Balancer (ALB)**
* Install a **dummy web app (Apache)**
* Simulate **CPU load** using `stress`
* See how AWS **scales automatically**

---

## 🧰 **Pre-requisites**

* AWS Account
* AWS Region (e.g., `ap-south-1`)
* A Key Pair (for SSH access)
* A VPC with 2 public subnets
* Internet Gateway, Route Table setup

---

## 🛠️ **Step-by-Step Configuration via AWS Console**

---

### 🔹 Step 1: Create Security Group

1. Go to **EC2 > Security Groups > Create Security Group**
2. Name: `asg-web-sg`
3. Inbound Rules:

   * HTTP (port 80) from `0.0.0.0/0`
   * SSH (port 22) from your IP
4. Outbound Rule: Allow all
5. Attach it to your default VPC or your custom VPC

![image](https://github.com/user-attachments/assets/b77bea36-c590-4c39-a2fa-4b6b06ccaeb6)

---

### 🔹 Step 2: Create Launch Template

1. Go to **EC2 > Launch Templates > Create launch template**

![image](https://github.com/user-attachments/assets/0efcf6ae-b81b-4781-86cf-01d510718373)

2. Name: `web-template`

![image](https://github.com/user-attachments/assets/95e04b3f-2903-4c6c-b228-28b88481de19)

3. AMI: Choose **Amazon Linux 2**

![image](https://github.com/user-attachments/assets/6f8c09c3-a61d-41a2-a8f7-25cc21998a05)

4. Instance Type: `t2.micro`
5. Key Pair: Choose existing or create a new one

![image](https://github.com/user-attachments/assets/fcd25478-d2a3-41b7-9f82-9c85c266dff3)

6. Security Group: Select the one you just created

![image](https://github.com/user-attachments/assets/c288818e-9cfe-41cc-a496-d229a13d792d)


7. Advanced > User Data:

```bash
#!/bin/bash
yum update -y
amazon-linux-extras install epel -y
yum install stress -
systemctl start httpd
systemctl enable httpd

# Create a beautiful HTML page with your name and ASG info
cat <<EOF > /var/www/html/index.html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AWS ASG Instance - Deepak Yadav</title>
  <style>
    body {
      background: linear-gradient(to right, #4facfe, #00f2fe);
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      text-align: center;
      padding: 50px;
      color: white;
    }
    h1 {
      font-size: 48px;
      animation: glow 2s ease-in-out infinite alternate;
    }
    h2 {
      font-size: 28px;
      margin-top: 40px;
    }
    .box {
      background-color: rgba(255, 255, 255, 0.1);
      padding: 30px;
      border-radius: 15px;
      box-shadow: 0 0 15px rgba(0,0,0,0.3);
      display: inline-block;
    }
    @keyframes glow {
      from {
        text-shadow: 0 0 10px #fff, 0 0 20px #0ff;
      }
      to {
        text-shadow: 0 0 20px #fff, 0 0 40px #0ff;
      }
    }
  </style>
</head>
<body>
  <div class="box">
    <h1>🚀 Hello from Auto Scaling Instance</h1>
    <h2>👤 Created by: <strong>Deepak Yadav</strong></h2>
    <h2>📘 Topic: <strong>AWS Auto Scaling Group (ASG)</strong></h2>
    <h2>🖥️ Hostname: <strong>$(hostname)</strong></h2>
  </div>
</body>
</html>
EOF

```
8. Click **Create launch template**

![image](https://github.com/user-attachments/assets/5f87e012-508b-4024-893f-04687c4ecd15)

![image](https://github.com/user-attachments/assets/ffcc8f80-46d4-42d0-b8ec-038978c5ad5c)

---

### 🔹 Step 3: Create Target Group

1. Go to **EC2 > Target Groups > Create target group**
2. Choose **Instances**
3. Protocol: HTTP, Port: 80
4. VPC: Select your VPC
5. Health check path: `/`
6. Click **Create target group**

![image](https://github.com/user-attachments/assets/0ec50e14-6522-4c64-beb5-c23e3199be51)
![image](https://github.com/user-attachments/assets/9e6f5b9a-6db2-4aff-8a47-58a5fc6d7f05)


---

### 🔹 Step 4: Create Application Load Balancer

1. Go to **EC2 > Load Balancers > Create Load Balancer**
2. Choose **Application Load Balancer**
3. Name: `web-alb`
4. Scheme: Internet-facing
5. Listeners: HTTP, Port 80
6. VPC & Subnets: Select your VPC and **2 public subnets**
7. Security Group: Use the same group from Step 1
8. Target Group:

   * Select **existing target group** (from Step 3)
9. Click **Create**

![image](https://github.com/user-attachments/assets/30d273d3-1cd6-4bdb-b77e-2f7cc25ec4d7)


---

### 🔹 Step 5: Create Auto Scaling Group

1. Go to **EC2 > Auto Scaling Groups > Create Auto Scaling group**
2. Name: `web-asg`
3. Launch Template: Select `web-template`

![image](https://github.com/user-attachments/assets/adfcaad9-5c09-49c9-a669-479f0f6f24ed)


4. VPC & Subnets: Select **2 subnets**
5. Attach to Load Balancer:

   * Choose existing Target Group (from Step 3)

![image](https://github.com/user-attachments/assets/d42a0d3d-46ed-45bf-87b2-e75cedae6722)

6. Desired Capacity: 2, Min: 1, Max: 4
7. Scaling Policies:

   * Select **Target tracking scaling policy**
   * Metric type: Average CPU utilization
   * Target value: 50%
8. Click **Create Auto Scaling Group**

![image](https://github.com/user-attachments/assets/2da0ed1d-a6e1-40a8-a1ef-5975927aad44)


---

## 🔍 **Step 6: Test the Setup**

### ✅ Check App:

1. Go to **EC2 > Load Balancers > web-alb > DNS name**
2. Open it in browser: `http://<ALB-DNS-name>`
3. You should see:

   ```
   Hello from Auto Scaling Instance - ip-xxxxxx
   ```
![image](https://github.com/user-attachments/assets/3d32ecbf-e539-4d76-bbb2-676c601e00ae)

---

## 🔥 **Step 7: Simulate Load with stress**

1. SSH into an EC2 instance in the ASG:

   ```bash
   ssh -i your-key.pem ec2-user@<EC2-Public-IP>
   ```

2. Run:

   ```bash
   stress --cpu 2 --timeout 300
   ```

3. This will trigger **high CPU usage**, and after \~5–10 minutes, **Auto Scaling should launch more instances** (up to max size).

![image](https://github.com/user-attachments/assets/f4d45266-2974-40c0-be05-0a371966492a)

![image](https://github.com/user-attachments/assets/f9d16077-f25a-4754-aec6-192f0b6f329f)

![image](https://github.com/user-attachments/assets/4e2d41e6-e341-4329-a352-3b1dcf4ef486)

---

## ✅ **Verify Scaling**

1. Go to **EC2 > Auto Scaling Groups > web-asg**
2. Check the **Instance count increasing**
3. Once CPU drops, it should **scale back down**


![image](https://github.com/user-attachments/assets/85c7a4e2-9431-4f44-9813-1cb25c8cbbdb)

---

Yes ✅ **it can and should be done that way!**

---

## 🔍 **Clarification:**

You **do not need to create EC2 instances manually**.

When you create an **Auto Scaling Group (ASG)** using a **Launch Template**, **the ASG itself will launch and manage EC2 instances automatically** — **no need to create EC2 instances manually**.

---

## 🧩 **How it Works**

| Component           | Purpose                                                                                    |
| ------------------- | ------------------------------------------------------------------------------------------ |
| **Launch Template** | Blueprint for creating EC2 instances (AMI, instance type, user data, etc.)                 |
| **ASG**             | Uses the launch template to automatically create/terminate EC2 instances based on policies |
| **Scaling Policy**  | Tells ASG *when* to scale (e.g., based on CPU)                                             |

---

## ✅ **What You Do:**

1. **Create Launch Template** (includes:

   * AMI ID
   * Instance Type
   * Security Group
   * User Data (install web app/stress)
   * Key Pair

2. **Create Target Group** (for ALB)

3. **Create Application Load Balancer**

4. **Create Auto Scaling Group**:

   * Attach launch template
   * Attach target group (via ALB)
   * Define Min, Max, Desired EC2 count
   * Configure scaling policy (like target CPU = 50%)

---

## 🧪 Then What Happens:

* ASG automatically creates EC2 instances using the **Launch Template**
* ALB distributes traffic to these EC2s
* When CPU > 50%, ASG adds more EC2s
* When CPU < 30%, ASG removes EC2s
* You don’t manually create/destroy EC2s at all!

---

## 📌 Real-World Tip:

Even in production:

> ✅ You **never create EC2 manually** in Auto Scaling scenarios.
> 🔄 Auto Scaling Group + Launch Template is your "source of truth."

---


## 🧹 **Optional Cleanup**

To avoid charges:

* Delete the Auto Scaling Group
* Delete the Load Balancer and Target Group
* Delete Launch Template and Security Groups

---

## 📌 Summary

| Component       | Purpose                                    |
| --------------- | ------------------------------------------ |
| Launch Template | Defines how EC2s are created               |
| ASG             | Scales EC2s based on CPU load              |
| ALB             | Distributes traffic to EC2s                |
| User Data       | Installs Apache & test page                |
| `stress`        | Simulates high CPU load to trigger scaling |

---


### Here’s a complete breakdown of the **Auto Scaling Group (ASG) scaling options in AWS**, with examples and real-world use cases.

---

## 🔁 **Scaling Options in Auto Scaling Group**

| Scaling Option                 | Description                                                                   |
| ------------------------------ | ----------------------------------------------------------------------------- |
| 1. **Manual Scaling**          | You manually set desired capacity (e.g., from 2 to 5)                         |
| 2. **Dynamic Scaling**         | Automatically adds/removes EC2s based on CloudWatch metrics (e.g., CPU > 70%) |
| 3. **Target Tracking Scaling** | Automatically keeps a metric (like CPU) at a target value (e.g., 50%)         |
| 4. **Step Scaling**            | Adjusts capacity in steps based on metric thresholds                          |
| 5. **Scheduled Scaling**       | Scales in/out at specific times (e.g., business hours)                        |

---

## ✅ 1. **Manual Scaling**

* **Set ASG size manually**
* Useful for testing or controlled environments

### Example:

```bash
aws autoscaling update-auto-scaling-group \
  --auto-scaling-group-name web-asg \
  --min-size 2 --max-size 6 --desired-capacity 3
```

### Use Case:

* Testing in Dev environment
* During maintenance windows

---

## ✅ 2. **Target Tracking Scaling (Most Common)**

* Automatically adjusts capacity to maintain a **target metric value**
* No need to define alarm thresholds

### Example:

* **Target CPU utilization**: 50%
* If CPU > 50%, add instances
* If CPU < 50%, remove instances

### Use Case:

* E-commerce websites to handle variable load
* Web apps during unpredictable traffic

---

## ✅ 3. **Step Scaling**

* Triggered by **CloudWatch alarms**
* You define specific steps to scale by depending on how much a metric exceeds a threshold

### Example:

```text
If CPU > 70% for 5 min → add 1 instance  
If CPU > 90% for 5 min → add 2 instances
If CPU < 30% → remove 1 instance
```

### Use Case:

* Apps that require **finer control** over scaling behavior
* Gradual scale-out to avoid cost spikes

---

## ✅ 4. **Scheduled Scaling**

* Define scaling **in advance** based on time
* Useful for predictable workloads

### Example:

```text
At 9 AM Mon–Fri → set desired capacity to 4  
At 6 PM Mon–Fri → set desired capacity to 2
```

### Use Case:

* Office-hours based internal applications
* Batch jobs that run at night

---

## ✅ 5. **Dynamic Scaling (CloudWatch Alarms)**

* Based on **CloudWatch metric thresholds**
* Trigger **scaling policies** (step or simple)

### Example:

```text
If NetworkIn > 5 MB/s → add instance  
If CPU < 20% for 10 min → remove instance
```

### Use Case:

* Media streaming platforms (scale on network I/O)
* Memory/Storage intensive workloads using custom metrics

---

## 🧠 **Which One Should You Use?**

| Use Case                     | Recommended Scaling                    |
| ---------------------------- | -------------------------------------- |
| Sudden traffic spikes        | Target Tracking or Step Scaling        |
| Predictable traffic patterns | Scheduled Scaling                      |
| Full control on thresholds   | Step Scaling                           |
| Cost-sensitive environments  | Target Tracking with low min size      |
| Custom metrics (e.g., queue) | Dynamic Scaling with CloudWatch alarms |

---

## 🎯 Bonus: Combine Them for Best Results

You can **combine multiple scaling policies**:

* Use **Scheduled Scaling** to scale up before peak hours
* Use **Target Tracking** to handle sudden spikes
* Use **Manual Scaling** during testing

---
