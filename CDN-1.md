# CDN -Cloud Delivery Network 
---
## 🔍 **What is a CDN?**

A **Content Delivery Network (CDN)** is a globally distributed network of **proxy servers** and **data centers** that **delivers content** (web pages, images, videos, scripts, etc.) to users **based on their geographic location**, the origin of the content, and the CDN server.

---

## 🎯 **Case Scenario: Why, Where, and When is CDN Required?**

### 🔧 Problem:

You have a website hosted in **Mumbai (India)** and users access it from **New York**, **London**, and **Sydney**.

* Users in New York report **slow page load times**.
* Video streaming **buffers** frequently.
* Image-heavy pages **load slowly**.

### 🚦Challenges:

* Long latency due to **geographic distance**.
* Bandwidth throttling during **traffic spikes**.
* Load on the **origin server** is very high.

### ✅ Solution: Use a **CDN**

By caching content at edge locations near the users (e.g., New York, London, Sydney), the CDN will:

* Serve **static assets (images, CSS, JS)** quickly.
* Reduce latency and **improve performance**.
* Reduce **load on the origin server**.
* Protect against **DDoS attacks**.

---

## 🔧 **Setup Example (Using AWS CloudFront as CDN)**

Assume you're hosting a static website in an S3 bucket (`my-static-site.s3.amazonaws.com`).

### ✅ Steps:

1. **Create an S3 bucket** and upload your static content.

2. **Go to AWS CloudFront** and create a distribution:

   * Origin: `my-static-site.s3.amazonaws.com`
   * Default behavior:

     * Allowed HTTP Methods: `GET, HEAD`
     * Caching: Enable
     * Viewer Protocol Policy: Redirect HTTP to HTTPS
   * Price Class: Use only selected edge locations to control cost.

3. CloudFront generates a **distribution URL**:
   `https://d123abc.cloudfront.net` (this becomes your CDN endpoint)

4. (Optional) Set a **custom domain** (`cdn.mysite.com`) using Route53 and an SSL certificate.

5. Update your website or app to use CDN URLs for static assets (images, JS, CSS).

---

## 📦 **Key CDN Parameters Explained**

| Parameter              | Description                                                     |
| ---------------------- | --------------------------------------------------------------- |
| **Origin**             | The original location of content (e.g., S3 bucket, web server). |
| **Edge Location**      | CDN's data center closer to end-users that caches content.      |
| **TTL (Time to Live)** | How long content is cached at edge (e.g., 1 hour).              |
| **Caching Behavior**   | Rules that decide how and what to cache.                        |
| **Geo-Restriction**    | Restrict access to content based on the user's location.        |
| **Signed URLs**        | Secure content by requiring authentication for access.          |
| **Invalidation**       | Force CDN to clear cache and re-fetch from origin.              |
| **Compression**        | Enable gzip/brotli to reduce size of files.                     |
| **Logging**            | Track access logs and analytics of CDN usage.                   |
| **Protocol Policy**    | Define HTTP/HTTPS behavior.                                     |
| **Price Class**        | Limit regions for cost optimization.                            |

---

## 🧠 **Common Use Cases of CDN**

### 1. **Static Website Hosting**

* Host site on S3 + CloudFront for global reach.
* Speeds up HTML, CSS, JS delivery.

### 2. **Video Streaming**

* Netflix, YouTube use CDN to deliver videos closer to the user.
* Reduces buffering and latency.

### 3. **E-commerce**

* Faster image/product catalog loading.
* Reduces cart abandonment.

### 4. **Software Delivery**

* Deliver software updates globally (e.g., Ubuntu mirrors via CDN).

### 5. **API Acceleration**

* Use CDN to cache GET API responses.
* Reduces backend compute cost.

### 6. **DDoS Protection & Security**

* CDNs absorb large-scale traffic spikes (Cloudflare, Akamai).
* Prevent attacks from reaching the origin.

---

## 📈 Real-World Example: Amazon CloudFront (CDN)

```hcl
# Terraform example to configure CloudFront
resource "aws_cloudfront_distribution" "cdn" {
  origin {
    domain_name = "mybucket.s3.amazonaws.com"
    origin_id   = "S3Origin"
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "CDN for my static site"
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3Origin"

    viewer_protocol_policy = "redirect-to-https"

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }
  }

  price_class = "PriceClass_100"

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}
```

---

## 📌 Summary

| Feature         | CDN Impact                                             |
| --------------- | ------------------------------------------------------ |
| **Performance** | Faster content delivery due to caching and proximity   |
| **Scalability** | Handles traffic spikes without overloading origin      |
| **Security**    | Shields backend, offers SSL, DDoS protection           |
| **Cost**        | Reduces data transfer from origin, but CDN costs apply |

---
Let's explore **AWS CloudFront Origin Settings** in a **real-world, scenario-based approach** — with **setup steps, use cases, all parameters explained**, and examples in both **AWS Console** and **Terraform**.

---

## 🧠 **Case Scenario: Why, Where, and When CloudFront Origin is Required**

### 🔧 Problem:

You’re hosting a multi-national web application:

* Static website hosted in **S3**.
* APIs served from an **Application Load Balancer (ALB)**.
* Images stored in **S3 or Media Server (custom origin)**.

### 😕 Issues:

* Users in Europe & US experience **slow load times**.
* The origin server in Mumbai is overloaded.
* No security or access control at the edge.
* Higher cost due to repeated fetching from origin.

### ✅ Need:

You want to:

* Deliver content from locations closest to users.
* **Cache static content** at the edge.
* Separate behavior for APIs vs. static content.
* Use **custom domain and HTTPS**.

---

## 🧭 **Where & When CloudFront Origin is Used**

| Use Case                           | CloudFront Origin Type                   |
| ---------------------------------- | ---------------------------------------- |
| **Static Site Hosting**            | Amazon S3 (without public access)        |
| **API Acceleration**               | ALB or EC2                               |
| **Video Streaming**                | Media Server as custom origin            |
| **E-commerce Images**              | S3 with cache behaviors                  |
| **Hybrid Site (Static + Dynamic)** | Multiple origins with path-based routing |

---

## 🏗️ **What is a CloudFront Origin?**

An **origin** is the backend source that CloudFront fetches content from.

CloudFront supports:

* **S3 Bucket**
* **HTTP(S) Server / Custom Origin** (EC2, ALB, on-prem)
* **MediaStore, MediaPackage**

---

## 🧩 **All Origin Settings (Parameters Explained)**

| Parameter                 | Description                                                                      |
| ------------------------- | -------------------------------------------------------------------------------- |
| `Origin ID`               | Unique identifier for the origin.                                                |
| `Domain Name`             | Hostname of the origin (S3, ALB, EC2, etc.).                                     |
| `Origin Path`             | Optional path appended to requests (e.g. `/static`).                             |
| `Origin Type`             | S3, ALB, EC2, MediaStore, etc.                                                   |
| `Origin Access Control`   | Use OAC to securely access private S3.                                           |
| `Custom Headers`          | Add headers in CloudFront-to-origin requests.                                    |
| `Connection Attempts`     | Retry attempts before failing.                                                   |
| `Connection Timeout`      | Timeout value for the origin.                                                    |
| `Origin Shield`           | Adds a regional cache layer for protection.                                      |
| `Origin Protocol Policy`  | How CloudFront connects to origin: `HTTP-only`, `HTTPS-only`, or `Match Viewer`. |
| `Origin SSL Protocols`    | For HTTPS origin, defines allowed TLS versions.                                  |
| `Origin Custom KeepAlive` | Reuse TCP connection; improves performance.                                      |

---

## ⚙️ **CloudFront Origin Setup Example (Console UI)**

1. **Open AWS CloudFront** → Create Distribution.
2. **Set Origin Domain**:

   * For S3: `my-bucket.s3.amazonaws.com`
   * For ALB: `my-api-alb-123.ap-south-1.elb.amazonaws.com`
3. Choose:

   * **Origin Type**: S3 or Custom
   * **Origin ID**: `S3-Origin`, `ALB-Origin`
4. **Restrict Access** (S3 origin only): Enable Origin Access Control (OAC)
5. **Origin Protocol Policy**: Choose `HTTPS Only` for secure access.
6. (Optional) Add **Custom Headers** to forward.
7. Configure **Cache Behaviors** to map `/static`, `/api`, etc.

---

## 📜 **Terraform Example with Multiple Origins**

```hcl
resource "aws_cloudfront_distribution" "example" {
  origin {
    domain_name = "my-bucket.s3.amazonaws.com"
    origin_id   = "S3Origin"

    s3_origin_config {
      origin_access_control_id = aws_cloudfront_origin_access_control.example.id
    }
  }

  origin {
    domain_name = "my-api.example.com"
    origin_id   = "APIOrigin"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    target_origin_id       = "S3Origin"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
  }

  ordered_cache_behavior {
    path_pattern           = "/api/*"
    target_origin_id       = "APIOrigin"
    viewer_protocol_policy = "https-only"
    allowed_methods        = ["GET", "POST", "OPTIONS", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  price_class = "PriceClass_100"
}
```

---

## 🔐 **Security Tips for Origin Settings**

| Feature                         | Use                                                                  |
| ------------------------------- | -------------------------------------------------------------------- |
| **OAC (Origin Access Control)** | Replace old OAI. Controls access to private S3.                      |
| **HTTPS-Only Policy**           | Enforce TLS from CloudFront to origin.                               |
| **WAF Integration**             | Use AWS WAF with CloudFront to block threats before they hit origin. |
| **Signed URLs/Cookies**         | Secure premium content or API access.                                |

---

## 🔄 **Real-World Use Case: E-Commerce Website**

| Content Type      | Origin            | Cache Behavior            |
| ----------------- | ----------------- | ------------------------- |
| Homepage, CSS, JS | S3                | Cache long (static)       |
| Product Images    | S3 / Media Server | Cache long                |
| Login/API         | ALB/EC2           | No caching, HTTPS-only    |
| Admin Panel       | EC2 / Lambda      | No cache, restrict access |

---

## ✅ **Summary Table**

| Component                  | Role                                             |
| -------------------------- | ------------------------------------------------ |
| **Origin**                 | Source server of content                         |
| **Origin ID**              | Identifier used in cache behaviors               |
| **Origin Type**            | S3, ALB, EC2, etc.                               |
| **Origin Access Control**  | Grants private S3 access                         |
| **Origin Protocol Policy** | HTTP/HTTPS control between CloudFront and origin |
| **Cache Behavior**         | Maps paths like `/api/*` to specific origins     |

---

## 🧠 **Case Scenario: Why, Where, and When Default Cache Behavior is Required**

### 🧩 Scenario:

You're deploying a **static website** for a **global e-commerce platform** using:

* S3 for website assets (`/`, `/products.html`, `/style.css`)
* API hosted on a different backend (`/api/*`)

You want to:

* Serve **all site content fast globally**.
* Cache static files aggressively.
* Use HTTPS, block HTTP.
* Prevent caching of API endpoints.

### 🔥 Problem:

If **you don't configure behaviors properly**, CloudFront:

* Might send unnecessary requests to your S3.
* May not enforce HTTPS.
* Will cache sensitive content incorrectly.

### ✅ Solution:

Use **Default Cache Behavior** to control:

* **What is cached**
* **How it’s accessed**
* **Who can access it**
* **When cache is refreshed**

---

## 📘 **What is Default Cache Behavior in CloudFront?**

CloudFront requires **at least one cache behavior**, and the **default cache behavior** is the catch-all rule applied to all requests **unless explicitly overridden** (via `ordered_cache_behavior`).

📌 Think of it as:

> “All traffic that doesn’t match specific patterns (like `/api/*`) follows this rule.”

---

## ⚙️ **Where Is It Used?**

| Use Case               | How Default Cache Behavior Helps        |
| ---------------------- | --------------------------------------- |
| **Static Website**     | Handles `/`, `/about.html`, `/logo.png` |
| **Global Blog**        | Serves HTML + assets                    |
| **API Gateway Site**   | Cache Swagger docs, but not `/api/*`    |
| **Multi-origin Setup** | Acts as fallback behavior               |

---

## 🧪 **Example Setup in AWS Console**

### ✅ Setup (for S3 static hosting):

1. **Go to CloudFront** → Create Distribution.
2. **Origin**: `my-bucket.s3.amazonaws.com`
3. Scroll to **Default Cache Behavior Settings**:

   * **Viewer Protocol Policy**: Redirect HTTP to HTTPS
   * **Allowed Methods**: `GET`, `HEAD`
   * **Cache Based on Headers**: None (for static)
   * **Compress Objects Automatically**: ✅ Yes
   * **Caching TTLs**: Default (e.g., 86400s)
4. Save and deploy.

---

## 📦 **Default Cache Behavior Parameters Explained**

| Parameter                   | Description                                                | Example / Best Practice                               |
| --------------------------- | ---------------------------------------------------------- | ----------------------------------------------------- |
| `target_origin_id`          | Which origin to route to                                   | `"S3Origin"`                                          |
| `viewer_protocol_policy`    | Force HTTPS, allow HTTP                                    | `"redirect-to-https"` recommended                     |
| `allowed_methods`           | What HTTP methods to allow                                 | `["GET", "HEAD"]` for static                          |
| `cached_methods`            | Which methods are cached                                   | Usually same as allowed, but cache only `GET`, `HEAD` |
| `cache_policy_id`           | Reuse cache policy                                         | AWS Managed Policy or custom one                      |
| `origin_request_policy_id`  | Forward headers/query                                      | Only if needed for personalization                    |
| `compress`                  | Enable gzip/brotli                                         | ✅ Improves performance                                |
| `forwarded_values`          | (legacy) How cookies, headers, query strings are forwarded | Avoid forwarding cookies unless needed                |
| `min_ttl`                   | Minimum cache duration                                     | 0s for dynamic content                                |
| `default_ttl`               | Default duration if no cache-control header                | E.g., 86400s (1 day)                                  |
| `max_ttl`                   | Max time an object can be cached                           | E.g., 31536000 (1 year)                               |
| `smooth_streaming`          | For media (HLS)                                            | false unless you're streaming                         |
| `field_level_encryption_id` | For encrypted headers                                      | Use if required for compliance                        |

---

## 🧾 **Terraform Example: Default Cache Behavior**

```hcl
default_cache_behavior {
  target_origin_id       = "S3Origin"
  viewer_protocol_policy = "redirect-to-https"
  allowed_methods        = ["GET", "HEAD"]
  cached_methods         = ["GET", "HEAD"]
  compress               = true

  cache_policy_id          = "658327ea-f89d-4fab-a63d-7e88639e58f6" # AWS Managed CachingOptimized
  origin_request_policy_id = "88a5eaf4-2fd4-4709-b370-b4c650ea3fcf" # AWS Managed AllViewer

  lambda_function_association {
    event_type   = "viewer-request"
    lambda_arn   = "arn:aws:lambda:us-east-1:123456789:function:redirectToLowercase"
    include_body = false
  }
}
```

---

## 🧠 **Use Cases**

### ✅ Use Case 1: Static Website

* Enforce HTTPS.
* Cache for 1 year.
* Don’t forward cookies.

### ✅ Use Case 2: API Gateway (not recommended for default behavior)

* Instead, use `ordered_cache_behavior` for `/api/*`.

### ✅ Use Case 3: Public S3 Images

* Use long TTLs.
* Enable Brotli/gzip compression.
* No query string forwarding.

---

## 📌 Summary Table

| Feature          | Recommendation                         |
| ---------------- | -------------------------------------- |
| Protocol Policy  | Redirect HTTP to HTTPS                 |
| Allowed Methods  | `GET`, `HEAD` (for static)             |
| Compression      | ✅ Enable                               |
| Caching TTLs     | Use defaults or aggressive for static  |
| Forwarding       | Avoid cookies/headers unless necessary |
| Use Lambda\@Edge | For redirects, auth, URL rewriting     |

---


## 🧠 **Case Scenario: Why, Where, and When CloudFront Origin Access is Required**

### 🎯 Scenario:

You host a **static website** (HTML, JS, CSS, images) in a **private S3 bucket**. Users will access it **only through CloudFront**.

### ⚠️ Problem:

If the S3 bucket is public:

* Anyone can bypass CloudFront and access S3 files directly via:

  ```
  https://my-bucket.s3.amazonaws.com/index.html
  ```

This:

* Breaks **security** and **logging**
* Adds **cost** (users hit S3, not CDN)
* Bypasses **WAF/DDoS protection**

### ✅ Need:

Restrict S3 bucket so:

* It **only accepts requests from CloudFront**.
* Everything is served through the **CDN edge locations**.

---

## 🛡️ **What is CloudFront Origin Access?**

It ensures **CloudFront has permission to access a private S3 bucket**, while blocking public access to that bucket.

There are two methods:

1. ❌ **OAI (Origin Access Identity)** → **Legacy**
2. ✅ **OAC (Origin Access Control)** → **Modern, recommended**

---

## 📘 **Where & When CloudFront Origin Access is Required**

| Situation                                 | Use CloudFront Origin Access?       |
| ----------------------------------------- | ----------------------------------- |
| Hosting private S3 static site            | ✅ Yes                               |
| Serving PDFs, docs from S3 via CloudFront | ✅ Yes                               |
| Public bucket with unrestricted files     | ❌ No                                |
| Custom origin (EC2/ALB)                   | ❌ Not required, use security groups |

---

## ✅ **Use Cases**

| Use Case                     | CloudFront Origin Access Benefit                  |
| ---------------------------- | ------------------------------------------------- |
| Static website in private S3 | Restrict access to S3 only via CloudFront         |
| Image CDN                    | Prevent direct access to image URLs               |
| E-learning content           | Secure PDFs/videos only via signed CloudFront URL |
| API responses stored in S3   | Secure & cache them globally                      |

---

## ⚙️ **CloudFront OAC Setup (Step-by-Step)**

### 🛠️ Setup via AWS Console

#### 1. Create S3 Bucket:

* Disable **public access**
* Upload `index.html`, `style.css`

#### 2. Create Origin Access Control (OAC):

* Go to **CloudFront > Origin Access Control > Create**
* Name: `MyOAC`
* Origin Type: **S3**
* Signing Behavior: **Always**
* Signing Protocol: **SigV4**

#### 3. Create CloudFront Distribution:

* Origin Domain: `my-bucket.s3.amazonaws.com`
* Attach **OAC** to this origin
* Default Cache Behavior: Configure protocols, caching, compression

#### 4. Update S3 Bucket Policy:

> Use the **CloudFront-generated policy snippet** that allows access from OAC.

Example:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowCloudFrontAccessViaOAC",
      "Effect": "Allow",
      "Principal": {
        "Service": "cloudfront.amazonaws.com"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/*",
      "Condition": {
        "StringEquals": {
          "AWS:SourceArn": "arn:aws:cloudfront::123456789012:distribution/EDFDVBD6EXAMPLE"
        }
      }
    }
  ]
}
```

---

## 📜 **Terraform Example (CloudFront with OAC for S3)**

```hcl
# 1. Create OAC
resource "aws_cloudfront_origin_access_control" "oac" {
  name                              = "MyOAC"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

# 2. Create CloudFront Distribution
resource "aws_cloudfront_distribution" "cdn" {
  origin {
    domain_name = "my-bucket.s3.amazonaws.com"
    origin_id   = "S3Origin"

    s3_origin_config {
      origin_access_control_id = aws_cloudfront_origin_access_control.oac.id
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"

  default_cache_behavior {
    target_origin_id       = "S3Origin"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    compress               = true

    cache_policy_id = "658327ea-f89d-4fab-a63d-7e88639e58f6" # CachingOptimized
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

# 3. S3 Bucket Policy (manually added or use data block)
```

---

## 📦 **Parameters in OAC (Explained)**

| Parameter                           | Description                   | Recommended Value                                        |
| ----------------------------------- | ----------------------------- | -------------------------------------------------------- |
| `origin_access_control_origin_type` | Only `s3` is supported now    | `s3`                                                     |
| `signing_behavior`                  | How CloudFront signs requests | `always`                                                 |
| `signing_protocol`                  | Protocol for signing requests | `sigv4`                                                  |
| `origin_access_control_id`          | ID used in CloudFront origin  | Use from `aws_cloudfront_origin_access_control` resource |

---

## 🔐 **Security Benefits of OAC**

| Feature            | Benefit                                     |
| ------------------ | ------------------------------------------- |
| ✅ No public access | Prevents bypassing CloudFront               |
| ✅ Signed requests  | Uses SigV4 to authenticate                  |
| ✅ Integrated IAM   | Scoped access to only specific distribution |
| ✅ Replaces OAI     | Modern, easier to manage                    |

---

## ✅ **Summary Table**

| Feature         | Value                               |
| --------------- | ----------------------------------- |
| Purpose         | Restrict S3 bucket to CloudFront    |
| Method          | Origin Access Control (OAC)         |
| Bucket Public?  | ❌ No                                |
| Protocol        | SigV4                               |
| When to Use     | Always with private S3 content      |
| CloudFront Role | Assumes identity to access objects  |
| Setup Time      | \~5–10 min via Console or Terraform |

---



