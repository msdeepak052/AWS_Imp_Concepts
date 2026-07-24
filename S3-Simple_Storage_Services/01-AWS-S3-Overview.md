# 01 - AWS Simple Storage Service (S3) — Overview

> Goal: place S3 on the storage map from `EC2-Storage/01-AWS-Storage-Basics-Overview.md` — it's the **object storage** corner of that map — and preview the shape of this whole folder before going deep note by note.

---

## 1. Where S3 fits versus everything in EC2-Storage

The `EC2-Storage` folder covered storage that attaches to (or is mounted by) an EC2 instance: **Instance Store**, **EBS** (block storage), **EFS**/**FSx** (file storage). **S3** is the fourth major AWS storage model — **object storage** — and it is deliberately **not attached to any instance at all**. It's reached over HTTPS, via an API call, from anywhere with the right credentials and network path — an EC2 instance, a Lambda function, a browser, or your laptop, all the same way.

> 🧠 **Mental model:** if EBS is a disk plugged into one computer, and EFS is a shared network drive mounted by several computers, S3 is a key-value store for whole files, reachable over the internet (or privately over a VPC endpoint, Note 39) — you don't "mount" S3, you make API calls (`PutObject`, `GetObject`, `DeleteObject`) against it.

---

## 2. Core building blocks

| Concept | What it is |
|---|---|
| **Bucket** | A top-level, **globally uniquely named** container for objects — created in one specific Region, though the name itself must be unique across **all** of AWS, every account, every Region |
| **Object** | The actual data you store — a **key** (its full path-like name, e.g. `images/logo.png`), the **value** (the raw bytes, up to 5 TB per object), and **metadata** (content type, custom key-value tags, etc.) |
| **Key** | The unique identifier for an object **within its bucket** — S3 has no real nested "folders"; a key like `photos/2026/beach.jpg` just looks hierarchical, but the bucket itself is a flat namespace of full keys |

> ⚠️ "Folders" in the S3 console are a **UI convenience only** — internally, an object's key is a single flat string that happens to contain `/` characters. There's no separate folder object being created or navigated the way a real filesystem (EFS/FSx) works.

---

## 3. What S3 is used for (the recurring exam framing)

S3's core promise is **99.999999999% (11 nines) durability** for S3 Standard (achieved by redundantly storing data across a minimum of 3 Availability Zones) and effectively **unlimited scale** — no capacity to provision ahead of time, unlike every EBS volume type in `EC2-Storage`. This makes it the default answer for:

- Static website assets, backups, data lake storage, application logs, and any "just store this file durably and retrieve it later" need.
- The **source or target** for many other services covered elsewhere in this repo: CloudFront origins, Lambda triggers, Athena/data-lake queries, EBS snapshot storage (`EC2-Storage/08`), AMI backing (`EC2-Storage/09`).

---

## 4. What this folder covers

This folder mirrors the lecture sequence closely: **fundamentals and storage classes** (Notes 02-05), **versioning and lifecycle** (06-08), **access control — bucket policies, IAM policies, ACLs** (09-13), **Object Lock** (14), **encryption — all flavors** (15-22), **public access controls** (23-25), **static website hosting** (26-28), **CORS, replication, transfer acceleration** (29-31), **logging and auditing** (32-34), **presigned URLs and MFA delete** (35-36), **event notifications** (37), **multipart upload** (38), and **network-path/access-scoping features — VPC Gateway Endpoints and Access Points** (39-41).

> 🎯 **Exam tip:** S3 is one of the most heavily tested services on SAA-C03 precisely because it has so many independently-configurable features (versioning, lifecycle, encryption, replication, access control) that all interact — most exam questions test whether you know which *specific* feature solves a *specific* stated problem, not just "what is S3."

---

## 5. Recap

- S3 is AWS's **object storage** service — flat key/value storage per bucket, reached via API, not attached to any single instance.
- **Buckets** are globally uniquely named containers created in one Region; **objects** are identified by a **key** (a full string, not a real nested path) plus their data and metadata.
- 11 nines of durability (S3 Standard) and no pre-provisioned capacity are S3's headline properties, distinguishing it from every storage type in `EC2-Storage`.
- Next: Note 02 — Introduction of AWS S3 Simple Storage Service, covering bucket/object creation mechanics in more depth.

### Sources
- [What is Amazon S3? — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
- [Amazon S3 buckets — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingBucket.html)
- [Amazon S3 objects overview — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingObjects.html)
