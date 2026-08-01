# 34 - AWS API Gateway - Exam Cheat Sheet

> Goal: a compact, scenario-keyed quick reference over everything this folder's API Gateway section (files 06-33) covered — for review, not first-time learning.

---

## 1. API type decision

| Scenario says... | Pick |
|---|---|
| Generic request/response API, no special feature mentioned | **HTTP API** — cheaper, faster, AWS's default recommendation |
| Needs API Keys/Usage Plans, private VPC-only endpoint, or edge-optimized global distribution | **REST API** |
| Server needs to push data to connected clients without polling | **WebSocket API** |

---

## 2. Endpoint & security quick table

| Need | Feature |
|---|---|
| Minimize latency for a globally distributed audience | **Edge-optimized** endpoint |
| Internal-only API, never internet-reachable | **Private** endpoint + VPC endpoint |
| Enforce a modern TLS handshake minimum | **Security policy: TLS 1.2** |
| Stop the default `execute-api` URL from bypassing custom-domain-scoped controls | **Strict Mode** |
| Restrict by source IP/VPC/AWS account, regardless of credentials | **Resource Policy** |
| Meter/limit usage per client | **API Keys + Usage Plans** |
| Real authentication (not metering) | **IAM / Lambda / Cognito authorizer** |
| Block attack patterns at the edge | **AWS WAF** |
| Safely test a new deployment on a slice of traffic | **Canary Deployment** |

---

## 3. Integration & request handling

| Symptom / need | Answer |
|---|---|
| `502 Bad Gateway` despite Lambda executing successfully | Lambda's return value doesn't match the required `statusCode`/`headers`/`body` proxy shape |
| Call another AWS service directly, no Lambda needed | **AWS service integration** |
| Reject malformed requests before they cost a backend invocation | **Request Validator** |
| REST API change not showing up on the live URL | Forgot to **redeploy to the stage** — REST API has no auto-deploy |

---

## 4. Recap

- This cheat sheet is a lookup aid, not a replacement for the full notes it summarizes — when a table row is unclear, the linked concept note (06 through 33) has the full reasoning.
- The single most valuable habit from this whole section: **read for the specific missing feature or specific failure symptom**, not just "which service is this about" — API Gateway questions are almost always testing a specific configuration detail.
- This closes out the API Gateway section of this folder; next: the [Introduction to Amazon SQS](35-Introduction-Amazon-SQS.md) note — moving into asynchronous, queue-based integration.

### Sources
- [Amazon API Gateway developer guide — AWS docs](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html)
