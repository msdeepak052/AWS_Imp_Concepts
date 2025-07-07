# Amazon Simple Notification Service (SNS) - Comprehensive Guide

## What is Amazon SNS?

Amazon Simple Notification Service (SNS) is a fully managed pub/sub messaging service that enables you to decouple microservices, distributed systems, and serverless applications. It allows you to send messages or notifications to a large number of subscribers (endpoints) through various protocols.

![image](https://github.com/user-attachments/assets/92396279-4c7c-41c3-bed7-cfab632787c7)

![image](https://github.com/user-attachments/assets/cd6405c4-2973-4baa-94b6-64b214afab47)


## 🔹 **Core Concepts of Amazon SNS**

| Term                   | Description                                                                                |
| ---------------------- | ------------------------------------------------------------------------------------------ |
| **Topic**              | A communication channel for messages to be published to.                                   |
| **Publisher**          | An application or AWS service that sends messages to the topic.                            |
| **Subscriber**         | An endpoint (email, Lambda, SQS, HTTP/S, SMS, etc.) that receives messages from the topic. |
| **Subscription**       | The link between the topic and subscriber.                                                 |
| **Message**            | The data sent by a publisher to the topic.                                                 |
| **Message Attributes** | Key-value pairs that give metadata about the message (for filtering).                      |
| **Delivery Protocols** | Supported endpoints (Email, SMS, SQS, Lambda, HTTP/S, etc.).                               |

## 🔹 **Supported Protocols (Subscribers)**

| Protocol                  | Description                                            |
| ------------------------- | ------------------------------------------------------ |
| **HTTP/HTTPS**            | Delivers message via HTTP POST                         |
| **Email / Email-JSON**    | Delivers message via email                             |
| **SMS**                   | Sends message as a text                                |
| **Amazon SQS**            | Pushes messages into a queue                           |
| **AWS Lambda**            | Invokes a Lambda function                              |
| **Platform Applications** | Push notifications to mobile devices (APNS, GCM, etc.) |

## 🔹 **Parameters of SNS (Explained)**

| Parameter                  | Description                                           |
| -------------------------- | ----------------------------------------------------- |
| `DisplayName`              | Friendly name for the topic                           |
| `DeliveryPolicy`           | JSON defining retry behavior for HTTP/HTTPS           |
| `MessageStructure`         | Can be `json` for different protocols                 |
| `MessageAttributes`        | Metadata for message filtering                        |
| `SubscriptionFilterPolicy` | Filters messages by attribute to specific subscribers |
| `AccessPolicy`             | Controls who can publish or subscribe                 |

---

![image](https://github.com/user-attachments/assets/d3e51fd5-2c7f-4a99-9fcb-2e06fb4b9190)

---

Missing Line - To broadcast the messages of a message-producer system (for example, an e-commerce website) working with multiple other services that require its messages (for example, checkout and fulfillment systems), you can create a topic for your producer system.

## Key Features

1. **Pub/Sub Messaging**: Decouple message producers from consumers
2. **Fanout**: Deliver messages to multiple subscribers in parallel
3. **High Durability**: Messages are stored redundantly across multiple AZs
4. **Security**: Encryption at rest and in transit, fine-grained access control
5. **Message Filtering**: Deliver only relevant messages to subscribers
6. **Message Attributes**: Structured metadata for messages
7. **Dead Letter Queues**: Handle undeliverable messages
8. **Message Retries**: Automatic retries for failed deliveries

## Use Cases

1. **Application Alerts**: Send notifications for system failures or performance issues
2. **Mobile Push Notifications**: Deliver messages to iOS and Android apps
3. **Event Notifications**: Broadcast events from one system to multiple consumers
4. **Workflow Coordination**: Trigger downstream processes when events occur
5. **SMS Messaging**: Send text messages to users worldwide
6. **Email Notifications**: Send transactional or marketing emails
7. **Fanout to SQS Queues**: Distribute messages to multiple queues for parallel processing
8. **Serverless Architecture**: Trigger Lambda functions in response to events

## Pricing Model

1. **Requests**: $0.50 per million publish requests
2. **Deliveries**:
   - HTTP/HTTPS: $0.60 per million notifications
   - Email/Email-JSON: $2.00 per 100,000 notifications
   - SMS: Varies by country ($0.00645 in US, $0.033 in India)
   - SQS/Lambda: $0.50 per million notifications
3. **Data Transfer**: Standard AWS data transfer rates apply

## Message Attributes

- **DataType**: String, Number, Binary, or custom type
- **Name**: Attribute identifier
- **Value**: Attribute value
- Used for message filtering and routing

## Message Filtering Policies

- JSON-based policies that determine which subscribers receive which messages
- Can filter based on message attributes
- Example: `{"store": ["example_corp"]}` would only deliver messages with `store=example_corp`

## Delivery Retries

- SNS retries failed deliveries with exponential backoff
- Default retry policy:
  - 3 delivery attempts
  - Minimum delay of 20 seconds
  - Maximum delay of 20 minutes
- Configurable per subscription

## Dead Letter Queues (DLQ)

- SQS queue to capture undeliverable messages
- Configured at the subscription level
- Helps debug delivery issues and prevent message loss

## Sample Project: Building a Notification System via AWS Console

### Step 1: Create an SNS Topic

1. Log in to AWS Management Console
2. Navigate to SNS service
3. Click "Create topic"
4. Choose "Standard" type (FIFO is for ordered delivery)
5. Enter name (e.g., "OrderNotifications")
6. Click "Create topic"

![image](https://github.com/user-attachments/assets/3112192a-ad08-407b-9489-148a4573edd3)


### Step 2: Create Subscriptions

#### Email Subscription:
1. In your topic, click "Create subscription"
2. Protocol: "Email"
3. Endpoint: Enter your email address
4. Click "Create subscription"
5. Check your email and confirm the subscription

![image](https://github.com/user-attachments/assets/a5dad6ba-6e48-4088-9013-5ffd0039fb5c)

![image](https://github.com/user-attachments/assets/4126f238-1869-4ea8-afe8-4946a9288738)

![image](https://github.com/user-attachments/assets/8de48018-2196-4c0f-b04d-4531f3697614)

![image](https://github.com/user-attachments/assets/69b74cf2-f9ed-4118-93c3-596a75844427)


#### SMS Subscription:
1. Click "Create subscription"
2. Protocol: "SMS"
3. Endpoint: Enter your phone number with country code (e.g., +15551234567)
4. Click "Create subscription"

![image](https://github.com/user-attachments/assets/d9d882c5-298a-4ce1-a920-b87183a144da)


#### Lambda Subscription:
1. First create a Lambda function (skip if you have one)
   - Go to Lambda service
   - Click "Create function"
   - Use Node.js/Python runtime
   - Add basic code to log the event


     ```python
     def lambda_handler(event, context):
         print("SNS Message Received:", event)
         return {"statusCode": 200}
     ```
![image](https://github.com/user-attachments/assets/db1653f8-30f2-4309-9a1b-557270e90a50)

2. Back in SNS, create subscription
3. Protocol: "AWS Lambda"
4. Endpoint: Select your Lambda function
5. Click "Create subscription"

![image](https://github.com/user-attachments/assets/6f0fa34c-14c2-48ec-a869-1e7d862417ab)


### Step 3: Publish a Message

1. In your SNS topic, click "Publish message"
2. Enter subject: "New Order Received"
3. Message body: `{"orderId": "12345", "customer": "John Doe", "amount": 99.99}`
4. (Optional) Add message attributes:
   - Name: "priority", Type: "String", Value: "high"
5. Click "Publish message"

![image](https://github.com/user-attachments/assets/e629a571-c5d3-4280-9226-74e52d1c457d)
![image](https://github.com/user-attachments/assets/2db01f8e-e56c-42cf-82fb-3bdac8dec7ce)
![image](https://github.com/user-attachments/assets/479cf15a-6185-4aa2-8cce-060d8ce5cd34)

### Lambda
![image](https://github.com/user-attachments/assets/1b653b19-fd88-462f-bf71-059b5a6376d7)

![image](https://github.com/user-attachments/assets/2e6e6709-7241-4197-9a06-5f3a307008b2)


### Step 4: Verify Deliveries

1. Check your email inbox for the notification
2. Check your phone for the SMS
3. Check CloudWatch logs for your Lambda function execution

### Step 5: Set Up Message Filtering

1. Edit the email subscription
2. Enable "Enable message filtering"
3. Add filter policy:
```json
{
  "priority": ["high"]
}
```
4. Now publish two messages:
   - One with `"priority": "high"` (should be delivered)
   - One with `"priority": "low"` (should be filtered out)
5. Verify only high priority messages are received

## 🧪 Testing with Filters (Optional)

Let’s say you want **only critical messages** to go to one email and **all** messages to go to another.

1. **Create Subscription A**:

   * Protocol: Email
   * Endpoint: [critical@example.com](mailto:critical@example.com)
   * Add **Filter Policy**:

     ```json
     {
       "severity": ["critical"]
     }
     ```

2. **Create Subscription B**:

   * Protocol: Email
   * Endpoint: [allalerts@example.com](mailto:allalerts@example.com)
   * No filter

3. **Publish message** with attributes:

   * Message: `Database down`
   * Message attributes:

     * Key: `severity`
     * Value: `critical`

Only [critical@example.com](mailto:critical@example.com) will get this; [allalerts@example.com](mailto:allalerts@example.com) will always get everything.

---


### Step 6: Set Up Dead Letter Queue

1. Create an SQS queue:
   - Go to SQS service
   - Click "Create queue"
   - Name: "OrderNotificationsDLQ"
   - Click "Create queue"
2. Edit your Lambda subscription
3. Under "Dead-letter queue", select your SQS queue
4. Set "Maximum receives" to 3 (after 3 failed attempts, message goes to DLQ)
5. To test:
   - Temporarily make your Lambda function fail (throw error)
   - Publish messages
   - After 3 attempts, check your DLQ for messages

## Advanced Configurations

### Access Control (IAM Policies)

1. Go to your topic's "Access control" tab
2. Create or edit policy to control who can publish/subscribe
3. Example policy allowing a specific IAM user to publish:
```json
{
  "Version": "2012-10-17",
  "Id": "ExamplePolicy",
  "Statement": [
    {
      "Sid": "AllowPublish",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:user/JohnDoe"
      },
      "Action": "sns:Publish",
      "Resource": "arn:aws:sns:us-east-1:123456789012:OrderNotifications"
    }
  ]
}
```

### Encryption

1. Go to your topic's "Encryption" tab
2. Enable encryption
3. Select AWS KMS key (or create new)
4. Choose whether to allow AWS to manage keys or use your own

### Delivery Status Logging

1. Go to your topic's "Delivery status" tab
2. Enable "Enable delivery status logging"
3. Select IAM role (or create new)
4. Choose to log success, failure, or both
5. Select CloudWatch log group

## Monitoring

1. **CloudWatch Metrics**:
   - NumberOfMessagesPublished
   - NumberOfNotificationsDelivered
   - NumberOfNotificationsFailed
   - PublishSize
   - SMSSuccessRate

2. **CloudWatch Logs**:
   - Delivery status logs
   - SMS usage reports

3. **SNS Dashboard**:
   - View pending confirmations
   - Recent deliveries
   - Subscription statistics

## Best Practices

1. Use message attributes for filtering rather than parsing message body
2. Implement DLQs for critical notifications
3. Monitor failed deliveries and set up alarms
4. Use appropriate protocols based on latency requirements
5. Secure your topics with proper IAM policies
6. Consider cost when sending high volumes of SMS/email
7. Use platform endpoints for mobile push to manage device tokens
8. Consider FIFO topics when message ordering is critical

## Clean Up

1. Delete subscriptions
2. Delete the SNS topic
3. Delete the DLQ if created
4. Delete the Lambda function if created for testing

This comprehensive guide covers all major aspects of Amazon SNS with a practical walkthrough. The sample project demonstrates core functionality that can be extended for real-world applications.
