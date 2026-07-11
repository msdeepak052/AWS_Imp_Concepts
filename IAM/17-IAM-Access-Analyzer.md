# 17 - IAM Reports, Part 3: IAM Access Analyzer

> Goal: understand **IAM Access Analyzer** — the most powerful and most heavily exam-tested of the three IAM reporting tools in this mini-series — and its three distinct capabilities: external access findings, unused access findings, and policy validation/custom policy checks.

---

## 1. What makes Access Analyzer different from Notes 15-16

Access Analyzer doesn't read historical logs the way Access Advisor does (Note 16) — it uses **automated/logic-based reasoning** (a formal analysis technique, not just log-scraping) to mathematically evaluate what a **resource policy** or **IAM policy** actually, provably permits, across every possible combination of conditions — closer to a policy "prover" than a report generator.

> 🧠 **Mental model:** Access Advisor (Note 16) tells you what an identity **has done**. Access Analyzer tells you what a policy **provably allows**, including paths that were never actually exercised yet — catching a dangerously overbroad grant *before* it's ever misused, not just after the fact.

---

## 2. Set up an analyzer

1. **IAM console** → **Access Analyzer** → **Create analyzer**.
2. **Zone of trust**: your current account, or (if using AWS Organizations, Note 18) the entire organization.
3. **Analyzer type**: an **external access analyzer** (Section 3) and/or an **unused access analyzer** (Section 4) — these are configured as separate analyzer types, both available once Access Analyzer is enabled.

---

## 3. External access findings

Continuously scans **resource-based policies** (S3 bucket policies, IAM role trust policies, KMS key policies, Lambda resource policies, and others) and generates a **finding** for every case where a resource is accessible by a principal **outside your defined zone of trust** — e.g. a different AWS account, or a public/anonymous principal.

- This is the direct, automated version of manually auditing every bucket policy and role trust policy in the account for "did I accidentally make this public, or share it with the wrong account?"
- Findings can be marked **Resolved** (if the external access was intentional — e.g. a legitimate cross-account role from Note 09) or trigger a fix if it wasn't.

> ⚠️ External access findings are provided **at no additional charge** — this is the original, foundational capability Access Analyzer launched with, and remains free to run continuously.

---

## 4. Unused access findings

A newer analyzer type, generating findings for three categories of access that exist but have gone **unused** for a configurable observation window:

| Finding type | What it flags |
|---|---|
| **Unused IAM roles** | A role with no access activity at all in the window |
| **Unused IAM user credentials** | Passwords or access keys that haven't been used in the window |
| **Unused permissions** | Specific service- or even action-level permissions granted (via policy) that a role never actually exercised in the window |

This directly overlaps with — and goes further than — Note 16's Access Advisor manual review, by proactively surfacing unused access as **findings** rather than requiring someone to open each identity's Access Advisor tab individually.

> ⚠️ Unlike external access findings, **unused access findings are a paid feature**, billed based on the number of IAM roles/users analyzed per month.

---

## 5. Policy validation and custom policy checks

Before you even deploy a policy, Access Analyzer can check it for problems:

- **Basic policy validation** (free) — checks for syntax errors and general best-practice warnings (e.g. an overly permissive wildcard) directly in the policy editor, as you write it.
- **Custom policy checks** (a **paid** feature) — lets you ask specific, pointed questions about a policy before deploying it, such as *"does this updated policy grant any new public/external access compared to the previous version?"* or *"does this policy grant access to this specific sensitive action?"* — validated using the same logic-based reasoning engine, not just a lint pass.

> 🎯 **Exam tip:** "identify S3 buckets or IAM roles that are unintentionally accessible from outside the account/organization" is the textbook **external access finding** scenario — far and away the most exam-relevant Access Analyzer capability. If a question instead emphasizes "unused permissions that should be removed," that overlaps with Note 16's Access Advisor territory, but Access Analyzer's unused access findings automate that same discovery as standing findings.

---

## 6. All three IAM reports, side by side

| | Credential Report (15) | Access Advisor (16) | Access Analyzer (17) |
|---|---|---|---|
| Method | Static CSV snapshot | Per-identity usage history | Logic-based reasoning over policies |
| Core question | "Are credentials stale/risky?" | "What has this identity actually used?" | "What does this policy provably allow, and is any of it external or unused?" |
| Findings for external sharing? | No | No | ✅ Yes (external access findings) |
| Findings for unused access? | No | Manual (you read the tab yourself) | ✅ Yes, as standing findings (paid) |
| Pre-deployment policy validation? | No | No | ✅ Yes (basic free, custom checks paid) |

---

## 7. Recap

- **IAM Access Analyzer** uses automated/logic-based reasoning (not log history) to evaluate what policies provably allow, across three capabilities: **external access findings** (free), **unused access findings** (paid), and **policy validation/custom policy checks** (basic free, custom paid).
- External access findings are the single most exam-relevant capability — the automated way to catch unintentionally public or cross-account-shared resources.
- This closes the three-part IAM reporting series (Notes 15-17). Next: Note 18 — AWS Organization, Part 1, moving from single-account identity governance to managing **multiple** AWS accounts as one structured whole.

### Sources
- [Using IAM Access Analyzer — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html)
- [IAM Access Analyzer findings — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-findings.html)
- [IAM Access Analyzer policy validation — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html)
- [IAM Access Analyzer pricing — AWS](https://aws.amazon.com/iam/access-analyzer/pricing/)
