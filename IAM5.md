# **AWS Organizations** 

---

## 🏢 What is **AWS Organizations**?

**AWS Organizations** is a **centralized account management service** that enables you to:

* **Centrally manage** billing, policies, and access
* **Group accounts** into organizational units (OUs)
* Apply **Service Control Policies (SCPs)** across multiple AWS accounts
* Set up a **multi-account strategy** with centralized governance

---

## 🧠 Why Use AWS Organizations?

| 🔍 Use Case                           | ✅ Benefit                                     |
| ------------------------------------- | --------------------------------------------- |
| Multi-team or multi-project isolation | Separate workloads/account-level blast radius |
| Centralized billing                   | Aggregate usage and use consolidated billing  |
| Policy control                        | Set guardrails using SCPs                     |
| Automate account creation             | With Account Factory or APIs                  |
| Enable governance and compliance      | Enforce security controls across all accounts |

---

## 🛠️ AWS Organizations Architecture

```
AWS Organization (Root)
│
├── Organizational Unit: Security
│   ├── Account: Audit
│   └── Account: SecurityTools
│
├── Organizational Unit: Development
│   ├── Account: Dev1
│   └── Account: Dev2
│
└── Organizational Unit: Production
    ├── Account: Prod1
    └── Account: Prod2
```

---

## 🧱 Core Concepts

| Concept                          | Description                                                         |
| -------------------------------- | ------------------------------------------------------------------- |
| **Root**                         | The top node of your Org; created when you enable AWS Organizations |
| **Account**                      | A standard AWS account (child or management)                        |
| **OU (Organizational Unit)**     | Logical grouping of accounts                                        |
| **SCP (Service Control Policy)** | Guardrails that define maximum permissions an account/OUs can have  |
| **Management Account**           | Formerly "Master"; central account to create/manage others          |
| **Member Account**               | An account under the Org hierarchy managed via Organizations        |

---

## ✅ Options and Features Available in AWS Organizations

| Feature                               | Description                                                            |
| ------------------------------------- | ---------------------------------------------------------------------- |
| ✔️ Consolidated Billing               | View & manage all linked accounts' bills from management account       |
| ✔️ OU Hierarchies                     | Organize accounts logically (Dev, Test, Prod)                          |
| ✔️ SCPs                               | Restrict services/regions/actions at org, OU, or account level         |
| ✔️ Account Invitation                 | Add existing accounts                                                  |
| ✔️ Account Creation                   | Create accounts programmatically or manually                           |
| ✔️ Trusted Access                     | Enable integration with AWS services like AWS Config, CloudTrail, etc. |
| ✔️ Integration with AWS Control Tower | For automated landing zone setup                                       |
| ✔️ Tagging                            | Assign tags for cost tracking & management                             |

---

## 🎯 Step-by-Step: Set Up AWS Organizations from Console

### 🔹 Step 1: Enable AWS Organizations

1. Sign in to your **primary account**
2. Go to **AWS Organizations** service
3. Click **“Create organization”**
4. Choose:

   * **Consolidated billing only** ✅
   * OR **All features** (to use OUs and SCPs — recommended)

---

### 🔹 Step 2: Create Organizational Units (OUs)

1. Click **Organize accounts**
2. Choose **“Create organizational unit”**
3. Name it (e.g., `Development`, `Security`, `Production`)
4. Drag/drop existing accounts or create new ones into the OU

---

### 🔹 Step 3: Invite Existing Accounts (optional)

1. Go to **Accounts**
2. Click **“Add account” → Invite account**
3. Enter the email or account ID of the AWS account
4. The other account owner will receive an invite email

---

### 🔹 Step 4: Create a New AWS Account

1. Click **“Add account” → Create account**
2. Fill:

   * Email ID
   * Account name
   * IAM role name (for management access)
3. Account gets created and added under the Org

---

### 🔹 Step 5: Apply SCPs (Service Control Policies)

1. Go to **Policies → Service control policies**
2. Click **“Create policy”**
3. Example SCP: Deny access to `us-west-1`

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Action": "*",
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:RequestedRegion": "us-west-1"
        }
      }
    }
  ]
}
```

4. Attach this policy to an **OU or account**

---

## 💡 Example: Real-World OU Structure

```
Root
├── OU: Security
│   └── Account: audit@example.com
├── OU: Sandbox
│   ├── Account: dev1@example.com
│   └── Account: dev2@example.com
├── OU: Prod
│   ├── Account: app1@example.com
│   └── Account: database@example.com
```

* Sandbox OU: SCP to **deny access to production services**
* Security OU: SCP to **enforce CloudTrail, GuardDuty**
* Prod OU: SCP to **deny use of non-approved regions**

---

## 🔐 SCP Enforcement Model

> 🧠 **IAM + SCP = Effective Permissions**

If:

* IAM allows something ✅
* SCP denies it ❌

➡️ The action is **DENIED**

> SCPs are always **deny-first** unless explicitly allowed and not denied.

---

## 📈 Monitoring & Auditing

| Tool                           | Use                                |
| ------------------------------ | ---------------------------------- |
| **CloudTrail**                 | Logs Org changes                   |
| **AWS Config**                 | Track compliance with policies     |
| **Access Analyzer (Org-wide)** | Monitor external access across Org |
| **Cost Explorer**              | View costs per account             |
| **Service Quotas**             | Monitor limits centrally           |

---

## 🧰 CLI Examples

### List all accounts:

```bash
aws organizations list-accounts
```

### Create an OU:

```bash
aws organizations create-organizational-unit \
  --parent-id <root-id> \
  --name "Dev"
```

---

## 🧠 Best Practices

| Best Practice                                            | Reason                                           |
| -------------------------------------------------------- | ------------------------------------------------ |
| Use **OUs by environment or business unit**              | Logical separation                               |
| Enable **all features** in Organizations                 | Full control (OUs, SCPs, etc.)                   |
| Apply **least-privilege SCPs**                           | Reduce risk of misconfiguration                  |
| Use **audit and security accounts**                      | Separate accounts for logging & security tooling |
| Use **Control Tower** for large-scale landing zone setup | Faster setup and governance                      |
| Enable **trusted access** with AWS services              | Centralized config, guardrails                   |

---

## ✅ Summary

| Feature                     | Description                         |
| --------------------------- | ----------------------------------- |
| Multi-account mgmt          | ✅ Centralized                       |
| Consolidated billing        | ✅ Included                          |
| SCPs                        | ✅ Guardrails across Org             |
| OU hierarchy                | ✅ Logical account structure         |
| Account creation/invitation | ✅ Manual or automated               |
| Integration with services   | ✅ CloudTrail, Config, Control Tower |

---

# **AWS IAM Identity Center** (formerly AWS SSO)

---

## 🔐 What is AWS IAM Identity Center?

**AWS IAM Identity Center** is a **centralized access management service** that allows you to:

* **Centrally manage** workforce access to multiple AWS accounts
* Assign **user roles and permissions** using existing identity providers (like Okta, Azure AD, etc.)
* Enable **Single Sign-On (SSO)** to AWS Console, CLI, and applications
* Enforce **MFA**, session timeouts, and **fine-grained access**

> ✅ It replaces AWS SSO (Single Sign-On) and integrates with IAM, Organizations, and identity providers.

---

## 🧱 Key Concepts

| Concept                 | Description                                                                                 |
| ----------------------- | ------------------------------------------------------------------------------------------- |
| **Identity Source**     | Where users are authenticated (e.g., IAM Identity Center, Active Directory, Okta, Azure AD) |
| **Permission Sets**     | A reusable set of IAM policies assigned to users or groups                                  |
| **Account Assignments** | Mapping of users/groups → permission set → AWS account                                      |
| **SSO Portal**          | Web interface for users to sign in and access assigned AWS resources                        |
| **SCIM**                | Protocol to sync users/groups from external IdPs like Okta                                  |

---

## 🛠️ How to Set Up IAM Identity Center (From Console)

### 🔹 Step 1: Enable IAM Identity Center

1. Open the AWS Console
2. Go to **IAM Identity Center**
3. Click **“Enable”**
4. Choose **Identity source**:

   * AWS IAM Identity Center (default)
   * External (Azure AD, Okta via SAML/SCIM)

---

### 🔹 Step 2: Add Users and Groups

* Go to **Users → Add user**

  * Name, email, password, and group (optional)
* Go to **Groups → Add group**

  * Name the group and assign users to it

---

### 🔹 Step 3: Create Permission Sets

1. Go to **Permission Sets**
2. Click **“Create permission set”**
3. Choose:

   * **AWS Managed Policies** (e.g., AdministratorAccess)
   * **Custom permissions** (attach your own IAM policies)
4. Name it (e.g., `DevOpsAdminSet`)
5. Optionally configure session duration, relay state, tags

> 📌 Example: A custom permission set for read-only access:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "*",
      "Resource": "*"
    }
  ]
}
```

---

### 🔹 Step 4: Assign Users/Groups to AWS Accounts

1. Go to **AWS Accounts → Select account(s)**
2. Click **“Assign users or groups”**
3. Choose:

   * User/Group
   * Permission set
4. Click **Submit**

✅ Now, the selected users/groups can sign in and access AWS with defined roles.

---

### 🔹 Step 5: User Sign-In (SSO Portal)

* Users go to the **SSO URL** (e.g., `https://your-company.awsapps.com/start`)
* Enter credentials or federate via IdP
* See a **dashboard** with accessible AWS accounts and roles

---

## 🌐 Supported Identity Providers (IdPs)

You can integrate IAM Identity Center with:

| IdP                     | Integration Type      |
| ----------------------- | --------------------- |
| **Okta**                | SCIM + SAML           |
| **Azure AD**            | SCIM + SAML           |
| **Google Workspace**    | SAML                  |
| **Active Directory**    | AWS Directory Service |
| **Custom SAML 2.0 IdP** | Manual setup          |

> With **SCIM**, you can auto-provision and de-provision users and groups.

---

## 📊 Real-World Use Case: DevOps Team

| Role          | Access Level                              | Target                |
| ------------- | ----------------------------------------- | --------------------- |
| DevOps Admin  | AdminAccess                               | Dev and Test accounts |
| SRE           | ReadOnlyAccess                            | All accounts          |
| Security Team | Custom permission (CloudTrail, GuardDuty) | Security OU           |

With IAM Identity Center:

* Define permission sets once
* Assign them to groups
* Easily update or revoke access
* Track user logins and activity via **CloudTrail**

---

## 🛡️ Security Features

| Feature                        | Purpose                                          |
| ------------------------------ | ------------------------------------------------ |
| MFA enforcement                | Extra layer of security for sign-in              |
| Session duration control       | Set session timeouts (15 mins to 12 hours)       |
| Attribute-based access control | Use attributes like department or cost center    |
| Central audit logs             | View all sign-ins and assignments via CloudTrail |

---

## 🧰 CLI + SDK Access

Once configured, users can use:

```bash
aws sso login --profile devops-admin
aws sso list-accounts
aws sso list-roles --account-id <acc-id>
```

Set up `~/.aws/config` with:

```ini
[profile devops-admin]
sso_start_url = https://your-company.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = DevOpsAdminSet
region = us-east-1
output = json
```

Then run:

```bash
aws sso login --profile devops-admin
```

---

## 🚦 Comparison: IAM Identity Center vs IAM Roles

| Feature                    | IAM Identity Center  | IAM Roles              |
| -------------------------- | -------------------- | ---------------------- |
| Centralized access control | ✅                    | ❌ (per account)        |
| SSO Web Portal             | ✅                    | ❌                      |
| SCIM + IdP Integration     | ✅                    | ❌                      |
| MFA and session control    | ✅                    | Limited                |
| Cross-account ease         | ✅ One click          | Manual assume role     |
| Best for                   | Org-wide user access | Infra automation, apps |

---

## 📈 Monitoring & Auditing

* Use **AWS CloudTrail** to track:

  * User logins
  * Role assumptions
  * Permission assignments
* Use **AWS CloudWatch** for alarms
* Integrate with **AWS Config** for compliance

---

## 🧠 Best Practices

| Best Practice                                  | Benefit                  |
| ---------------------------------------------- | ------------------------ |
| Use groups over individual user assignments    | Scalability              |
| Limit permission sets to specific tasks        | Least privilege          |
| Enable MFA for all users                       | Strong security          |
| Integrate with IdP (SCIM + SAML)               | Automated user lifecycle |
| Regularly audit assignments                    | Compliance readiness     |
| Use custom permission sets for non-admin users | Minimize blast radius    |

---

## ✅ Summary

| Feature                  | IAM Identity Center |
| ------------------------ | ------------------- |
| Manage users centrally   | ✅                   |
| Multi-account access     | ✅                   |
| SSO portal for users     | ✅                   |
| Fine-grained permissions | ✅                   |
| Supports external IdPs   | ✅                   |
| CLI and SDK login        | ✅                   |
| Audit-ready logs         | ✅                   |

---
# **AWS IAM Identity Center** and **Amazon Cognito**, 

---

## 🧭 High-Level Comparison: IAM Identity Center vs. Cognito

| Feature                         | **AWS IAM Identity Center**                           | **Amazon Cognito**                                       |
| ------------------------------- | ----------------------------------------------------- | -------------------------------------------------------- |
| 🎯 **Purpose**                  | Centralized access control for **workforce users**    | Authentication for **application (end) users**           |
| 👥 **Users**                    | Employees, admins, DevOps, internal users             | App users, mobile/web app customers                      |
| 🔐 **SSO Support**              | ✅ Enterprise SSO (Okta, Azure AD, AD, etc.)           | ✅ Social login (Google, Facebook, etc.), custom IdP      |
| 📲 **Use Case**                 | Access to **AWS Console/Accounts/Apps** for workforce | Login/auth for **customer-facing apps** (web/mobile)     |
| 🎛️ **Managed Permissions**     | ✅ IAM permission sets, SCPs across AWS accounts       | ❌ Permissions not tied to IAM policies (unless extended) |
| 🔄 **User Federation**          | ✅ SAML / SCIM federation with IdPs                    | ✅ OIDC / SAML / Federated IdPs                           |
| 🎫 **Token Type**               | IAM temporary credentials (AWS STS)                   | OIDC/JWT tokens (OAuth 2.0)                              |
| 📋 **Integration Targets**      | AWS accounts, CLI, SDK, Control Tower, applications   | Web/mobile applications                                  |
| 🔒 **MFA Support**              | ✅ MFA enforcement per session                         | ✅ MFA for app login (TOTP, SMS)                          |
| 📈 **Session Duration Control** | ✅ Console/CLI session duration                        | ✅ Access/Refresh token expiration                        |
| 🌍 **Login Portal**             | Central SSO user dashboard                            | Custom UI hosted by Cognito                              |
| 🧩 **Custom App Integration**   | Indirect (via application assignments)                | Direct (auth flows in React, Android, iOS, etc.)         |

---

## 📌 Use Case Breakdown

| Scenario                                                 | Use Which?            | Why?                                                   |
| -------------------------------------------------------- | --------------------- | ------------------------------------------------------ |
| Give **DevOps teams** secure SSO access to AWS accounts  | ✅ IAM Identity Center | Centralize and federate workforce access               |
| Allow users to **sign in to your mobile/web app**        | ✅ Amazon Cognito      | Handles signup, login, JWT tokens, identity federation |
| Manage **SSO with Microsoft Azure AD** to AWS            | ✅ IAM Identity Center | Integrates via SCIM + SAML                             |
| Support **Google login on your app**                     | ✅ Amazon Cognito      | Supports social IdP login                              |
| Central policy enforcement across **multiple AWS accts** | ✅ IAM Identity Center | Works with OUs, SCPs, permission sets                  |

---

## 💡 Example Scenarios

### 🧑‍💼 IAM Identity Center

> You work in a company with multiple AWS accounts (Dev, QA, Prod). You want to allow internal employees to:

* Log in using Azure AD credentials
* Access only the Dev account with read-only permissions

✅ Use **IAM Identity Center** with SCIM + SAML to federate Azure AD and manage access via permission sets.

---

### 🧑‍💻 Amazon Cognito

> You’re building a **FinTech web app** and want users to:

* Sign up using email
* Log in with Google or Facebook
* Receive JWT tokens for authenticated API calls

✅ Use **Cognito User Pools** (authentication) + **Identity Pools** (federation & AWS credentials)

---

## 🔧 Under the Hood

| Feature                     | IAM Identity Center                        | Amazon Cognito                                |
| --------------------------- | ------------------------------------------ | --------------------------------------------- |
| **Authentication Protocol** | SAML 2.0, SCIM, OAuth (indirect)           | OIDC, OAuth 2.0, SAML                         |
| **Auth Token**              | Temporary AWS credentials (via STS)        | JWT tokens (ID, access, refresh)              |
| **Integration with IAM**    | ✅ (via permission sets & account mappings) | ❌ (only indirectly via identity pools)        |
| **User Data Management**    | Limited (attributes via SCIM)              | Extensive (attributes, custom fields, groups) |
| **Audit Trail**             | CloudTrail logs all access events          | Limited to Cognito events                     |

---

## 🧠 Summary Table

| Area                         | IAM Identity Center        | Amazon Cognito                              |
| ---------------------------- | -------------------------- | ------------------------------------------- |
| **User Type**                | Internal (Workforce)       | External (App Users)                        |
| **Login UI**                 | AWS-hosted SSO Portal      | Hosted or custom UI                         |
| **Federation Support**       | SAML/SCIM (Enterprise IdP) | SAML/OIDC/Social IdPs                       |
| **Manages AWS permissions**  | ✅ Yes                      | ❌ No (unless via Identity Pool + IAM roles) |
| **SSO for AWS Console/CLI**  | ✅ Yes                      | ❌ No                                        |
| **Used for Mobile/Web Apps** | ❌ No                       | ✅ Yes                                       |

---

## ✅ Conclusion

* Use **IAM Identity Center** for managing **employee/internal team access to AWS resources** (SSO, CLI, permission sets).
* Use **Amazon Cognito** for managing **customer or external user login into web/mobile applications**.

---

## If you want to **keep using Keycloak with OIDC**, and integrate it with AWS for authentication/access management, here’s a **clear breakdown of how to do it** — while **Keycloak remains your Identity Provider (IdP)**.

---

## ✅ Objective

**Use Keycloak (OIDC)** as the **central IdP** and integrate it with AWS to:

* Authenticate users using Keycloak
* Authorize access to **AWS Console, CLI, or SDK**
* Or authenticate users to your **applications (via Cognito or directly)**

---

## 🔄 Integration Options (Keycloak + OIDC)

| Target                              | Integration Method                                                        |
| ----------------------------------- | ------------------------------------------------------------------------- |
| AWS Console / CLI / SDK (Workforce) | 🔸 IAM Identity Center + SAML (indirect OIDC via SAML bridge)             |
| AWS API access for apps             | 🔸 Cognito Identity Pool with OIDC Federation to Keycloak                 |
| Custom application login            | ✅ Direct OIDC login via Keycloak (OAuth2/JWT)                             |
| Federate into IAM Role              | 🔸 Web Identity Federation via IAM Role with Trust Policy (OIDC provider) |

---

# 🧭 Option 1: **Federate Keycloak with Cognito (OIDC)** for Application Auth

This is ideal for customer- or user-facing **web/mobile apps**.

---

### ✅ Architecture

```
[User] → [Keycloak (OIDC)] → [Cognito User Pool Federation] → [App]
```

---

### 🔹 Steps to Implement

#### 1. Create a **Cognito User Pool**

* AWS Console → Cognito → User Pools → Create User Pool
* Name it (e.g., `app-auth`)

#### 2. Add Keycloak as an **OIDC IdP**

* Go to **Federation > Identity providers**
* Choose **OIDC provider**
* Enter:

  * **Provider name**: `keycloak`
  * **Client ID/Secret** (created in Keycloak)
  * **Issuer URL**: e.g., `https://keycloak.example.com/realms/dev`
  * OIDC endpoints (`.well-known/openid-configuration`)

#### 3. Map Attributes

* Map Keycloak claims like `email`, `name`, `groups`, etc., to Cognito attributes

#### 4. Create an **App Client**

* Enable `Authorization Code` flow
* Enable `client_secret` if needed

#### 5. Add Domain

* Create a Cognito domain (or use a custom one)

#### 6. Test the Flow

* Navigate to:
  `https://<your-domain>.auth.<region>.amazoncognito.com/login?response_type=code&client_id=...`
* You will be redirected to **Keycloak** for login

---

# 🧭 Option 2: **Use Cognito Identity Pool + Keycloak (OIDC)** to Get Temporary AWS Credentials

This allows users authenticated via Keycloak to assume **IAM roles** and call AWS APIs.

---

### ✅ Architecture

```
[User] → [Keycloak OIDC Token] → [Cognito Identity Pool] → [IAM Role] → [AWS Services]
```

---

### 🔹 Steps to Implement

#### 1. Create Cognito Identity Pool

* Go to **Cognito → Federated Identities**
* Create new Identity Pool (name: `keycloak-access`)

#### 2. Choose **OIDC Provider**

* Add **Keycloak OIDC provider**

  * `Issuer`: `https://keycloak.example.com/realms/dev`
  * Set audience/client ID to match Keycloak app

#### 3. Create IAM Roles

* Create IAM role with trust policy:

```json
{
  "Effect": "Allow",
  "Principal": {
    "Federated": "cognito-identity.amazonaws.com"
  },
  "Action": "sts:AssumeRoleWithWebIdentity",
  "Condition": {
    "StringEquals": {
      "cognito-identity.amazonaws.com:aud": "<identity-pool-id>",
      "cognito-identity.amazonaws.com:amr": "authenticated"
    }
  }
}
```

* Attach this role to authenticated users

#### 4. Get Token from Keycloak

* Call:

```bash
curl -X POST https://keycloak.example.com/realms/dev/protocol/openid-connect/token \
 -d "grant_type=password" \
 -d "client_id=myapp" \
 -d "username=alice" \
 -d "password=secret"
```

* Extract the `id_token` (JWT)

#### 5. Get AWS Credentials

```bash
aws sts assume-role-with-web-identity \
  --role-arn arn:aws:iam::<account-id>:role/KeycloakWebAccess \
  --role-session-name test-session \
  --web-identity-token file://id_token.jwt
```

---

# 🧭 Option 3: **Federate Keycloak Directly with IAM Role (OIDC Trust)**

This works **without Cognito** — you register Keycloak as an **OIDC provider** in IAM.

---

### 🔹 Steps

#### 1. In IAM, create an OIDC Provider

```bash
aws iam create-open-id-connect-provider \
  --url https://keycloak.example.com/realms/dev \
  --client-id-list my-client-id \
  --thumbprint-list <cert-thumbprint>
```

#### 2. Create IAM Role with Trust Policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::<account-id>:oidc-provider/keycloak.example.com/realms/dev"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "keycloak.example.com/realms/dev:aud": "my-client-id"
        }
      }
    }
  ]
}
```

#### 3. Use Keycloak ID Token to Assume Role

* Use STS CLI as above

---

# ✅ Summary Table

| Use Case                 | Service                                                | Notes                                       |
| ------------------------ | ------------------------------------------------------ | ------------------------------------------- |
| AWS access for employees | IAM Identity Center (via SAML, OIDC bridge not native) | Indirect — use SAML via Keycloak            |
| Application login        | Cognito User Pool (OIDC Federation)                    | Best for hosted web/mobile apps             |
| AWS API access           | Cognito Identity Pool or STS with Web Identity         | Use Keycloak JWT to get temporary AWS creds |
| Direct IAM role access   | IAM OIDC Provider + STS                                | Bypass Cognito, more control                |

---


