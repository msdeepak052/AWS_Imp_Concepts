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

# **Amazon EventBridge** — one of the most powerful, flexible services for **event-driven architecture** on AWS.

---

## ✅ What is **Amazon EventBridge**?

**Amazon EventBridge** is a **serverless event bus** service that:

* **Ingests events** from:

  * AWS services (CloudWatch, EC2, S3, etc.)
  * SaaS applications (like Zendesk, Datadog, Auth0)
  * Your **own applications**
* **Filters events** using JSON-based rules
* **Routes them** to various **targets** (Lambda, SQS, Step Functions, etc.)

---

### 📌 Key Concepts

| Component            | Description                                                             |
| -------------------- | ----------------------------------------------------------------------- |
| **Event Bus**        | Pipe where events are sent and rules listen (default, custom, partner)  |
| **Event**            | JSON document representing something that happened (e.g., EC2 launched) |
| **Rule**             | Pattern matcher that triggers on specific event structure               |
| **Target**           | The AWS service to invoke (Lambda, SNS, SQS, etc.)                      |
| **Archive & Replay** | Store and reprocess past events                                         |

---

## 📋 Example Event Structure

```json
{
  "source": "aws.ec2",
  "detail-type": "EC2 Instance State-change Notification",
  "detail": {
    "instance-id": "i-1234567890abcdef0",
    "state": "running"
  },
  "time": "2025-07-06T12:00:00Z",
  "region": "ap-south-1",
  "account": "123456789012"
}
```

---

## 🎯 Use Cases for EventBridge

| Use Case                    | Description                                                   |
| --------------------------- | ------------------------------------------------------------- |
| **Serverless automation**   | Trigger Lambda when S3 object uploaded, EC2 launched, etc.    |
| **Resource management**     | Automatically tag or shut down unused EC2 based on events     |
| **Security response**       | Detect changes (e.g., IAM policy edits) and respond instantly |
| **Data flow orchestration** | Chain together services (S3 → Lambda → SQS → StepFunction)    |
| **Audit & compliance**      | Monitor unauthorized changes                                  |
| **Integration with SaaS**   | Ingest events from external apps like PagerDuty, Zendesk      |

---

## 🔧 Event Sources

| Source Type             | Examples                         |
| ----------------------- | -------------------------------- |
| **AWS services**        | CloudTrail, EC2, ECS, S3, Lambda |
| **SaaS partners**       | Datadog, Auth0, Okta, Zendesk    |
| **Custom applications** | Send events via SDK, CLI, or API |

---

## 🧱 Event Buses

| Type        | Description                               |
| ----------- | ----------------------------------------- |
| **Default** | Pre-configured bus for AWS service events |
| **Custom**  | For application or cross-account use      |
| **Partner** | For third-party SaaS integrations         |

---

## 🛠️ How to Create an EventBridge Rule (AWS Console)

### ✅ Example: Trigger a Lambda on EC2 State Change

#### Step 1: Go to **Amazon EventBridge → Rules → Create Rule**

1. **Name**: `ec2-state-change-lambda`
2. **Event Bus**: `default`
3. **Event Pattern**: Choose `AWS services`

   * Service: `EC2`
   * Event Type: `EC2 Instance State-change Notification`
4. **Add filter** for specific state (e.g., "stopped")

```json
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "state": ["stopped"]
  }
}
```

---

#### Step 2: Add Target

* **Target Type**: `Lambda function`
* Choose a function like `handleEC2Stop`
* Grant permissions automatically

---

#### Step 3: Create Rule

✅ Done — your Lambda is now automatically triggered when **any EC2 instance stops**.

---

## 🎁 Other Example Targets

| Target             | Description                             |
| ------------------ | --------------------------------------- |
| **SNS**            | Send notification to admin or team      |
| **SQS**            | Buffer events for downstream processing |
| **Step Functions** | Start a workflow                        |
| **EC2 / ECS**      | Stop, start, or run commands            |
| **CodeBuild**      | Trigger builds on repo update           |
| **Kinesis**        | Stream to analytics pipeline            |

---

## 🧪 Use Case Examples

### 1. **Auto-tag EC2 instance when launched**

* Event: `RunInstances`
* Lambda target: `add-tags-based-on-launcher.py`

### 2. **Trigger remediation when S3 bucket is public**

* Event: S3 ACL change via CloudTrail
* Target: Lambda to remove public access

### 3. **Notify Slack when IAM role changes**

* Event: `PutRolePolicy` or `AttachRolePolicy`
* Target: Lambda → Slack webhook

---

## 🔐 IAM Permissions for EventBridge

### Role assumed by EventBridge needs:

```json
{
  "Effect": "Allow",
  "Action": "lambda:InvokeFunction",
  "Resource": "arn:aws:lambda:ap-south-1:123456789012:function:yourLambdaFunction"
}
```

---

## ⏪ Archive & Replay (Advanced)

* **Archive** your event stream (store JSON in EventBridge)
* **Replay** historical events for debugging/testing

### Create via Console:

1. Go to **EventBridge → Archives**
2. Select event bus → Create archive
3. Set retention period (up to 10 years)

Replay:

```bash
aws events start-replay \
  --replay-name test-replay \
  --source-arn arn:aws:events:...:archive/... \
  --destination event-bus-name
```

---

## 💡 Best Practices

| Tip                                 | Reason                               |
| ----------------------------------- | ------------------------------------ |
| Use **fine-grained event patterns** | Avoid unnecessary Lambda invocations |
| Use **dead-letter queues (DLQs)**   | For failed Lambda or SQS targets     |
| Enable **archive & replay**         | For critical flows or debugging      |
| Use **custom buses** for apps       | Separate from AWS service events     |
| Monitor with **CloudWatch Logs**    | Log event delivery and failures      |

---

## 🧠 Extra 

* EventBridge is **fully managed, scalable**, and **pay-per-event**, making it great for microservice and serverless design.
* It’s ideal for building **decoupled systems** with **real-time reactions**.
* Use **Schema Registry** in EventBridge to automatically detect and version event structure.

---

Would you like:

* A project combining **S3 upload → EventBridge → Lambda → SNS**?
* A **Terraform/CloudFormation** to automate the setup?
* Real-time **Slack notification** using EventBridge + Lambda?
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

