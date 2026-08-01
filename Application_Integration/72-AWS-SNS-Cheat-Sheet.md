# 72 - AWS SNS Cheat Sheet

> Goal: a compact, scenario-keyed quick reference over everything this folder's SNS section (files 57-71) covered — for review, not first-time learning.

---

## 1. SQS vs. SNS, and topic type

| Scenario says... | Pick |
|---|---|
| One message, eventually processed by one worker | **SQS** |
| One event, multiple independent systems need to know immediately | **SNS** |
| Both — broadcast plus durable per-consumer buffering | **SNS Fan-Out to SQS queues** |
| Strict order + exactly-once, and only SQS FIFO queues as subscribers | **SNS FIFO Topic + SQS FIFO Queue(s)** |

---

## 2. Configuration quick table

| Need | Feature |
|---|---|
| Message published but a subscriber never got it | Check the subscription is actually **Confirmed** — unconfirmed subscriptions fail silently |
| Different subscribers should get different subsets of messages | **Subscription Filter Policy**, based on message attributes |
| Prevent sensitive data (card numbers, PII) from being delivered | **Data Protection Policy**, Deny or De-identify action |
| Control retry behavior for a flaky HTTP(S) subscriber | **Delivery retry policy** |
| SNS can't deliver into a subscribed SQS queue | Check the queue's **Access Policy** allows `sns.amazonaws.com` |
| Encrypt topic messages at rest, with audit control | **SSE with a customer managed KMS key** |

---

## 3. Recap

- This cheat sheet is a lookup aid — when a row is unclear, the linked concept note has the full reasoning and, where applicable, a hands-on demo that proved it directly.
- The recurring exam skill across this whole SNS section: recognizing **push vs. pull** and **broadcast vs. point-to-point** as the two axes that separate SNS from SQS.
- This closes out the SNS section of this folder; next: the [Amazon EventBridge](73-Amazon-EventBridge.md) note — a third messaging model, built around routing structured events by content rather than simple topic subscription.

### Sources
- [Amazon Simple Notification Service Developer Guide — AWS docs](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)
