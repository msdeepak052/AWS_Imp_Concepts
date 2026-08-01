# 67 - Amazon SQS Vs Amazon SNS

> Goal: bring the two services fully together in one direct comparison, now that both have been covered in depth — the single most reliably tested "which service" distinction in this entire folder.

---

## 1. The one-sentence distinction

- **SQS** = a **queue** — a message is delivered to (eventually) **one** consumer, who pulls it.
- **SNS** = a **topic** — a message is pushed to **every** current subscriber.

---

## 2. Side-by-side

| | Amazon SQS | Amazon SNS |
|---|---|---|
| **Model** | Point-to-point queue | Publish/subscribe (pub/sub) |
| **Delivery** | **Pull** — consumer calls `ReceiveMessage` | **Push** — SNS delivers immediately on publish |
| **Number of recipients per message** | Effectively **one** (whichever consumer receives and deletes it) | **Every** current subscriber |
| **Message persistence if no one's listening** | Yes — sits in the queue up to the retention period | **No** — SNS doesn't durably store messages for future subscribers; a subscriber that didn't exist at publish time gets nothing |
| **Typical role** | Buffer/work queue between a producer and a processor | Broadcast/notification layer, often fanning out **into** multiple SQS queues |

---

## 3. Why they're frequently used together, not as alternatives

The [Fan-Out](65-SNS-Fan-Out.md) note already showed this directly: SNS's broadcast reach plus SQS's durable, per-consumer buffering solves a problem **neither service solves alone**. A scenario asking "how do we notify three different systems about one event, and make sure none of them lose the notification if they're briefly unavailable" needs **both** — SNS to broadcast, SQS (one queue per system) to durably hold each system's copy.

> 🎯 **Exam tip**: "one message, must eventually be processed by exactly one worker" → **SQS**. "One event, multiple independent systems all need to know" → **SNS**, likely fanning out to **SQS** queues for durability. If a scenario describes both properties at once, the answer is almost always **SNS + SQS together**, not a forced single-service choice.

---

## 4. Recap

- SQS is point-to-point and pull-based; SNS is pub/sub and push-based — genuinely different delivery models, not competing options for the same job.
- SNS does **not** durably retain messages for future subscribers — only currently-subscribed endpoints receive a given publish.
- The two are frequently combined (Fan-Out) rather than chosen between.
- Next: the [SNS + SQS Integration](68-SNS-SQS-Integration.md) note — building this combination for real.

### Sources
- [What is Amazon SNS? — AWS docs](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)
- [What is Amazon Simple Queue Service? — AWS docs](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html)
