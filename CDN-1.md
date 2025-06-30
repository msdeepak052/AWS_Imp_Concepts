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



