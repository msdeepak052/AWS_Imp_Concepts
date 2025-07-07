# Amazon Simple Queue Service (SQS) - Comprehensive Guide

## What is Amazon SQS?

Amazon Simple Queue Service (SQS) is a fully managed message queuing service that enables you to decouple and scale microservices, distributed systems, and serverless applications. It allows you to send, store, and receive messages between software components at any volume without losing messages or requiring other services to be available.

## Key Concepts

1. **Queues**: Temporary repositories for messages awaiting processing
2. **Messages**: Data (up to 256KB) sent to a queue by producers
3. **Producers**: Components that send messages to queues
4. **Consumers**: Components that receive and process messages from queues
5. **Visibility Timeout**: Period during which a message is invisible after being received
6. **Dead Letter Queues (DLQ)**: Queues for messages that couldn't be processed successfully

---

## 🔹 **SQS Core Parameters & Concepts**

| Parameter                                    | Description                                                            |
| -------------------------------------------- | ---------------------------------------------------------------------- |
| **Visibility Timeout**                       | Time a message is hidden from others after one consumer picks it       |
| **Message Retention**                        | How long SQS retains a message (1 min to 14 days)                      |
| **Delivery Delay**                           | Time to delay delivery of all new messages (0–15 mins)                 |
| **Receive Message Wait Time (Long Polling)** | Waits for message availability instead of constant polling (0–20 secs) |
| **Dead Letter Queue (DLQ)**                  | Captures messages that failed multiple processing attempts             |
| **Message Group ID** (FIFO only)             | Grouping for message ordering                                          |
| **Deduplication ID** (FIFO only)             | Ensures exactly-once delivery                                          |
| **Maximum Message Size**                     | Up to 256 KB                                                           |
| **Batch Receive**                            | Receive up to 10 messages in a single API call                         |

---


## Queue Types

### 1. Standard Queues
- Unlimited throughput (nearly unlimited number of transactions per second)
- Best-effort ordering (messages may be delivered out of order)
- At-least-once delivery (occasional duplicates)
- No per-message delay

### 2. FIFO Queues
- Exactly-once processing (no duplicates)
- Strict ordering (first-in-first-out)
- Limited throughput (300 transactions per second without batching)
- Per-message delay capability
- Requires message group ID for ordering

## Key Features

1. **Durability**: Messages stored redundantly across multiple AZs
2. **Scalability**: Automatically scales with your workload
3. **Security**: Encryption at rest and in transit, fine-grained access control
4. **Delay Queues**: Postpone message delivery (0-15 minutes)
5. **Dead Letter Queues**: Handle failed message processing
6. **Long Polling**: Reduce empty responses (1-20 second wait time)
7. **Message Attributes**: Structured metadata for messages
8. **Batch Operations**: Send, receive, delete up to 10 messages per batch
9. **Server-side Encryption**: Optional KMS encryption

## Use Cases

1. **Decoupling Microservices**: Allow services to communicate asynchronously
2. **Buffer for Batch Operations**: Smooth out workload spikes
3. **Task Queues**: Distribute work among worker processes
4. **Order Processing**: Ensure ordered processing (FIFO)
5. **Message Fanout**: Combined with SNS to deliver to multiple queues
6. **Event Source for AWS Lambda**: Trigger Lambda functions from queue messages
7. **Backpressure Management**: Prevent overwhelming downstream systems
8. **Retry Mechanisms**: Handle temporary failures gracefully

## Pricing Model

1. **Requests**: $0.40 per million requests (Standard), $0.50 per million (FIFO)
2. **Data Transfer**: Standard AWS data transfer rates apply
3. **Additional Costs**:
   - KMS encryption keys if used ($1/month per key + $0.03 per 10,000 requests)
   - DLQ storage if messages accumulate

## Message Parameters

1. **Message Body**: Up to 256KB of text (any format)
2. **Message Attributes**: Key-value pairs (up to 10 attributes, 256KB total)
3. **Delay Seconds**: 0-900 (15 minutes) for Standard, 0-15 for FIFO
4. **Message Group ID**: Required for FIFO queues (determines ordering)
5. **Message Deduplication ID**: Required for FIFO queues (prevents duplicates)
6. **Visibility Timeout**: 0-12 hours (default 30 seconds)

## Delivery Mechanisms

1. **Short Polling**: Returns immediately (may be empty)
2. **Long Polling**: Waits up to 20 seconds for messages (reduces empty responses)
3. **Batch Operations**: Process up to 10 messages per API call
4. **Lambda Triggers**: Automatic invocation when messages arrive

## Sample Project: Building an Order Processing System via AWS Console

### Step 1: Create an SQS Queue

1. Log in to AWS Management Console
2. Navigate to SQS service
3. Click "Create queue"
4. Choose queue type:
   - For this example, select "FIFO" (check "Content-based deduplication")
5. Enter queue name (must end with `.fifo`, e.g., `OrderProcessing.fifo`)
6. Configure settings:
   - Visibility timeout: 5 minutes (300 seconds)
   - Delivery delay: 0 seconds
   - Message retention period: 4 days (default)
   - Maximum message size: 256KB (default)
   - Enable "Content-based deduplication" (for FIFO)
7. Click "Create queue"

### Step 2: Create a Dead Letter Queue

1. Click "Create queue" again
2. Name: `OrderProcessingDLQ.fifo`
3. Type: FIFO
4. Leave other settings as default
5. Click "Create queue"
6. Go back to your main queue (`OrderProcessing.fifo`)
7. Select "Edit" → "Dead-letter queue"
8. Select your DLQ
9. Set "Maximum receives" to 3 (after 3 failed attempts, message moves to DLQ)
10. Click "Save"

### Step 3: Send Messages to the Queue

1. Select your `OrderProcessing.fifo` queue
2. Click "Send and receive messages"
3. In the "Message body" enter:
```json
{
  "orderId": "12345",
  "customer": "Jane Smith",
  "items": [
    {"id": "A100", "qty": 2},
    {"id": "B200", "qty": 1}
  ],
  "total": 59.98
}
```
4. Under "Message attributes":
   - Add attribute: Name="priority", Type="String", Value="high"
5. For FIFO queues:
   - Message group ID: "Orders" (all messages with same group ID are ordered)
   - (Optional) Message deduplication ID: "order-12345"
6. Click "Send message"

### Step 4: Receive and Process Messages

1. In the queue, click "Send and receive messages"
2. Under "Receive messages" section:
   - Set "Maximum number of messages" to 10
   - Set "Wait time" to 20 seconds (long polling)
3. Click "Poll for messages"
4. Messages will appear in the bottom section
5. To process a message:
   - Select the message
   - Click "Delete message" after processing (or leave it to reappear after visibility timeout)

### Step 5: Test the Dead Letter Queue

1. Send 3 messages to the main queue
2. Receive them but don't delete (simulate processing failures)
3. After 3 attempts, check the DLQ - messages should appear there
4. You can then analyze failed messages in the DLQ

### Step 6: Set Up Lambda Trigger (Optional)

1. Go to AWS Lambda service
2. Create a new function (Node.js/Python runtime)
3. Add basic code to process messages (example for Node.js):
```javascript
exports.handler = async (event) => {
    console.log('Processing order:', JSON.stringify(event, null, 2));
    event.Records.forEach(record => {
        const body = JSON.parse(record.body);
        console.log('Order ID:', body.orderId);
    });
    return { statusCode: 200, body: 'Processed messages' };
};
```

```python

import json

def lambda_handler(event, context):
    print("Processing order:", json.dumps(event, indent=2))
    
    for record in event['Records']:
        body = json.loads(record['body'])
        print("Order ID:", body['orderId'])
        # Add your processing logic here
        
    return {
        'statusCode': 200,
        'body': 'Processed messages'
    }

```
4. In the Lambda configuration, click "Add trigger"
5. Select "SQS"
6. Choose your `OrderProcessing.fifo` queue
7. Set batch size to 10 (max)
8. Click "Add"
9. Now when you send messages to the queue, Lambda will automatically process them

---

## ✅ **Sample Project: Order Processing Using SQS (Standard Queue)**

### 🔸 **Goal**:

Simulate an online order system where orders are placed (sent to SQS), and a worker (e.g., Lambda or manual pull) processes them.

---

## 🪜 **Step-by-Step Guide via AWS Console**

---

### 🔹 Step 1: Create a Standard Queue

1. Go to **SQS Console**
2. Click **Create queue**
3. Choose **Standard Queue**
4. Enter details:

   * **Name**: `OrderQueue`
   * **Default Visibility Timeout**: `30` seconds
   * **Message retention**: `4` days (default)
   * **Delivery delay**: `0` seconds
   * Enable **Long polling** with `10` seconds (optional but efficient)
5. Click **Create Queue**

---

### 🔹 Step 2: Send a Message (Simulate Order)

1. Open your `OrderQueue`
2. Click **Send and receive messages**
3. Under **Message body**, enter:

   ```json
   {
     "orderId": "12345",
     "item": "Wireless Mouse",
     "quantity": 2
   }
   ```
4. Click **Send message**

---

### 🔹 Step 3: Receive Messages (Manual Simulation)

1. Click **Poll for messages**
2. If a message is there, you'll see it listed
3. Select and click **View/Delete**

   * If you **don’t delete**, it will reappear after visibility timeout

---

### 🔹 Step 4 (Optional): Create a Lambda Consumer

1. Go to **Lambda Console** → Create Function
2. Runtime: **Python 3.12**
   Code:

   ```python
   import json

   def lambda_handler(event, context):
       for record in event['Records']:
           body = json.loads(record['body'])
           print(f"Processing order: {body['orderId']}, Item: {body['item']}")
       return {"statusCode": 200}
   ```
3. Add **SQS trigger**:

   * Choose queue: `OrderQueue`
   * Accept IAM permissions
4. Now, every message will be automatically processed by Lambda.

---

### 🔹 Step 5 (Optional): Add Dead-Letter Queue (DLQ)

1. Create another Standard queue: `OrderQueueDLQ`
2. Go back to `OrderQueue` → **Edit**
3. Under **Dead-letter queue**, choose `OrderQueueDLQ`
4. Set **Max receive count**: `3`

   * After 3 failed attempts, message is moved to DLQ

---



## Advanced Configurations

### Access Control (IAM Policies)

1. Go to your queue's "Access policy" tab
2. Edit policy to control who can send/receive messages
3. Example policy allowing a specific IAM user to send messages:
```json
{
  "Version": "2012-10-17",
  "Id": "ExamplePolicy",
  "Statement": [
    {
      "Sid": "AllowSendMessage",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:user/JaneDoe"
      },
      "Action": "sqs:SendMessage",
      "Resource": "arn:aws:sqs:us-east-1:123456789012:OrderProcessing.fifo"
    }
  ]
}
```

### Encryption

1. Go to your queue's "Encryption" tab
2. Enable encryption
3. Select AWS KMS key (or create new)
4. Choose whether to allow AWS to manage keys or use your own

### Monitoring

1. **CloudWatch Metrics**:
   - NumberOfMessagesSent
   - NumberOfMessagesReceived
   - NumberOfMessagesDeleted
   - ApproximateNumberOfMessagesVisible
   - ApproximateAgeOfOldestMessage

2. **CloudWatch Logs**:
   - Lambda execution logs if using Lambda triggers

3. **SQS Dashboard**:
   - View queue depth
   - Monitor message age
   - Track processing rates

## Best Practices

1. Choose queue type based on requirements:
   - Standard for maximum throughput
   - FIFO for ordering/exactly-once processing

2. Set appropriate visibility timeout:
   - Should cover your processing time plus buffer

3. Use DLQs for handling poison pills (messages that repeatedly fail)

4. Implement exponential backoff for processing failures

5. Use batch operations to reduce costs

6. Consider message size when designing your system (max 256KB)

7. For high throughput, use multiple message group IDs in FIFO queues

8. Monitor queue depth and set up alarms for backlog

## Clean Up

1. Delete all messages from your queues
2. Delete the Lambda function if created
3. Delete the DLQ
4. Delete the main SQS queue

This comprehensive guide covers all major aspects of Amazon SQS with a practical walkthrough. The sample project demonstrates core functionality that can be extended for real-world order processing systems or other message-based workflows.
