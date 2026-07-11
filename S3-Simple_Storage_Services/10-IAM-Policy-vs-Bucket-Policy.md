# 10 - AWS S3 — AWS IAM Policy Vs Bucket Policy

> Goal: put IAM policies and bucket policies side by side directly, since Note 09 introduced them separately — same JSON syntax, genuinely different attachment point and authority, and each with situations where only one of them actually works.

---

## 1. Same language, different attachment point

Both an IAM policy and a bucket policy are written in the **exact same JSON policy language** (`Version`, `Statement`, `Effect`, `Action`, `Resource`, optional `Condition` — all from `IAM/01`). The difference is entirely about **what the policy is attached to**, which changes what `Principal` means and who the policy can actually reach:

| | IAM policy | Bucket policy |
|---|---|---|
| Attached to | A user, group, or role | The bucket itself |
| Has a `Principal` element? | **No** — the identity it's attached to *is* the principal, implicitly | **Yes** — must explicitly name who the statement applies to |
| Can grant access to another AWS account? | No | **Yes** |
| Can grant public/anonymous access? | No | **Yes** (subject to Block Public Access, Notes 24-25) |
| Where you'd look to answer "what can this specific user do everywhere?" | IAM policy | N/A — bucket policies don't describe a user's full permission set |
| Where you'd look to answer "who can reach this specific bucket?" | N/A — IAM policies don't describe a bucket's exposure | Bucket policy |

> 🧠 **Mental model:** an IAM policy is written from the identity's point of view ("here's everything **I** can do"); a bucket policy is written from the resource's point of view ("here's everyone who's allowed to touch **me**"). Same language, opposite vantage point — and S3 checks both.

---

## 2. A bucket policy needs an explicit Principal; an IAM policy doesn't

```json
// IAM policy — attached to a user; no Principal needed, the user IS the principal
{
  "Version": "2012-10-17",
  "Statement": [
    { "Effect": "Allow", "Action": "s3:GetObject", "Resource": "arn:aws:s3:::demo-bucket/*" }
  ]
}
```

```json
// Bucket policy — attached to the bucket; must say WHO this applies to
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::444455556666:user/external-partner" },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::demo-bucket/*"
    }
  ]
}
```

The bucket policy example grants read access to a **specific user in a completely different AWS account** — something no IAM policy, written anywhere, could ever do on its own, since IAM policies only govern the identity they're attached to, and that identity lives in the *other* account entirely.

---

## 3. When each one alone is sufficient, and when you need both

| Scenario | IAM policy alone enough? | Bucket policy needed? |
|---|---|---|
| A user in your own account needs S3 access, and no cross-account/public sharing is involved | ✅ Often yes | Not necessarily |
| An external AWS account needs access to your bucket | ❌ No | ✅ Yes, on your bucket |
| The bucket must be reachable anonymously/publicly (e.g. static website hosting, Note 26) | ❌ No | ✅ Yes (plus Block Public Access must allow it) |
| A centralized security team wants one place to see and audit **everyone** who can reach a specific sensitive bucket | Harder — would mean checking every IAM identity in every account | ✅ A bucket policy is the natural single place to see this |

> 🎯 **Exam tip:** whenever a scenario explicitly names **cross-account** or **public** access, the answer almost always requires a **bucket policy** — an IAM policy is never sufficient by itself for either of those two cases, no matter how permissive it is, because IAM policies have no authority outside the account (and identity) they're attached to.

---

## 4. Both are still gated by the same evaluation logic

Exactly as Note 09 diagrammed: an explicit `Deny` in **either** an IAM policy or a bucket policy blocks the request, regardless of what the other one allows — there's no "the more permissive one wins" shortcut. This is the same explicit-deny-always-wins rule from `IAM/01`, just spanning identity-based and resource-based policies simultaneously.

---

## 5. Recap

- IAM policies and bucket policies use the **same JSON syntax**, but an IAM policy is identity-attached (no `Principal` needed) while a bucket policy is resource-attached (`Principal` required, since it must state who it applies to).
- Only a **bucket policy** can grant **cross-account** or **public** access — an IAM policy's authority never extends outside its own account.
- Effective access is still governed by the same "any explicit Deny wins" rule across both mechanisms together.
- Next: Note 11 — AWS IAM Policy For S3 Bucket (Hands-On), authoring the identity-based side of this in practice.

### Sources
- [Identity and access management in Amazon S3 — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-access-control.html)
- [Bucket policies for Amazon S3 — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-policies.html)
- [IAM JSON policy elements: Principal — AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html)
