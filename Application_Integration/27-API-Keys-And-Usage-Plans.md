# 27 - API Keys And Usage Plans

> Goal: understand API Keys and Usage Plans as a **metering and throttling** mechanism — not an authentication mechanism — since confusing the two is a genuinely common mistake this note exists to prevent.

---

## 1. The problem: identifying and limiting individual clients, not just "authenticated or not"

Authorization (IAM, Lambda authorizers, Cognito) answers "is this caller allowed to call the API at all?" A separate question is "**which specific client** is calling, and how much are they allowed to use it?" — the exact problem **API Keys and Usage Plans** solve, this is a REST-API-only feature (see [REST API vs. HTTP API Part 2](08-REST-API-vs-HTTP-API-Part-2.md)).

---

## 2. Architecture & workflow

```mermaid
flowchart LR
    CLIENT["Client, sends x-api-key header"]
    KEY["API Key"]
    PLAN["Usage Plan<br/>throttle + quota limits"]
    STAGE["Associated API stage(s)"]

    CLIENT --> KEY --> PLAN --> STAGE
```

---

## 3. The two pieces

| Concept | What it is |
|---|---|
| **API Key** | An identifier a client includes in the `x-api-key` header — identifies **which client** is calling, not whether they're generally authorized |
| **Usage Plan** | Defines **throttle limits** (requests per second) and **quota limits** (e.g. 10,000 requests per month) — then gets **associated with one or more API Keys** and one or more API stages |

---

## 4. Why this is genuinely not authentication

An API Key is **not encrypted, not a secret credential in the cryptographic sense**, and should **never** be relied on as the sole security control for a sensitive API — it's meant for **identifying and metering** clients (e.g. different partners on different pricing tiers), typically layered **on top of** real authorization, not instead of it.

> 🎯 **Exam tip**: "meter and limit usage per customer/partner, with different tiers of allowed request volume" → **API Keys + Usage Plans**. "Ensure only legitimate, authenticated callers can access this API at all" → a real authorizer (IAM/Lambda/Cognito) — these are two different problems, and a scenario mixing them is testing whether you'll conflate metering with security.

---

## 5. Recap

- **API Keys** identify individual clients; **Usage Plans** define throttle/quota limits and get associated with keys and stages.
- This is a **metering** mechanism, not an authentication mechanism — never rely on it as the sole access control for a sensitive API.
- This is REST-API-only — not available on HTTP APIs.
- Next: the [LAB - API Keys And Usage Plans](28-LAB-API-Keys-And-Usage-Plans.md) note — building a real API key and usage plan, and proving the quota limit actually triggers.

### Sources
- [Setting up API keys using the API Gateway console — AWS docs](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-setup-api-key-with-console.html)
- [Creating and using usage plans with API keys — AWS docs](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html)
