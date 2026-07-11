# 38 - AWS S3 Multipart Upload (Hands-On)

> Goal: perform a real multipart upload — splitting a large file into independently-uploaded parts — and see exactly why Note 08's "abort incomplete multipart uploads" lifecycle action exists, by observing what an abandoned upload actually leaves behind.

---

## 1. Why multipart upload exists

Recall from Note 02: a single `PUT` request is capped at **5 GB**, and any object can be up to **5 TB**. **Multipart upload** is the mechanism that closes this gap — a large file is split into **parts** (each 5 MB - 5 GB, except the last part, which can be smaller), uploaded **independently** (potentially in parallel, potentially with retries per-part), then S3 assembles them into one final object once every part is confirmed received.

> 🧠 **Mental model:** instead of mailing one enormous, fragile package that has to arrive perfectly intact in one attempt, multipart upload mails several smaller, independently-trackable boxes — if one box gets lost or damaged in transit, you only need to resend *that* box, not the entire shipment.

---

## 2. Benefits beyond just "getting past the size limit"

- **Improved throughput**: parts can be uploaded **in parallel**, from one or even multiple network connections, rather than one long sequential stream.
- **Resilience to network interruptions**: if uploading a single part fails, only that one part needs to be retried — not the whole object.
- **AWS recommends multipart upload for any object over ~100 MB**, even though the hard technical requirement only kicks in above 5 GB — the parallelism and resilience benefits matter well before the size limit forces your hand.

---

## 3. The three-step API flow

```bash
# 1. Initiate — get an UploadId
aws s3api create-multipart-upload --bucket demo-bucket --key bigfile.zip
# returns an "UploadId"

# 2. Upload each part, referencing the UploadId and a part number
aws s3api upload-part --bucket demo-bucket --key bigfile.zip \
  --part-number 1 --body part1.bin --upload-id <UploadId>
aws s3api upload-part --bucket demo-bucket --key bigfile.zip \
  --part-number 2 --body part2.bin --upload-id <UploadId>

# 3. Complete — S3 assembles all parts into the final object
aws s3api complete-multipart-upload --bucket demo-bucket --key bigfile.zip \
  --upload-id <UploadId> --multipart-upload file://parts-manifest.json
```

In practice, the AWS CLI's high-level `aws s3 cp`/`aws s3 sync` commands **automatically** use multipart upload behind the scenes for large files — you rarely need to call these low-level API steps by hand except when integrating custom upload logic (e.g. a browser-based direct upload using presigned URLs per part, Note 35).

---

## 4. What an abandoned multipart upload leaves behind

1. Start a multipart upload and successfully upload one or two parts (Section 3, steps 1-2).
2. **Don't** call `complete-multipart-upload` — simulate a crashed client.
3. Check:
   ```bash
   aws s3api list-multipart-uploads --bucket demo-bucket
   ```
   The in-progress upload (and its already-uploaded parts) still shows up — and **those uploaded parts are billed as storage**, even though no complete, listable object was ever created. This is exactly the scenario Note 08's `AbortIncompleteMultipartUpload` lifecycle action exists to clean up automatically.
4. Manually clean it up instead:
   ```bash
   aws s3api abort-multipart-upload --bucket demo-bucket --key bigfile.zip --upload-id <UploadId>
   ```

---

## 5. S3 Transfer Acceleration and multipart upload work together

Note 31's Transfer Acceleration applies to multipart upload parts too — a large file being multipart-uploaded from a distant client benefits from **both** optimizations simultaneously: faster network routing (Transfer Acceleration) and parallel, resumable part uploads (multipart) — the two features are complementary, not alternatives.

> 🎯 **Exam tip:** "uploads of large files (over 100 MB, or approaching/exceeding 5 GB) are slow or unreliable over an unstable connection" is the signature **multipart upload** scenario. Combine with "clients are geographically distant" and Transfer Acceleration (Note 31) becomes relevant too — the two are frequently tested together as a combined answer.

---

## 6. Recap

- **Multipart upload** splits a large object into independently-uploaded, resumable parts, required above 5 GB and recommended above ~100 MB, with S3 assembling the final object once all parts complete.
- Abandoned (never-completed) multipart uploads leave **billed, orphaned parts** behind — cleaned up either manually (`abort-multipart-upload`) or automatically via Note 08's lifecycle rule.
- Works alongside Transfer Acceleration (Note 31) for large uploads from distant clients.
- Next: Note 39 — AWS VPC Gateway Endpoint For S3 (Hands-On), keeping traffic between a VPC and S3 off the public internet entirely.

### Sources
- [Uploading and copying objects using multipart upload — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html)
- [Multipart upload overview — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html)
