# 11 - Introduction Of Amazon Q

> Goal: understand what Amazon Q is at a high level, before the next few notes go deeper — and get an important, current (2026) status update up front, since this specific corner of AWS has changed significantly and a course recorded even a year or two ago would already be describing something that's since shifted.

---

## 1. What Amazon Q is, simply

**Amazon Q** is AWS's family of generative-AI assistants, built into the AWS ecosystem. Instead of a general-purpose chatbot that knows nothing about your specific AWS account, Amazon Q's assistants are designed to be **aware of AWS itself** — your resources, your documentation, your code, your account's actual configuration — so it can answer questions and take actions in that specific context.

> 🧠 **Simple analogy**: a general AI chatbot is like asking a very smart stranger for advice — they're knowledgeable, but they don't know anything about *your* specific house, your specific bills, or your specific situation. Amazon Q is more like asking a smart assistant who already has access to your actual AWS account — it can look at your actual EC2 instances, your actual IAM policies, your actual code, not just give generic advice.

---

## 2. Amazon Q isn't one single product — it's a family

| Product | What it's for |
|---|---|
| **Amazon Q Business** | A workplace assistant for **non-developers** — answers questions using your company's internal documents, wikis, and data sources |
| **Amazon Q Developer** | An AI coding assistant for **developers** — code suggestions, chat, debugging help, integrated into IDEs and AWS consoles (covered in depth in the [Amazon Q Developer](12-Amazon-Q-Developer.md) note) |
| **Amazon Q in QuickSight / Connect / other services** | Feature-specific AI assistants embedded inside individual AWS services |

This folder focuses on **Amazon Q Developer**, since that's the one relevant to writing and understanding Lambda functions.

---

## 3. ⚠️ Important 2026 status update — read this before the next three notes

At the time of writing (mid-2026), AWS has announced that **Amazon Q Developer is being retired**, replaced by a new product called **Kiro** — an agentic, "spec-driven" IDE built by AWS. The concrete timeline:

- **New signups** for Amazon Q Developer (Free tier and Pro) were **blocked starting May 15, 2026**.
- Existing IDE plugins and paid subscriptions continue to work, with **full end-of-support on April 30, 2027**.
- AWS is directing both new and existing users toward **Kiro** going forward.

This matters directly for this folder: the next few notes (12, 13, 14) explain Amazon Q Developer as a concept and how it integrates with Lambda **because it's still a valid, testable SAA-C03 topic and many existing AWS accounts still have it active** — but if you're setting this up fresh today, you may not be able to enable it as a **new** user, and AWS's own current recommendation is Kiro instead. Each of the next three notes calls this out again at the relevant point, rather than leaving it as a one-time footnote here.

> 🧠 This is exactly why this whole folder was built by checking AWS's *current* documentation rather than relying on memorized course content — a course recorded even a year ago could easily be describing a console flow that's already partially retired.

---

## 4. Why AWS builds these assistants directly into the console at all

The general theme across the whole Amazon Q family: reduce how much a user has to already know to get useful help. Instead of leaving the console (to search documentation, ask in a forum, or paste an error into a separate chatbot), the assistant is available **right where you're already working** — inside the Lambda code editor, inside the EC2 console, inside a chat panel in the AWS console itself.

---

## 5. Recap

- **Amazon Q** is AWS's family of AI assistants, built to be aware of your actual AWS account/resources/code, not just a generic chatbot.
- **Amazon Q Business** targets non-developers (internal company knowledge); **Amazon Q Developer** targets developers (code, debugging, AWS console help).
- **Amazon Q Developer is being retired in favor of Kiro** — new signups blocked since May 15, 2026, full end-of-support April 30, 2027 for existing users. Keep this in mind through the next three notes.
- Next: the [Amazon Q Developer](12-Amazon-Q-Developer.md) note, going deeper into what it actually does (and its current status in more detail).

### Sources
- [What is Amazon Q? — AWS docs](https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/what-is.html)
- [Amazon Q Developer end-of-support announcement — AWS DevOps & Developer Productivity Blog](https://aws.amazon.com/blogs/devops/amazon-q-developer-end-of-support-announcement/)
