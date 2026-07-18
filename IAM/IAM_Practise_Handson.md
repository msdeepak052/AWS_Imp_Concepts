# IAM Practice Hands-On Checklist

> Goal: 15 self-driven hands-on exercises to actually build IAM concepts from Notes 01-23, rather than just reading about them — geared toward being able to explain and defend these setups in an interview, not just complete a lab. Report-only topics (Credential Reports, Access Advisor) are deliberately excluded, per the practice's own framing — the value here is in building and breaking things, not reading a static report.

Check items off as you complete them. Each one names the interview question it's meant to prepare you for.

---

## Policies & Permissions

- [ ] **1. Write a least-privilege customer-managed policy from scratch**
  Create a policy granting `s3:GetObject`/`s3:PutObject` on exactly one bucket/prefix — no wildcards on `Resource`. Attach it to a test user and confirm they *can't* touch a second bucket.
  > Interview question: "How do you enforce least privilege in IAM?"

- [ ] **2. Prove explicit deny beats allow**
  Put a user in a group with `AmazonS3FullAccess`, then attach an inline policy directly to the user that explicitly denies `s3:DeleteObject`. Try to delete an object — confirm it fails despite the group's full access.
  > Interview question: "Walk me through IAM policy evaluation logic."

- [ ] **3. Inline vs. managed, side by side**
  Create the same permission twice — once as a customer-managed policy attached to two users, once as an inline policy duplicated on each user. Then change the permission and observe: one edit updates both users; the other requires editing twice.
  > Interview question: "When would you use an inline policy over a managed one?"

---

## Roles & Federation

- [ ] **4. EC2 instance role — no access keys, ever**
  Launch an EC2 instance with an instance profile role granting S3 read-only. SSH in, run the AWS CLI with **no credentials configured**, and confirm it works via the instance metadata service. Then try `aws s3 ls` for a bucket the role doesn't have access to and watch it fail.
  > Interview question: "Why shouldn't you hardcode access keys on an EC2 instance?"

- [ ] **5. Same-account AssumeRole from the CLI**
  Create Role A with S3 access. Create User B with only `sts:AssumeRole` on Role A and nothing else. From User B's credentials, run `aws sts assume-role`, export the temporary creds, and use them to touch S3 — then confirm User B's own long-term credentials can't touch S3 directly.
  > Interview question: "What's the difference between a user's permissions and a role's permissions?"

- [ ] **6. Cross-account AssumeRole with External ID (confused deputy)**
  Using two AWS accounts (or two sandbox accounts if you have them), set up Account A's role to trust Account B, requiring an External ID condition. Try assuming without the External ID (fails), then with it (succeeds).
  > Interview question: "What's the confused deputy problem, and how does External ID solve it?"

- [ ] **7. Custom trust policy with conditions**
  Modify a role's trust policy to only allow AssumeRole if the request has MFA present (`aws:MultiFactorAuthPresent`) or comes from a specific source IP. Test both the passing and failing case.
  > Interview question: "Can you restrict *when* or *how* a role can be assumed, not just *who* can assume it?"

- [ ] **8. Web Identity Federation, hands-on**
  Set up Cognito Identity Pool (or a basic `AssumeRoleWithWebIdentity` call using a test OIDC token) so an unauthenticated app user gets temporary AWS credentials scoped to a role — no IAM user involved at all.
  > Interview question: "How would a mobile app give end-users temporary AWS access without creating an IAM user per user?"

---

## Root User & MFA

- [ ] **9. Lock down root properly**
  On a sandbox account: enable MFA on root, delete any root access keys if present, set up a CloudTrail-based CloudWatch alarm (or EventBridge rule) that fires on any root login. Trigger a root login and confirm the alert fires.
  > Interview question: "What's your root account security checklist?"

- [ ] **10. Enforce MFA via policy condition**
  Write a policy that denies all actions unless `aws:MultiFactorAuthPresent` is true, attach it to a user, and confirm the user is blocked until they authenticate with a virtual MFA device.
  > Interview question: "How do you *force* MFA usage, not just enable it as an option?"

---

## Organizations & SCPs

- [ ] **11. Build a real OU + SCP deny-list**
  Create an Organization, add a member account into an OU, and attach an SCP that denies a specific service (e.g., deny all EC2 actions region-wide except one region). Confirm the member account is blocked even with `AdministratorAccess`, and confirm the **management account is unaffected**.
  > Interview question: "What's the difference between an SCP and an IAM policy? Why doesn't SCP apply to the management account?"

- [ ] **12. SCP allow-list strategy**
  Rebuild Exercise 11 as an allow-list instead (deny everything except an explicit list of allowed services), and articulate why this is riskier to maintain than a deny-list.
  > Interview question: "When would you use an SCP allow-list vs deny-list strategy?"

---

## IAM Identity Center

- [ ] **13. Permission sets across multiple accounts**
  Set up IAM Identity Center, create a permission set (e.g., read-only), assign it to two different member accounts, and log in via the access portal — confirm you can switch between accounts without separate IAM users in each.
  > Interview question: "How do you manage human access across 20+ AWS accounts without creating IAM users in each one?"

---

## Access Analyzer (the one hands-on exception)

- [ ] **14. Generate a real external-access finding**
  Deliberately create an over-permissive S3 bucket policy (grants access to another account or `*`), then run IAM Access Analyzer and watch it surface the finding. Fix the policy and confirm the finding resolves.
  > Interview question: "How would you detect unintended external access before it becomes an incident?"
  >
  > This is the one "report" tool worth doing hands-on — the value is in causing and then fixing a real finding, not reading a static report.

---

## Capstone

- [ ] **15. Tie it together: a realistic access model**
  Build one small scenario end-to-end: an Organization with 2 accounts, an SCP restricting the member account, an EC2 role in the member account for an app, a cross-account role for a central logging/security account to read CloudTrail logs, and IAM Identity Center for your own human login. This forces you to explain the *whole* access model in one breath — which is exactly what a system-design interview question tends to ask.

---

## Note

A pattern worth noticing across all 15: nearly every one ends in "confirm it fails" as much as "confirm it works" — that's deliberate. Interviewers care more about whether you tested the boundary than whether you can describe the happy path.
