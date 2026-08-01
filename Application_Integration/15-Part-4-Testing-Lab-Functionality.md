# 15 - Part 4: Testing Lab Functionality

> Goal: call the real invoke URL built across [Part 2](13-Part-2-API-Using-Lambda.md) and [Part 3](14-Part-3-Create-API-Gateway-HTTP-API.md), confirm it genuinely works end to end, and clean up.

---

## 1. Step 1 — Find the invoke URL

1. **API Gateway console** → `devopswithdeepak-http-api` → note the **Invoke URL** on the API's main page, of the form `https://<api-id>.execute-api.<region>.amazonaws.com`.

---

## 2. Step 2 — Call it for real

```bash
curl https://<api-id>.execute-api.<region>.amazonaws.com/hello
```
Or open the same URL directly in a browser. Confirm the JSON response includes `"path": "/hello"` and `"method": "GET"` — proof the request actually flowed through API Gateway's routing into the real Lambda execution built in Part 2, not a cached or static response.

---

## 3. Step 3 — Confirm it in CloudWatch too

1. **Lambda console** → `http-api-demo-function` → **Monitor** tab → **View CloudWatch logs**.
2. Confirm a new log stream/entry exists matching the timestamp of your `curl` call — the same automatic CloudWatch integration covered in this project's [Monitoring](../Monitoring/01-Amazon-CloudWatch-Introduction.md) folder, here proving this specific invocation genuinely happened.

---

## 4. Troubleshooting

| Symptom | Likely cause |
|---|---|
| `{"message":"Not Found"}` | The path doesn't match `/hello` exactly, or the method isn't `GET` — recheck Part 3, Section 3 |
| `{"message": "Internal Server Error"}` | Check the Lambda function's CloudWatch logs — almost always a code-level exception, not an API Gateway issue |
| Nothing at all / connection refused | Wrong Region in the URL, or the API wasn't actually created successfully — recheck Part 3 |

---

## 5. Cleanup

1. **API Gateway console** → delete `devopswithdeepak-http-api`.
2. **Lambda console** → delete `http-api-demo-function`.

---

## 6. Recap

- The full lab — Lambda function, HTTP API, route, and a real tested invoke URL — is now built and verified end to end, closing out [Part 1](12-Part-1-Lab-Prerequisites.md) through this part.
- CloudWatch logs independently confirmed the invocation, tying this lab back to this project's Monitoring folder.
- Next: the [REST API Endpoint Type](16-REST-API-Endpoint-Type.md) note — moving into REST API's deeper configuration surface, since this lab only used the simpler HTTP API type.

### Sources
- [Setting up an HTTP API — AWS docs](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-quick-start.html)
