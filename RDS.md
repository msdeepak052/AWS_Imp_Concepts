### 📘 **Relational Database Service (RDS) – Overview**

**AWS RDS (Relational Database Service)** is a **managed service** that makes it easier to **set up, operate, and scale** a relational database in the cloud.

It automates common administrative tasks such as:

* Provisioning hardware
* Database setup
* Patching
* Backups
* Recovery
* Monitoring

---

### ✅ **Key Features of RDS**

* **Multi-AZ Deployment** for high availability
* **Automated Backups & Snapshots**
* **Read Replicas** for scaling read traffic
* **Monitoring with Amazon CloudWatch**
* **VPC Integration** for network isolation
* **Encryption** using AWS KMS

---

### 🛠️ **Supported Database Engines in RDS**

RDS supports 6 popular relational database engines:

| Engine            | Description / Use Case                           |
| ----------------- | ------------------------------------------------ |
| **Amazon Aurora** | AWS-optimized, high-performance MySQL/PostgreSQL |
| **MySQL**         | Widely-used open-source database                 |
| **PostgreSQL**    | Advanced open-source relational DB (extensible)  |
| **MariaDB**       | MySQL-compatible, community-driven               |
| **Oracle**        | Enterprise-grade, licensed database              |
| **SQL Server**    | Microsoft’s commercial DB engine                 |

---

### 🌐 **Real-World Example**

You’re building a **banking application** with 3 tiers: frontend, backend (Java), and database.

* You use **RDS PostgreSQL** as the backend database.
* You enable **Multi-AZ** for high availability.
* You create **read replicas** to handle reporting traffic.
* Backups are scheduled automatically every night.

➡️ You don’t worry about patches, provisioning, or failovers — AWS RDS handles it.

---

### 🔄 **RDS vs. Other AWS Database Services**

| AWS Service            | When to Use It                                        |
| ---------------------- | ----------------------------------------------------- |
| **RDS**                | For traditional SQL workloads needing full control    |
| **Amazon Aurora**      | Need high performance + availability (5x MySQL speed) |
| **Amazon DynamoDB**    | For NoSQL, key-value workloads                        |
| **Amazon Redshift**    | For analytics/data warehousing (OLAP)                 |
| **Amazon ElastiCache** | For in-memory caching                                 |
| **Amazon Neptune**     | For graph databases (social network-type data)        |

---

### 🧠 Summary (for notes)

* **RDS is a fully managed SQL database service** by AWS.
* Supports 6 popular engines like MySQL, PostgreSQL, Oracle, and Aurora.
* **Automates backups, scaling, patching, and replication.**
* **Use RDS when you need traditional relational databases** without managing the infra.
* Aurora is a faster, cloud-native alternative to MySQL/PostgreSQL.
* Use **DynamoDB** for NoSQL, **Redshift** for analytics, and **ElastiCache** for caching layers.

---

---

### 📘 **Introduction to Databases & DBMS**

#### 🔹 What is a **Database**?

A **database** is an organized collection of data that can be easily accessed, managed, and updated.

> Think of it as a digital file cabinet where structured information is stored.

#### 🔹 What is a **DBMS (Database Management System)?**

A **DBMS** is software that interacts with users, applications, and the database itself to capture and analyze data.

It helps in:

* Data storage, retrieval, and update
* Security and access control
* Backup and recovery

---

### 🛠️ **Types of Databases (by structure)**

| Type                       | Description                                  | Example Use Case                        |
| -------------------------- | -------------------------------------------- | --------------------------------------- |
| **Relational (SQL)**       | Stores data in tables with rows and columns  | Banking system, ERP, CRM                |
| **NoSQL (Non-Relational)** | Schema-less, key-value, document, graph etc. | Social media, IoT, gaming               |
| **In-memory**              | Extremely fast, stores data in RAM           | Session store, real-time analytics      |
| **Time-series**            | Optimized for time-stamped data              | IoT sensors, monitoring logs            |
| **Ledger**                 | Immutable, cryptographically verifiable      | Financial transactions, audit logs      |
| **Graph**                  | Represents relationships using nodes/edges   | Social networks, recommendation engines |

---

### 🧰 **AWS Database Services & Types**

| Category             | AWS Service            | Engine/Description                                |
| -------------------- | ---------------------- | ------------------------------------------------- |
| **Relational (SQL)** | **Amazon RDS**         | MySQL, PostgreSQL, Oracle, MariaDB, SQL Server    |
|                      | **Amazon Aurora**      | Cloud-native MySQL/PostgreSQL-compatible          |
| **NoSQL**            | **Amazon DynamoDB**    | Key-value, document-based NoSQL DB                |
| **In-Memory**        | **Amazon ElastiCache** | Redis or Memcached                                |
| **Time-Series**      | **Amazon Timestream**  | Purpose-built for time-series data                |
| **Graph**            | **Amazon Neptune**     | Graph database supporting Gremlin/ SPARQL         |
| **Ledger**           | **Amazon QLDB**        | Immutable, cryptographically verifiable ledger DB |
| **Data Warehouse**   | **Amazon Redshift**    | For analytics, OLAP workloads                     |

---

### 📌 Example for Clarity:

Say you're building a **fitness tracking app**:

* Use **RDS MySQL** to store user profile and login info.
* Use **DynamoDB** to store unstructured workout records and logs.
* Use **Timestream** to store and analyze time-based heart rate or step data.
* Use **ElastiCache Redis** to cache user sessions.
* Use **Redshift** to generate business insights from user activity.

---

### 🧠 Summary (for notes)

* A **DBMS manages the database** and performs operations like querying, storing, and securing data.
* **Databases are categorized** based on data structure: SQL, NoSQL, time-series, graph, etc.
* AWS offers a **broad suite of database services** for each use case:

  * RDS/Aurora → SQL
  * DynamoDB → NoSQL
  * ElastiCache → In-memory
  * Neptune → Graph
  * Timestream → Time-series
  * Redshift → Analytics/Data Warehousing

---


---

## 📘 **What is a Relational Database (RDB) & Relational Database Service (RDS)?**

### 🔹 **Relational Database (RDB)**

A **Relational Database** organizes data into **tables** (rows and columns), where each table is related to others through **keys**.

> Example: In a banking app, you may have a `Users` table and a `Transactions` table linked by `user_id`.

---

### 🔹 **Relational Database Service (RDS)**

**Amazon RDS** is a **fully managed service** for relational databases in AWS. It takes care of:

* Hardware provisioning
* DB installation and setup
* Backups, patching, monitoring
* Replication and scaling

✅ It supports popular relational DB engines: **MySQL, PostgreSQL, MariaDB, Oracle, SQL Server**, and **Aurora**.

---

## ✅ **Common Use Cases for RDS**

| Use Case                             | Description                                     |
| ------------------------------------ | ----------------------------------------------- |
| **Web & Mobile Apps**                | Store user data, sessions, and profiles         |
| **eCommerce Platforms**              | Store products, orders, transactions            |
| **ERP/CRM Systems**                  | Manage employees, customers, inventory, finance |
| **Content Management Systems (CMS)** | Blogs, publishing, media platforms              |
| **Financial Applications**           | Store secure and consistent transactional data  |
| **Healthcare/HR Systems**            | Relational, structured, compliant data storage  |

---

## 🏷️ **Key RDS Terminologies with Explanation & Examples**

| Term                    | Description                                                       | Example                                        |
| ----------------------- | ----------------------------------------------------------------- | ---------------------------------------------- |
| **DB Instance**         | A single RDS database environment (like a virtual machine for DB) | `db.t3.medium` running MySQL 8.0               |
| **DB Engine**           | The type of database (MySQL, PostgreSQL, etc.)                    | Aurora PostgreSQL                              |
| **Multi-AZ Deployment** | High availability setup with standby in another AZ                | Automatic failover in case of outage           |
| **Read Replica**        | Read-only copy of DB for scaling read queries                     | Reporting or analytics queries                 |
| **Storage Type**        | The storage backend used (GP2, GP3, IO1)                          | General Purpose SSD (gp3)                      |
| **Parameter Group**     | Configuration settings for the DB engine                          | Turn on slow query logging                     |
| **Option Group**        | Additional features for engines like Oracle/SQL Server            | Enable Oracle TDE                              |
| **Subnet Group**        | Set of subnets in VPC where DB can be launched                    | Public vs Private subnet                       |
| **Security Group**      | Acts as a firewall to control inbound/outbound DB access          | Allow app server IP on port 3306               |
| **Snapshot**            | Backup of the entire DB instance at a point in time               | Daily backups at midnight                      |
| **Endpoint**            | Hostname used by app to connect to the database                   | `mydb.abcdefg123.ap-south-1.rds.amazonaws.com` |

---

## 🧠 Summary (For Your Notes)

* **RDS** is a **managed service** to run relational databases like MySQL, PostgreSQL, and Aurora.
* It’s used in **web apps, financial systems, CMS, ERP**, and more.
* Key concepts include: **DB Instance, Engine, Multi-AZ, Read Replica, Snapshots, Security Group, Parameter Group**.
* AWS **abstracts away infrastructure management** so you can focus on the application layer.

---

✅ **Real Example Scenario**

> You're deploying a CRM application for a company:
>
> * You choose **RDS PostgreSQL**.
> * Configure it as **Multi-AZ** for high availability.
> * Add a **Read Replica** for analytics.
> * Enable **automated backups** with a 7-day retention period.
> * Use **CloudWatch** for monitoring DB performance.

---


---

## 📘 **Core Terminologies in Relational Databases (RDBMS)**

These concepts apply whether you're using MySQL, PostgreSQL, Oracle, or any relational system — including RDS.

---

### 🧱 **1. Table**

* A **table** is a collection of related data in rows and columns.
* Each table represents a single entity (like customers, orders, etc.).

📌 *Example:*

```sql
CREATE TABLE Customers (
  id INT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100)
);
```

---

### 🔑 **2. Primary Key**

* A **primary key** uniquely identifies each row in a table.
* It must be **unique** and **not null**.

📌 *Example:* `id` in the `Customers` table.

---

### 🔗 **3. Foreign Key**

* A **foreign key** links one table to another.
* It enforces **referential integrity** between related tables.

📌 *Example:* `customer_id` in `Orders` referencing `Customers(id)`

---

### 📚 **4. Schema**

* A **schema** is a logical container for database objects like tables, views, and procedures.
* Think of it as a **namespace** or folder.

📌 *Example:* `public.customers` in PostgreSQL

---

### 🧾 **5. Row (Record)**

* A **row** is a single entry in a table.
* It contains data for all columns defined.

📌 *Example:* One customer: `(1, 'Deepak', 'deepak@email.com')`

---

### 📐 **6. Column (Field)**

* A **column** defines a data type and name for an attribute.
* Columns make up the structure of the table.

📌 *Example:* `name VARCHAR(100)` in the Customers table.

---

### 📋 **7. SQL (Structured Query Language)**

* Language used to **interact with relational databases**.
* Includes commands like:

  * `SELECT` (read data)
  * `INSERT` (add data)
  * `UPDATE` (modify)
  * `DELETE` (remove)

📌 *Example:*

```sql
SELECT * FROM Customers WHERE id = 1;
```

---

### 🔄 **8. Normalization**

* Process of **organizing data** to reduce redundancy and improve integrity.
* Involves splitting data into multiple related tables.

📌 *Example:* Instead of storing customer info in every order row, use a separate `Customers` table.

---

### 🧠 **9. Index**

* An **index** speeds up search queries on one or more columns.
* Acts like a book index — you find data faster.

📌 *Example:* Index on `email` for fast user lookup.

---

### 🔍 **10. View**

* A **view** is a **virtual table** created by a query.
* It doesn't store data but presents data in a structured form.

📌 *Example:* A view showing active customers:

```sql
CREATE VIEW ActiveCustomers AS
SELECT * FROM Customers WHERE is_active = true;
```

---

### 🔒 **11. Transaction**

* A **transaction** is a group of SQL operations treated as a single unit.
* Follows **ACID** properties: Atomicity, Consistency, Isolation, Durability.

📌 *Example:* Transferring money between accounts (debit + credit)

---

### 🧾 **12. Constraint**

* Rules applied to columns or tables to enforce data integrity.
* Types: `NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`, `PRIMARY KEY`, `FOREIGN KEY`

📌 *Example:* `email UNIQUE` ensures no duplicates.

---

## 🧠 Summary for Notes

| Term          | Description                             |
| ------------- | --------------------------------------- |
| Table         | Structure to store data in rows/columns |
| Row           | A record in a table                     |
| Column        | A field/attribute in the table          |
| Primary Key   | Unique identifier for rows              |
| Foreign Key   | Link between two related tables         |
| SQL           | Language to manage DB                   |
| Schema        | Logical group of DB objects             |
| Index         | Speed up data lookup                    |
| View          | Virtual table from a SELECT query       |
| Transaction   | Unit of work with ACID properties       |
| Constraint    | Rule for data integrity                 |
| Normalization | Process to reduce redundancy            |

---


---

## 🔍 **Why AWS RDS?**

**Amazon RDS** is used because it offers a **fully managed, scalable, secure, and cost-effective solution** for running relational databases in the cloud — without managing the underlying infrastructure.

---

### ✅ **Key Reasons to Use AWS RDS**

---

### 🔧 1. **Fully Managed Service**

AWS handles:

* OS-level updates & patching
* Database installation & upgrades
* Backups, snapshots, & maintenance
* Failover and recovery

📌 *Benefit:* Focus on application logic instead of DB management.

---

### ☁️ 2. **Easy to Deploy & Scale**

* Launch a production-grade database in **minutes** via console/CLI/CloudFormation/Terraform
* Scale **compute and storage** separately (Vertical and Storage Auto Scaling)

📌 *Use Case:* Auto-scale DB storage for an eCommerce site during sales season.

---

### 🛡️ 3. **Built-in High Availability**

* Use **Multi-AZ deployment** for automatic failover
* Data is replicated across AZs
* **99.95% SLA** for availability

📌 *Use Case:* Banking app with zero tolerance for downtime.

---

### 📈 4. **Read Scalability via Read Replicas**

* Create **Read Replicas** to distribute read traffic and improve performance
* Supports MySQL, PostgreSQL, MariaDB, Aurora

📌 *Use Case:* Reporting dashboard pulls data from read replica, not primary DB.

---

### 🔐 5. **Security & Compliance**

* **Encryption at rest** using AWS KMS
* **Encryption in transit** via SSL/TLS
* Integration with **IAM**, **VPC**, **Security Groups**
* HIPAA, PCI-DSS, SOC compliance

📌 *Use Case:* A healthcare app requiring encrypted patient data.

---

### 💸 6. **Cost Optimization**

* **Pay-as-you-go** pricing
* Reserved Instances for long-term savings (up to 69%)
* Stop/start instances to save costs in dev/test environments

---

### 📊 7. **Monitoring & Alerts**

* Integrated with **Amazon CloudWatch** for metrics and alarms
* View CPU, disk I/O, query latency, and more

📌 *Use Case:* Set up alarms for high CPU usage or low free storage.

---

### 🔁 8. **Automated Backups & Snapshots**

* Daily automatic backups with **point-in-time recovery**
* Manual DB snapshots retained as long as needed

📌 *Use Case:* Recover a DB to state 2 days ago after a faulty data import.

---

## 🧠 Summary for Notes

| Benefit               | Description                             |
| --------------------- | --------------------------------------- |
| Fully Managed         | No server management, patching, backups |
| Highly Available      | Multi-AZ failover support               |
| Scalable              | Easy to resize compute/storage          |
| Secure                | Encryption, VPC, IAM integration        |
| Cost-Effective        | Pay-per-use + reserved pricing options  |
| Performance-Optimized | Read replicas, Aurora auto-scaling      |
| Easy Monitoring       | Built-in metrics via CloudWatch         |
| Reliable Backups      | Auto backup + snapshots + PITR          |

---

✅ **In Short:**
**AWS RDS = “Run relational DBs without worrying about infrastructure, while meeting performance, availability, and security requirements.”**

---

---

## 🏗️ **1. Explanation of All 3 Deployment Models**

---

### 🖥️ **A. On-Premises Database**

* You **install and manage the DB** on your own physical servers (in your data center).
* You handle **everything**: power, network, hardware, OS, patches, backups, scaling.

📌 *Use Case:* Organizations with strict data control, compliance needs, or legacy systems.

---

### ☁️ **B. Database on Amazon EC2**

* You launch a **virtual machine (EC2)** and install the DB engine (like MySQL, PostgreSQL) yourself.
* You control the OS, DB engine, backups, scaling, patching, and failover.
* **More flexibility**, but **more management** too.

📌 *Use Case:* Custom DB configurations not supported by RDS or need OS-level control.

---

### 🛠️ **C. Database on Amazon RDS (Managed)**

* You **just choose the DB engine**, version, size, and backup settings — AWS handles the rest.
* No OS-level access, but you get built-in HA, backups, read replicas, monitoring, and security.

📌 *Use Case:* Modern, scalable, production-ready applications with minimal admin effort.

---

## 📊 **2. Comparison Table**

| Feature/Factor         | On-Premises                   | EC2 Hosted DB                    | Amazon RDS (Managed)                |
| ---------------------- | ----------------------------- | -------------------------------- | ----------------------------------- |
| **Setup Time**         | Weeks (hardware, software)    | Hours (launch EC2, install DB)   | Minutes (console/CLI setup)         |
| **Control**            | Full (hardware, OS, DB)       | High (OS + DB control)           | Limited (only DB settings)          |
| **Maintenance**        | Manual (patches, backups)     | Manual (you manage it all)       | Automated by AWS                    |
| **Scaling**            | Hardware upgrade (slow)       | Manual (resize EC2/volume)       | Easy (Auto storage scaling, Aurora) |
| **High Availability**  | Custom, complex setup         | DIY with scripts, Load Balancers | Built-in (Multi-AZ, Aurora HA)      |
| **Monitoring**         | Custom tools                  | Use CloudWatch manually          | Integrated with CloudWatch          |
| **Backup/Restore**     | Manual, script-based          | Manual snapshots/scripts         | Auto backups, point-in-time restore |
| **Cost**               | High CapEx (servers, cooling) | Pay for EC2, EBS, ops time       | Pay-as-you-go, cost-efficient       |
| **Compliance & Audit** | Custom controls               | Full control, but manual         | AWS compliance (PCI, HIPAA, etc.)   |
| **Use Case Fit**       | Legacy, strict control needed | Custom setup, migration/testing  | Modern apps, fast delivery, DevOps  |

---

## ✅ **3. Which Is Better for You?**

Since you’re working on:

* **DevOps**
* **CI/CD**
* **Kubernetes**
* **Cloud-native projects**
* Building **real-time apps like banking**

👉 **Amazon RDS is your best fit**, because:

* You don’t want to manage OS or patches.
* You need **auto backups**, **HA**, and **read replicas** fast.
* It integrates well with **Jenkins, EKS, Terraform, CloudWatch**.
* It follows DevOps principles: **automation, speed, scalability, low ops burden**.

However:

| Use Case                        | Best Option           |
| ------------------------------- | --------------------- |
| Learning & practicing DB tuning | EC2 (for control)     |
| Legacy systems, no internet     | On-Prem               |
| Modern production workloads     | **RDS (Best)**        |
| Custom engine/OS-level tuning   | EC2                   |
| Compliance with less admin load | RDS (HIPAA, PCI etc.) |

---

## 🧠 Summary for Notes

* **On-Prem** = Full control, full responsibility. Expensive, slow to scale.
* **EC2** = Cloud VM with full OS & DB control. Flexible but manual work.
* **RDS** = Managed, fast, reliable, scalable, and best for cloud-native work.

🎯 **RDS is best for modern apps, DevOps, CI/CD, and Kubernetes deployments.**

---

---

## 🧪 **RDS Lab: Launching a MySQL DB in AWS Console**

We’ll create a **MySQL DB instance** in **Amazon RDS** using the **free tier**.

---

### 🔧 **Pre-Requisites**

* AWS account (free tier eligible)
* A default **VPC** or create a new one
* Basic IAM access with **RDS, VPC, and EC2 permissions**

---

## ✅ **Step-by-Step Instructions**

---

### 🔹 **Step 1: Go to Amazon RDS Console**

* Navigate to: [https://console.aws.amazon.com/rds](https://console.aws.amazon.com/rds)
* Click **"Create database"**

---

### 🔹 **Step 2: Choose a Database Creation Method**

* Select: **Standard Create**

![image](https://github.com/user-attachments/assets/b66c3b6b-adc8-49a8-9da3-af86ec65c0eb)

![image](https://github.com/user-attachments/assets/20c8e610-235e-4c92-a2d0-800ac9c225cd)


---

### 🔹 **Step 3: Select Engine**

* Engine type: ✅ **MySQL**
* Edition: MySQL 8.x
* Templates: ✅ **Free tier** (for lab)
![image](https://github.com/user-attachments/assets/b76fff76-b881-49d7-9fe0-69d158277939)

---

### 🔹 **Step 4: Configure Settings**

* DB instance identifier: `deepak-rds-lab`
* Master username: `admin`
* Master password: `StrongPassword123!`
* Confirm password

![image](https://github.com/user-attachments/assets/de789658-ac42-45ec-9b26-88d343fa5320)

---

### 🔹 **Step 5: DB Instance Size**

* DB instance class: `db.t3.micro` ✅ *(Free Tier)*
* Storage: General Purpose (gp2)
* Allocated storage: 20 GiB (default)

![image](https://github.com/user-attachments/assets/502473a1-485e-4d90-8754-8ee1b8f40bff)

![image](https://github.com/user-attachments/assets/8b702a3f-a24d-4e66-9e60-08271b1a1823)

![image](https://github.com/user-attachments/assets/b10bba65-2bc1-41ff-bfaf-10abf9f7a67e)


**Uncheck** “Enable storage autoscaling” (optional for lab)

---

### 🔹 **Step 6: Connectivity**

* Virtual Private Cloud (VPC): Choose **default** or your custom VPC
* Subnet group: default
* Public access: ✅ **Yes** (for lab/demo; not for production)
* VPC security group: Create new OR select existing

  * Allow port `3306` (MySQL) from your IP
![image](https://github.com/user-attachments/assets/046e3d1a-84b7-4400-bd47-803fe0af8c02)

---

### 🔹 **Step 7: Additional Configuration**

* DB name: `demodb`
* DB port: `3306`
* Leave default for rest (log exports, backups, monitoring, etc.)

---

### 🔹 **Step 8: Create Database**

* Click **"Create database"**
* Wait 5–10 mins until status becomes **"Available"**
![image](https://github.com/user-attachments/assets/0e0736aa-7b98-4f6f-a54f-4705d5933bd2)

![image](https://github.com/user-attachments/assets/78b8a80a-78b5-47d2-95ac-5b3c36da23a5)


---

## 🔍 **Step 9: Connect to RDS DB**

### Option A: Using MySQL Workbench

* Host: `<your-RDS-endpoint>` (from Console)
* Port: `3306`
* Username: `admin`
* Password: `StrongPassword123!`

![image](https://github.com/user-attachments/assets/a83bf579-3e9e-4b66-a03f-340e5f7da46a)

![image](https://github.com/user-attachments/assets/12299d8c-8dc2-4405-82b9-bbf44f0dd867)

![image](https://github.com/user-attachments/assets/04be15c1-950b-447a-ab3f-d49a091820d9)

![image](https://github.com/user-attachments/assets/8d3729f7-2acd-4f10-8bd7-8d4c46bff9d3)



### Option B: Using EC2 Instance (secure)

1. Launch a **t2.micro EC2 Linux** in same VPC
2. SSH into it and install MySQL client:

   ```bash
   sudo yum install mysql -y
   ```
3. Connect:

   ```bash
   mysql -h <RDS-endpoint> -u admin -p
   ```

---

## ✅ **Step 10: Test SQL Query**

![image](https://github.com/user-attachments/assets/37efa4c7-85bc-4c5d-8845-cf943a05eb19)

![image](https://github.com/user-attachments/assets/a056de08-10f9-482a-8d0d-a78c303c5904)

![image](https://github.com/user-attachments/assets/f6790768-5801-4fcf-ac73-1aa90f8fce31)


---

## 🛠️ **1. Create a Database in MySQL**

```sql
CREATE DATABASE deepak_db;
```

> ✅ Use underscores (`_`) instead of hyphens (`-`) in DB names to avoid quoting issues.

---

## 📌 **2. Select the Database to Use**

Before creating tables or inserting data, select the DB:

```sql
USE deepak_db;
```

> ✅ This makes `deepak_db` the **active/default database** for the current session.

---

## 💡 **3. Do I Need to Mention the DB Name Every Time?**

### ❌ **No — If you've already run:**

```sql
USE deepak_db;
```

Then this is valid:

```sql
CREATE TABLE employee (
  id INT PRIMARY KEY,
  name VARCHAR(100)
);
```

### ✅ **Yes — If you didn’t use `USE`**

You must fully qualify the table name like this:

```sql
CREATE TABLE deepak_db.employee (
  id INT PRIMARY KEY,
  name VARCHAR(100)
);
```

---

## 🧪 Example: Full Setup

```sql
-- Create database
CREATE DATABASE deepak_db;

-- Use database
USE deepak_db;

-- Create table
CREATE TABLE employee (
  id INT PRIMARY KEY,
  name VARCHAR(100)
);

-- Insert data
INSERT INTO employee VALUES (1, 'Deepak');

-- Query data
SELECT * FROM employee;
```

---


![image](https://github.com/user-attachments/assets/1d0e3f89-dd97-44cc-bf98-37a736fe828f)

![image](https://github.com/user-attachments/assets/f4af01e7-1423-4d59-87dd-8e0771db2075)


---

## 🧹 **Optional: Clean-Up**

* Go to **RDS > Databases**
* Select your DB → **Actions > Delete**
* Choose option to delete final snapshot (for labs)

![image](https://github.com/user-attachments/assets/e5f07ba9-67c0-4fa5-8d1d-696d7066c2ee)


---

## 🧠 Summary for Notes

| Task          | Step                           |
| ------------- | ------------------------------ |
| Engine        | MySQL 8.0                      |
| Instance type | db.t3.micro (Free tier)        |
| VPC           | Default or custom              |
| Public access | Yes (for lab)                  |
| Connection    | Workbench / EC2 + MySQL Client |
| Cleanup       | RDS Console → Delete DB        |

---


## 🧪 **Lab: EC2 to RDS MySQL Connection – Full Steps via AWS Console**

---

### ✅ **Goal**

* Create a **MySQL RDS instance**
* Launch an **EC2 instance**
* **Connect to the RDS** from EC2 using MySQL client

---

## 🔧 **Step-by-Step Instructions**

---

### 🔹 **Step 1: Create RDS MySQL Instance**

1. Go to **Amazon RDS Console** → Click **Create database**
2. Choose:

   * Creation method: ✅ *Standard create*
   * Engine: ✅ *MySQL*
   * Version: Default or latest 8.x
   * Template: ✅ *Free tier*
3. Settings:

   * DB instance identifier: `deepak-rds-mysql`
   * Username: `admin`
   * Password: `StrongPassword123!`
4. DB instance size:

   * Instance class: `db.t3.micro`
   * Storage: General Purpose (20 GiB)
5. Connectivity:

   * VPC: Select default or custom
   * Public access: ❌ *No*
   * VPC Security Group: **Create new or choose existing**, allow **port 3306**
6. DB name: `deepak_db` (optional)
7. Click **Create database**
8. Wait for **status = available** and note the **endpoint** (e.g., `deepak-rds-mysql.abcxyz.rds.amazonaws.com`)

---

### 🔹 **Step 2: Create EC2 Instance (Linux)**

1. Go to **EC2 Console** → Launch Instance
2. Name: `deepak-ec2-mysql-client`
3. AMI: ✅ *Amazon Linux 2*
4. Instance type: `t2.micro`
5. Key pair: Select or create new
6. Network settings:

   * VPC: Same as RDS
   * Subnet: Choose one in same AZ (optional)
   * Security Group:

     * Allow SSH (port 22)
     * Allow **outbound access** to **RDS port 3306**
7. Launch instance
8. Connect to instance:

   ```bash
   ssh -i "your-key.pem" ec2-user@<EC2-Public-IP>
   ```

---

### 🔹 **Step 3: Install MySQL Client on EC2**

```bash
sudo yum update -y
sudo yum install mysql -y
# if not working we can install using mariadb as mariadb and mysql are almost same
sudo dnf install mariadb105
```

---

### 🔹 **Step 4: Modify RDS Security Group to Allow EC2 Access**

1. Go to **EC2 Console** → Instances → Note the **private IP** of your EC2
2. Go to **RDS Console** → Your DB → Find its **Security Group**
3. Edit **Inbound Rules**:

   * Type: MySQL/Aurora
   * Port: 3306
   * Source: ✅ *EC2's Security Group* OR *EC2’s Private IP/32*

✅ This allows EC2 to talk to the RDS.

---

### 🔹 **Step 5: Connect to RDS from EC2**

1. Run:

   ```bash
   mysql -h <RDS-ENDPOINT> -u admin -p
   ```

   * Enter password: `StrongPassword123!`

2. Once connected:

   ```sql
   SHOW DATABASES;

   CREATE DATABASE deepak_db;
   USE deepak_db;

   CREATE TABLE users (
     id INT PRIMARY KEY,
     name VARCHAR(100)
   );

   INSERT INTO users VALUES (1, 'Deepak');
   SELECT * FROM users;
   ```

✅ You’re now connected from EC2 to RDS securely using internal networking.

![image](https://github.com/user-attachments/assets/d55aebbd-8fc2-4a58-86a7-13818b60a6f1)

---

## 🧹 **Clean Up (Optional)**

* Terminate EC2 instance
* Delete RDS instance (disable final snapshot if not needed)

---

## 🧠 Summary for Notes

| Component          | Value                                            |
| ------------------ | ------------------------------------------------ |
| EC2 Role           | MySQL Client                                     |
| RDS Role           | MySQL Server                                     |
| Secure Access      | RDS Security Group allows EC2 IP/SG on port 3306 |
| Connection Command | `mysql -h <RDS-ENDPOINT> -u admin -p`            |

---




