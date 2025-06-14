# Elastic Load Balancer (ELB) and Application Load Balancer (ALB) on AWS

## What is Elastic Load Balancer (ELB)?

Elastic Load Balancer (ELB) is an AWS service that automatically distributes incoming application traffic across multiple targets, such as Amazon EC2 instances, containers, and IP addresses. ELB helps improve the availability and fault tolerance of your applications.

### Types of ELB:
1. **Classic Load Balancer (CLB)** - The original offering (now legacy)
2. **Application Load Balancer (ALB)** - Operates at the application layer (Layer 7)
3. **Network Load Balancer (NLB)** - Operates at the transport layer (Layer 4)

## Application Load Balancer (ALB)

ALB is best suited for load balancing of HTTP and HTTPS traffic and provides advanced request routing targeted at delivery of modern application architectures, including microservices and containers.

### Key Features of ALB:
- Operates at Layer 7 (application layer)
- Supports path-based and host-based routing
- Supports containerized applications
- Supports WebSockets and HTTP/2
- Integrates with AWS WAF for web application firewall capabilities
- Supports redirects and fixed responses

## Path-Based and URL-Based Routing

ALB allows you to route requests to different target groups based on:
- **Path-based routing**: Routes based on the URL path (e.g., `/api/*` to one group, `/images/*` to another)
- **Host-based routing**: Routes based on host headers (e.g., `api.example.com` to one group, `web.example.com` to another)

## Steps to Create an ALB with Path-Based Routing

### Prerequisites:
- At least two EC2 instances in different target groups
- Security groups configured to allow HTTP/HTTPS traffic

### Step-by-Step Guide:

#### 1. Create Target Groups
1. Open the Amazon EC2 console
2. In the navigation pane, under "Load Balancing," choose "Target Groups"
3. Choose "Create target group"
4. For "Target type," select "Instances"
5. Enter a name for the target group (e.g., `web-servers`)
6. Set protocol and port (HTTP, 80)
7. Configure health checks as needed
8. Click "Next" and register your EC2 instances
9. Repeat to create another target group (e.g., `api-servers`)

#### 2. Create the Application Load Balancer
1. In the EC2 console, under "Load Balancing," choose "Load Balancers"
2. Click "Create Load Balancer"
3. Select "Application Load Balancer"
4. Configure basic settings:
   - Name: `my-alb`
   - Scheme: internet-facing or internal
   - IP address type: ipv4
5. Under "Network mapping," select your VPC and availability zones
6. Under "Security groups," select a security group that allows HTTP/HTTPS traffic
7. Under "Listeners and routing," add a listener (HTTP, 80)
8. For "Default action," select one of your target groups (e.g., `web-servers`)
9. Click "Create load balancer"

#### 3. Configure Path-Based Routing Rules
1. After the ALB is created, select it and go to the "Listeners" tab
2. Select the listener (HTTP:80) and click "View/edit rules"
3. Click the "+" icon to add a new rule
4. Click "Insert Rule" to add a condition
5. For condition, choose "Path" and enter `/api/*`
6. For action, choose "Forward to" and select your `api-servers` target group
7. Click the checkmark to save the rule
8. The default action will handle all other paths (forward to `web-servers`)

#### 4. Configure Host-Based Routing (Optional)
1. In the same rules editor, click "Add condition"
2. Choose "Host" and enter your domain (e.g., `api.example.com`)
3. Set the action to forward to your `api-servers` target group
4. Add another rule for `www.example.com` to forward to `web-servers`

#### 5. Test Your Configuration
1. Note the DNS name of your ALB (found in the ALB description)
2. Access the following URLs:
   - `http://<ALB-DNS>/` → should route to web-servers
   - `http://<ALB-DNS>/api/` → should route to api-servers
   - If configured, `http://api.example.com` → should route to api-servers

## Additional Considerations

1. **HTTPS Configuration**:
   - You can add an HTTPS listener (port 443)
   - Need an SSL certificate (can use ACM to provision one)
   - Configure security policies for SSL negotiation

2. **Auto Scaling Integration**:
   - You can attach your ALB to Auto Scaling groups
   - This allows automatic scaling based on traffic

3. **Access Logs**:
   - Enable access logs to track requests
   - Logs are stored in S3

4. **Monitoring**:
   - Use CloudWatch to monitor ALB metrics
   - Set up alarms for unusual traffic patterns


---

## 🔶 **Elastic Load Balancer (ELB) - Overview**

**Elastic Load Balancer (ELB)** is a service from AWS that **automatically distributes incoming application traffic across multiple targets** (like EC2 instances, containers, IPs) in one or more Availability Zones.

It ensures:

* **High availability**
* **Fault tolerance**
* **Scalability**
* **Security (integrates with ACM, SG, IAM)**

---

### ✅ Types of ELB in AWS:

| Type                                | Purpose                        | Layer                          | Use Case                      |
| ----------------------------------- | ------------------------------ | ------------------------------ | ----------------------------- |
| **ALB (Application Load Balancer)** | For HTTP/HTTPS traffic         | Layer 7                        | Web apps, microservices       |
| **NLB (Network Load Balancer)**     | For TCP/UDP/ TLS               | Layer 4                        | High performance, low latency |
| **CLB (Classic Load Balancer)**     | Legacy applications            | Layer 4 & 7                    | Not recommended for new apps  |
| **GWLB (Gateway Load Balancer)**    | Third-party virtual appliances | Transparent traffic inspection | Security appliances           |

---

## 🔷 **Application Load Balancer (ALB)**

**ALB** operates at **Layer 7 (HTTP/HTTPS)** and allows:

* URL/path-based routing
* Host-based routing
* WebSocket support
* Redirects and fixed responses
* Routing to microservices

### 🔁 Example Use Case:

| URL                           | Routing Target              |
| ----------------------------- | --------------------------- |
| `devopswithdeepak.co.in/app1` | Target Group A              |
| `devopswithdeepak.co.in/app2` | Target Group B              |
| `app2.devopswithdeepak.co.in` | Target Group B (host-based) |

---

## 🔀 Path-Based Routing vs Host-Based Routing

| Type                   | Description                                | Example                                |
| ---------------------- | ------------------------------------------ | -------------------------------------- |
| **Path-based routing** | Route based on the **path in URL**         | `/app1`, `/app2`                       |
| **Host-based routing** | Route based on the **hostname** in request | `app1.example.com`, `app2.example.com` |

---

## 🛠️ Steps to Create an Application Load Balancer in AWS Console

---

### ✅ **Step 1: Open ELB Console**

* Go to **EC2 Dashboard**
* Click on **Load Balancers** in the left panel
* Click **Create Load Balancer**
* Select **Application Load Balancer**

---

### ✅ **Step 2: Configure Load Balancer**

* **Name**: `my-app-alb`
* **Scheme**: `Internet-facing` or `Internal`
* **IP address type**: `IPv4`
* **Listeners**: `HTTP:80` (add HTTPS:443 if SSL required)
* **VPC**: Choose your VPC
* **Availability Zones**: Select at least 2 AZs and public subnets

Click **Next: Configure Security Settings**

---

### ✅ **Step 3: Configure Security Group**

* Create or choose a **Security Group**
* Allow **HTTP (80)** and/or **HTTPS (443)** inbound traffic

Click **Next: Configure Routing**

---

### ✅ **Step 4: Create Target Groups (for each app)**

* **Target group name**: `tg-app1`, `tg-app2`
* **Target type**: Instance / IP / Lambda
* **Protocol**: HTTP
* **Port**: 80
* **Health check path**: `/`

➡️ Click **Create target group**, then repeat for each app.

➡️ After creating, go back to **ALB configuration** and **select the default target group** for now.

Click **Next: Register Targets**

---

### ✅ **Step 5: Register Targets**

* Select EC2 instances to register to each target group (or skip for now)

Click **Next: Review** → Click **Create**

---

## ➕ Add Path-Based or Host-Based Routing Rules

After ALB is created:

### ✅ Step 6: Add Listener Rules (for Path/Host Routing)

1. Go to **Load Balancers**
2. Select your ALB → Go to **Listeners**
3. Click **View/edit rules** on port 80
4. Click the **"+" icon** to add new rule

---

### 🔁 **Path-Based Routing (URL-based)**

**Condition**:

* IF **Path** is `/app1`

**Action**:

* THEN **Forward to target group** `tg-app1`

Repeat:

* IF Path is `/app2` → forward to `tg-app2`

---

### 🌐 **Host-Based Routing**

**Condition**:

* IF **Host** is `app1.devopswithdeepak.co.in`

**Action**:

* THEN forward to target group `tg-app1`

Repeat:

* Host: `app2.devopswithdeepak.co.in` → `tg-app2`

Click **Save**

---

### ✅ Step 7: Test the Setup

* Point your domain (`devopswithdeepak.co.in`) to **ALB DNS name** using Route 53 A Record (alias)
* Access:

  * `http://devopswithdeepak.co.in/app1`
  * `http://devopswithdeepak.co.in/app2`

OR

* `http://app1.devopswithdeepak.co.in`
* `http://app2.devopswithdeepak.co.in`

---

![image](https://github.com/user-attachments/assets/c4818507-94a8-4e39-a652-801872c2b80f)



## Terraform Configuration for 3 EC2 Instances in Different AZs with Apache HTTPD

#### Terraform configuration to create 3 t2.micro instances in different availability zones in ap-south-1 region, install Apache HTTPD, and configure the web content as specified:


## 1. `main.tf`

```hcl
provider "aws" {
  region = "ap-south-1"
}

locals {
  az_instance_mapping = {
    "ap-south-1a" = "t2.micro"
    "ap-south-1b" = "t2.micro"
    "ap-south-1c" = "t3.micro"
  }
}

resource "aws_instance" "httpd_servers" {
  count             = 3
  ami               = "ami-0b09627181c8d5778" # Amazon Linux 2 in ap-south-1
  instance_type          = local.az_instance_mapping[element(["ap-south-1a", "ap-south-1b", "ap-south-1c"], count.index)]
  key_name          = "newawss"
  availability_zone = element(["ap-south-1a", "ap-south-1b", "ap-south-1c"], count.index)
  user_data = templatefile("${path.module}/user_data_server${count.index + 1}.sh", {
    server_name = "Server ${count.index + 1}"
  })

  tags = {
    Name = "httpd-server-${count.index + 1}"
  }
}

output "server_details" {
  description = "Details of the HTTPD servers"
  value = [for i, instance in aws_instance.httpd_servers : {
    "server-${i + 1}" = {
      public_dns = instance.public_dns,
      public_ip  = instance.public_ip,
      private_ip = instance.private_ip,
      az         = instance.availability_zone,
      url_root   = i == 0 ? "http://${instance.public_dns}/" : null,
      url_second = i == 1 ? "http://${instance.public_dns}/second/" : null,
      url_third  = i == 2 ? "http://${instance.public_dns}/third/" : null
    }
  }]
}
```

## 2. `user_data_server1.sh`

```bash
#!/bin/bash
set -ex

# Update and install HTTPD
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd

# Get instance metadata
# Public IP (via external service)
PUBLIC_IP=$(curl -s ifconfig.me)

# Private IP (first IP from hostname -I)
PRIVATE_IP=$(hostname -I | awk '{print $1}')

# Hostname
HOSTNAME=$(hostname)

TOKEN=$(curl -sX PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")

AZ=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone \
  -H "X-aws-ec2-metadata-token: $TOKEN")

# Create index.html
cat > /var/www/html/index.html <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>${server_name}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f8ff; }
        .container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); max-width: 600px; margin: 0 auto; }
        h1 { color: #2e8b57; text-align: center; }
        .info { margin: 15px 0; padding: 10px; background: #f8f9fa; border-left: 4px solid #2e8b57; }
        .highlight { font-weight: bold; color: #2e8b57; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to <span class="highlight">${server_name}</span></h1>
        <div class="info"><strong>Public IP:</strong> $PUBLIC_IP</div>
        <div class="info"><strong>Private IP:</strong> $PRIVATE_IP</div>
        <div class="info"><strong>Hostname:</strong> $HOSTNAME</div>
        <div class="info"><strong>Availability Zone:</strong> $AZ</div>
        <div class="info"><strong>Context Path:</strong> Root (/)</div>
    </div>
</body>
</html>
EOF

# Set permissions
chmod 644 /var/www/html/index.html
```

## 3. `user_data_server2.sh`

```bash
#!/bin/bash
set -ex

# Update and install HTTPD
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd

# Create directory for second context
mkdir -p /var/www/html/second

# Get instance metadata
# Public IP (via external service)
PUBLIC_IP=$(curl -s ifconfig.me)

# Private IP (first IP from hostname -I)
PRIVATE_IP=$(hostname -I | awk '{print $1}')

# Hostname
HOSTNAME=$(hostname)

TOKEN=$(curl -sX PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")

AZ=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone \
  -H "X-aws-ec2-metadata-token: $TOKEN")

# Create index.html
cat > /var/www/html/second/index.html <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>${server_name}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #fff0f5; }
        .container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); max-width: 600px; margin: 0 auto; }
        h1 { color: #8b2e65; text-align: center; }
        .info { margin: 15px 0; padding: 10px; background: #f8f9fa; border-left: 4px solid #8b2e65; }
        .highlight { font-weight: bold; color: #8b2e65; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to <span class="highlight">${server_name}</span></h1>
        <div class="info"><strong>Public IP:</strong> $PUBLIC_IP</div>
        <div class="info"><strong>Private IP:</strong> $PRIVATE_IP</div>
        <div class="info"><strong>Hostname:</strong> $HOSTNAME</div>
        <div class="info"><strong>Availability Zone:</strong> $AZ</div>
        <div class="info"><strong>Context Path:</strong> /second/</div>
    </div>
</body>
</html>
EOF

# Set permissions
chmod 644 /var/www/html/second/index.html
```

## 4. `user_data_server3.sh`

```bash
#!/bin/bash
set -ex

# Update and install HTTPD
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd

# Create directory for third context
mkdir -p /var/www/html/third

# Get instance metadata
# Public IP (via external service)
PUBLIC_IP=$(curl -s ifconfig.me)

# Private IP (first IP from hostname -I)
PRIVATE_IP=$(hostname -I | awk '{print $1}')

# Hostname
HOSTNAME=$(hostname)

TOKEN=$(curl -sX PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")

AZ=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone \
  -H "X-aws-ec2-metadata-token: $TOKEN")

# Create index.html
cat > /var/www/html/third/index.html <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>${server_name}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f0ff; }
        .container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); max-width: 600px; margin: 0 auto; }
        h1 { color: #4b2e8b; text-align: center; }
        .info { margin: 15px 0; padding: 10px; background: #f8f9fa; border-left: 4px solid #4b2e8b; }
        .highlight { font-weight: bold; color: #4b2e8b; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to <span class="highlight">${server_name}</span></h1>
        <div class="info"><strong>Public IP:</strong> $PUBLIC_IP</div>
        <div class="info"><strong>Private IP:</strong> $PRIVATE_IP</div>
        <div class="info"><strong>Hostname:</strong> $HOSTNAME</div>
        <div class="info"><strong>Availability Zone:</strong> $AZ</div>
        <div class="info"><strong>Context Path:</strong> /third/</div>
    </div>
</body>
</html>
EOF

# Set permissions
chmod 644 /var/www/html/third/index.html
```

## Key Improvements:

1. **Simplified Template Handling**: Used `templatefile()` directly in the resource block
2. **Better Error Handling**: Added `set -ex` in user data scripts
3. **Enhanced Output**: Improved output format with direct URLs
4. **Consistent Styling**: Uniform HTML structure with different color schemes
5. **Security**: Added proper file permissions
6. **Metadata**: Added availability zone information
7. **Path Specification**: Used `${path.module}` for better module compatibility
8. **Documentation**: Added descriptions for outputs


After deployment, Terraform will output the URLs for accessing each server with their specific context paths. Each server will have a distinct color scheme and display its metadata.

## Deployment Steps

1. Save all files in a directory:
   - `main.tf` (the main Terraform configuration)
   - `user_data_server1.sh`
   - `user_data_server2.sh`
   - `user_data_server3.sh`

2. Initialize Terraform:
   ```bash
   terraform init
   ```

3. Review the execution plan:
   ```bash
   terraform plan
   ```

4. Apply the configuration:
   ```bash
   terraform apply
   ```

5. After deployment, Terraform will output the public DNS names and IP addresses of all three servers. You can access them at:
   - Server 1: `http://<public-dns>/`
   - Server 2: `http://<public-dns>/second/`
   - Server 3: `http://<public-dns>/third/`

Each server will display its name, IP addresses, and context path with a different color scheme for easy identification.

## 1. Application Load Balancer

### a. Path Based Routing

![image](https://github.com/user-attachments/assets/1d9432c8-5ea8-4cb2-ba5a-194fbbae9bcd)

![image](https://github.com/user-attachments/assets/867961ad-d9f6-41b0-8e23-c3bf12add46b)

![image](https://github.com/user-attachments/assets/ef138480-ff5c-4fe4-9fa9-d7f3ed2a99a6)



#### Route 53

![image](https://github.com/user-attachments/assets/18f2b01c-0284-4d4c-b6e8-5bac692c41e0)


![image](https://github.com/user-attachments/assets/d9d93ba3-1dd1-4dfe-80c7-a77324cc18fd)


### b. Host Based Routing

![image](https://github.com/user-attachments/assets/b6167c27-a4b0-4699-be90-715b8aab2085)

![image](https://github.com/user-attachments/assets/a1573c29-d1b7-44bf-bc5b-b884baff0def)

![image](https://github.com/user-attachments/assets/6c9d5390-f231-4275-9826-b08c4752f365)



