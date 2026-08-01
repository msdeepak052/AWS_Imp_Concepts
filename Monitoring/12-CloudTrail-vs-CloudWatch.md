# 12 - AWS CloudTrail vs. Amazon CloudWatch

> Goal: resolve the other genuinely common mix-up in this folder — the two services' names both sound like general-purpose "monitoring," and CloudTrail events **can** even end up inside CloudWatch Logs, which makes the boundary feel blurrier than it actually is.

---

## 1. The one-sentence distinction

- **CloudWatch** = operational **health and performance** — metrics, logs, alarms, dashboards.
- **CloudTrail** = **who did what** — an audit trail of API activity, for security and accountability.

If the question is "is my application/infrastructure healthy right now, and can I react automatically if it isn't," that's CloudWatch. If the question is "who created/deleted/modified this specific resource, and were they authorized to," that's CloudTrail.

---

## 2. Side-by-side

| | Amazon CloudWatch | AWS CloudTrail |
|---|---|---|
| **Primary concern** | Operational health/performance | Account security/accountability |
| **Core data types** | Metrics (numeric), Logs (text), Alarms, Events | API call records ([management/data events](08-CloudTrail-Event-Types.md)) |
| **Typical question answered** | "Is CPU/latency/error rate within normal range?" | "Who deleted this resource, and when?" |
| **Reacts automatically?** | Yes — **Alarms** can notify or trigger remediation | No — it's a passive record; reacting to it needs something else reading it (e.g. EventBridge, or a subscription filter if delivered to CloudWatch Logs) |
| **Default retention** | Metrics: 15 months, at declining resolution; Logs: **indefinite by default** unless set | Event History: fixed **90 days**; a Trail: whatever you configure |

---

## 3. Where the confusion genuinely comes from: they can be wired together

A CloudTrail **Trail** can be configured to **also** deliver its events into **CloudWatch Logs** — at that point, CloudTrail data is sitting inside a CloudWatch Logs log group, queryable with [Logs Insights](05-CloudWatch-Logs-Insights.md), and a **CloudWatch Alarm** can be built on a **metric filter** over that log group (e.g. alarm the moment a `DeleteBucket` or `ConsoleLogin` failure event appears). At that point, CloudWatch is doing the *reacting*, but CloudTrail is still the thing that originally *recorded* the event — the two roles don't merge, they connect.

> 🎯 **Exam tip**: "alert me in near-real-time whenever a specific API call happens" sounds like it could be either service — the actual mechanism is **CloudTrail → CloudWatch Logs (via a Trail) → a metric filter → a CloudWatch Alarm**. Recognizing that chain, rather than picking one service in isolation, is what the exam is actually testing here.

---

## 4. Recap

- **CloudWatch** watches operational health; **CloudTrail** watches **who did what** to your account.
- CloudWatch **can act automatically** (alarms → SNS/remediation); CloudTrail is a **passive record** unless paired with something else reading it.
- Delivering a Trail's events into **CloudWatch Logs** is the standard bridge between the two — it doesn't blur their separate jobs, it chains them.
- Next: the [Amazon Inspector](13-Amazon-Inspector.md) note — a fourth, distinct concern (vulnerability scanning) rounding out this folder's monitoring/auditing services.

### Sources
- [What is Amazon CloudWatch? — AWS docs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html)
- [Sending events to CloudWatch Logs — AWS CloudTrail docs](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/monitor-cloudtrail-log-files-with-cloudwatch-logs.html)
- [Creating a metric filter for a CloudWatch Logs log group — AWS docs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/MonitoringLogData.html)
