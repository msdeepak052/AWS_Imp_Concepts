# 06 - AWS Global Accelerator - Super Lab Part 1

> Goal: build the regional infrastructure — VPC, subnets, ALB, and Auto Scaling Group — independently in **two Regions**, before Global Accelerator (Note 07) ever enters the picture. This is deliberately identical to a standard single-Region HA setup, repeated twice.

---

## 1. Repeat this section in each Region

Pick two Regions (e.g. `ap-south-1` and `ap-southeast-1`). **Everything in this note is done identically in both**, so the two Regions end up as mirror images of each other.

---

## 2. VPC and subnets

1. **VPC console** → create a VPC (e.g. `10.0.0.0/16`) spanning **at least 2 AZs** within the Region — Global Accelerator adds Region-level HA, but each Region's own ALB/ASG still needs AZ-level HA underneath it (same requirement as any standalone `EC2/LoadBalancer` deployment).
2. Create **2 public subnets** (one per AZ) for the ALB, and **2 private subnets** (one per AZ) for the EC2 instances.
3. Attach an **Internet Gateway**, and a **NAT Gateway** in a public subnet if the private instances need outbound internet access (package installs, etc.).

---

## 3. Security groups

- **ALB security group**: inbound HTTP (80) from `0.0.0.0/0` (public-facing).
- **EC2 security group**: inbound HTTP (80) **only from the ALB's security group** — not from the internet directly, consistent with this repo's `EC2/LoadBalancer/04-LB-Security-Group-Design-HandsOn` pattern.

---

## 4. Launch template and Auto Scaling Group

1. Create a **launch template**: AMI, instance type, the EC2 security group from Section 3, and **user data** that installs/starts a small web server returning a page identifying **this Region** (same idea as Note 04, now scaled across a fleet).
2. Create an **Auto Scaling Group** using that launch template, across the **2 private subnets**, with a small desired/min/max capacity (e.g. 2/2/4) — enough to prove HA within the Region without over-provisioning for a lab.

---

## 5. Application Load Balancer

1. Create an **Application Load Balancer** in the **2 public subnets**, using the ALB security group.
2. Create a **target group** (type: instances), attach the **Auto Scaling Group** to it (so ASG automatically registers/deregisters instances as it scales).
3. Add a **listener** on port 80 forwarding to that target group.
4. Confirm the ALB's **health checks** pass and its target group shows healthy targets before moving on.

---

## 6. Verify each Region independently

Before touching Global Accelerator at all, confirm each Region works **on its own**:

```bash
curl http://<region-A-alb-dns-name>/
curl http://<region-B-alb-dns-name>/
```

Both should return their Region-identifying response, proving each Region's ALB + ASG stack is independently healthy — isolating any later Global Accelerator issue (Note 07-08) from a basic regional infrastructure problem.

---

## 7. Recap

- Built **two independent, mirror-image regional stacks**: VPC (2 AZs) → public/private subnets → ALB (public) → Auto Scaling Group (private).
- Verified each Region's ALB DNS name directly, confirming healthy infrastructure **before** Global Accelerator is introduced — isolating variables for the next parts.
- Next: Note 07 — Super Lab Part 2, creating the Global Accelerator itself and attaching each Region's ALB as an endpoint.

### Sources
- [Application Load Balancers — AWS docs](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html)
- [Amazon EC2 Auto Scaling — AWS docs](https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html)
- [VPCs and subnets — AWS docs](https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html)
