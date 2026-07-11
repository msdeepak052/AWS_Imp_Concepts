# 13 - IAM Root User Best Practices, Part 2: Never Use Root User

> Goal: know the short, specific list of tasks that genuinely still require the root user, so that literally everything else can (and should) go through a dedicated IAM identity instead — continuing directly from Note 12's MFA setup.

---

## 1. The rule: create an admin identity immediately, then stop signing in as root

The very next action after Note 12's MFA setup should be creating a **dedicated administrative IAM identity** (an IAM user with `AdministratorAccess`, or — in a real multi-account setup — an **IAM Identity Center** permission set, Notes 22-23) and using **that** for all day-to-day administrative work, no matter how tempting it is to "just stay signed in as root since it can do everything."

> 🧠 **Mental model:** root is the fire-alarm pull-station key, not the front-door key you use every morning — it exists for the rare moment nothing else works, not for routine entry.

---

## 2. The (short) list of tasks that genuinely require root

Most of these are one-time, account-level, or billing/legal actions that AWS deliberately scopes to root only, precisely because they're too consequential to delegate broadly:

| Task | Why it's root-only |
|---|---|
| Changing the **account's root email address or password** | Controls the account's fundamental recovery identity |
| **Closing the AWS account** | The single most destructive possible action |
| Changing the **AWS Support plan** | Billing/contractual-level decision |
| Restoring **IAM user permissions** if the last remaining admin locked themselves out | The one genuine "break glass" recovery scenario |
| Some **legacy actions on very old S3 buckets** created before per-bucket IAM policies fully covered them | Historical artifact, rare in practice today |
| Registering as a **seller in the AWS Marketplace**, or certain **GovCloud** account tasks | Account-type-specific administrative actions |
| Viewing certain **billing/tax/account settings** not exposed to IAM at all | Deliberately kept outside IAM's reach |

Everything **not** on a list like this — creating resources, managing services, writing policies, reading logs, essentially all of day-to-day cloud administration — should go through an IAM user, role, or federated identity instead.

> ⚠️ This list changes slowly over time as AWS moves more account-level settings into IAM-addressable territory — the durable exam-relevant takeaway isn't memorizing every entry, it's the **principle**: root is reserved for a short, specific, mostly-account-level task list, not general administration.

---

## 3. What to actually do instead, day to day

1. Sign in as root **once**, only to: enable MFA (Note 12), create the first administrative IAM identity, then sign out.
2. From then on, sign in as that **IAM user/role** (or through IAM Identity Center, Notes 22-23) for all normal work — including tasks that feel "big," like creating other users or attaching broad policies. `AdministratorAccess` attached to a **named IAM identity** already covers essentially all of this.
3. Reserve root sign-in exclusively for the specific list in Section 2, and even then, treat it as a rare, deliberate, logged event — not a routine occurrence.

> 🎯 **Exam tip:** any scenario describing routine administrative work (creating users, managing EC2, configuring services) being done "as the root user" is describing an **anti-pattern** — the correct SAA-C03 answer is always to delegate that work to an IAM user or role with appropriately scoped permissions instead, reserving root for the narrow account-level task list above.

---

## 4. Recap

- Root should be used only for a short, specific list of account-level tasks (closing the account, changing the support plan, root email/password recovery, and a handful of others) — not for any routine administrative work.
- The correct pattern: sign in as root once to enable MFA and create a dedicated administrative IAM identity, then use that identity (or IAM Identity Center) for everything else going forward.
- Next: Note 14 — Root User Best Practices, Part 3: Root User Security, covering the remaining hardening steps (access keys, contacts, monitoring) beyond MFA and avoiding routine use.

### Sources
- [AWS account root user — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html)
- [Tasks that require root user credentials — AWS docs](https://docs.aws.amazon.com/general/latest/gr/aws_tasks-that-require-root.html)
- [Security best practices in IAM — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
