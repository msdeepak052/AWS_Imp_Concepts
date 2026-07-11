# 03 - AWS S3 Storage Class — Part 1

> Goal: cover the core, general-purpose storage classes — **Standard**, **Standard-IA**, **One Zone-IA**, and **Intelligent-Tiering** — the trade-off between availability/durability and cost that every S3 storage decision comes down to. Part 2 (Note 04) covers Express One Zone; Part 3 (Note 05) covers the Glacier/archive family.

---

## 1. The trade-off every storage class makes

Every S3 storage class balances the same handful of dimensions against each other: **durability**, **availability** (uptime SLA), **number of AZs data is spread across**, **retrieval speed**, and **cost** (both per-GB storage price and any retrieval fees). Cheaper almost always means either lower availability, fewer AZs, or a retrieval delay/fee — never a free lunch.

> 🧠 **Mental model:** think of these classes as a dial between "instantly available, unlimited retrievals, priciest per GB" and "cheapest per GB, but slower or costlier to actually get the data back out" — you pick a point on that dial based on **how often you'll actually read this data**.

---

## 2. S3 Standard

- **Durability**: 99.999999999% (11 nines) — data is redundantly stored across a **minimum of 3 Availability Zones**.
- **Availability**: 99.99% SLA.
- **Retrieval**: milliseconds, no retrieval fee, no minimum storage duration.
- **Use case**: frequently accessed data — the **default** choice, and the right one whenever access patterns are unknown or genuinely frequent.

---

## 3. S3 Standard-IA (Infrequent Access)

- Same 11-nines durability and multi-AZ (3+ AZ) spread as Standard — **only availability and cost model differ**, not durability.
- **Availability**: 99.9% SLA (slightly lower than Standard).
- **Lower per-GB storage cost** than Standard, but adds a **per-GB retrieval fee** every time you read an object, plus a **minimum storage duration of 30 days** (delete or transition an object before 30 days and you're still billed as if it stayed the full 30).
- **Use case**: data accessed **infrequently but needs to be available immediately when it is** — backups, disaster recovery files, older data still occasionally queried.

---

## 4. S3 One Zone-IA

- Same infrequent-access cost/retrieval profile as Standard-IA, but stored in **only one Availability Zone** instead of 3+.
- **~20% cheaper** than Standard-IA, in exchange for losing AZ-level redundancy — if that one AZ is destroyed, the data is gone.
- **Use case**: infrequently accessed data that's **easily recreatable** or already durably stored elsewhere (e.g. a secondary copy of on-premises data, or data you could regenerate) — never for your only copy of anything irreplaceable.

> ⚠️ One Zone-IA is the first storage class in this note that gives up multi-AZ durability entirely — the same "is losing this actually a problem?" question from `EC2-Storage/04`'s Instance Store scenarios applies here too.

---

## 5. S3 Intelligent-Tiering

- Automatically **monitors access patterns per object** and moves objects between tiers for you — no lifecycle rule authoring needed (contrast with Note 07-08's manual lifecycle rules).
- Built-in tiers (from most to least frequently accessed): **Frequent Access**, **Infrequent Access** (after 30 days with no access), **Archive Instant Access** (after 90 days), and optional, opt-in **Archive Access** and **Deep Archive Access** tiers (after a configurable 90-180+ days) for even deeper savings.
- **No retrieval fees at all**, regardless of tier — the trade-off instead is a small **monthly per-object monitoring/automation fee**.
- **Use case**: **unknown or changing** access patterns — exactly the situation where manually picking Standard vs. IA vs. One Zone-IA would require guessing wrong some of the time.

> 🎯 **Exam tip:** "access patterns are unknown, unpredictable, or likely to change over time, and we don't want to manage lifecycle rules by hand" is the textbook **Intelligent-Tiering** scenario — it's the answer whenever the question is explicitly about *not knowing* the access pattern, as opposed to a known, stated one (which points to Standard, IA, or archive classes directly).

---

## 6. Side-by-side comparison

| Class | AZs | Retrieval time | Retrieval fee | Min. storage duration | Use case |
|---|---|---|---|---|---|
| **Standard** | 3+ | Milliseconds | None | None | Frequently accessed, default choice |
| **Standard-IA** | 3+ | Milliseconds | Per-GB | 30 days | Infrequent, but immediate access needed |
| **One Zone-IA** | 1 | Milliseconds | Per-GB | 30 days | Infrequent, re-creatable/non-critical data |
| **Intelligent-Tiering** | 3+ (or 1, if Archive tiers used) | Milliseconds (Frequent/Infrequent/Archive Instant); hours (opt-in Archive tiers) | None | None | Unknown/changing access patterns |

---

## 7. Recap

- Every S3 storage class trades cost against availability, AZ redundancy, and retrieval speed/fees — never durability alone within the "Standard family" covered here (all keep 11 nines; One Zone-IA trades AZ count, not the underlying durability model).
- **Standard** = default, frequent access. **Standard-IA** = infrequent but immediate, multi-AZ. **One Zone-IA** = infrequent, immediate, single-AZ, cheaper, riskier. **Intelligent-Tiering** = let AWS figure out the right tier automatically, for unknown/changing patterns.
- Next: Note 04 — S3 Storage Class, Part 2: S3 Express One Zone, the newer, high-performance single-AZ tier built for a very different goal than the IA classes above.

### Sources
- [Amazon S3 storage classes — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html)
- [Amazon S3 Intelligent-Tiering — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/intelligent-tiering-overview.html)
- [Amazon S3 pricing — AWS](https://aws.amazon.com/s3/pricing/)
