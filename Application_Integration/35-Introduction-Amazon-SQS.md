# 35 - Introduction - Amazon SQS

> Goal: get a first orientation to Amazon Simple Queue Service — AWS's fully managed message queue, and the primary tool for the **asynchronous** side of the [Synchronous vs. Asynchronous](05-Synchronous-VS-Asynchronous.md) note.

---

## 1. The problem: work that shouldn't be lost if the processor is busy or down

Imagine an e-commerce site's order processing: at checkout, an order needs to be validated, charged, and fulfilled. If that all happened **synchronously** inside the checkout API call, a slow fulfillment step would make the customer wait, and a fulfillment outage would make checkout fail entirely. **Amazon SQS** solves this: the checkout process drops a message onto a queue and returns immediately, while a separate process consumes and handles that message whenever it's ready — completely decoupled.

---

## 2. Architecture & workflow

```mermaid
flowchart LR
    PRODUCER["Producer — e.g. checkout service"]
    QUEUE["SQS Queue"]
    CONSUMER["Consumer — e.g. fulfillment service"]

    PRODUCER -->|"SendMessage"| QUEUE -->|"ReceiveMessage"| CONSUMER
```

---

## 3. What makes SQS specifically valuable

| Property | Why it matters |
|---|---|
| **Fully managed** | No servers to run or scale — AWS operates the queue infrastructure entirely |
| **Durable** | Messages are stored redundantly across multiple Availability Zones |
| **Decouples producer and consumer** | The producer never needs to know if, or how fast, the consumer is processing |
| **Absorbs traffic spikes** | A sudden burst of messages queues up rather than overwhelming the consumer |
| **Nearly unlimited throughput** (Standard queues) | Scales automatically with demand, no capacity planning required |

---

## 4. Recap

- SQS is a fully managed message queue — the standard AWS tool for asynchronous, decoupled communication between producer and consumer.
- It exists specifically to solve the fragility problems direct, synchronous calls create: unavailability, slowness, and traffic bursts all get absorbed by the queue instead of directly impacting the caller.
- Next: the [Core Components SQS](36-Core-Components-SQS.md) note — the actual pieces (queues, messages, producers, consumers) this all runs on.

### Sources
- [What is Amazon Simple Queue Service? — AWS docs](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html)
