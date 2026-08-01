# 15 - Amazon Inspector vs. AWS Trusted Advisor

> Goal: separate these two cleanly — both can flag "your EC2 instance has a security problem," which makes them feel interchangeable, but they're looking for genuinely different kinds of problems, using genuinely different methods.

---

## 1. The one-sentence distinction

- **Inspector** = deep, continuous **vulnerability scanning** — specific CVEs in specific installed package versions, plus network reachability, on EC2/ECR/Lambda.
- **Trusted Advisor** = broad, lightweight **best-practices checklist** — across cost, performance, security, fault tolerance, and service limits, account-wide.

Inspector asks "does this exact instance have `openssl` version X, which has known CVE-Y, and can that actually be reached over the network?" Trusted Advisor asks a much broader set of shallower questions: "is MFA enabled on root? Is this S3 bucket public? Are you close to a service quota?"

---

## 2. Side-by-side

| | Amazon Inspector | AWS Trusted Advisor |
|---|---|---|
| **Scope** | EC2, ECR container images, Lambda functions | Account-wide — nearly every service, five categories |
| **Depth on security specifically** | Deep — actual CVE-level package vulnerability data, with severity scoring | Shallow but broad — configuration-level checks (public resources, open ports, MFA), not CVE scanning |
| **Categories covered** | Security only (vulnerabilities + network reachability) | **Cost**, **Performance**, **Security**, **Fault Tolerance**, **Service Limits** |
| **How it collects data** | Agent-based (SSM) or agentless (EBS snapshot) — see [Amazon Inspector](13-Amazon-Inspector.md) Section 3 | Reads account/resource configuration via each service's own API — no agent involved at all |
| **Cost model** | Pay per resource scanned | Free core checks on every account; full library needs **Business Support+** — see [AWS Trusted Advisor](14-AWS-Trusted-Advisor.md) Section 3 |

---

## 3. When a scenario points to which

- "A specific EC2 instance is running a package with a known CVE" → **Inspector** — this is precisely its specialty, and Trusted Advisor has no equivalent CVE-level check at all.
- "Is our root account missing MFA, or is this S3 bucket accidentally public" → either could technically flag it, but **Trusted Advisor**'s free-tier checks cover exactly these two by default, at zero cost and zero setup — the simpler, more direct answer.
- "We're approaching a service quota and need a warning before it becomes a problem" → **Trusted Advisor** — Inspector has no concept of account service limits at all, that's purely a Trusted Advisor category.
- "We need continuous, automatic re-scanning as new CVEs are published, not just a point-in-time check" → **Inspector**, specifically because of its event-driven re-scan behavior described in [Amazon Inspector](13-Amazon-Inspector.md) Section 3.

> 🎯 **Exam tip**: if the scenario mentions a **CVE**, a **specific vulnerable package version**, or **container/Lambda scanning**, that's Inspector. If it mentions **cost savings**, **service limits**, or a **broad account health checklist** spanning multiple unrelated categories, that's Trusted Advisor. Security-flavored scenarios are the only real overlap zone, and even there, "deep/specific" vs. "broad/shallow" is the tiebreaker.

---

## 4. Recap

- Inspector is a **specialist**: deep vulnerability scanning on a narrow set of resource types (EC2, ECR, Lambda).
- Trusted Advisor is a **generalist**: broad, lightweight checks across five categories, account-wide, with no agent required at all.
- Their only real overlap is security, and even there they operate at different depths — CVE-level detail vs. configuration-level checklist items.
- This closes out the Monitoring & Auditing topic series for this project — together, [CloudWatch](01-Amazon-CloudWatch-Introduction.md) (health), [CloudTrail](07-AWS-CloudTrail-Introduction.md) (who-did-what), [Config](10-AWS-Config.md) (configuration state), [Inspector](13-Amazon-Inspector.md) (vulnerabilities), and Trusted Advisor (best practices) cover five genuinely distinct, commonly-confused angles on "is my AWS account okay."

### Sources
- [Amazon Inspector user guide — AWS docs](https://docs.aws.amazon.com/inspector/latest/user/what-is-inspector.html)
- [AWS Trusted Advisor check reference — AWS docs](https://docs.aws.amazon.com/awssupport/latest/user/trusted-advisor-check-reference.html)
