# 56 - AWS SQS Cheat Sheet

> Goal: a compact, scenario-keyed quick reference over everything this folder's SQS section (files 35-55) covered — for review, not first-time learning.

---

## 1. Queue type decision

| Scenario says... | Pick |
|---|---|
| Order doesn't matter, extremely high throughput, occasional duplicates tolerable | **Standard queue** |
| Strict order required, exactly-once processing required | **FIFO queue** (`.fifo` name required) |

---

## 2. Configuration quick table

| Need | Setting |
|---|---|
| Message being processed twice by different consumers | Increase **Visibility Timeout**, or call `ChangeMessageVisibility` |
| Reduce empty-poll API calls/cost | **Receive Message Wait Time** > 0 (long polling) |
| Messages disappearing after a long consumer outage | **Message Retention Period** — max 14 days, default 4 |
| A "poison pill" message retries forever | **Dead-Letter Queue** + Redrive Policy `maxReceiveCount` |
| Only specific queues should redirect into a DLQ | **Redrive Allow Policy: `byQueue`** |
| Two identical-content messages must both be processed | Explicit **`MessageDeduplicationId`**, not content-based dedup |
| Ordering needed per-entity but not globally, with higher throughput | **Message Group ID** + **Deduplication Scope: Message Group** |
| Need FIFO throughput beyond 3,000/sec batched | **High Throughput Mode** |
| Encrypt at rest with audit control over the key | **SSE with a customer managed KMS key** |
| S3 event notifications to SQS aren't arriving | Check the queue's **Access Policy** first |
| Scale EC2 consumers with backlog | CloudWatch alarm on **`ApproximateNumberOfMessagesVisible`** → Auto Scaling |
| Serverless consumer, auto-scaling, no infrastructure | **Lambda + SQS event source mapping** |
| Process urgent messages before routine ones | **Separate queues per priority**, consumer checks high-priority first |

---

## 3. Recap

- This cheat sheet is a lookup aid — when a row is unclear, the linked concept note has the full reasoning and, where applicable, a hands-on demo that proved it directly.
- SQS questions on the exam are almost always testing a **specific setting or symptom**, not general awareness that "SQS is for queuing."
- This closes out the SQS section of this folder; next: the [Amazon SNS - Introduction](57-Amazon-SNS-Introduction.md) note — moving into push-based, pub/sub messaging.

### Sources
- [Amazon Simple Queue Service Developer Guide — AWS docs](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html)
