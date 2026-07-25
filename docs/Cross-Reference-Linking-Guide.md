# Guide: Replacing bare "Note N" references with linked topic names

> Use this whenever a folder of numbered study notes (e.g. `Cloudfront_CDN`, `EC2`, `IAM`) has cross-references written as bare numbers — `Note 09`, `Notes 07-10`, `(Note 18)` — and needs them turned into human-readable, clickable links. This is the exact process used to fix `Cloudfront_CDN/` on 2026-07-25.

---

## 1. Why this matters

A human reader doesn't carry note numbers in their head the way an AI does. `See Note 09 for details` forces the reader to go look up what "09" even is. The fix is to name the actual topic **and** link to it, so the reference is self-explanatory without cross-checking a table:

```
Note 09 established the two-leg model.
```
becomes
```
the [Cache Key and Origin Requests](09-Default-Cache-Behavior-Cache-Key-and-Origin-Requests.md) note established the two-leg model.
```

**Do not do this as a mechanical find/replace.** A regex can find the matches, but only reading each sentence tells you whether it's a self-reference, a range, a cross-folder reference, or needs a "note's"/"Section 2" suffix preserved. Every substitution must come from actually reading the sentence it sits in.

---

## 2. Step-by-step process

### Step 1 — Build the topic map for the target folder
List every numbered file in the folder and record its topic name (from its `# NN - Title` H1 heading, not the filename). Include numbered sub-demos (`09.01`, `10.01`, etc.) if present.

```bash
cd "<target-folder>"
for f in [0-9]*.md; do
  n=$(echo "$f" | grep -oE '^[0-9]+(\.[0-9]+)?')
  title=$(grep -m1 '^# ' "$f" | sed -E 's/^# [0-9]+(\.[0-9]+)? - //')
  echo "$n | $title | $f"
done
```

Produce a table like:

| # | Topic | File |
|---|---|---|
| 09 | Cache Key and Origin Requests | 09-Default-Cache-Behavior-Cache-Key-and-Origin-Requests.md |
| 18 | Cache Invalidation | 18-CloudFront-Cache-Invalidation.md |

### Step 2 — Find every bare reference
```bash
grep -rno "Note[s]\? [0-9][0-9]*\(\.[0-9]*\)\?\(-[0-9][0-9]*\)\?\('s\)\?" *.md
```
This also catches ranges (`Notes 07-10`) and possessives (`Note 09's`). Adjust the pattern if the folder uses a different word than "Note" (e.g. "Topic", "Section", "Lab").

### Step 3 — Read each match in full sentence context
For every match, open the file and read the surrounding sentence — do not trust the grep line alone. Classify it as one of:

- **Simple reference** — points to another file's topic. → name + link it.
- **Self-reference** — the file refers to its own number. → replace with **"this note"**, no link.
- **Range** (`Notes 07-10`, `Notes 04-11`) — **spell out every topic in the range individually**, each linked. Never compress a range into "through" phrasing — clarity beats brevity even for long ranges (this was an explicit correction: don't shorten 8-topic ranges either).
- **Cross-folder reference** — the number refers to a file in a *different* top-level folder (e.g. a CloudFront note pointing at an S3 note). → use that repo's existing `Folder/NN (Topic Name)` convention, **no markdown link** (different folder, link would break/be ambiguous). Example: `S3-Simple_Storage_Services/26 (S3 Static Web Hosting)`.
- **Section/possessive suffix** — `Note 09 Section 2`, `Note 10.01's`. → preserve the suffix naturally after the link: `the [Cache Key and Origin Requests](09-...) note's Section 2`.

### Step 4 — Apply substitutions with Edit
Edit file by file, one at a time. Use the file's own H1 topic name as the link text — not a paraphrase, not the filename. Standard phrasing pattern:

```
the [Topic Name](NN-File-Name.md) note
```

Adjust the surrounding grammar (a/the/this, possessive 's, "notes" plural for ranges) so the sentence still reads naturally — this is why it can't be a blind regex substitution.

### Step 5 — Verify
Re-run the same grep from Step 2 across the whole folder — it must return **zero matches** (empty output, exit code 1):
```bash
grep -rno "Note[s]\? [0-9][0-9]*\(\.[0-9]*\)\?\(-[0-9][0-9]*\)\?\('s\)\?" *.md
```
Then spot-read 3-4 of the most heavily-edited files (especially any file with a long recap/summary section listing many other notes) to confirm the sentences still read naturally and no links are broken.

---

## 3. Rules recap (apply in order)

1. Bare number reference → topic name as visible link text: `Note 18` → `the [Cache Invalidation](18-...) note`.
2. Section/possessive suffixes are preserved after the link, not dropped.
3. Ranges are **fully spelled out**, every constituent topic named and linked — no compression regardless of range length.
4. Self-references become **"this note"** — no self-link.
5. Cross-folder references use `Folder/NN (Topic Name)` plain text, no link.
6. Nothing else in the file changes — this is purely a reference-phrasing fix, not a content rewrite.

---

## 4. Scope note

Only touch files that actually contain the bare-number pattern (check with the Step 2 grep first) — don't proactively rewrite files that don't need it. Legacy/consolidated docs that don't use this numbering convention (e.g. a folder's single all-in-one summary file) are typically out of scope; confirm with a scoped grep before including them.
