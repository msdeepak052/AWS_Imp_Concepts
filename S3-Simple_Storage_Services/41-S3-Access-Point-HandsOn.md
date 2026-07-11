# 41 - AWS S3 Access Point (Hands-On)

> Goal: create two real access points on the same shared bucket — one for a read-only analytics app, one VPC-restricted — and prove each one enforces only its own scope, completing this folder's access-control coverage.

---

## 1. Create the first access point — read-only, prefix-scoped

1. **S3 console** → **Access Points** → **Create access point**.
2. **Access point name**: `analytics-ap`.
3. **Bucket**: select the shared bucket (e.g. `demo-shared-bucket`).
4. **Network origin**: **Internet** (reachable from anywhere the caller's own IAM permissions allow — contrast with Section 3's VPC-restricted example).
5. **Block Public Access settings for this access point**: leave all four enabled (Note 24's settings, now scoped per-access-point).
6. **Access point policy**:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": { "AWS": "arn:aws:iam::111122223333:role/analytics-app-role" },
         "Action": "s3:GetObject",
         "Resource": "arn:aws:s3:ap-south-1:111122223333:accesspoint/analytics-ap/object/reports/*"
       }
     ]
   }
   ```
7. **Create access point**.

---

## 2. Confirm the underlying bucket policy still needs to agree

Per Note 40, Section 4: the bucket itself must also permit access **through** access points. Add this to the bucket's own policy (or delegate broadly to any access point in the account):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": ["arn:aws:s3:::demo-shared-bucket", "arn:aws:s3:::demo-shared-bucket/*"],
      "Condition": {
        "StringEquals": { "s3:DataAccessPointAccount": "111122223333" }
      }
    }
  ]
}
```

This delegates authorization decisions to whichever access point handled the request, rather than re-listing every consumer directly in the bucket policy — exactly the simplification Note 40 described.

---

## 3. Create a second, VPC-restricted access point

1. **Create access point** again → name: `audit-ap`.
2. **Network origin**: **This VPC** → select the specific VPC ID (e.g. the audit team's own VPC).
3. **Access point policy**: grant the audit team's role `s3:GetObject` on the same bucket, scoped to whatever prefix audits need.
4. **Create access point**.

This access point is now **only reachable from within the specified VPC** — even a caller with a technically-valid IAM permission on this access point's policy will be rejected if the request doesn't originate from that VPC, an extra network-layer restriction beyond anything policy alone can express.

---

## 4. Test both

```bash
# Via analytics-ap (internet-reachable, prefix-scoped to reports/)
aws s3api get-object \
  --bucket arn:aws:s3:ap-south-1:111122223333:accesspoint/analytics-ap \
  --key reports/q1.csv q1.csv

# Attempting to reach a different prefix through the same access point fails:
aws s3api get-object \
  --bucket arn:aws:s3:ap-south-1:111122223333:accesspoint/analytics-ap \
  --key uploads/other-team-file.csv out.csv   # denied — outside analytics-ap's scoped policy
```

From an EC2 instance **inside** the audit team's VPC, `audit-ap` succeeds; the same call attempted from outside that VPC (even with a technically-permitted IAM identity) fails due to the VPC restriction from Section 3.

---

## 5. Recap

- Two access points on the **same bucket** each enforce their **own** scope: `analytics-ap` restricts by prefix and grants internet reachability; `audit-ap` adds a **VPC-only** network restriction on top of its own policy.
- The bucket's own policy still must independently permit access-point-mediated requests (commonly via the `s3:DataAccessPointAccount` condition, delegating the finer-grained decision to whichever access point handled the call).
- This closes the entire S3 folder: Notes 01-05 covered fundamentals and storage classes, 06-08 versioning/lifecycle, 09-14 access control and Object Lock, 15-22 the full encryption landscape, 23-25 public access, 26-31 website hosting/CORS/replication/acceleration, 32-37 logging/auditing/cost/notification features, and 38-41 multipart upload, VPC-private access, and access points.

### Sources
- [Managing access with Amazon S3 access points — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-points.html)
- [Creating access points restricted to a VPC — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-points-vpc.html)
- [Configuring IAM policies for using access points — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-points-policies.html)
