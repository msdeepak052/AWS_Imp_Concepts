# 01 - AWS Global Accelerator

> Goal: get the one-paragraph mental model of what AWS Global Accelerator is *for* before diving into its components (Note 02) and features (Note 03) — and immediately place it against the two services it's most often confused with, CloudFront and Route 53.

---

## 1. The problem: the public internet is a bad path between regions

A user in Mumbai hitting an application hosted in `us-east-1` doesn't travel over a single well-managed network the whole way — their request hops across **many independent internet service providers**, each with its own routing, congestion, and occasional packet loss, before it ever reaches an AWS Region. That path is often not the shortest or fastest one available; it's just whatever the public internet's routing tables happen to pick.

**AWS Global Accelerator** fixes this by giving you **static anycast IP addresses** that are announced from **AWS edge locations all over the world**. A user's traffic enters the **AWS global network backbone** at the *nearest* edge location to them, and travels over AWS's own private, high-performance network the rest of the way to your actual application — instead of riding the unpredictable public internet for that entire distance.

> 🧠 **Mental model:** CloudFront (this repo's `Cloudfront_CDN` folder) shortens the trip by **caching a copy of your content** near the user. Global Accelerator shortens the trip differently — it doesn't cache anything, it just gets the user's *live* traffic onto AWS's fast private backbone as early as possible, all the way to your unchanged origin.

---

## 2. What kind of traffic this is for

Because Global Accelerator works at the **network layer (TCP/UDP)**, not the HTTP layer, it is not limited to web traffic the way CloudFront is. It's the right fit for:

- Non-HTTP TCP/UDP workloads — gaming, VoIP, IoT, custom protocols.
- HTTP(S) workloads that **must not be cached** — highly dynamic APIs, real-time dashboards.
- Any workload needing **fixed IP addresses** that client firewalls can allow-list, even while the backend infrastructure behind them changes.
- Multi-Region architectures wanting **fast, automatic failover** between healthy Regions, at the network level rather than DNS level.

---

## 3. Global Accelerator vs. CloudFront vs. Route 53 — placing the three

| | **CloudFront** | **Global Accelerator** | **Route 53 (failover/latency routing)** |
|---|---|---|---|
| OSI layer | Application (L7, HTTP/S) | Network (L4, TCP/UDP) | DNS resolution |
| Caches content? | Yes | No | No — just resolves names to IPs |
| Entry point | Distribution domain name | 2 static anycast IPs (or BYOIP) | Whatever IP the DNS answer returns |
| Failover speed | N/A (origin groups: per-request) | Fast — health-checked at the network layer, no DNS/TTL involved | Bound by **DNS TTL** — clients cache the old answer until it expires |
| Best for | Static/cacheable HTTP(S) content, global web audiences | Non-HTTP protocols, uncacheable traffic, fixed-IP requirements, fast multi-Region failover | Routing decisions made *before* a connection even starts |

> 🎯 **Exam tip:** if a scenario says content **cannot be cached**, needs a **non-HTTP protocol**, or needs a **fixed IP address for firewall allow-listing** while the backend can still change — that combination almost always signals **Global Accelerator**, not CloudFront. If the scenario is purely about DNS-level routing decisions and tolerates TTL-bound failover delay, that's **Route 53**.

---

## 4. Recap

- Global Accelerator improves performance by routing traffic onto **AWS's private global network backbone** as early as possible (nearest edge location), rather than caching content like CloudFront does.
- It operates at **layer 4 (TCP/UDP)**, so it isn't limited to HTTP(S) traffic the way CloudFront is.
- It's the right tool when content **can't be cached**, the protocol **isn't HTTP**, or the requirement is a **fixed IP address** in front of changeable backend infrastructure — with faster failover than DNS-based Route 53 routing, since it isn't bound by TTL/caching on the client side.
- Next: Note 02 — Introduction of AWS Global Accelerator, covering its actual components (accelerator, listener, endpoint group, endpoint) and how a request flows through them.

### Sources
- [What is AWS Global Accelerator? — AWS docs](https://docs.aws.amazon.com/global-accelerator/latest/dg/what-is-global-accelerator.html)
- [AWS Global Accelerator features](https://aws.amazon.com/global-accelerator/features/)
- [AWS Global Accelerator FAQs](https://aws.amazon.com/global-accelerator/faqs/)
