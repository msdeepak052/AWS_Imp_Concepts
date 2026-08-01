# 11 - AWS Config vs. AWS CloudTrail

> Goal: pin down the single most commonly confused pairing in this entire folder — both services clearly relate to "account history," but they record two genuinely different things, and the [AWS Config](10-AWS-Config.md) hands-on demo's own Section 6 (the configuration timeline) is the clearest concrete illustration of the gap.

---

## 1. The one-sentence distinction

- **CloudTrail** = a log of **API calls** — the *actions* people and services took.
- **Config** = a timeline of **resource configuration state** — what a resource actually *looked like*, before and after.

CloudTrail tells you `ModifySecurityGroupRules` was called, by whom, at what time. Config tells you what the security group's rule set actually **was** before that call, and what it became after — the *result*, not just the *action*.

---

## 2. Side-by-side

| | AWS CloudTrail | AWS Config |
|---|---|---|
| **What it records** | Every API call — a sequence of discrete **events** | A resource's **configuration snapshots** over time |
| **The question it answers** | "Who did this, when, from where?" | "What did this resource look like at time X, and what changed?" |
| **Default behavior** | Always on — 90-day free Event History from account creation | **Off** until you explicitly set it up |
| **Compliance checking?** | No — it's a record, not an evaluator | **Yes** — Config Rules continuously evaluate resources against a desired state |
| **Granularity** | Every individual API call (management events by default; data events opt-in) | Configuration Items generated on meaningful resource changes |
| **Typical evidence in an audit** | "User X called `DeleteBucket` on bucket Y at 14:02 UTC" | "Bucket Y's public-access setting changed from blocked to open at 14:02 UTC, and stayed non-compliant until 14:15 UTC" |

---

## 3. Why they're often used together, not instead of each other

A real investigation frequently needs **both**: CloudTrail identifies **who** made a change and **when**; Config shows **what that change actually did** to the resource's configuration, and whether it violated policy. Neither one fully replaces the other — this is the same complementary relationship this folder's [AWS Config demo](10.01-AWS-Config-Demo.md) exercised directly: the bucket policy edit was one CloudTrail event, but Config's timeline is what showed the bucket's full before/after public-access state.

> 🎯 **Exam tip**: "who made this API call" → CloudTrail. "Is this resource compliant, and when did it stop being compliant" → Config. A scenario combining both ("who made the change that caused this resource to become non-compliant") genuinely needs both services correlated together — not a trick, just the realistic real-world use case.

---

## 4. Recap

- CloudTrail logs **actions** (API calls); Config tracks **state** (resource configuration over time) and evaluates it against rules.
- CloudTrail is **on by default**; Config must be **explicitly enabled**.
- Only Config does **compliance evaluation** — CloudTrail has no concept of "compliant"/"non-compliant."
- They're complementary, frequently correlated together in real investigations, not competing choices.
- Next: the [CloudTrail vs. CloudWatch](12-CloudTrail-vs-CloudWatch.md) note — the other frequently-confused pairing in this folder.

### Sources
- [What is AWS Config? — AWS docs](https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html)
- [What is AWS CloudTrail? — AWS docs](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html)
