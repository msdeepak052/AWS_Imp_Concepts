# 18 - AWS CloudFront Cache Invalidation

> Goal: forcibly remove content from CloudFront's cache **before** its TTL naturally expires — the standard fix for "I updated the origin, but visitors are still seeing the old version" — and understand its cost model and the versioned-filename alternative.

---

## 1. The problem: TTLs mean stale content by design

Note 04 established that cached content is deliberately served **without** re-checking the origin until its TTL expires — that's the entire point of caching. But this means updating the origin's content (a new `logo.png`, a bug-fixed `app.js`) doesn't automatically reach viewers already being served a cached copy — they'll keep seeing the **old** version until the TTL runs out naturally.

**Cache invalidation** forces CloudFront to treat specified paths as **immediately expired**, so the **next** request for them is treated as a cache miss and re-fetched from the origin, regardless of remaining TTL.

---

## 2. Create an invalidation

1. **CloudFront console** → distribution → **Invalidations** tab → **Create invalidation**.
2. **Object paths**: one or more paths, one per line:
   ```
   /images/logo.png
   /css/style.css
   /*
   ```
3. `/*` invalidates **everything** in the distribution — the blunt, "just clear it all" option.
4. **Create invalidation** — takes anywhere from seconds to a few minutes to fully propagate across all edge locations.

```bash
aws cloudfront create-invalidation \
  --distribution-id EDFDVBD6EXAMPLE \
  --paths "/images/logo.png" "/css/style.css"
```

---

## 3. Cost model — invalidations are not free at scale

- The first **1,000 invalidation paths per month** are **free**.
- Beyond that, **each additional path is billed**.
- Critically, **`/*` counts as a single path** for billing purposes — a wildcard invalidating an entire distribution's worth of content is billed the same as invalidating one specific file, making `/*` both operationally blunt **and** cost-efficient compared to submitting thousands of individual specific paths.

> ⚠️ Frequent, large-scale invalidations (e.g. as part of every single deployment) can still add up in cost and in the several-minutes propagation delay each time — for high-deployment-frequency workloads, Section 4's alternative is usually the better long-term pattern.

---

## 4. The alternative: versioned file names (avoid needing invalidation at all)

Instead of invalidating `/app.js` every time it changes, many production pipelines instead **change the filename itself** on every deploy — e.g. `/app.v2.js`, or a content-hash-based name like `/app.3f2a91b.js` — referenced by an HTML file that itself has a **short TTL** (so the *reference* to the new filename propagates quickly) while the **versioned asset files** get very long, effectively "cache forever" TTLs, since a new deployment simply uses a new, never-before-seen filename rather than overwriting an old one.

> 🎯 **Exam tip:** "we need updated content to reach users immediately after a deployment" can point to **either** cache invalidation **or** versioned filenames, depending on the exact scenario framing — but the exam (and real-world best practice) increasingly favors recognizing **versioned filenames** as the more scalable, cost-effective long-term solution, with invalidation reserved for occasional, unplanned "we need this specific stale content gone right now" situations rather than routine deployment tooling.

---

## 5. Recap

- **Cache invalidation** forces specified paths (or `/*` for everything) to be treated as immediately expired, bypassing the remaining TTL — the direct fix for stale cached content after an origin update.
- First 1,000 paths/month are free; **`/*` counts as one path** regardless of how much content it actually covers.
- **Versioned/content-hashed filenames** avoid needing invalidation at all for routine deployments — the more scalable pattern for frequent releases, reserving invalidation for occasional, unplanned situations.
- This closes the entire CloudFront folder: Notes 01-03 covered fundamentals and origins, 04-11 covered every cache-behavior setting in depth, 12-14 covered distribution-wide settings and geographic restriction, 15-16 covered Origin Group failover, and 17-18 covered error handling and cache invalidation.

### Sources
- [Invalidating files — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Invalidation.html)
- [Adding, removing, or replacing content that CloudFront distributes — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/UpdatingExistingObjects.html)
- [Amazon CloudFront pricing — AWS](https://aws.amazon.com/cloudfront/pricing/)
