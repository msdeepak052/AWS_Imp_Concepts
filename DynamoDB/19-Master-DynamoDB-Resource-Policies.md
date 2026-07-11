# 19 - Master DynamoDB Resource Policies: Essential for AWS Certification

> Goal: cover DynamoDB resource-based policies — a comparatively recent access-control feature — verified against current AWS documentation, and how it compares to IAM identity-based policies.

---

## 1. What a resource-based policy is

A **resource-based policy** is attached directly to a DynamoDB **table** (rather than to an IAM user/role/group), granting specified principals — including principals in **other AWS accounts** — permission to access that table and its indexes/streams.

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "AWS": "arn:aws:iam::222222222222:role/AnalyticsRole" },
    "Action": ["dynamodb:GetItem", "dynamodb:Query"],
    "Resource": "arn:aws:dynamodb:us-east-1:111111111111:table/Orders"
  }]
}
```

---

## 2. Why this exists: simplifying cross-account access

Before resource-based policies, cross-account DynamoDB access required the accessing account to **assume an IAM role** in the table's owning account (`IAM/09-IAM-Roles-Cross-Account-Access-HandsOn`'s pattern). A resource-based policy lets the table owner **directly grant** a specific principal in another account access, **without** that principal needing to assume any role first.

> 🧠 **Mental model:** this is the same identity-vs-resource-policy duality this repo's `S3-Simple_Storage_Services` folder covers for S3 bucket policies, and `IAM`'s cross-account notes cover for role trust policies — DynamoDB simply gained its own resource-based policy option more recently than S3 had one.

---

## 3. Key considerations

- Maximum policy size: **20 KB** per resource.
- Covers the table, its indexes, and its streams under one attached policy.
- Can be attached at **table creation** or to an **existing table**, via console, `PutResourcePolicy` API, CLI, SDK, or CloudFormation.

> 🎯 **Exam tip:** "grant access to a DynamoDB table for a principal in another AWS account, without that principal assuming a role" is the resource-based-policy signal — the simplification it provides over the traditional AssumeRole cross-account pattern.

---

## 4. Recap

- DynamoDB resource-based policies attach directly to a table, simplifying cross-account (and cross-principal) access grants without requiring AssumeRole — a newer alternative/complement to IAM identity-based policies.
- Next: Note 20 — DynamoDB Global Tables Explained, covering multi-Region replication.

### Sources
- [Using resource-based policies for DynamoDB — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/access-control-resource-based.html)
- [DynamoDB resource-based policy considerations — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/rbac-considerations.html)
