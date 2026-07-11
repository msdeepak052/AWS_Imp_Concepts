# 21 - AWS Organization, Part 4: Service Control Policies (SCPs) Practical

> Goal: enable SCPs, author a real deny-list SCP, attach it to an OU, and prove it actually blocks an action even for a user holding `AdministratorAccess` — the concrete demonstration of Note 20's "SCPs are a ceiling, not a grant" rule.

---

## 1. Prerequisites

- An Organization in **all features** mode (Note 18) — SCPs are unavailable under consolidated-billing-only mode.
- At least one OU with a member account inside it (Note 18, Section 2).

---

## 2. Enable the SCP policy type

1. **AWS Organizations console** (management account) → **Policies** → **Service control policies** → **Enable**.
2. Once enabled, every existing OU and account already has AWS's default `FullAWSAccess` SCP attached automatically — the deny-list starting baseline described in Note 20, Section 3.

---

## 3. Author a deny-list SCP — block a Region outside your approved list

1. **Policies** → **Service control policies** → **Create policy**.
2. **Name**: `DenyOutsideApSouth1`.
3. **JSON**:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "DenyAllOutsideApprovedRegion",
         "Effect": "Deny",
         "NotAction": [
           "iam:*",
           "organizations:*",
           "route53:*",
           "support:*",
           "sts:*"
         ],
         "Resource": "*",
         "Condition": {
           "StringNotEquals": { "aws:RequestedRegion": "ap-south-1" }
         }
       }
     ]
   }
   ```
4. **Create policy**.

> 🧠 The `NotAction` list carves out AWS's **global services** (IAM, Organizations, Route 53, Support, STS) so the SCP doesn't accidentally break account-wide functionality that isn't Region-scoped in the first place — a real production Region-restriction SCP always needs this kind of exclusion list, not just a blanket deny.

---

## 4. Attach the SCP to an OU

1. **AWS Organizations console** → **Organize accounts** → select the target OU (e.g. `Development`, from Note 18's diagram).
2. **Policies** tab → **Service control policies** → **Attach** → select `DenyOutsideApSouth1` → **Attach policy**.
3. Every account inside this OU (and any nested OUs beneath it) now inherits this Region restriction.

---

## 5. Prove the ceiling — even an admin can't bypass it

1. Inside a member account under this OU, sign in as (or assume a role with) **`AdministratorAccess`** — the broadest possible IAM identity-based grant.
2. Attempt to launch an EC2 instance in, say, `us-east-1` (outside the approved `ap-south-1`):
   ```bash
   aws ec2 run-instances --region us-east-1 --image-id ami-xxxxxxxx --instance-type t3.micro
   ```
3. The call fails with an **access denied** error citing the SCP — even though `AdministratorAccess` alone would normally allow this action anywhere. This is Note 20's core rule made concrete: the SCP's `Deny` sits **above** the account's own IAM grant, and no identity-based policy inside the account, no matter how broad, can override it.

---

## 6. Testing an SCP safely, without locking anyone out

Before attaching a new SCP broadly, test it narrowly first:

1. Attach the candidate SCP to a **single, low-risk test account** or a dedicated **sandbox OU** first, not directly to the Organization root.
2. Verify expected actions are still allowed, and only the intended actions are blocked.
3. Only then propagate it up to broader OUs / the Organization root.

> ⚠️ A too-broad SCP (e.g. denying `iam:*` without exceptions) can lock every user in an affected account out of managing their own permissions at all, with no in-account workaround — since the whole point of an SCP is that nothing inside the account can override it. Always test narrow before scaling wide.

---

## 7. Recap

- Enabling SCPs requires **all features** mode; every OU/account starts with the default `FullAWSAccess` allow-everything SCP already attached.
- A real deny-list SCP (like the Region-restriction example here) needs a `NotAction` exclusion list for AWS's global services, or it breaks account-wide functionality unintentionally.
- SCPs are attached to OUs (inherited downward) or individual accounts, and — proven directly in Section 5 — **override even `AdministratorAccess`**, since SCPs are a ceiling no identity-based policy inside the account can raise.
- Always test a new SCP on a narrow, low-risk scope before attaching it broadly.
- This closes the SCP/Organizations series (Notes 18-21). Next: Note 22 — AWS IAM Identity Center, centralizing **workforce sign-in** across every account in the Organization (rather than each account managing its own separate IAM users).

### Sources
- [Service control policies (SCPs) — AWS docs](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html)
- [Enabling and disabling a policy type — AWS docs](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_enable-disable.html)
- [SCP examples — AWS docs](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_examples.html)
