# 82 - AWS EventBridge Cheat Sheet

> Goal: a compact, scenario-keyed quick reference over everything this folder's EventBridge section (files 73-81) covered — for review, not first-time learning.

---

## 1. Core pipeline quick table

| Piece | Role |
|---|---|
| **Event Source** | AWS service, SaaS partner, or custom app emitting structured JSON events |
| **Event Bus** | Default (AWS services), custom (your app), or partner (a specific SaaS integration) |
| **Rule** | Contains an event pattern; matches events by content, not just by source |
| **Target** | What a fired rule invokes — supports multiple targets per rule, natively, across many AWS services |

---

## 2. Scenario quick table

| Scenario says... | Answer |
|---|---|
| React to native AWS service activity (e.g. EC2 state change) | Rule on the **default event bus** |
| Keep custom application events organizationally separate | A dedicated **custom event bus** |
| Receive events from a specific SaaS platform | **Partner event bus** |
| Route based on the actual content/values inside an event | An **event pattern** matching into the `detail` field |
| One event should trigger several independent actions | A single **Rule with multiple Targets** |
| Reshape an event before a target receives it | **Input Transformer** |
| New time-based (scheduled) triggering requirement | **EventBridge Scheduler** — not the legacy scheduled rule mechanism |
| One-time future invocation, specific time zone | **EventBridge Scheduler** — a legacy scheduled rule can't do either |

---

## 3. Recap

- This cheat sheet is a lookup aid — when a row is unclear, the linked concept note has the full reasoning and, where applicable, a hands-on demo that proved it directly.
- The single most valuable habit from this section: EventBridge is fundamentally about **content-based routing across many sources**, distinct from SQS's point-to-point queue and SNS's topic-subscription broadcast.
- This closes out the EventBridge section of this folder; next: the [Data Processing](83-Data-Processing.md) note — moving into streaming/analytics services.

### Sources
- [Amazon EventBridge User Guide — AWS docs](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html)
