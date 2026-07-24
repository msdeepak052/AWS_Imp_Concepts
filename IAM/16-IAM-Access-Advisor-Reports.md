# 16 - IAM Reports, Part 2: IAM Access Advisor Reports

> Goal: use **Access Advisor** (a.k.a. service last accessed data) to see exactly which AWS services a specific user, group, or role has actually **used** — turning "least privilege" from a one-time policy-authoring decision into an ongoing, evidence-based tightening process.

---

## 1. The question Access Advisor answers

Note 15's credential report answers "how old/healthy are this account's credentials?" — a completely different question from the one **Access Advisor** answers: **"of everything this identity is *permitted* to do, which parts has it actually *used*, and when?"**

This is the practical engine behind **least privilege in practice**: a policy might grant access to 40 services, but if Access Advisor shows only 3 of them were ever actually touched in the last 90+ days, that's direct evidence the other 37 can likely be safely removed.

> 🧠 **Mental model:** a policy document tells you what a door key *could* open. Access Advisor tells you which doors it's actually *walked through*, and when it last did — the gap between the two is exactly the unused, safely-removable permission surface.

---

## 2. Where to find it

1. **IAM console** → **Users** (or **User groups**, or **Roles**) → open any specific identity.
2. **Access Advisor** tab.
3. The table lists every AWS **service** included in that identity's attached/inline policies, with columns for:
   - **Last accessed** — the most recent date this identity actually called that service.
   - **Never accessed** shown explicitly where applicable — the clearest possible signal of an unused permission.

> ⚠️ Access Advisor tracks activity at the **service** level (e.g. "Amazon S3," "Amazon EC2"), not down to the individual **API action** — it tells you *whether* S3 was used at all, not specifically which S3 actions (`GetObject` vs. `DeleteBucket`) were called. For action-level granularity, you'd instead look at **AWS CloudTrail** event history directly.

---

## 3. Using Access Advisor to tighten a policy

1. Open the `EC2-S3ReadOnly-Role` from Note 07 → **Access Advisor** tab.
2. Suppose the attached policy also happens to include broader service coverage than actually needed, and Access Advisor shows several listed services as **Never accessed** over a long observation window.
3. That's direct, evidence-based justification to **edit the policy** (Note 03's customer-managed-policy pattern) and remove those unused service permissions — narrowing the role to only what it's demonstrably ever used.

This turns least privilege into a **repeatable, ongoing** practice rather than a single guess made at policy-authoring time — exactly the sort of "don't just write a policy once and forget it" discipline the exam rewards recognizing.

---

## 4. Access Advisor vs. the other two IAM reports

| | Credential Report (Note 15) | Access Advisor (this note) | Access Analyzer (Note 17) |
|---|---|---|---|
| Scope | Whole account, every user | One identity at a time | Whole account, resource + policy focused |
| Answers | "Are credentials old/risky?" | "Which services has this identity actually used?" | "Is anything shared externally, or granted but unused, based on policy logic?" |
| Granularity | Credential metadata (age, MFA, last used) | Service-level usage history | Resource-sharing and policy-logic findings |

> 🎯 **Exam tip:** "identify unused permissions on a role so they can be safely removed, based on actual usage history" is Access Advisor's signature scenario. If the question instead says "identify resources shared with accounts outside my organization," that's Access Analyzer (Note 17), not Access Advisor — the two are easy to confuse by name alone.

---

## 5. Recap

- **Access Advisor** shows, per identity, the **last-accessed date per service** — direct evidence for shrinking overly broad policies down to what's actually used.
- It operates at **service granularity**, not individual API-action granularity (CloudTrail is the tool for that finer level).
- It's distinct from both the credential report (Note 15, account-wide credential hygiene) and Access Analyzer (Note 17, policy-logic-based external-sharing and unused-access findings).
- Next: Note 17 — IAM Reports, Part 3: IAM Access Analyzer, the most powerful and most exam-relevant of the three reporting tools.

### Sources
- [Refining permissions in AWS using last accessed information — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_access-advisor.html)
- [Security best practices in IAM — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
