# 11 - End-to-End Testing, HA Validation, and Cleanup

> Goal: prove CloudMart actually works end to end, deliberately break it in controlled ways to confirm the HA design from Note 02 holds up, be honest about the one place it doesn't, and then tear the whole capstone down safely, in the right order, so nothing keeps billing after you're done.

---

## 1. End-to-end functional test

1. Open `cloudmart-public-alb`'s DNS name (or `www.cloudmart.example`, conceptually, per Note 10) in a browser. Confirm the CloudMart page renders with all 5 seeded products.
2. Test the **write path**, not just the read path — from any machine that can reach the ALB:
   ```bash
   curl -X POST http://<cloudmart-public-alb-dns>/api/products \
     -H "Content-Type: application/json" \
     -d '{"name": "CloudMart Tote Bag", "price": 12.50, "stock": 80}'
   ```
3. Refresh the browser page. **CloudMart Tote Bag** should now appear in the list — this single request travels through the public ALB, the frontend's Nginx proxy, the internal ALB, a backend Flask instance, and an `INSERT` on `cloudmart-db-1`, and the read-back in step 2 proves every hop in Note 04's request-workflow diagram actually works, not just the parts that are easy to see.

---

## 2. HA validation — web and app tiers

Both `cloudmart-web-asg` and `cloudmart-app-asg` are supposed to survive losing one instance without a full outage. Prove it:

1. **EC2 console** → **Instances** → find one of the two running instances that belongs to `cloudmart-web-asg` (check the **Auto Scaling Group name** column) → **Instance state** → **Terminate instance**.
2. Immediately keep refreshing the CloudMart page in your browser. It should keep loading throughout — the ALB stops sending traffic to the terminated instance the moment it's gone and simply routes 100% of traffic to the surviving instance in the other AZ.
3. Watch `cloudmart-web-asg`'s **Activity** tab: within roughly a minute you should see a **Terminating** event followed by a **Launching** event, and the replacement instance rejoin `cloudmart-web-tg` as Healthy a few minutes later (Note 04's auto-healing sequence, playing out for real).
4. Repeat the same test against one instance in `cloudmart-app-asg`. The browser test this time is the `curl .../api/products` command from Section 1 — it should keep succeeding throughout, because the internal ALB has the same failover behavior as the public one.

Both tests should show **zero failed requests** from the browser/curl's perspective (at most, a request or two might briefly hit slightly higher latency while the ALB detects the failure) — this is exactly what "minimum 2, one per AZ" buys.

---

## 3. The one test that will NOT pass — the database

> ⚠️ **Do not actually run this test against a system anyone depends on** — it's described here to be explicit about the architecture's honest limitation, not as something to casually try. If `cloudmart-db-1` were terminated right now, every request to `/api/products` would start failing immediately, because there is no second database instance, no replica, and no automatic failover target for the app tier to fall back to — Note 02 named this exact gap up front, and this is what it looks like in practice: the frontend and backend tiers would stay perfectly healthy and keep serving traffic, but every one of their database queries would simply start erroring out. Fixing this gap for real means replacing `cloudmart-db-1` with **Amazon RDS in Multi-AZ mode**, which is explicitly out of scope for this 5-service capstone (Note 01, Section 4) but is the natural next step for CloudMart's architecture if it ever needs to close this gap.

---

## 4. ⚠️ Cleanup — tear everything down, in this order

Every resource below bills continuously while it exists. Delete them in this exact order — AWS will block several of the later deletions if you try to skip ahead (e.g. it won't let you delete a VPC while a NAT Gateway or an attached Internet Gateway still exists inside it).

| Step | Delete | Why this order |
|---|---|---|
| 1 | `cloudmart-web-asg` and `cloudmart-app-asg` — **delete the Auto Scaling Groups themselves** (not just their instances; terminating instances one by one only makes the ASG launch replacements) | Removes all EC2 instances in both compute tiers cleanly |
| 2 | `cloudmart-public-alb` and `cloudmart-internal-alb` | Load balancers must go before their subnets/security groups can be removed |
| 3 | `cloudmart-app-tg` and `cloudmart-web-tg` | Target groups can only be deleted once no load balancer references them |
| 4 | Route 53: delete the `www.cloudmart.example` record, then `cloudmart-alb-health-check`, then the `cloudmart.example` hosted zone | The record must go before the health check it references; the zone can't be deleted while custom records (other than the default NS/SOA) remain |
| 5 | `cloudmart-db-1` — terminate the instance | The last EC2 instance still running |
| 6 | `cloudmart-nat-gw-1` and `cloudmart-nat-gw-2` — delete both NAT Gateways, then **release** their two Elastic IPs separately | An EIP still associated with a NAT Gateway can't be released; deleting the gateway first frees it |
| 7 | `cloudmart-igw` — detach from `cloudmart-vpc`, then delete | A VPC can't be deleted while an Internet Gateway is still attached |
| 8 | All 6 subnets (`cloudmart-web-subnet-1/2`, `cloudmart-app-subnet-1/2`, `cloudmart-db-subnet-1/2`) | Subnets can't be deleted while a NAT Gateway or any ENI still lives inside them — by this point, none do |
| 9 | The 3 route tables (`cloudmart-web-rt`, `cloudmart-app-rt-1`, `cloudmart-app-rt-2`) | Only the default/main route table is required to remain; custom ones can be deleted once unassociated |
| 10 | `cloudmart-vpc` itself | Deletable only once nothing above still references it |
| 11 | The 5 security groups (`cloudmart-alb-web-sg`, `cloudmart-web-asg-sg`, `cloudmart-alb-internal-sg`, `cloudmart-app-asg-sg`, `cloudmart-db-sg`) | Deleted automatically with the VPC, or manually beforehand if you prefer to see it happen explicitly |
| 12 | The IAM role/instance profile `cloudmart-ssm-role` | Not VPC-scoped, safe to delete any time after step 5, once no instance references it |

🎯 **Exam tip:** this dependency-ordered teardown is exactly the kind of "why can't I delete my VPC" troubleshooting scenario the exam likes to test — the answer is almost always "something inside it (a NAT Gateway, an ENI, an attached IGW, a non-default route table association) still exists and must be removed first."

---

## 5. Recap — did this build meet Note 01's requirements?

| Requirement (Note 01) | Met by |
|---|---|
| F1-F3: dynamic product catalog with a real read+write API | Notes 03, 08, 09 — confirmed again in Section 1 above |
| F4: friendly domain name | Note 10's Alias record |
| F5: backend never directly internet-reachable | Note 02's subnet isolation + SG chain, confirmed by the internal-scheme ALB in Note 08 |
| HA: survive losing an AZ, self-healing | Confirmed for real in Section 2 above, for both compute tiers |
| Security: no SSH, private tiers, chained SGs | Notes 05-06, verified throughout the build |
| Scalability: independent per-tier auto scaling | Both ASGs' target-tracking policies, Notes 08-09 |
| DNS: health-check-aware | Note 10 |
| Cost-awareness: stated plainly, not discovered later | Note 01, Section 3.5 — and now torn down in Section 4 above |

CloudMart's one honestly-acknowledged gap — a single-instance, non-Multi-AZ database — was named up front in Note 01 as the deliberate cost of staying within exactly five AWS services, and confirmed in Section 3 above rather than glossed over. Every other requirement was built, tested under simulated failure, and just as importantly, cleanly torn back down.

### Sources
- [Deleting an Auto Scaling group — AWS docs](https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-process-shutdown.html)
- [Delete a VPC — AWS docs](https://docs.aws.amazon.com/vpc/latest/userguide/delete-vpc.html)
- [Release an Elastic IP address — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html#using-instance-addressing-eips-releasing)
