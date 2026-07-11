# 39 - AWS VPC Gateway Endpoint For S3 (Hands-On)

> Goal: keep traffic between a private-subnet EC2 instance and S3 entirely off the public internet, using a **VPC Gateway Endpoint** — directly relevant to this repo's CloudMart capstone pattern of private-subnet compute needing outbound access.

---

## 1. The problem: private instances normally reach S3 via NAT

Recall the CloudMart capstone (`Capstone-Project/Project-1`): private-subnet instances reach the internet only via a NAT Gateway. Without any further configuration, that means **S3 traffic from a private instance also goes out through the NAT Gateway**, across the public internet (even though it's still encrypted via HTTPS) — costing NAT Gateway data-processing charges for traffic that never actually needed to leave AWS's own network at all, since S3 is itself an AWS service.

> 🧠 **Mental model:** a VPC Gateway Endpoint is a private, direct on-ramp from your VPC straight to S3, entirely within AWS's network — instead of exiting through the NAT Gateway and traveling out to the public internet just to reach a service that was never actually "out there" in the first place.

---

## 2. Gateway Endpoint vs. Interface Endpoint (brief distinction)

VPC endpoints come in two flavors; S3 (and DynamoDB) uniquely support the **free, simpler Gateway Endpoint** type, while most other AWS services use **Interface Endpoints** (ENI-based, with an hourly charge):

| | Gateway Endpoint (S3, DynamoDB only) | Interface Endpoint (most other services) |
|---|---|---|
| Mechanism | A special **route table entry** pointing at the service | An **ENI** with a private IP inside your subnet |
| Cost | **Free** | Hourly charge + data processing charge |
| Reachability | Reachable via the route table, no in-subnet address consumed | Reachable via a private IP address in your subnet |

> 🎯 **Exam tip:** "reduce NAT Gateway costs for private-subnet traffic to S3 or DynamoDB, at no additional cost for the endpoint itself" is the signature **Gateway Endpoint** scenario — its free pricing model (versus Interface Endpoints' hourly charge) is a frequently tested distinguishing detail.

---

## 3. Create the Gateway Endpoint

1. **VPC console** → **Endpoints** → **Create endpoint**.
2. **Service category**: **AWS services**.
3. **Service name**: search for `s3`, select the entry with **Type: Gateway** (as opposed to the Interface-type S3 entry, which also exists for different use cases).
4. **VPC**: select the target VPC (e.g. `cloudmart-vpc`).
5. **Route tables**: select the route table(s) associated with the **private subnets** that need this (e.g. `cloudmart-private-rt`, from the capstone) — this is what actually wires the endpoint in.
6. **Policy**: optionally attach an endpoint policy restricting which S3 actions/buckets are reachable through this endpoint specifically (defaults to full access).
7. **Create endpoint**.

---

## 4. What actually changed — inspect the route table

```bash
aws ec2 describe-route-tables --route-table-ids rtb-xxxxxxxx
```

The output now shows a new route: destination is S3's specific **prefix list** (a managed, AWS-maintained list of S3's IP ranges, not a single CIDR) → target is the new **VPC Endpoint ID**. Any traffic from that subnet destined for S3 now matches this route **before** falling through to the `0.0.0.0/0 → NAT Gateway` route, keeping it on AWS's private network end to end.

---

## 5. Verify from a private instance

```bash
# From an EC2 instance in a private subnet associated with the endpoint's route table
aws s3 ls s3://demo-bucket/
```

This now succeeds **without** the NAT Gateway processing this traffic at all — confirmable by checking VPC Flow Logs or simply noting the request still works even in a test where the NAT Gateway is temporarily unreachable, since S3 traffic no longer depends on it.

---

## 6. Recap

- A **VPC Gateway Endpoint** for S3 routes traffic from a VPC directly to S3 over AWS's private network, via a route table entry — avoiding the NAT Gateway (and its data-processing cost) entirely for S3-bound traffic.
- S3 and DynamoDB are the **only** services with the free **Gateway Endpoint** type; everything else uses a paid **Interface Endpoint**.
- Directly applicable to any private-subnet architecture (like the CloudMart capstone) where compute needs to reach S3 without traversing the public internet.
- Next: Note 40 — AWS S3 Access Point Theory, a different scoping mechanism for simplifying access management on buckets shared by many applications/teams.

### Sources
- [Gateway endpoints for Amazon S3 — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html)
- [VPC endpoints — AWS docs](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints.html)
- [Gateway endpoints — AWS docs](https://docs.aws.amazon.com/vpc/latest/privatelink/vpce-gateway.html)
