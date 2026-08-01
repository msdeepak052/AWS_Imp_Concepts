# 26 - REST API Lab - Part 4: Testing Lab Functionality

> Goal: test every route built across [Part 2](24-REST-API-Lab-Part-2-Create-REST-API-And-Define-Resources.md) and [Part 3](25-REST-API-Lab-Part-3-Add-Method-Resources-and-Deploy.md) for real, confirm the path parameter and POST body both work correctly, then clean up.

---

## 1. Step 1 — Test every route

```bash
curl https://<api-id>.execute-api.<region>.amazonaws.com/demo/orders
curl https://<api-id>.execute-api.<region>.amazonaws.com/demo/orders/order-1
curl -X POST https://<api-id>.execute-api.<region>.amazonaws.com/demo/orders -d '{"item":"widget"}'
```

Confirm:
- The first call returns the full order list.
- The second call returns `"order_id": "order-1"` — proof the `{id}` path parameter was correctly extracted from the URL and passed to Lambda via `pathParameters`.
- The third call returns `"received_body"` containing the literal JSON you sent — proof the POST body passed through untouched via proxy integration.

---

## 2. Step 2 — Prove the explicit-deploy requirement directly

1. Go back to `/orders/{id}`'s **GET** method → **Method Response** → add a new response header (any harmless change).
2. Test the same `curl` command from Section 1 again — the change **won't** appear yet.
3. **Deploy API** → same `demo` stage → **Deploy**.
4. Test again — now the change is live. This directly proves [Part 3](25-REST-API-Lab-Part-3-Add-Method-Resources-and-Deploy.md)'s note that every change needs its own explicit redeploy.

---

## 3. Troubleshooting

| Symptom | Likely cause |
|---|---|
| `{"message":"Missing Authentication Token"}` | The path/method combination doesn't exist, or the API wasn't (re)deployed after the last change |
| `{id}` arrives as the literal string `"{id}"` instead of the real value | The resource wasn't created as a genuine path parameter — recheck it was named exactly `{id}` in Part 2 |
| A change made in the console doesn't show up when testing | Expected — redeploy to the `demo` stage, exactly as demonstrated in Section 2 |

---

## 4. Cleanup

1. **API Gateway console** → delete `devopswithdeepak-rest-api`.
2. **Lambda console** → delete `rest-api-demo-function`.

---

## 5. Recap

- All three routes worked correctly, including a genuine path parameter extraction and an untouched POST body — real, tested proof of REST API's proxy integration mechanics.
- The explicit-redeploy requirement was proven directly, not just described — a change genuinely didn't take effect until a fresh deployment ran.
- Next: the [API Keys And Usage Plans](27-API-Keys-And-Usage-Plans.md) note — controlling and metering who's allowed to call an API like this one at all.

### Sources
- [Deploy a REST API in Amazon API Gateway — AWS docs](https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-deploy-api.html)
