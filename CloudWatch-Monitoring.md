# **AWS CloudWatch**, **Alarms**, and **EventBridge**
---

## ✅ What is **AWS CloudWatch**?

**Amazon CloudWatch** is a **monitoring and observability** service for:

* AWS resources (EC2, RDS, Lambda, etc.)
* Custom applications
* On-premises infrastructure

### CloudWatch includes:

| Feature                      | Description                                                 |
| ---------------------------- | ----------------------------------------------------------- |
| **Metrics**                  | Numerical data (e.g., CPU usage, memory, disk I/O)          |
| **Logs**                     | Collect, monitor, and analyze logs (from EC2, Lambda, etc.) |
| **Alarms**                   | Trigger actions when metrics cross a threshold              |
| **Dashboards**               | Visualize metrics                                           |
| **Events/EventBridge**       | Respond to state changes in AWS                             |
| **CloudWatch Logs Insights** | Query logs using SQL-like language                          |
| **CloudWatch Agent**         | Collect OS-level metrics (memory, disk, etc.)               |

---

## 🎯 Common Use Cases

| Use Case               | Description                                 |
| ---------------------- | ------------------------------------------- |
| Monitor EC2 health     | Trigger alarms when CPU > 80% for 5 minutes |
| Alert on Lambda errors | Monitor `Errors` or `Throttles` metric      |
| Track deployments      | Capture logs from CodeDeploy, ECS, EKS      |
| Automated response     | Restart EC2 if CPU > 90% via EventBridge    |
| Log aggregation        | Centralize logs from multiple AWS services  |

---

## 📊 Example: Monitor EC2 CPU and Trigger Alarm

---

### 🔢 Step-by-Step: CloudWatch Alarm via Console

#### Scenario: Alert when EC2 CPU usage > 80% for 5 minutes

1. **Go to CloudWatch Console**
2. Navigate to **Alarms → Create Alarm**
3. **Select Metric**:

   * Browse: EC2 → Per-Instance Metrics → CPUUtilization
   * Select your EC2 instance
4. **Define Threshold**:

   * Threshold type: *Static*
   * Condition: *Greater than 80%*
   * Period: *5 minutes*
   * Evaluation periods: *1* (means trigger if condition is met for 1 consecutive period)
5. **Configure Actions**:

   * Select SNS topic (create one if needed)
   * Add email subscribers
6. **Name and create the alarm**

#### ✅ Result:

* If CPU > 80% for 5 minutes, email is sent.
* State changes: OK → ALARM → OK

---

## 🔔 Alarm Parameters Explained

| Parameter              | Description                                      |
| ---------------------- | ------------------------------------------------ |
| **Metric**             | The data to monitor (e.g., CPUUtilization)       |
| **Statistic**          | Aggregation function: Average, Sum, Min, Max     |
| **Period**             | Data aggregation interval (e.g., 5 min)          |
| **Threshold**          | Numeric limit for triggering the alarm           |
| **Evaluation Periods** | How many periods must breach the threshold       |
| **Actions**            | What to do (e.g., send to SNS, auto-recover EC2) |
| **State**              | `OK`, `ALARM`, `INSUFFICIENT_DATA`               |

---

## 🧠 Use Case Examples for Alarms

| Use Case            | Metric                          | Action                            |
| ------------------- | ------------------------------- | --------------------------------- |
| EC2 Overload        | CPUUtilization > 85%            | Notify via SNS                    |
| Lambda Errors       | `Errors` > 1                    | Trigger EventBridge rule or alarm |
| Disk Space          | Custom metric `DiskUsed%` > 90% | Notify or stop instance           |
| API Gateway Latency | `Latency` > 1s                  | Trigger alert                     |
| Auto Recovery       | EC2 StatusCheckFailed           | Automatically recover instance    |

---

## 🧩 What is **EventBridge**?

Formerly known as **CloudWatch Events**, **Amazon EventBridge** is a **serverless event bus** that:

* Delivers a near real-time stream of events
* From AWS services, your apps, or SaaS apps
* **Routes** events to **targets** like:

  * Lambda
  * SNS
  * SQS
  * Step Functions
  * EC2 actions

---

### 🧪 Example: Auto-stop EC2 instances every day at 7 PM

---

### Step-by-Step: EventBridge Scheduled Rule

1. Go to **EventBridge Console**

2. Select **Rules** → **Create Rule**

3. Enter name: `stop-ec2-at-7pm`

4. **Define Rule Type**: *Schedule*

5. **Define Schedule Expression**:

   * `cron(30 13 * * ? *)` → 7 PM IST (13:30 UTC)

6. **Define Target**:

   * Target type: *EC2*
   * Action: *StopInstances*
   * Resource ID: Select instance(s)

7. **Create IAM Role** if needed with permission to stop EC2

8. **Create Rule**

#### ✅ Result:

* EC2 instance will stop automatically every day at 7 PM.

---

## 🧠 Use Cases for EventBridge

| Use Case                                  | Trigger              | Target                 |
| ----------------------------------------- | -------------------- | ---------------------- |
| Auto start/stop EC2                       | Schedule             | EC2 actions            |
| Monitor IAM role changes                  | IAM API calls        | Lambda                 |
| Auto-tag EC2 instances                    | `RunInstances` event | Lambda                 |
| React to S3 uploads                       | S3 event             | Lambda or SQS          |
| Slack notification for CloudTrail actions | CloudTrail events    | Lambda + Slack webhook |

---

## 🔍 EventBridge Parameters

| Parameter               | Description                                |
| ----------------------- | ------------------------------------------ |
| **Event Pattern**       | JSON structure defining the event filter   |
| **Schedule Expression** | cron or rate expressions                   |
| **Target**              | What to invoke (Lambda, EC2, SNS, SQS)     |
| **Role**                | IAM role EventBridge uses to invoke target |
| **Event Bus**           | Default or custom event bus                |

---

### 🧠 Extra from ChatGPT

* Combine **CloudWatch Alarms** + **EventBridge** for powerful automation.
* Use **CloudWatch Logs Metric Filters** to trigger alarms based on specific log messages (e.g., `"ERROR"` string).
* You can **forward EventBridge events to other accounts** via Event Bus sharing.
* CloudWatch Dashboards can display Alarm state and real-time graphs.

---

## 💡 Example Project: Monitor & Auto-Recover EC2

### Scenario:

* CPU > 90% for 5 mins → Alarm triggers
* CloudWatch Alarm → EventBridge rule
* EventBridge → Lambda that:

  * Checks tags
  * Restarts EC2 if allowed

Perfect, Deepak! Let's build this **end-to-end automation** project:

---

## ✅ **Objective Recap**

> Automatically monitor EC2 CPU usage, and if it's consistently high (>90% for 5 minutes), trigger a Lambda function via EventBridge. The Lambda:

* Checks if a tag `AutoRecover = true` exists
* If yes, **restarts** the EC2 instance

---

## 🧱 COMPONENTS NEEDED

| Component          | Purpose                              |
| ------------------ | ------------------------------------ |
| ✅ CloudWatch Alarm | Monitor CPUUtilization               |
| ✅ EventBridge Rule | Trigger on ALARM state               |
| ✅ Lambda Function  | Logic to check tag & restart EC2     |
| ✅ IAM Roles        | Permissions for Lambda & EventBridge |

---

## 🔧 STEP 1: Create CloudWatch Alarm

### In AWS Console:

1. Go to **CloudWatch → Alarms → Create alarm**
2. **Choose metric**:

   * EC2 → Per-Instance Metrics → `CPUUtilization`
3. **Set condition**:

   * Threshold type: `Static`
   * Condition: `Greater than 90`
   * Period: `5 minutes`
   * Evaluation periods: `1`
4. **Next** → Skip notification → Click **Create Alarm**
5. Note the **alarm name**, e.g., `HighCPUAlarm-MyInstance`

---

## 🧩 STEP 2: Create EventBridge Rule for CloudWatch Alarm State Change

1. Go to **EventBridge → Rules → Create Rule**
2. Name: `TriggerLambdaOnHighCPU`
3. **Event Source**: *AWS services*
4. **Event Pattern**: Choose **CloudWatch Alarms**
5. Event pattern:

```json
{
  "source": ["aws.cloudwatch"],
  "detail-type": ["CloudWatch Alarm State Change"],
  "detail": {
    "state": {
      "value": ["ALARM"]
    },
    "alarmName": ["HighCPUAlarm-MyInstance"]
  }
}
```

6. **Target**: Lambda function (create in next step)

---

## 💻 STEP 3: Create Lambda Function to Check Tag and Restart EC2

### Lambda Role Permissions:

Create an IAM role with this policy and attach to the Lambda function:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:StartInstances",
        "ec2:RebootInstances",
        "ec2:StopInstances"
      ],
      "Resource": "*"
    }
  ]
}
```

---

### Lambda Code (Python 3.9+)

```python
import json
import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    # Extract instance ID from alarm dimensions
    alarm_detail = event['detail']
    dimensions = alarm_detail.get('configuration', {}).get('metrics', [])[0]['metricStat']['metric']['dimensions']
    
    instance_id = None
    for dim in dimensions:
        if dim['name'] == 'InstanceId':
            instance_id = dim['value']
            break

    if not instance_id:
        print("Instance ID not found")
        return {"status": "failed", "reason": "No instance ID in dimensions"}

    print(f"Checking tags for instance: {instance_id}")

    # Check for tag AutoRecover = true
    response = ec2.describe_instances(InstanceIds=[instance_id])
    tags = response['Reservations'][0]['Instances'][0].get('Tags', [])

    should_recover = any(tag['Key'] == 'AutoRecover' and tag['Value'].lower() == 'true' for tag in tags)

    if should_recover:
        print(f"AutoRecover tag is true, restarting {instance_id}")
        ec2.reboot_instances(InstanceIds=[instance_id])
        return {"status": "success", "action": "rebooted"}
    else:
        print(f"AutoRecover tag not present or false on {instance_id}")
        return {"status": "skipped", "reason": "Tag missing or false"}
```

---

## 🧪 STEP 4: Tag Your EC2 Instances

1. Go to **EC2 → Instances**
2. Select the instance → **Tags** → Add tag:

   * **Key**: `AutoRecover`
   * **Value**: `true`

Only instances with this tag will be restarted.

---

## 🧪 STEP 5: Test the Setup

1. Simulate high CPU or manually set alarm to `ALARM` state using AWS CLI:

```bash
aws cloudwatch set-alarm-state \
  --alarm-name HighCPUAlarm-MyInstance \
  --state-value ALARM \
  --state-reason "Testing Lambda trigger"
```

2. Watch Lambda logs in **CloudWatch Logs** to verify execution.
3. Confirm instance reboot in **EC2 Console**.

---

## 🛡 Best Practices

| Practice        | Tip                                                           |
| --------------- | ------------------------------------------------------------- |
| Least privilege | Limit Lambda IAM to specific instance IDs                     |
| Logging         | Use `print()` or CloudWatch Logs for audit                    |
| Rate limiting   | Add delay or backoff if many instances                        |
| Filtering       | Use EventBridge `detail.alarmName` filter for scoped triggers |

---

## 📘 Optional Add-ons

* **Email alert** from the alarm using SNS
* **Slack/Teams integration** using Lambda
* **Tag-based filtering** across multiple instances
* **Add stop/start logic based on different tags**

---

