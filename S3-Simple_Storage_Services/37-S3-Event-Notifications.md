# 37 - AWS S3 Event Notification

> Goal: configure a bucket to automatically notify a destination service whenever specific events happen (object created, deleted, restored, etc.) — the trigger mechanism behind a huge range of event-driven S3 architectures.

---

## 1. What S3 Event Notifications are

**S3 can automatically send a notification** whenever a specified event occurs on a bucket — most commonly `s3:ObjectCreated:*` (any kind of upload) or `s3:ObjectRemoved:*` (any kind of delete) — to one of **three** destination types, letting downstream systems react immediately instead of polling the bucket for changes.

> 🧠 **Mental model:** this is the same "let something happen automatically in response to an event" philosophy as a Lifecycle rule (Notes 07-08) reacting to *age*, except here the trigger is a *specific action* (a new object landing, an object disappearing) happening *right now*, not a scheduled age threshold.

---

## 2. The three destination types

| Destination | Best for |
|---|---|
| **Amazon SNS** (Simple Notification Service) | Fan-out to multiple subscribers at once (e.g. email, SMS, multiple SQS queues, multiple Lambda functions) |
| **Amazon SQS** (Simple Queue Service) | Decoupling — a queue that downstream consumers poll and process at their own pace, with built-in retry/redrive behavior |
| **AWS Lambda** | Direct, immediate custom code execution in response to the event — e.g. resizing an uploaded image, validating a file, kicking off a processing pipeline |

> 🧠 A common real pattern: **upload triggers a Lambda function** that processes the file (e.g. generates a thumbnail, extracts metadata, or validates a CSV) — this exact "S3 upload → Lambda processing" chain is one of the most common serverless architecture building blocks in AWS, referenced throughout this repo's `Lambda` folder.

---

## 3. Configure a notification (S3 → Lambda)

1. **S3 console** → bucket → **Properties** tab → **Event notifications** → **Create event notification**.
2. **Name**: `on-upload-process`.
3. **Prefix/suffix filter** (optional): e.g. suffix `.csv` to only trigger for CSV uploads, not every file type.
4. **Event types**: check **All object create events** (`s3:ObjectCreated:*`).
5. **Destination**: **Lambda function** → select an existing function (must already have a **resource-based policy** allowing S3 to invoke it — the console offers to add this automatically).
6. **Save changes**.

---

## 4. EventBridge — the modern, more flexible alternative

S3 can also send **every event** to **Amazon EventBridge** (a single toggle: **Properties** → **Amazon EventBridge** → **Enable**), which then lets you build **much more flexible routing rules** than the three-destination-type model above — matching on event patterns, routing to dozens of possible AWS service targets (Step Functions, additional Lambda functions, Kinesis, and more), and combining S3 events with events from other services in one unified rule engine.

> 🎯 **Exam tip:** "route S3 events to multiple different types of targets with complex filtering logic, or combine S3 events with events from other AWS services" points to the **EventBridge** integration — the classic three-destination-type notification config (Section 2) is simpler and sufficient for straightforward single-destination cases, but EventBridge is the more powerful, flexible modern answer whenever the question emphasizes complex routing.

---

## 5. Common triggering events

| Event | Fires when |
|---|---|
| `s3:ObjectCreated:*` | Any object is uploaded (PUT, POST, COPY, multipart complete) |
| `s3:ObjectRemoved:*` | An object (or a specific version) is deleted |
| `s3:ObjectRestore:*` | A Glacier-class object's restore request (Note 05) completes |
| `s3:Replication:*` | A CRR (Note 30) replication event completes or fails |

---

## 6. Recap

- **S3 Event Notifications** trigger automatically on specific bucket events, delivered to **SNS**, **SQS**, or **Lambda** — the standard building block for event-driven, serverless S3 processing pipelines.
- **EventBridge** integration (a single toggle) unlocks far more flexible routing/filtering than the native three-destination model, and lets S3 events combine with events from other services.
- Next: Note 38 — AWS S3 Multipart Upload (Hands-On), the mechanism referenced back in Note 02 for uploading objects larger than a single PUT request can handle.

### Sources
- [Amazon S3 Event Notifications — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/NotificationHowTo.html)
- [Using EventBridge with Amazon S3 — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventBridge.html)
- [Supported event types — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-how-to-event-types-and-destinations.html)
