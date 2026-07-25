# 09 - AWS CloudFront Default Cache Behavior — Cache Key And Origin Requests

> Goal: understand exactly what makes two requests "the same" for caching purposes — the **cache key** — via the modern **Cache Policy** and **Origin Request Policy** objects that replaced the older, more limited legacy TTL/forwarding settings.

---

## 1. What a cache key actually is

The **cache key** is the set of request attributes CloudFront uses to decide whether an incoming request can be served from an **existing** cached copy, or needs to be treated as a **different** cacheable variant entirely. By default, the cache key is just the **request path**.

**Example — a streaming service:** imagine a video URL like `/watch/inception`, requested at different quality levels and audio languages via a query string or header — say `?res=1080p&lang=en` versus `?res=4k&lang=hi`. By default, the cache key is *just* `/watch/inception` — meaning, without further configuration, CloudFront would treat **every resolution/language combination as the exact same cache entry**, potentially serving a viewer who asked for 4K Hindi the cached 1080p English copy instead.

> ⚠️ This default-cache-key behavior is a classic real-world CloudFront misconfiguration: dynamic content that varies by query string, header, or cookie needs those specific elements **explicitly added to the cache key**, or CloudFront will happily serve one user's cached response to a completely different request.

---

## 2. Architecture & workflow — two legs, two different controls

Every CloudFront request involves up to **two separate legs**, and each one is governed by a different setting from this note:

```mermaid
flowchart LR
    U["User / Viewer"] -->|"① Request arrives — CACHE KEY evaluated here"| E["CloudFront Edge Location"]
    E -->|"② Cache HIT → served straight back, origin never contacted"| U
    E -->|"③ Cache MISS → forwarded onward, per ORIGIN REQUEST POLICY"| O["Origin"]
    O -->|"④ Response comes back, stored under that Cache Key"| E
```

- **Leg 1 — Viewer → Edge Location**: governed by the **Cache Key** (Section 4). CloudFront checks whether it already has a cached entry matching this specific request's cache key. This single check is what decides **Hit vs. Miss**.
- **Leg 2 — Edge Location → Origin**: only happens **on a Cache Miss**, and is governed by the **Origin Request Policy** (Section 5) — it decides what CloudFront actually sends onward to your origin, independent of whatever was or wasn't included in the cache key.

> 🧠 If Leg 1 is a Hit, Leg 2 never happens — the Origin Request Policy is completely irrelevant to that particular request. It only comes into play the instant the Cache Key check fails and CloudFront actually has to go ask the origin.

This split is easiest to see across multiple edge locations, using the streaming example from Section 1 — each edge independently runs Leg 1, and only reaches for Leg 2 when *it* personally has a miss:

```mermaid
sequenceDiagram
    participant A as Viewer A (near Edge-1)
    participant E1 as Edge Location 1
    participant O as Origin (holds every variant)
    participant B as Viewer B (near Edge-2)
    participant E2 as Edge Location 2

    A->>E1: GET /watch/inception?res=1080p&lang=en
    Note over E1: LEG 1 — CACHE KEY check (path+res+lang) → no match → MISS
    E1->>O: LEG 2 — forwarded per ORIGIN REQUEST POLICY (only because of the Miss)
    O-->>E1: Returns the 1080p / English variant
    E1->>E1: Stored under this cache key
    E1-->>A: Serve 1080p / English

    B->>E2: GET /watch/inception?res=4k&lang=hi
    Note over E2: LEG 1 — CACHE KEY check (path+res+lang) → no match here either → MISS
    E2->>O: LEG 2 — forwarded per ORIGIN REQUEST POLICY (only because of the Miss)
    O-->>E2: Returns the 4K / Hindi variant
    E2->>E2: Stored under this cache key
    E2-->>B: Serve 4K / Hindi
```

The streaming example also reveals something the two-leg diagram alone doesn't show: **each edge location's cache is independent**. CloudFront doesn't maintain one single global cache; every edge location builds up its own cache purely from the requests *it personally* has seen. A variant cached at one edge location is not automatically present at another — which is exactly why both Viewer A and Viewer B above hit a Leg-1 Miss, even though they're asking about the same movie.

After both requests above, the two edge locations and the origin end up holding **different amounts of the same content**:

```mermaid
flowchart LR
    subgraph Origin["Origin — source of truth, holds every variant"]
        O1["1080p · English"]
        O2["1080p · Hindi"]
        O3["4K · English"]
        O4["4K · Hindi"]
    end

    subgraph E1["Edge Location 1"]
        C1["Cached: 1080p · English only"]
    end

    subgraph E2["Edge Location 2"]
        C2["Cached: 4K · Hindi only"]
    end

    E1 -. "cache miss, pulled once" .-> Origin
    E2 -. "cache miss, pulled once" .-> Origin
```

- **Origin** always holds the *full* catalog of variants — it's unaffected by any CloudFront cache configuration, since it's the authoritative source every edge eventually pulls from.
- **Edge Location 1** has only ever seen requests for 1080p/English, so that's the *only* variant it has cached — a Hindi or 4K request arriving at Edge Location 1 for the first time would still be a cache miss there, even though Edge Location 2 already has a 4K/Hindi copy.
- This is why "first request from a given region is a cache miss" (Note 01) applies **per cached variant, per edge location** — not just once globally.

> 🧠 **Mental model:** the cache key is the "address" CloudFront uses to file away a cached response — the narrower the address (path only), the more requests share one cache slot (higher hit ratio, but risk of serving the wrong content for anything actually variable, like the wrong resolution or language above); the wider the address (path + query + headers + cookies), the more precisely correct each cache slot is, at the cost of more cache misses overall — and that trade-off plays out independently at *every* edge location.

---

## 3. Real-world walkthrough: a Netflix-style user journey, end to end

> ⚠️ Real Netflix doesn't actually deliver video through AWS CloudFront — it runs its own purpose-built CDN, **Open Connect** (appliances embedded directly inside ISP networks worldwide). Its account/API/backend services do run substantially on AWS, but video delivery bypasses CloudFront entirely in real life. Netflix is used here purely as a relatable stand-in — every concept below maps 1:1 onto how CloudFront actually behaves, just not onto Netflix's literal infrastructure.

Take a concrete session: a user in **India** opens the Netflix web app, logs in, searches for "Inception" in Hindi, and watches it — while the backend lives in the **US**.

```mermaid
sequenceDiagram
    participant U as User Browser (India)
    participant E as CloudFront Edge — Mumbai
    participant O as Origin / Backend (US)

    Note over U,O: 1. Opens the web app — static UI files
    U->>E: GET /index.html, /main.js, /styles.css
    alt Already cached at this edge (an earlier Indian visitor warmed it)
        E-->>U: LEG 1 - CACHE KEY match, HIT, served in a few ms
    else First hit at this edge
        E->>O: LEG 1 miss, LEG 2 forwarded per ORIGIN REQUEST POLICY
        O-->>E: Static files
        E->>E: Cached, path-only key, updates via versioned filenames
        E-->>U: Served
    end

    Note over U,O: 2. Login — POST, dynamic, NEVER cached
    U->>E: POST /api/login (credentials)
    E->>O: CachingDisabled, LEG 2 always runs, per ORIGIN REQUEST POLICY
    O-->>E: Auth token / session cookie
    E-->>U: Full India to US round trip, every single time

    Note over U,O: 3. Search "Inception" in Hindi — personalized
    U->>E: GET /api/search?q=Inception&lang=hi (+ session cookie)
    E->>O: Ranked by this user's history, CachingDisabled
    O-->>E: Personalized results
    E-->>U: Round trip again — can't be shared across users

    Note over U,O: 4. Watches the movie — video segments
    U->>E: GET /videos/inception/hi/1080p/seg0042.ts
    alt Already cached at this edge
        E-->>U: LEG 1 - CACHE KEY match, HIT, smooth playback
    else First Indian viewer requesting this exact segment
        E->>O: LEG 1 miss, LEG 2 forwarded per ORIGIN REQUEST POLICY
        O-->>E: Video segment
        E->>E: Cached, path already encodes movie, language, quality
        E-->>U: Served
    end
```

### Where the cache key actually matters — and where it doesn't

| Stage | Request | Cacheable? | Cache Policy | Why |
|---|---|---|---|---|
| 1. Open web app | `index.html`, `main.js`, `styles.css` | ✅ Yes | Path-only (`CachingOptimized`) | Identical for every visitor |
| 2. Login | `POST /api/login` | ❌ No | `CachingDisabled` | Mutating, security-sensitive, unique per attempt — nothing to share |
| 3. Search | `GET /api/search?q=...&lang=hi` | **Depends** | `CachingDisabled` if ranked by viewing history; otherwise a custom policy keying on `q` + `lang` | The real fork: identical results for every Hindi searcher of "Inception" → cacheable; personalized per account → not cacheable at the CDN at all, no matter how the key is tuned |
| 4. Watch | `GET /videos/inception/hi/1080p/seg0042.ts` | ✅ Yes | Path-only | Movie/language/quality already baked into the **path** by the encoding pipeline — a plain path-only key already does the right thing |

That table also settles a common point of confusion directly: it's **not only the video** that gets cached — static site files (Stage 1) and video segments (Stage 4) are *both* cached, via **separate cache behaviors** (different path patterns, different policies) on the same distribution — exactly like this folder's `demo-site` default behavior plus [Note 09.01](09.01-Cache-Behavior_Demo.md)'s `/get` behavior. Real streaming systems typically encode the variant in the **URL path** rather than a query string, which is why Stage 4 needs no special Cache Policy tuning at all — a cleaner design than this note's earlier `?res=&lang=` illustration in Sections 1-2.

### Who actually sets the cache key's values?

Two different actors — this is usually the actual source of confusion:

- **Who decides which fields matter** (which query strings/headers/cookies get included) → whoever configures the **Cache Policy** on the distribution. That's done once, as infrastructure, by whoever runs the platform — not per request.
- **Who supplies the actual values on any given request** → the client. The browser/app already sends `Accept-Language: hi-IN` because the device's locale is Hindi, or appends `?lang=hi` because the user picked Hindi audio in the player. CloudFront doesn't invent or inject anything — per the Cache Policy, it only *selects* which of the fields already present in the incoming request get folded into the cache key.

### Why this matters more in India than in the US

Stages 1 and 4 are exactly what a CDN is for: without CloudFront, every static file and every video segment would round-trip India↔US (roughly 400-500ms round trip) — a sluggish UI and constant buffering. A Mumbai edge location means the first Indian viewer eats that round trip once; every viewer after them gets a **Leg 1 Hit** in a few milliseconds. Stages 2 and 3, being genuinely dynamic/personalized, get no such benefit no matter how the Cache Key is tuned — Leg 2 (Section 2) always has to run for them, every time.

---

## 4. Cache Policy — controlling the cache key

A **Cache Policy** (attached to a cache behavior) explicitly declares which of three categories of request data should be included in the cache key. These are the exact dropdown options CloudFront's **Create cache policy** console page (**CloudFront → Policies → Cache → Create cache policy**) gives you for each, under **Cache key settings**:

| Category | Console options (exact dropdown values) | Example |
|---|---|---|
| **Headers** | `None` / `Include the following headers` | e.g. `Accept-Language`, or a custom `X-Resolution` header, to cache a different version per locale or quality level |
| **Query strings** | `None` / `All` / `All query strings except` / `Include the following query strings` | e.g. `Include the following query strings` → `res`, `lang` in the streaming example above |
| **Cookies** | `None` / `All` / `All cookies except` / `Include the following cookies` | e.g. a session/personalization cookie needing its own distinct cache entry per value |

> 🧠 **Note the asymmetry:** Headers only ever get `None` or an explicit allow-list (`Include the following headers`) — there's no `All` option for headers in a cache policy, unlike query strings and cookies. This is a deliberate CloudFront limit: blindly keying on *every* header (many of which vary per-request for reasons that have nothing to do with content, like `User-Agent` or `Referer`) would fragment the cache into near-uselessness. If you genuinely need broad header-based forwarding, that's what the Origin Request Policy (Section 5) is for — it *can* forward `All` headers to the origin, independent of the cache key.

Including `res` and `lang` in the cache key is exactly what makes Section 2's diagram correct — without it, Edge Location 1 and Edge Location 2 would both cache under the same key (`/watch/inception`) and could hand out mismatched quality/language to the next visitor who happens to hit that edge.

Each additional included dimension **increases the number of distinct cached variants** stored — improving correctness (no more wrongly-shared cache entries) but potentially lowering the **cache hit ratio** (more distinct variants means each one is requested less often, so fewer requests find an existing cached copy).

---

## 5. Origin Request Policy — what CloudFront forwards to the origin on a cache miss

Separately, an **Origin Request Policy** controls what CloudFront sends **to the origin** on a cache miss — which can be **broader** than the cache key itself. In the streaming example: the origin needs to know `res` and `lang` on every cache miss to return the correct variant at all — but whether that combination also gets its *own* cache slot at the edge is a completely separate decision, made by the Cache Policy. You could, in principle, forward `res`/`lang` to the origin (Origin Request Policy) while *not* including them in the cache key (Cache Policy) — decoupling "what makes this cacheable as distinct" from "what the origin needs to know to answer the request." (Note 09.01's hands-on demo shows exactly this gap happening live, with a header that's forwarded but not cache-keyed.)

> 🎯 **Exam tip:** "the cache hit ratio is too low because too much varies the cache key" or "users are intermittently seeing the wrong quality/language/version of content" are the two opposite-direction signals this note's settings resolve — too broad a cache key hurts hit ratio; too narrow a cache key (or none at all) risks serving stale/wrong content, exactly like the mismatched-resolution scenario above. The fix is always tuning the **Cache Policy**, with the **Origin Request Policy** handling anything the origin needs but that shouldn't affect caching itself.

---

## 6. Managed policies vs. custom policies

CloudFront ships several **AWS managed** cache policies and origin request policies for common cases (e.g. `CachingOptimized`, `CachingDisabled`, `AllViewer`) — usable directly without authoring your own, exactly parallel to `IAM/02`'s AWS managed IAM policies. A **custom** policy is created when the specific combination of query strings/headers/cookies needed doesn't match any managed option — e.g. "cache key = path + `res` + `lang`" from this note's example has no managed equivalent.

---

## 7. Recap

- Every request has up to **two legs**: Viewer → Edge (governed by the **Cache Key**, decides Hit/Miss) and, only on a Miss, Edge → Origin (governed by the **Origin Request Policy**) — Section 2.
- The **cache key** (governed by a **Cache Policy**) determines which requests are treated as the same cached entry — by default, just the path, which is often too coarse for dynamic content varying by query string, header, or cookie (Section 1's resolution/language example).
- Each **edge location caches independently** — a variant cached at one edge isn't automatically present at another; the same cache-key logic plays out separately, per location, per variant (Section 2).
- A full request-journey walkthrough (Section 3) showed exactly which real-world requests are cacheable (static UI, video segments) versus never cacheable (login, personalized search) — and that the cache key's *values* come from the client, while its *shape* is configured once as infrastructure.
- An **Origin Request Policy** independently controls what's forwarded to the origin on a cache miss, which can be broader than the cache key itself (Section 5).
- Broadening the cache key improves correctness for variable content but can reduce the cache hit ratio — a real trade-off to tune deliberately, not a "more is always better" setting (Section 4).
- Next: [Note 09.01](09.01-Cache-Behavior_Demo.md) — a hands-on demo that makes this exact cache-key vs. origin-request-policy gap directly observable. Then Note 10 — AWS CloudFront Default Cache Behavior: Response Header Policy, controlling what headers actually come back to the viewer.

### Sources
- [Understanding the cache key — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/understanding-the-cache-key.html)
- [Controlling the cache key with a cache policy — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/controlling-the-cache-key.html)
- [Controlling origin requests with an origin request policy — AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/controlling-origin-requests.html)
