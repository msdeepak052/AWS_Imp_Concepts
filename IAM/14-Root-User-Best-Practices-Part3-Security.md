# 14 - IAM Root User Best Practices, Part 3: Root User Security

> Goal: close out the root-user series with the remaining hardening steps beyond MFA (Note 12) and avoiding routine use (Note 13) — access keys, contact information, monitoring, and organization-level lockdown.

---

## 1. Delete root's access keys entirely — don't just avoid using them

If root access keys exist at all (some accounts have them left over from before best practices were followed, or from initial account setup), the correct move isn't to "be careful with them" — it's to **delete them entirely**:

1. Sign in as root → **Security credentials** → **Access keys**.
2. If any exist, **Deactivate**, then **Delete** each one.
3. Root **never needs programmatic (CLI/SDK/API) access** for any of the narrow task list from Note 13 — every one of those tasks is a console-only action. A root access key existing at all is pure downside with no corresponding legitimate use case in normal operation.

> ⚠️ A root access key is the single most dangerous credential an AWS account can have — long-term, tied to an identity that bypasses IAM's policy evaluation entirely (Note 12), and usable programmatically without ever triggering a console MFA prompt. Deleting it outright is stronger than any rotation policy.

---

## 2. Set alternate contacts

**Billing console** (or **Account settings**) → **Alternate Contacts** → configure separate contacts for **Billing**, **Operations**, and **Security**.

- These contacts receive AWS communications (including security notifications) **even if the root email inbox is unreachable or the root credentials are compromised** — a real resilience gap alternate contacts specifically close.
- Especially important for accounts tied to a single individual's personal email address, where that one inbox being compromised or abandoned would otherwise be a single point of failure for account recovery communication too.

---

## 3. Monitor root activity — CloudTrail and alerting

Every root sign-in and every action root takes is logged in **AWS CloudTrail** exactly like any other identity's actions. Given how rare legitimate root usage should be (Note 13), **any** root activity is worth actively alerting on:

- Set up a **CloudWatch alarm** (or an **EventBridge rule**) that triggers on any `ConsoleLogin` or API event where the identity is `Root`, notifying security/ops immediately.
- Treat an unexpected root sign-in alert as a genuine incident to investigate, not routine noise — if root usage is truly reserved for the narrow task list from Note 13, an alert firing outside of a deliberate, planned root action is a strong compromise signal.

---

## 4. Organization-level root lockdown (multi-account setups)

For accounts managed under **AWS Organizations** (Note 18), AWS offers additional centralized controls specifically for root:

- **Centralized root access management** lets the **management account** remove or restrict root credentials in **member accounts** entirely, rather than relying on each member account's own root user being individually secured.
- **Service Control Policies (SCP, Notes 20-21)** can restrict *some* root actions in member accounts (though root in the **management account itself** is generally exempt from SCPs and remains the most sensitive credential in the entire organization).

---

## 5. The full root-hardening checklist (Notes 12-14, combined)

| # | Action | Covered in |
|---|---|---|
| 1 | Enable MFA on root (security key/passkey preferred, virtual MFA acceptable) | Note 12 |
| 2 | Create a dedicated administrative IAM identity immediately; stop signing in as root routinely | Note 13 |
| 3 | Delete any root access keys entirely | This note, Section 1 |
| 4 | Set alternate Billing/Operations/Security contacts | This note, Section 2 |
| 5 | Alert on any root CloudTrail activity | This note, Section 3 |
| 6 | For multi-account orgs, centralize root management from the management account | This note, Section 4 |

> 🎯 **Exam tip:** SAA-C03 scenario questions about "securing a newly created AWS account" or "an account was compromised via root" almost always map to one or more items on this exact checklist — MFA and eliminating root access keys are the two most frequently tested individual items.

---

## 6. Recap

- Root access keys should be **deleted outright**, not merely handled carefully — root never legitimately needs programmatic access.
- **Alternate contacts** (Billing/Operations/Security) keep AWS communications reaching someone even if root's own inbox or credentials are compromised.
- **CloudTrail + alerting on any root activity** turns "root usage should be rare" into an actively monitored, enforced fact rather than just a policy on paper.
- In **AWS Organizations**, centralized root access management extends this hardening across every member account from one place.
- This closes the three-part root-user series. Next: Note 15 — IAM Reports, Part 1: IAM Credential Reports, shifting from root-specific hardening to account-wide visibility into every identity's credential hygiene.

### Sources
- [AWS account root user — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html)
- [Security best practices in IAM — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Centralized root access management for member accounts — AWS docs](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_root-access-mgmt.html)
- [Managing alternate contacts — AWS docs](https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-update-contact-alternate.html)
