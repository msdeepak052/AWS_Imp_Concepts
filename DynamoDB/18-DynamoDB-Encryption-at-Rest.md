# 18 - DynamoDB Encryption at Rest Explained!

> Goal: cover DynamoDB's encryption-at-rest model — notably simpler than RDS's (Note 24), since it's always on.

---

## 1. Always on, by default

Unlike RDS (where encryption at rest must be chosen at creation time and can't be retrofitted directly — `RDS/24`), **every DynamoDB table is encrypted at rest by default**, with no way to opt out — there is no "unencrypted DynamoDB table."

---

## 2. Three key options

| Option | Who manages the KMS key |
|---|---|
| **AWS owned key** (default) | AWS, at no additional cost, no visibility into the key itself |
| **AWS managed key** | AWS, but visible/manageable in your account's KMS console, still no extra cost |
| **Customer managed key (CMK)** | You — full control over key policy, rotation, and the ability to revoke access by disabling the key |

- Switching between these options is possible **after table creation** (unlike RDS, Note 24) — a meaningfully more flexible model.

> 🎯 **Exam tip:** "need full control over the encryption key, including the ability to revoke access" → **customer managed key**; "encryption is required but no specific key-management need" → the **default AWS owned key** already satisfies that with zero additional setup or cost.

---

## 3. Recap

- DynamoDB tables are always encrypted at rest; you choose between an AWS owned key (default), AWS managed key, or your own customer managed KMS key — and can change this choice after creation, unlike RDS.
- Next: Note 19 — Master DynamoDB Resource Policies, covering resource-based access control.

### Sources
- [DynamoDB encryption at rest — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/EncryptionAtRest.html)
