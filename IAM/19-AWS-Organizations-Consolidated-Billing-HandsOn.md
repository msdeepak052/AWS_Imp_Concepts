# 19 - AWS Organization, Part 2 Practical: Consolidated Billing

> Goal: set up and understand **consolidated billing** — the billing-side benefit every Organization gets (even in "consolidated billing only" mode, Note 18) — including how volume discounts and Reserved Instance/Savings Plans sharing actually combine across accounts.

---

## 1. What consolidated billing does

Every member account's usage is billed to **one invoice**, paid by the **management account** — member accounts never receive (or need to individually pay) their own separate AWS bill.

> 🧠 **Mental model:** think of it like a corporate parent company getting one combined invoice for every subsidiary's spending, instead of each subsidiary being billed separately and having to be reimbursed — simpler accounting, and (Section 3) often cheaper too.

---

## 2. Set it up

1. **AWS Organizations console** (from the **management account**) → confirm the Organization exists (Note 18).
2. Accounts added via invitation or direct creation (Note 18, Section 3) are **automatically** included in consolidated billing — there's no separate opt-in step for billing specifically; it's inherent to being a member account.
3. **Billing and Cost Management console** (management account) → **Bills** → view the combined invoice, broken down **per linked account**, so you can still see exactly what each member account spent even though one entity pays the total.

---

## 3. Volume pricing discounts combine across accounts

Several AWS services offer **tiered volume discounts** that get cheaper per unit the more you use (e.g. S3 storage pricing tiers). Under consolidated billing, usage across **all** member accounts is **aggregated first**, then the volume discount tier is applied to that combined total — meaning a member account that individually would never reach a high-volume discount tier on its own can still benefit from the **combined** organization-wide usage crossing that threshold.

> 🎯 **Exam tip:** "multiple small accounts individually never qualify for a volume discount tier, but combined they would" is a direct, textbook signal pointing at **consolidated billing** — this benefit exists specifically because usage aggregates across the whole Organization before discount tiers are calculated.

---

## 4. Reserved Instances and Savings Plans sharing

By default, **Reserved Instance (RI)** and **Savings Plans** discounts purchased in **any one account** in the Organization can automatically apply to matching usage in **any other account** in the Organization — not just the account that purchased them.

- This means a central team can purchase RIs/Savings Plans once, and every member account running matching instance usage benefits automatically, without needing to purchase its own commitments separately.
- This sharing behavior can be **turned off** per account if isolation of purchasing benefit is specifically desired (e.g. a member account wants to track its own commitment ROI independently) — but it's **on by default** for all accounts in the Organization.

---

## 5. Cost visibility and reporting

- **Cost Explorer** and **Cost and Usage Reports**, run from the management account, can show spending **broken down by linked account**, service, tag, or other dimensions — combined billing doesn't mean combined *reporting* loses per-account granularity, it just means combined *payment*.
- This lets a central FinOps/finance function see the whole Organization's spend in one place while still attributing cost accurately per team/account for chargeback purposes.

---

## 6. Recap

- **Consolidated billing** combines every member account's usage into a **single invoice** paid by the management account, while still preserving **per-account breakdown** in cost reporting.
- **Volume discount tiers** apply to the Organization's **combined** usage, so smaller accounts can benefit from thresholds they'd never individually reach.
- **RI and Savings Plans discounts** are, by default, **automatically shared** across every account in the Organization, not siloed to the account that purchased them.
- This is available even in "consolidated billing only" mode (Note 18) — no need for "all features" mode just to get these billing benefits.
- Next: Note 20 — AWS Organization: Service Control Policies (SCP), the centralized-governance capability that specifically requires "all features" mode.

### Sources
- [Consolidated billing for AWS Organizations — AWS docs](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_billing.html)
- [Turning off Reserved Instance and Savings Plans discount sharing — AWS docs](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_ri-sp-sharing.html)
- [Understanding consolidated bills — AWS docs](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_billing_consolidated-billing.html)
