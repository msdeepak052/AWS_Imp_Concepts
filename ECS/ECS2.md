# **Amazon ECS Encryption**

---

## 🔐 What is **ECS Encryption**?

ECS does **not directly manage encryption itself**, but relies on **integrated AWS services like KMS, EBS, and EFS** to provide **encryption at rest** and **encryption in transit**.

ECS encryption focuses on:

1. ✅ **Data at Rest** (volumes, logs, secrets)
2. ✅ **Data in Transit** (network traffic)
3. ✅ **Task-level encryption configs** (via KMS)
4. ✅ **Fargate Ephemeral Storage Encryption**

---

## 💡 Why Encryption Matters in ECS?

| Scenario                           | Why Encryption Helps                  |
| ---------------------------------- | ------------------------------------- |
| Secrets stored in task definitions | Avoid plaintext passwords or tokens   |
| Logs in CloudWatch                 | Prevent log leakage and eavesdropping |
| EBS/EFS volumes attached to tasks  | Protect persistent data at rest       |
| Inter-service communication        | Prevent MITM attacks                  |

---

## 🔒 Types of ECS Encryption

![image](https://github.com/user-attachments/assets/5f5ae4f7-3978-4a78-9db9-484a53ff40f4)


### 1. **Task Storage Encryption (Fargate)**

#### 🔹 What is it?

* When running on **Fargate**, each task gets **ephemeral storage** (up to 200 GiB).
* You can encrypt this storage using a **KMS key**.

#### 🔧 Configuration Parameter:

* **KMS key ARN** during ECS Cluster creation or Task Execution.

#### 🧾 Example:

```json
"ephemeralStorage": {
  "sizeInGiB": 50
},
"encryptionConfiguration": {
  "kmsKey": "arn:aws:kms:ap-south-1:123456789012:key/abc-def-ghi"
}
```

---

### 2. **EBS Volume Encryption (EC2 Launch Type)**

#### 🔹 What is it?

* ECS tasks running on EC2 may use **EBS volumes** (e.g., for mounting persistent data).
* You can encrypt EBS volumes at creation with KMS.

#### 🔧 Configuration:

* Use encrypted AMIs
* Or use `blockDeviceMappings` when launching EC2 via ASG

#### 📌 Example (EC2 UserData):

```bash
aws ec2 create-volume --encrypted --kms-key-id alias/my-key
```

---

### 3. **Secrets Encryption (Parameter Store / Secrets Manager)**

#### 🔹 What is it?

* ECS integrates with **AWS Secrets Manager** or **SSM Parameter Store** to inject secrets securely into containers.
* These secrets are encrypted with **KMS** under the hood.

#### 🔧 Task Definition Example:

```json
"secrets": [
  {
    "name": "DB_PASSWORD",
    "valueFrom": "arn:aws:ssm:ap-south-1:123456789012:parameter/db_password"
  }
]
```

---

### 4. **Fargate Managed Storage Encryption**

When running in Fargate:

* The **container image**, **network traffic**, and **ephemeral storage** are encrypted using **KMS by default**.
* You can override the default KMS key.

#### 🔧 Cluster-level option:

During ECS cluster creation:

> **Encryption → Fargate ephemeral storage KMS key**

---

### 5. **CloudWatch Logs Encryption**

#### 🔹 What is it?

* Logs from ECS containers (via log drivers like awslogs, Fluent Bit, FireLens) go to CloudWatch.
* CloudWatch log groups can be configured to use a **KMS key for encryption at rest**.

#### 🔧 Configuration Example:

```bash
aws logs create-log-group \
  --log-group-name /ecs/my-app \
  --kms-key-id arn:aws:kms:ap-south-1:123456789012:key/my-cloudwatch-key
```

---

# **ECS Console UI during cluster creation** 

Let me explain **each option in detail**, their **purpose**, and how to use them effectively.

---

## 🔐 ECS Cluster Encryption Options (Visible in UI)

---

### 1️⃣ **Managed Storage Encryption**

> **"Choose the default KMS key used by tasks running in this cluster to encrypt managed storage."**

### 🔍 What it means:

* This refers to **persistent storage** used by **Amazon EFS or EBS** volumes **attached to ECS tasks** (when you configure them).
* You can **predefine a KMS key**, so when ECS tasks mount volumes, encryption is handled using this key.

### 💡 When to use:

* If you plan to use **Amazon EFS with ECS Fargate or EC2**, and want to **encrypt EFS at rest** with a **customer-managed KMS key** (instead of AWS default).

### 🔧 Example Use Case:

You run a containerized web app that stores session data or user-uploaded files on **EFS**. This EFS volume is mounted inside the task, and you want that data encrypted using your own KMS key.

---

### 2️⃣ **Fargate Ephemeral Storage Encryption**

> **"Choose the default KMS key used by tasks running in this cluster to encrypt Fargate ephemeral storage."**

### 🔍 What it means:

* Each Fargate task gets ephemeral storage (20 GiB default, up to 200 GiB if configured).
* That **ephemeral disk** is encrypted at rest using **AWS-managed KMS key by default**, but you can choose your **own KMS key**.

### 💡 When to use:

* If you're handling **sensitive data** temporarily inside the container (e.g., logs, processing files).
* If you want **control and audit** over how that encryption is managed using your own KMS key.

---

## 🛠️ How to Use These Options

1. 🔑 **Create your own KMS key**:

   * Go to **KMS Console**
   * Click **Create key**
   * Name it like: `ecs-cluster-storage-key`
   * Set key users (e.g., your IAM role)
   * Create

2. 🧩 **During ECS Cluster Creation**:

   * Under **Encryption → Managed Storage**, choose your custom KMS key.
   * Under **Encryption → Fargate Ephemeral Storage**, choose the same or a different key.

3. ✅ Proceed with **cluster creation** — the chosen keys will apply automatically to any compatible storage used by ECS tasks.

---

## 📌 Summary Table

| Option                        | Encrypts                                 | Default KMS Key Used | When to Customize                                         |
| ----------------------------- | ---------------------------------------- | -------------------- | --------------------------------------------------------- |
| **Managed Storage**           | EFS volumes attached to ECS tasks        | AWS-managed key      | If using EFS for file storage                             |
| **Fargate Ephemeral Storage** | Temporary disk attached to Fargate tasks | AWS-managed key      | If processing sensitive data in-memory or temporary files |

---

## ✅ Best Practices

* Use **customer-managed KMS keys** if:

  * You're in regulated industries (finance, healthcare).
  * You want to control access, rotation, and audit logs.
* Enable **CloudTrail** for KMS to track encryption/decryption activity.
* Combine this with **Secrets Manager** for full encryption coverage in ECS.

---



## 📊 Summary Table

| Encryption Area              | Service Used          | KMS Involved | Config Location              |
| ---------------------------- | --------------------- | ------------ | ---------------------------- |
| Fargate Ephemeral Storage    | Fargate               | ✅ Yes        | Cluster creation or task def |
| EBS volumes (EC2)            | EC2 + EBS             | ✅ Yes        | EC2 ASG config or AMI        |
| Secrets in containers        | SSM / Secrets Manager | ✅ Yes        | Task Definition              |
| Logs to CloudWatch           | CloudWatch Logs       | ✅ Yes        | Log group KMS setting        |
| Inter-service TLS (optional) | NLB/ALB + TLS         | Optional     | Load Balancer Config         |

---

## ✅ Use Cases

| Use Case                  | Encryption Details                                                                                                              |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **Banking App**           | Encrypt secrets using KMS via Secrets Manager. Enable CloudWatch encryption. Use Fargate ephemeral storage with custom KMS key. |
| **Healthcare (HIPAA)**    | Encrypt EBS volumes on EC2. Use Fargate with custom KMS keys. All logs encrypted at rest.                                       |
| **SaaS Application**      | Multi-tenant secrets stored per customer with different KMS keys.                                                               |
| **Dev/Test environments** | Use default KMS key. Rotate keys periodically in non-prod.                                                                      |

---

## 🔐 Best Practices

* ✅ **Use customer-managed KMS keys** for fine-grained access and audit logs.
* ✅ **Rotate keys regularly** using automatic or manual KMS rotation.
* ✅ **Use Secrets Manager** instead of embedding secrets in task definitions.
* ✅ **Enable CloudWatch Logs encryption** for all ECS log groups.
* ✅ **Use TLS (HTTPS)** for service-to-service or client-to-container traffic.

---


