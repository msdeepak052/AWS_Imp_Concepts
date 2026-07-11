# 32 - AWS S3 Server Access Logging

> Goal: enable **server access logging** — a record of every request made against a bucket — and understand exactly what it captures, its delivery delay, and how it differs from Note 33's CloudTrail data events, which cover very similar ground through a different mechanism.

---

## 1. What server access logging captures

Once enabled, S3 writes a **log file** (as plain-text objects, delivered into a **target bucket** you designate) recording detailed information about **every request** made to the source bucket: requester (if authenticated), request time, action performed, the specific key involved, response status, error code (if any), bytes sent, and more.

> 🧠 **Mental model:** this is a raw, detailed **access log**, similar in spirit to a web server's access log — every single request, logged as a line of text, delivered to another bucket for you to later analyze (often via Athena, a data-lake query tool, since these logs can get voluminous).

---

## 2. Enable it

1. **Target bucket** (where logs will land) — create one, or use an existing one, and ensure it grants the **S3 Log Delivery group** (Note 13's predefined ACL grantee) write permission — the console handles this automatically when enabling logging through it.
2. **Source bucket** → **Properties** tab → **Server access logging** → **Edit** → **Enable**.
3. **Target bucket**: select the logging destination bucket.
4. **Target prefix**: e.g. `logs/demo-bucket/` — keeps log objects organized if the target bucket is shared across multiple source buckets.
5. **Save changes**.

> ⚠️ The **target bucket must be in the same Region** as the source bucket, and — to avoid a confusing infinite loop — **should not be the same bucket that's being logged** (logging a bucket into itself would mean the log-delivery writes themselves also get logged, endlessly compounding).

---

## 3. Delivery is best-effort and NOT real-time

Log delivery is **asynchronous and best-effort** — log files typically arrive within a few hours, but AWS makes **no guarantee** on exact delivery time, and (rarely) some log records could be delayed further or, in very rare circumstances, not delivered at all. This makes server access logging unsuitable for anything requiring **real-time** or guaranteed-complete auditing.

> 🎯 **Exam tip:** "we need a best-effort, detailed record of every request for later analysis, cost isn't a major concern, but real-time alerting isn't required" points to **server access logging**. The moment a scenario says **real-time**, or emphasizes a **guaranteed, complete** audit trail (e.g. for compliance purposes where "we might have missed logging some requests" is unacceptable), that's pointing toward **CloudTrail data events** (Note 33) instead.

---

## 4. Recap

- **Server access logging** delivers detailed, per-request log files to a separate target bucket, in the **same Region**, on a **best-effort, asynchronous** basis (typically hours of delay).
- Requires the target bucket to grant the S3 Log Delivery group write access — handled automatically by the console.
- Not suitable for real-time or guaranteed-complete auditing needs — see Note 33 for that stronger guarantee.
- Next: Note 33 — AWS S3 CloudTrail Data Events, the more rigorous, real-time-capable alternative/complement to this note's logging.

### Sources
- [Logging requests using server access logging — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerLogs.html)
- [Amazon S3 server access log format — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/LogFormat.html)
