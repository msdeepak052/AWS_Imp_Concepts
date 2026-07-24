# 11 - IAM Roles Custom Trust Policy (Hands-On)

> Goal: skip the console's guided "choose a trusted entity type" wizard (used throughout Notes 07-10) and write a role's trust policy **directly as JSON**, for the cases the wizard's presets don't cleanly cover — such as trusting more than one principal type on the same role, or adding conditions the wizard doesn't expose.

---

## 1. Why go beyond the wizard

Every role so far in this folder was created via a guided flow: pick "AWS service," "AWS account," or "SAML/Web identity," and the console fills in a correct, single-purpose trust policy for you. Real-world trust requirements are sometimes more layered than any one preset covers — for example, a role that should be assumable **either** by a specific EC2 use case **or** by a specific human user for break-glass access, with conditions attached. The console **does** let you edit a role's trust policy as raw JSON after creation — that's exactly what this note walks through.

---

## 2. Edit an existing role's trust policy directly

1. **IAM console** → **Roles** → open `TempEC2Admin-Role` (from Note 08).
2. **Trust relationships** tab → **Edit trust policy**.
3. You're now looking at the exact same JSON structure the wizard generated — nothing new syntactically, just direct access to it instead of going through the guided prompts.

---

## 3. Add a second, independent principal to the same role

Suppose this role should also be assumable directly by a specific role in another account, in addition to the same-account trust it already has:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "SameAccountTrust",
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::111122223333:root" },
      "Action": "sts:AssumeRole"
    },
    {
      "Sid": "PartnerAccountTrust",
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::555566667777:role/PartnerAuditRole" },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": { "sts:ExternalId": "partner-shared-secret-123" }
      }
    }
  ]
}
```

Two independent `Statement` blocks, each with their own `Sid` (statement ID, purely a human-readable label), let one role serve two entirely different trust relationships at once — something no single guided wizard flow sets up in one pass.

---

## 4. Scope a trust policy down with conditions the wizard doesn't expose

The wizard's basic flows don't surface every possible `Condition` key. Written directly, you can restrict, for example, assumption to only happen from a specific source IP range, or only when MFA was present at the time of the original sign-in:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::111122223333:root" },
      "Action": "sts:AssumeRole",
      "Condition": {
        "Bool": { "aws:MultiFactorAuthPresent": "true" }
      }
    }
  ]
}
```

This forces anyone assuming the role to have authenticated with MFA first — a common hardening step for any role granting broad or sensitive permissions (e.g. the `TempEC2Admin-Role` pattern from Note 08).

> ⚠️ `aws:MultiFactorAuthPresent` reflects whether MFA was used for the **original** sign-in session, not something re-checked at the exact moment of the `AssumeRole` call itself — it's still a real, commonly-tested condition key, just worth understanding precisely what it verifies.

---

## 5. Custom trust policy vs. the guided wizard — when to write JSON directly

| Situation | Approach |
|---|---|
| Standard single trusted-entity type (one service, one account, one IdP) | Guided wizard (Notes 07-10) is faster and less error-prone |
| Multiple, independent trust relationships on one role | Custom JSON — combine multiple `Statement` blocks |
| Need a `Condition` key the wizard doesn't expose (MFA requirement, source IP, tag-based conditions, etc.) | Custom JSON |
| Migrating/importing a role definition from Infrastructure as Code (CloudFormation/Terraform/CDK) | Custom JSON — IaC tools always express trust policies as raw JSON/HCL under the hood anyway |

---

## 6. Recap

- Every role's trust policy is just JSON underneath the console's guided wizards — Notes 07-10's flows are conveniences, not a different underlying mechanism.
- Custom trust policies let one role trust multiple, independent principals at once (multiple `Statement` blocks), and expose `Condition` keys (like `aws:MultiFactorAuthPresent` or `sts:ExternalId`) the guided wizards don't surface.
- This closes out the role-assumption series (Notes 07-11). Next: Note 12 — IAM Root User Best Practices, Part 1: Multi-Factor Authentication (MFA), shifting focus to the account's single most powerful (and most dangerous) identity.

### Sources
- [IAM JSON policy elements: Principal — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html)
- [IAM JSON policy elements: Condition — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html)
- [AWS global condition context keys — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html)
- [Modifying a role trust policy (console) — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-managingrole-editing-console.html#roles-managingrole_edit-trust-policy)
