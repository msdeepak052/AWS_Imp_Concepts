### Let's dive into **Auto Scaling Group (ASG) Termination Policies** in detail — covering:

* What termination policies are
* All available options
* Behavior of each policy with examples
* How to configure them via the **AWS Console**

---

## 🔍 **What Are ASG Termination Policies?**

ASG **termination policies** determine **which EC2 instances should be terminated first** when the Auto Scaling Group needs to reduce capacity — such as during scale-in or manual adjustments.

They are important for:

* **Preserving balanced capacity** across AZs
* **Avoiding premature termination** of preferred or newer instances
* **Managing cost and performance**

---

## 🧩 **All Termination Policy Options (in order of evaluation)**

You can specify one or multiple policies — AWS evaluates them **in order**.

---

### ✅ 1. **Default**

* **Behavior:** AWS uses the following sequence:

  1. Instance in the AZ with most instances
  2. Instance with oldest launch configuration
  3. Oldest instance

**Use Case:**

> Basic scaling without specific preference

---

### ✅ 2. **OldestInstance**

* **Terminates:** The **oldest EC2 instance** in the group (based on launch time)

**Use Case:**

> Rolling out new app versions or replacing aging instances

---

### ✅ 3. **NewestInstance**

* **Terminates:** The **most recently launched instance**

**Use Case:**

> Revert to a stable version by removing newly added instances

---

### ✅ 4. **OldestLaunchConfiguration**

* **Terminates:** Instance using the **oldest Launch Configuration** or **Launch Template version**

**Use Case:**

> Gradual rollout of new AMI/template by replacing old-template instances

---

### ✅ 5. **ClosestToNextInstanceHour**

* **Terminates:** Instance closest to the **next billing hour** to optimize cost (mainly for hourly billing)

**Use Case:**

> Cost-optimization when scaling in frequently (note: less relevant for per-second billing types)

---

### ✅ 6. **Default**

* This is a **fallback** that ensures a termination always happens, using built-in logic.

---

### ✅ 7. **OldestLaunchTemplate**

* **Terminates:** Instance running the **oldest launch template version**

**Use Case:**

> Similar to `OldestLaunchConfiguration`, but for template-based groups

---

### ✅ 8. **AllocationStrategy**

* Only applies to **Mixed Instances Policy**.
* Terminates instance types that are **least desired or most expensive**.

**Use Case:**

> Cost control in spot/on-demand mixed environments

---

### 🧪 **Example Scenario**

#### Scenario:

* ASG has 6 instances:

  * 3 in AZ `us-east-1a`
  * 3 in AZ `us-east-1b`
* 2 are using old AMI (launch config), 4 are newer.

You set termination policy:

```bash
["OldestLaunchConfiguration", "OldestInstance"]
```

🔁 **When scale-in happens:**

* AWS first looks for instances using the **old launch config**.
* Among them, the **oldest** will be terminated.

---

## 🛠️ **How to Configure Termination Policies from AWS Console**

### ✅ Step-by-Step

1. **Go to AWS Console > EC2 > Auto Scaling Groups**
2. Select your ASG
3. Click on the **“Details”** tab
4. Scroll down to **Termination Policies**
5. Click **“Edit”**
6. Choose from the dropdown (you can select multiple and order them)

   * e.g., `OldestLaunchConfiguration`, then `OldestInstance`
7. Click **“Update”**

---

### 🧠 **Tips and Best Practices**

| Goal                         | Recommended Policy                                      |
| ---------------------------- | ------------------------------------------------------- |
| Gradual instance replacement | `OldestInstance` or `OldestLaunchConfiguration`         |
| Rollback new deployment      | `NewestInstance`                                        |
| Cost optimization            | `ClosestToNextInstanceHour`                             |
| Maintain AZ balance          | Always keep `Default` at end (AWS handles AZ rebalance) |
| Replace older AMIs           | `OldestLaunchTemplate` or `OldestLaunchConfiguration`   |

---

## 📘 Terraform Equivalent (Optional)

```hcl
resource "aws_autoscaling_group" "example" {
  name                 = "asg-example"
  ...
  termination_policies = [
    "OldestLaunchConfiguration",
    "OldestInstance",
    "Default"
  ]
}
```

---

## 🔚 Summary Table

| Policy                      | Terminates                              |
| --------------------------- | --------------------------------------- |
| `OldestInstance`            | Instance launched earliest              |
| `NewestInstance`            | Most recently launched instance         |
| `OldestLaunchConfiguration` | Instance with oldest launch config      |
| `OldestLaunchTemplate`      | Instance with oldest template version   |
| `ClosestToNextInstanceHour` | Instance closest to next hourly billing |
| `AllocationStrategy`        | Least desired type in mixed policy      |
| `Default`                   | AZ-balanced fallback logic              |



---

## 🧩 **What is a Custom Termination Policy in ASG (Conceptually)?**

A **custom termination policy** is simply a **user-defined ordered list** of AWS-supported policies that dictates how Auto Scaling should choose which instances to terminate **when scaling in**.

You can **combine multiple built-in policies** in a specific order to match your unique business logic.

---

## ✅ **Supported Built-in Termination Policies**

| Policy                      | Description                                                  |
| --------------------------- | ------------------------------------------------------------ |
| `OldestInstance`            | Terminates the oldest launched instance                      |
| `NewestInstance`            | Terminates the most recently launched instance               |
| `OldestLaunchConfiguration` | Terminates instances using the oldest launch config/template |
| `OldestLaunchTemplate`      | Terminates instances with the oldest launch template version |
| `ClosestToNextInstanceHour` | Cost-aware termination (rarely used now)                     |
| `AllocationStrategy`        | Used with mixed instances policy                             |
| `Default`                   | AZ-rebalancing logic                                         |

---

## 🛠️ **Example: Custom Termination Policy Strategy**

### 🎯 Scenario:

You want to:

* Always remove **old-template-based instances** first
* Among them, pick the **oldest** instance (longest running)
* Preserve AZ balance

### ✅ Custom Termination Policy:

```text
["OldestLaunchTemplate", "OldestInstance", "Default"]
```

### 🔁 Behavior:

1. AWS filters all instances using the **oldest launch template version**.
2. Among those, picks the **oldest** instance.
3. If none matches, falls back to **default AZ-balancing** logic.

---

## 🔧 **Steps to Set Custom Termination Policy from AWS Console**

1. **Go to AWS Console > EC2 > Auto Scaling Groups**
2. Select your ASG
3. Under **Details** tab → scroll to **Termination Policies**
4. Click **Edit**
5. In the dropdown, **add multiple policies** in your desired order

   * For example:

     1. `OldestLaunchTemplate`
     2. `OldestInstance`
     3. `Default`
6. Click **Update**

📌 **Order matters** — AWS follows your order *top to bottom*.

---

## ✅ **More Custom Strategies (Real-world)**

| Use Case                           | Termination Policy                                  |
| ---------------------------------- | --------------------------------------------------- |
| Rolling update to newest AMI       | `OldestLaunchTemplate`, `OldestInstance`, `Default` |
| Revert bad rollout                 | `NewestInstance`, `Default`                         |
| Cost optimization with rebalancing | `ClosestToNextInstanceHour`, `Default`              |
| Blue/Green deployment cleanup      | `OldestLaunchTemplate`, `OldestInstance`, `Default` |

---

## 🧱 **Terraform Snippet – Custom Termination Policy**

```hcl
resource "aws_autoscaling_group" "custom_termination_policy" {
  name                 = "custom-asg"
  max_size             = 5
  min_size             = 2
  desired_capacity     = 3
  vpc_zone_identifier  = ["subnet-xxxxxx"]

  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }

  termination_policies = [
    "OldestLaunchTemplate",
    "OldestInstance",
    "Default"
  ]
}
```

---

## 🧠 Pro Tips

* **Always end with `Default`** for AZ balance.
* Avoid conflicting logic, e.g., `OldestInstance` + `NewestInstance`.
* Pair with **Instance Maintenance Policy** for controlled scale-in.


---

## ✅ **Custom Termination Policy Using Lambda (Workaround Architecture)**

### 🔁 **Workflow Overview:**

1. **ASG Lifecycle Hook (on scale-in)** triggers a **Lambda function**.
2. Lambda inspects all ASG instances.
3. Based on **custom logic** (CPU, memory, tags, uptime, AZ, etc.), it decides which instance to terminate.
4. Lambda **calls EC2 terminate-instance** or **completes the lifecycle action** with the instance ID.
5. ASG proceeds with the termination.

---

## 🧠 **Why Use Lambda for Custom Termination?**

* Terminate instances based on **custom metrics** (e.g., memory, cost, AZ traffic, instance age).
* Integrate with **CloudWatch, Cost Explorer, Tag-based filtering, or external systems**.
* Extend ASG with **application-aware intelligence**.

---

## 🧩 **Components Involved**

| Component                       | Purpose                                                                           |
| ------------------------------- | --------------------------------------------------------------------------------- |
| **ASG Lifecycle Hook**          | Pauses termination at scale-in                                                    |
| **Lambda Function**             | Runs custom logic to pick instance                                                |
| **CloudWatch Event** or **SNS** | Triggers Lambda                                                                   |
| **IAM Role**                    | Grants Lambda permission to complete the lifecycle action and terminate instances |

---

## 🛠️ **Step-by-Step: Build a Custom Termination Logic with Lambda**

---

### ✅ 1. Create a Lifecycle Hook on ASG

```bash
aws autoscaling put-lifecycle-hook \
  --lifecycle-hook-name CustomScaleInHook \
  --auto-scaling-group-name my-asg \
  --lifecycle-transition autoscaling:EC2_INSTANCE_TERMINATING \
  --heartbeat-timeout 300 \
  --default-result CONTINUE
```

* Transition: `autoscaling:EC2_INSTANCE_TERMINATING`
* Timeout: 300 seconds (how long to wait for Lambda to act)

---

### ✅ 2. Create a Lambda Function

Sample logic:

```python
import boto3

asg_client = boto3.client('autoscaling')
ec2_client = boto3.client('ec2')

def lambda_handler(event, context):
    asg_name = event['detail']['AutoScalingGroupName']
    lifecycle_hook_name = event['detail']['LifecycleHookName']
    instance_id = event['detail']['EC2InstanceId']
    lifecycle_token = event['detail']['LifecycleActionToken']

    # Custom logic: terminate another instance (e.g., based on age, tag, metric, etc.)
    # In this example, we'll just complete the action on the original instance.
    
    asg_client.complete_lifecycle_action(
        LifecycleHookName=lifecycle_hook_name,
        AutoScalingGroupName=asg_name,
        LifecycleActionToken=lifecycle_token,
        LifecycleActionResult='CONTINUE'
    )
```

---

### ✅ 3. Trigger Lambda Using CloudWatch or SNS

* Create a CloudWatch rule:

  * Event pattern:

    ```json
    {
      "source": ["aws.autoscaling"],
      "detail-type": ["EC2 Instance-terminate Lifecycle Action"]
    }
    ```
  * Target: your Lambda function

---

### ✅ 4. Attach IAM Role to Lambda

Lambda requires:

```json
{
  "Effect": "Allow",
  "Action": [
    "autoscaling:CompleteLifecycleAction",
    "autoscaling:DescribeAutoScalingGroups",
    "ec2:DescribeInstances",
    "ec2:TerminateInstances"
  ],
  "Resource": "*"
}
```

---

## 🔁 **How This Works**

| Step | Action                                                                 |
| ---- | ---------------------------------------------------------------------- |
| 1    | ASG triggers scale-in                                                  |
| 2    | Lifecycle hook pauses termination                                      |
| 3    | Lambda is triggered                                                    |
| 4    | Lambda applies custom rules to choose instance                         |
| 5    | Lambda completes the action, possibly terminating a different instance |

---

## 🎯 Use Cases

* **Avoid terminating specific tagged instances** (`DoNotTerminate = true`)
* **Choose lowest CPU-load instance to terminate**
* **Rebalance based on custom AZ or zone performance**
* **Drain pods gracefully on EKS or ECS before termination**

---

## ⚠️ Things to Keep in Mind

* **Lambda execution time** must stay within the lifecycle hook timeout.
* **Don’t forget to complete the lifecycle action** — else the instance gets stuck.
* If you terminate a different instance than the one in the lifecycle event, **still complete the lifecycle action for the original** to avoid ASG timeout issues.

---

## 🧠 Bonus

For Kubernetes on EC2 (e.g., EKS), you can:

* Add a **lifecycle hook to drain the node gracefully**
* Run `kubectl drain` inside the Lambda before completing lifecycle action

---

## ⏰ **ASG “Timers” – Conceptual Overview**

When we talk about **timers in ASG**, we refer to these key mechanisms:

| Timer Type                         | Purpose                                                               |
| ---------------------------------- | --------------------------------------------------------------------- |
| **Cooldown Period**                | Prevents rapid/frequent scaling                                       |
| **Health Check Grace Period**      | Time to allow new instances to initialize before marking as unhealthy |
| **Instance Warm-up**               | Time for instances to become "ready" during scaling                   |
| **Scheduled Actions (Cron)**       | Time-based scaling using cron-style schedules                         |
| **Lifecycle Hook Timeout**         | Time to wait before force-terminating/adding an instance              |
| **Instance Refresh Warm-up Delay** | Controls how long to wait before replacing the next instance          |

---

Let’s go into detail about each of these.

---

## 1️⃣ **Cooldown Period**

### 🧠 What:

* Ensures there’s a pause between **scale-out or scale-in** activities.
* Gives time for instance metrics (like CPU) to **stabilize** before new scaling happens.

### 🛠️ Types:

* **Default cooldown** — for all activities
* **Scaling policy cooldown** — defined per scaling policy (overrides default)

### ⏱️ Example:

* Default cooldown = 300 seconds
* ASG scales out → waits 5 minutes before considering next scale

### 📍 Console Steps:

1. Go to **EC2 > Auto Scaling Groups**
2. Select your ASG
3. Click **Edit**
4. Set **Default Cooldown Period**

---

## 2️⃣ **Health Check Grace Period**

### 🧠 What:

* After launching a new instance, this period gives it **time to boot and register** before health checks begin.
* Prevents marking slow-starting apps as unhealthy prematurely.

### ⏱️ Example:

* Health check grace period = 300 seconds
* ASG waits 5 minutes after instance launch before health checks start

### 📍 Console Steps:

1. Go to **EC2 > Auto Scaling Groups**
2. Select your ASG
3. Click **Edit**
4. Set **Health Check Grace Period**

---

## 3️⃣ **Instance Warm-up**

### 🧠 What:

* Controls how long Auto Scaling waits **after launching a new instance** before it counts towards **desired capacity** in dynamic scaling.

### 📌 Used only when:

* `InstanceWarmup` is set inside **Target Tracking** or **Step Scaling policies**
* `Instance Maintenance Policy` during **Instance Refresh**

### ⏱️ Example:

* Warm-up = 300s → Auto Scaling doesn’t launch another instance until the new one has completed warm-up

### 📍 Console Steps:

1. Go to **EC2 > Auto Scaling Groups**
2. Add or edit a **Target Tracking or Step Scaling Policy**
3. Under **Instance Warm-up**, set value (e.g., 300 seconds)

---

## 4️⃣ **Scheduled Actions (Cron Timers)**

### 🧠 What:

* Schedule capacity changes **based on time**, like increasing capacity during business hours or weekends.

### 🔔 Supports cron-style expressions (UTC-based)

### 🧾 Example:

```plaintext
cron(0 9 * * 1-5) → Every weekday at 9 AM UTC
```

Set desired capacity = 6
At 6 PM → set desired capacity = 2

### 📍 Console Steps:

1. Go to **EC2 > Auto Scaling Groups**
2. Select your ASG → go to **Scheduled Actions** tab
3. Click **Create Scheduled Action**
4. Enter:

   * Recurrence (cron)
   * Start/end time
   * Min/Max/Desired capacity

---

## 5️⃣ **Lifecycle Hook Timeout**

### 🧠 What:

* When an instance is launched or terminated, ASG can **pause** that action (using Lifecycle Hooks).
* Timeout defines **how long to wait** before proceeding automatically.

### ⏱️ Example:

* Lifecycle hook timeout = 300 seconds
* Lambda or script has 5 minutes to complete tasks like `kubectl drain`

### 📍 Console Steps:

1. Go to **EC2 > Lifecycle Hooks**
2. Choose hook duration under **Heartbeat Timeout**

---

## 6️⃣ **Instance Refresh Warm-up Delay**

### 🧠 What:

* During **Instance Refresh**, this controls how long ASG waits before replacing the next batch of instances.
* Prevents too many simultaneous changes.

### ⏱️ Example:

* Instance warm-up = 300s
* ASG waits 5 minutes between replacing each instance

### 📍 Console Steps:

1. Go to **EC2 > Auto Scaling Groups**
2. Select ASG → Go to **Instance Refresh**
3. Click **Start Refresh** → Set **Instance Warm-up Delay**

---

## 🧠 Summary Table

| Timer Type                    | Use Case                         | Configurable At           |
| ----------------------------- | -------------------------------- | ------------------------- |
| **Cooldown**                  | Avoids rapid scaling             | ASG or Scaling Policy     |
| **Health Check Grace Period** | Delays health checks             | ASG settings              |
| **Instance Warm-up**          | Delay before instance counts     | Scaling policy or refresh |
| **Scheduled Actions**         | Time-based scaling               | Scheduled tab             |
| **Lifecycle Hook Timeout**    | Pause before termination/launch  | Lifecycle hook            |
| **Instance Refresh Warm-up**  | Throttles instance refresh speed | Instance refresh config   |

---
Perfect, Deepak! Here's a **Terraform example** that covers all the major **ASG "timers"** we discussed:

---

## ✅ **Terraform Snippet – ASG with All Timer Options**

```hcl
provider "aws" {
  region = "ap-south-1"
}

# Launch Template
resource "aws_launch_template" "example" {
  name_prefix   = "asg-launch-template-"
  image_id      = "ami-0abcdef1234567890"
  instance_type = "t3.micro"
}

# Auto Scaling Group with Timer Settings
resource "aws_autoscaling_group" "example" {
  name                      = "asg-timer-example"
  desired_capacity          = 2
  max_size                  = 4
  min_size                  = 1
  vpc_zone_identifier       = ["subnet-xxxxxxxx"] # replace with your subnet IDs
  health_check_type         = "EC2"
  health_check_grace_period = 300                     # Health Check Grace Period
  default_cooldown          = 180                     # Cooldown Period

  launch_template {
    id      = aws_launch_template.example.id
    version = "$Latest"
  }

  termination_policies = ["OldestInstance"]

  # Instance Maintenance Policy (affects instance refresh)
  instance_maintenance_policy {
    min_healthy_percentage = 75
    max_healthy_percentage = 125
  }

  tag {
    key                 = "Name"
    value               = "asg-instance"
    propagate_at_launch = true
  }
}
```

---

## ✅ **Scheduled Scaling Action (Timer-based scaling)**

```hcl
resource "aws_autoscaling_schedule" "scale_up_morning" {
  scheduled_action_name  = "scale-up-morning"
  min_size               = 2
  max_size               = 4
  desired_capacity       = 3
  recurrence             = "0 3 * * *"  # 8:30 AM IST (UTC+5:30)
  autoscaling_group_name = aws_autoscaling_group.example.name
}

resource "aws_autoscaling_schedule" "scale_down_evening" {
  scheduled_action_name  = "scale-down-evening"
  min_size               = 1
  max_size               = 2
  desired_capacity       = 1
  recurrence             = "0 15 * * *" # 8:30 PM IST (UTC+5:30)
  autoscaling_group_name = aws_autoscaling_group.example.name
}
```

---

## ✅ **Target Tracking Policy with Instance Warm-up**

```hcl
resource "aws_autoscaling_policy" "cpu_target_tracking" {
  name                   = "cpu-tracking"
  policy_type            = "TargetTrackingScaling"
  autoscaling_group_name = aws_autoscaling_group.example.name

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }
    target_value       = 50
    disable_scale_in   = false
    estimated_instance_warmup = 300   # Instance Warm-up time
  }
}
```

---

## 🧠 Optional: Lifecycle Hook with Timeout (via Lambda or SQS integration)

```hcl
resource "aws_autoscaling_lifecycle_hook" "example" {
  name                   = "custom-terminate-hook"
  autoscaling_group_name = aws_autoscaling_group.example.name
  lifecycle_transition   = "autoscaling:EC2_INSTANCE_TERMINATING"
  heartbeat_timeout      = 300
  default_result         = "CONTINUE"
}
```

---

## 📦 Summary of What This TF Does

| Feature                 | Configuration   | Resource                         |
| ----------------------- | --------------- | -------------------------------- |
| Health check grace      | 300 sec         | `health_check_grace_period`      |
| Cooldown                | 180 sec         | `default_cooldown`               |
| Instance warm-up        | 300 sec         | `estimated_instance_warmup`      |
| Instance refresh policy | 75–125%         | `instance_maintenance_policy`    |
| Scheduled scaling       | Morning/evening | `aws_autoscaling_schedule`       |
| Lifecycle hook timeout  | 300 sec         | `aws_autoscaling_lifecycle_hook` |

---
### Let’s simulate a **real-world timeline of ASG behavior** over **1 hour** with the settings you provided:

---

## 🧾 **ASG Configuration Summary**

| Setting                       | Value                                             |
| ----------------------------- | ------------------------------------------------- |
| **Initial EC2 Instances**     | 2                                                 |
| **Instance Warm-up**          | 5 minutes (300s)                                  |
| **Cooldown Period**           | 10 minutes (600s)                                 |
| **Health Check Grace Period** | 3 minutes (180s)                                  |
| **Target Tracking Policy**    | Scale out when CPU > 70%, scale in when CPU < 30% |

---

## 🧪 **Simulated Timeline (60 Minutes)**

> Each event assumes AWS CloudWatch checks every 1-minute period for average CPU utilization.

---

### **00:00 → 00:05** – ASG Starts with 2 Instances

* **CPU Usage:** 40% average
* **No scaling occurs.**
* Health checks delayed by 3 min, but both instances become healthy.

---

### **00:05 → 00:10** – CPU Spikes to 85%

* Average CPU > 70% → **Trigger scale-out**
* ASG adds **1 new instance** (Total: 3)
* **Warm-up timer for new instance starts (5 mins)**
* **Cooldown timer also starts (10 mins)**

📌 **Next scaling action cannot happen before 00:20 due to cooldown**

---

### **00:10 → 00:15** – CPU = 75%, but ASG in Cooldown

* **No scaling allowed** due to 10-min cooldown
* New instance still in warm-up
* Total capacity = 3 (2 active, 1 warming up)

---

### **00:15 → 00:20** – New instance finishes warm-up

* ASG now counts 3 full-capacity instances
* CPU load drops to 55% average
* **Still in cooldown — no action taken**

---

### **00:20 → 00:25** – CPU drops to 25% (low load)

* Cooldown period expired ✅
* CPU < 30% → **Trigger scale-in**
* ASG terminates **1 instance** → Total = 2
* **Cooldown starts again (10 mins)**

---

### **00:25 → 00:35** – CPU stable at 30–40%

* Still in cooldown from scale-in
* No scaling actions allowed
* ASG stays at **2 instances**

---

### **00:35 → 00:40** – Sudden traffic → CPU hits 78%

* Cooldown expired
* CPU > 70% → **Trigger scale-out**
* New instance launched (Total = 3)
* **Warm-up starts for 5 mins**
* **Cooldown restarts for 10 mins**

---

### **00:40 → 00:45** – CPU still high, but ASG in cooldown

* Instance warming up
* No additional scaling

---

### **00:45 → 00:50** – Warm-up ends, CPU drops to 50%

* Now 3 active instances
* Load distributed
* Still within cooldown → No change

---

### **00:50 → 00:55** – CPU drops further to 25%

* Cooldown expired
* CPU < 30% → **Scale-in triggered**
* Instance terminated → Total = 2
* Cooldown restarts

---

### **00:55 → 01:00** – CPU stays stable at 30–40%

* ASG remains at 2 instances
* In cooldown → **no change**

---

## 🔚 **Final Result after 1 Hour:**

| Time  | Event                 | Instances |
| ----- | --------------------- | --------- |
| 00:00 | Start                 | 2         |
| 00:05 | Scale-out (CPU > 70%) | 3         |
| 00:20 | Scale-in (CPU < 30%)  | 2         |
| 00:35 | Scale-out (CPU > 70%) | 3         |
| 00:50 | Scale-in (CPU < 30%)  | 2         |

---

![image](https://github.com/user-attachments/assets/eeb22a47-c9b2-4abb-be9b-6b1cc47c7640)


## 🧠 Key Behavior Recap:

* **Cooldown (10 min)** prevents rapid scaling reactions (scale-out/in only once per 10 min).
* **Warm-up (5 min)** delays instance from affecting scaling decisions.
* **Health Check Grace Period (3 min)** ensures newly launched instances aren’t judged unhealthy prematurely.
* **Target tracking** auto-adjusts based on **actual CPU averages**, always seeking to stay close to target.

---





