# IAM Practice Hands-On — Step-by-Step Answers (AWS Console)

> Companion to `IAM_Practise_Handson.md`. Each section below is a full console walkthrough for that exercise — exact navigation, the JSON you need, and how to verify both the "it works" and "it correctly fails" side. Do the exercise yourself first; use this to unblock or to check your work.
>
> ⚠️ Use a **sandbox/personal account**, not a production account — several exercises deliberately create over-permissive or restrictive configurations to observe the effect.

---

## 1. Write a least-privilege customer-managed policy from scratch

**Goal recap:** a policy scoped to one bucket/prefix, proven to *not* reach a second bucket.

1. **S3 console** → **Create bucket** twice: `iam-practice-bucket-a-<yourname>` and `iam-practice-bucket-b-<yourname>`. Upload a small test file into each.
2. **IAM console** → **Policies** → **Create policy** → **JSON** tab → paste:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": ["s3:GetObject", "s3:PutObject"],
         "Resource": "arn:aws:s3:::iam-practice-bucket-a-<yourname>/*"
       },
       {
         "Effect": "Allow",
         "Action": "s3:ListBucket",
         "Resource": "arn:aws:s3:::iam-practice-bucket-a-<yourname>"
       }
     ]
   }
   ```
3. **Next** → name it `PracticeLeastPrivilege-BucketA` → **Create policy**.
4. **IAM** → **Users** → **Create user** → name `practice-user-1` → **Attach policies directly** → search for and select `PracticeLeastPrivilege-BucketA` → **Create user**.
5. Give the user **console access** (check "Provide user access to the AWS Management Console" during creation, set an auto-generated or custom password) — or create an **access key** (Security credentials tab → Create access key → CLI use case) if you'd rather test via CLI.
6. **Verify success**: sign in as `practice-user-1` (or `aws s3 cp test.txt s3://iam-practice-bucket-a-<yourname>/`) → upload/download works on bucket A.
7. **Verify the boundary**: try `aws s3 ls s3://iam-practice-bucket-b-<yourname>` or the console equivalent → expect `AccessDenied`.

---

## 2. Prove explicit deny beats allow

**Goal recap:** group-level `AmazonS3FullAccess` + a user-level inline deny on `DeleteObject` → delete still fails.

1. **IAM** → **User groups** → **Create group** → name `practice-s3-full` → attach AWS managed policy **AmazonS3FullAccess** → **Create group**.
2. **IAM** → **Users** → **Create user** → `practice-user-2` → **Add user to group** → select `practice-s3-full` → create.
3. Open `practice-user-2` → **Permissions** tab → **Add inline policy** → **JSON**:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Deny",
         "Action": "s3:DeleteObject",
         "Resource": "*"
       }
     ]
   }
   ```
4. **Next** → name `DenyDeleteObject` → **Create policy** (this attaches directly to the user as an inline policy).
5. **Verify**: as `practice-user-2`, confirm you **can** upload/list objects (inherited from the group's full access), but `aws s3 rm s3://iam-practice-bucket-a-<yourname>/test.txt` (or the console delete button) returns `AccessDenied` — the explicit deny wins regardless of the group's allow.

---

## 3. Inline vs. managed, side by side

**Goal recap:** feel the maintenance difference between one managed policy shared by two users vs. the same permission duplicated as inline policies.

1. **IAM** → **Policies** → **Create policy** → JSON: allow `s3:GetObject` on `iam-practice-bucket-a-<yourname>/*` only → name `PracticeSharedRead`.
2. Create two users `practice-user-3a` and `practice-user-3b`. On **both**, attach `PracticeSharedRead` directly (Permissions tab → Add permissions → Attach policies directly).
3. On a **third** user `practice-user-3c` and a **fourth** `practice-user-3d`, instead add an **inline policy** with the identical JSON to each (Permissions tab → Add inline policy), naming it `SharedReadInline` on both.
4. Now change the requirement: you also want `s3:ListBucket`.
   - For the managed-policy pair: edit `PracticeSharedRead` **once** (IAM → Policies → select it → Edit policy → add the `ListBucket` statement) → both `practice-user-3a` and `practice-user-3b` get the new permission immediately.
   - For the inline pair: you must open **each user individually** (`practice-user-3c`, then `practice-user-3d`) and edit their inline policy separately — two edits for the same logical change.
5. **Takeaway to be able to say out loud**: managed policies are attach-once-edit-once; inline policies are a strict 1:1 binding to one identity, so N identities needing the same custom permission means N edits every time that permission changes.

---

## 4. EC2 instance role — no access keys, ever

1. **S3**: reuse `iam-practice-bucket-a-<yourname>` from Exercise 1; also note `iam-practice-bucket-b-<yourname>` exists but should stay unreachable.
2. **IAM** → **Roles** → **Create role** → Trusted entity type: **AWS service** → Use case: **EC2** → **Next**.
3. **Permissions**: attach **AmazonS3ReadOnlyAccess** (broad on purpose, so you can see it grant bucket A **and** bucket B — this exercise is about the metadata mechanism, not scoping; combine with Exercise 1's scoped policy afterward if you want the stricter version).
4. Name the role `PracticeEC2S3ReadOnly` → **Create role**.
5. **EC2 console** → **Launch instance** → any small Amazon Linux instance → under **Advanced details** → **IAM instance profile** → select `PracticeEC2S3ReadOnly` → launch (use an existing key pair or EC2 Instance Connect).
6. Connect to the instance (**EC2 Instance Connect** is easiest — no key pair to manage).
7. Confirm **no credentials are configured**:
   ```bash
   cat ~/.aws/credentials 2>/dev/null   # should not exist
   echo $AWS_ACCESS_KEY_ID              # should be empty
   ```
8. Run:
   ```bash
   aws s3 ls s3://iam-practice-bucket-a-<yourname>
   ```
   → succeeds, with **zero** credential configuration — the CLI is silently pulling temporary credentials from the instance metadata service (`http://169.254.169.254/latest/meta-data/iam/security-credentials/`).
9. Now try to **write**:
   ```bash
   aws s3 cp somefile.txt s3://iam-practice-bucket-a-<yourname>/
   ```
   → fails with `AccessDenied`, since `AmazonS3ReadOnlyAccess` grants read-only.
10. **Cleanup**: terminate the instance when done to avoid ongoing charges.

---

## 5. Same-account AssumeRole from the CLI

1. **IAM** → **Roles** → **Create role** → Trusted entity type: **AWS account** → **This account** → **Next**.
2. Attach **AmazonS3ReadOnlyAccess** → name it `PracticeAssumableRole` → **Create role**. Note its **ARN** (Role details page).
3. **IAM** → **Users** → **Create user** → `practice-user-5` → **no S3 permissions at all** — instead, attach an inline policy granting only:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": "sts:AssumeRole",
         "Resource": "arn:aws:iam::<YOUR_ACCOUNT_ID>:role/PracticeAssumableRole"
       }
     ]
   }
   ```
4. Also edit `PracticeAssumableRole`'s **Trust relationships** tab to confirm/set:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": { "AWS": "arn:aws:iam::<YOUR_ACCOUNT_ID>:user/practice-user-5" },
         "Action": "sts:AssumeRole"
       }
     ]
   }
   ```
5. Create an **access key** for `practice-user-5` (Security credentials tab → Create access key → Command Line Interface use case). Configure a named CLI profile:
   ```bash
   aws configure --profile practice-user-5
   ```
6. **Confirm the boundary first**:
   ```bash
   aws s3 ls s3://iam-practice-bucket-a-<yourname> --profile practice-user-5
   ```
   → `AccessDenied` — the user itself has no S3 permission, only `sts:AssumeRole`.
7. **Assume the role**:
   ```bash
   aws sts assume-role \
     --role-arn arn:aws:iam::<YOUR_ACCOUNT_ID>:role/PracticeAssumableRole \
     --role-session-name practice-session \
     --profile practice-user-5
   ```
8. Export the three returned values (`AccessKeyId`, `SecretAccessKey`, `SessionToken`) as environment variables:
   ```bash
   export AWS_ACCESS_KEY_ID=...
   export AWS_SECRET_ACCESS_KEY=...
   export AWS_SESSION_TOKEN=...
   ```
9. Now:
   ```bash
   aws s3 ls s3://iam-practice-bucket-a-<yourname>
   ```
   → succeeds, using the **temporary** role credentials, proving the user's own permissions and the role's permissions are entirely separate things.
10. `unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN` when done to stop using the temporary session.

---

## 6. Cross-account AssumeRole with External ID (confused deputy)

You need two AWS accounts for this — use a second free-tier/sandbox account if you have one, or an AWS Organizations member account (Exercise 11 sets one up, if you want to do that first).

1. **In Account A** (the account owning the resource, e.g. `111111111111`): **IAM** → **Roles** → **Create role** → **AWS account** → **Another AWS account** → enter Account B's ID (e.g. `222222222222`) → check **Require external ID** → enter a shared secret string, e.g. `practice-ext-id-2026` → **Next** → attach `AmazonS3ReadOnlyAccess` → name `PracticeCrossAccountRole` → **Create role**.
2. **In Account B**: create (or reuse) a user `practice-user-6` with an inline policy allowing `sts:AssumeRole` on Account A's role ARN.
3. Configure a CLI profile for `practice-user-6` in Account B (`aws configure --profile practice-user-6-b`).
4. **Try assuming without the External ID**:
   ```bash
   aws sts assume-role \
     --role-arn arn:aws:iam::111111111111:role/PracticeCrossAccountRole \
     --role-session-name test \
     --profile practice-user-6-b
   ```
   → fails with `AccessDenied` (the trust policy requires the External ID condition, which wasn't supplied).
5. **Try again with the External ID**:
   ```bash
   aws sts assume-role \
     --role-arn arn:aws:iam::111111111111:role/PracticeCrossAccountRole \
     --role-session-name test \
     --external-id practice-ext-id-2026 \
     --profile practice-user-6-b
   ```
   → succeeds, returning temporary Account-A-scoped credentials.
6. **Why this matters (say this out loud in an interview)**: without the External ID requirement, if Account A's role trusts a third-party SaaS vendor's account broadly, that vendor could be tricked by *another* one of its customers into assuming a role scoped to *your* resources — the External ID is a shared secret that proves the assumption request is genuinely on your behalf, not someone else's.

---

## 7. Custom trust policy with conditions

1. Reuse `PracticeAssumableRole` from Exercise 5 (or create a new role the same way).
2. Edit its **Trust relationships** tab to add an MFA condition:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": { "AWS": "arn:aws:iam::<YOUR_ACCOUNT_ID>:user/practice-user-5" },
         "Action": "sts:AssumeRole",
         "Condition": {
           "Bool": { "aws:MultiFactorAuthPresent": "true" }
         }
       }
     ]
   }
   ```
3. **Test the failing case**: without an MFA-verified session, repeat Exercise 5 Step 7's `aws sts assume-role` call → now fails, since the calling identity's session has no MFA claim.
4. **Test the passing case**: set up a **virtual MFA device** for `practice-user-5` (IAM → Users → `practice-user-5` → Security credentials → Assign MFA device — use an authenticator app). Then call `sts get-session-token` **with** the MFA code first:
   ```bash
   aws sts get-session-token \
     --serial-number arn:aws:iam::<YOUR_ACCOUNT_ID>:mfa/practice-user-5 \
     --token-code <6-DIGIT-CODE> \
     --profile practice-user-5
   ```
   Export those temporary (now MFA-tagged) credentials as environment variables, then re-run the `assume-role` call from Exercise 5 using them → succeeds this time.
5. **Alternative condition to try**: swap the `Bool` condition for `IpAddress` / `aws:SourceIp` restricted to your current public IP, and confirm assuming from that IP works while (if you can test from another network, e.g. mobile hotspot) a different IP fails.

---

## 8. Web Identity Federation, hands-on

1. **Amazon Cognito console** → **Identity pools** → **Create identity pool**.
2. Name it `PracticeIdentityPool`. Under **Guest access**, enable **Enable access to unauthenticated identities** (simplest path for this exercise — no real login provider needed).
3. On the permissions step, Cognito auto-creates an **unauthenticated role** (e.g. `Cognito_PracticeIdentityPoolUnauth_Role`) — edit its permissions to attach a scoped policy, e.g. read-only on `iam-practice-bucket-a-<yourname>`.
4. **Create the pool**.
5. From a local machine with the AWS CLI/SDK (or a small script), call:
   ```bash
   aws cognito-identity get-id --identity-pool-id <REGION>:<POOL_ID>
   aws cognito-identity get-credentials-for-identity --identity-id <IDENTITY_ID_FROM_ABOVE>
   ```
6. Use the returned temporary `AccessKeyId`/`SecretKey`/`SessionToken` to run `aws s3 ls s3://iam-practice-bucket-a-<yourname>` → succeeds, **without any IAM user ever being created** for this caller.
7. **Say out loud**: this is exactly how a mobile app gives each installed-app user their own scoped, temporary AWS credentials — the app never embeds a long-lived access key, and no IAM user is created per end-user (which wouldn't scale to millions of app users anyway).

---

## 9. Lock down root properly

1. **Enable MFA on root**: sign in as the **root user** (email + password, not an IAM user) → top-right account menu → **Security credentials** → **Multi-factor authentication (MFA)** → **Assign MFA device** → set up a virtual MFA app or a hardware key.
2. **Check for and delete root access keys**: still under root's **Security credentials** page → **Access keys** section → if any exist, **delete** them (root should never have long-term access keys at all).
3. **Confirm CloudTrail is on**: **CloudTrail console** → **Trails** → confirm a trail exists (or create one) delivering to an S3 bucket, capturing management events.
4. **Set up the alert**: **EventBridge console** → **Rules** → **Create rule** → **Event pattern**:
   ```json
   {
     "detail-type": ["AWS Console Sign In via CloudTrail"],
     "detail": {
       "userIdentity": { "type": ["Root"] },
       "eventName": ["ConsoleLogin"]
     }
   }
   ```
5. **Target**: an **SNS topic** you've created and subscribed your own email to (SNS console → Create topic → Create subscription → protocol Email → confirm the subscription email).
6. **Trigger it**: sign out, sign back in as root (using the MFA device from Step 1) → within a couple of minutes, confirm you receive the SNS email alert.
7. **Say out loud**: root should have MFA, no access keys, and any use of it should be rare enough that an alert firing is itself a notable event worth investigating — not routine noise.

---

## 10. Enforce MFA via policy condition

1. **IAM** → **User groups** → **Create group** → `practice-mfa-enforced`.
2. Attach a policy allowing users to **manage their own MFA/credentials** even before MFA is set up (otherwise a fully-locked-out user could never self-enroll):
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "AllowViewAccountInfo",
         "Effect": "Allow",
         "Action": ["iam:GetAccountPasswordPolicy", "iam:ListVirtualMFADevices"],
         "Resource": "*"
       },
       {
         "Sid": "AllowManageOwnMFA",
         "Effect": "Allow",
         "Action": [
           "iam:CreateVirtualMFADevice", "iam:DeleteVirtualMFADevice",
           "iam:EnableMFADevice", "iam:ResyncMFADevice",
           "iam:ListMFADevices", "iam:GetUser"
         ],
         "Resource": [
           "arn:aws:iam::*:mfa/${aws:username}",
           "arn:aws:iam::*:user/${aws:username}"
         ]
       }
     ]
   }
   ```
3. Attach a **second** policy to the same group denying everything else without MFA:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "DenyAllExceptMFASetupUnlessMFAd",
         "Effect": "Deny",
         "NotAction": [
           "iam:CreateVirtualMFADevice", "iam:EnableMFADevice",
           "iam:GetUser", "iam:ListMFADevices", "iam:ListVirtualMFADevices",
           "iam:ResyncMFADevice", "sts:GetSessionToken"
         ],
         "Resource": "*",
         "Condition": {
           "BoolIfExists": { "aws:MultiFactorAuthPresent": "false" }
         }
       }
     ]
   }
   ```
4. Also attach `AmazonS3ReadOnlyAccess` to the group, to have something to test with.
5. Put `practice-user-5` (or a fresh user) into `practice-mfa-enforced`.
6. **Verify the failing case**: sign in as this user **without** completing MFA setup/verification for the session → attempt `aws s3 ls` (or the console equivalent) → `AccessDenied`, because the deny statement fires whenever MFA isn't present on the session.
7. **Verify the passing case**: have the user set up their virtual MFA device (allowed by the first policy even pre-MFA) → sign out, sign back in **entering the MFA code** → now S3 access works, since `aws:MultiFactorAuthPresent` is `true` for that session.

---

## 11. Build a real OU + SCP deny-list

1. **AWS Organizations console** (from the management account) → if not already set up, **Create an organization**.
2. **Add an account**: **Invite account** (an existing sandbox account) or **Create account** to get a fresh member account into the org.
3. **Organize resources** tab → **Create organizational unit** → name it `PracticeOU` → move the member account into it.
4. **Policies** tab → **Service control policies** → confirm SCPs are **enabled** for the org (Organizations → Settings → enable the SCP policy type, if not already).
5. **Create policy** → JSON:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "DenyEC2OutsideApSouth1",
         "Effect": "Deny",
         "Action": "ec2:*",
         "Resource": "*",
         "Condition": {
           "StringNotEquals": { "aws:RequestedRegion": "ap-south-1" }
         }
       }
     ]
   }
   ```
6. Name it `PracticeDenyEC2OutsideRegion` → **Create policy**, then **Attach** it to `PracticeOU`.
7. **Verify in the member account**: sign in to the member account (even as a user/role with `AdministratorAccess` there) → try to launch an EC2 instance in a **different** Region (e.g. `us-east-1`) → fails with an `UnauthorizedOperation`/explicit deny from the organizational policy, **despite** having full admin rights inside that account.
8. Confirm the **same admin identity can still launch EC2 in `ap-south-1`** — the SCP only narrows what the account's *maximum possible* permissions are; it doesn't grant anything by itself.
9. **Verify the management account is unaffected**: from the management account itself, confirm you can still launch EC2 anywhere — SCPs **never apply to the management/root account** of the organization.

---

## 12. SCP allow-list strategy

1. In the same `PracticeOU`, **detach** the deny-list SCP from Exercise 11 (or leave it and add this as a second policy to compare both active at once, if you want to see them combine).
2. **Create policy** → JSON, an allow-list denying everything except a short list of services:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "DenyAllExceptAllowedServices",
         "Effect": "Deny",
         "NotAction": [
           "s3:*",
           "ec2:Describe*",
           "iam:Get*",
           "iam:List*"
         ],
         "Resource": "*"
       }
     ]
   }
   ```
3. Attach it to `PracticeOU` → in the member account, try an action **not** on the allow-list (e.g. `dynamodb:CreateTable`) → fails.
4. Try `s3:CreateBucket` → succeeds (still subject to whatever IAM permissions the calling identity actually has inside the account — the SCP only sets the ceiling).
5. **Articulate the risk out loud**: every new AWS service or action your teams legitimately need requires you to remember to add it to this list — an allow-list is much easier to accidentally under-scope and break someone's legitimate work than a deny-list, which only needs updating when you discover a *new specific thing to block*.
6. **Cleanup**: detach/delete the practice SCPs from `PracticeOU` when done, so the member account isn't left restricted.

---

## 13. Permission sets across multiple accounts

1. **IAM Identity Center console** → if not enabled yet, **Enable** it (choose the management account or a delegated administrator account as the Identity Center instance's home).
2. **Permission sets** → **Create permission set** → **Predefined permission set** → choose **ReadOnlyAccess** → set a session duration (e.g. 1 hour) → name it, e.g. `PracticeReadOnly` → **Create**.
3. **AWS accounts** tab → select **two** member accounts in your org (checkboxes) → **Assign users or groups** → create/select a user in Identity Center's own directory (**Users** tab → **Add user** first, if none exist) → assign that user to both accounts with the `PracticeReadOnly` permission set.
4. Identity Center provisions the permission set into both accounts as an IAM role behind the scenes (visible in each account's IAM → Roles, named something like `AWSReservedSSO_PracticeReadOnly_...`).
5. **Verify**: sign in to the **AWS access portal** URL (found on the Identity Center dashboard) as that user → you should see **both** accounts listed as tiles → click into each, confirm read-only access works in both, and confirm you never created a separate IAM user in either account.
6. **Say out loud**: this is the standard pattern for human access across many accounts — one identity, one login, permission sets assigned per account, no IAM users scattered across the organization.

---

## 14. Generate a real external-access finding

1. **IAM** → **Access Analyzer** → **Create analyzer** → **Zone of trust**: your account (or the whole organization, if you have Organizations set up) → name it `PracticeAnalyzer` → **Create analyzer**.
2. **Create the problem on purpose**: go to `iam-practice-bucket-a-<yourname>` in S3 → **Permissions** tab → **Bucket policy** → **Edit** → paste an over-permissive policy:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": "*",
         "Action": "s3:GetObject",
         "Resource": "arn:aws:s3:::iam-practice-bucket-a-<yourname>/*"
       }
     ]
   }
   ```
3. **Save changes** (you may need to also confirm **Block Public Access** settings on the bucket allow this, or Access Analyzer will still flag the *policy* as granting public access even if BPA is currently blocking it in practice).
4. Back in **IAM Access Analyzer** → **Findings** → wait a few minutes, then refresh — a finding should appear flagging `iam-practice-bucket-a-<yourname>` as granting **public/external access**.
5. Open the finding → review what it identifies (the specific principal, `*`, and the specific actions granted).
6. **Fix it**: edit the bucket policy back to something scoped (e.g. remove the public statement, or restrict `Principal` to a specific account ARN) → **Save**.
7. Back in Access Analyzer → the finding should transition to **Resolved** after its next evaluation cycle.
8. **Say out loud**: Access Analyzer's value is continuous, automatic detection of exactly this kind of drift — someone editing a bucket policy (or a role trust policy) to be broader than intended, which is one of the most common real-world cloud security incidents.

---

## 15. Capstone — tie it together

This is intentionally not a fresh build — it's an integration exercise assembling pieces from Exercises 4, 6, 11, and 13 into one coherent picture you can narrate end-to-end.

1. **Organization**: reuse the org from Exercise 11 — a management account and at least one member account (`PracticeOU`).
2. **SCP**: keep (or recreate) a deny-list SCP on `PracticeOU` restricting some clearly-scoped thing (e.g. Region restriction from Exercise 11).
3. **App role in the member account**: in the member account, create an EC2 instance role (same pattern as Exercise 4) scoped to only the S3 bucket that app needs.
4. **Cross-account logging/security role**: in the member account, create a role trusting a separate "security" or "logging" account (same pattern as Exercise 6, with an External ID), granting only `cloudtrail:LookupEvents` / read access to the CloudTrail S3 bucket — nothing else.
5. **Human access**: confirm IAM Identity Center (Exercise 13) is how *you* — a human — log into the member account for day-to-day work, rather than an IAM user.
6. **Now narrate it out loud, in one breath, as if answering a system-design interview question**: "The organization's SCP sets an outer ceiling on what any identity in this account can ever do, regardless of their IAM permissions. Inside that ceiling, the application itself runs under an EC2 instance role scoped to just its own bucket — no long-lived credentials anywhere. A separate security account can read this account's CloudTrail logs via a cross-account role locked down with an External ID, without ever holding a static credential in either account. And I, as a human operator, access this account through IAM Identity Center's permission sets — one login, temporary credentials, no IAM user created here at all."
7. If you can say that paragraph fluently while pointing at the actual consoles where each piece lives, you've internalized the material — which was the entire point of this checklist.

---

## Cleanup checklist (do this after finishing, to avoid stray cost/risk)

- Terminate any EC2 instances launched (Exercises 4, 11, 15).
- Delete the S3 test buckets and their contents (Exercises 1-3, 14).
- Detach and delete practice SCPs from `PracticeOU` (Exercises 11-12, 15) so the member account isn't left restricted.
- Remove the member account from the OU / leave the Organization if it was a sandbox account created solely for this practice (Exercises 6, 11-13, 15).
- Delete practice IAM users, groups, roles, and policies (`practice-user-*`, `practice-s3-full`, `Practice*` roles/policies).
- Delete the Cognito identity pool (Exercise 8) and its auto-created IAM roles.
- Delete the EventBridge rule and SNS topic/subscription from Exercise 9 if no longer wanted.
- Deregister IAM Identity Center permission-set assignments (Exercise 13) if you don't plan to keep using Identity Center.
