# 17 - AWS S3 Server Side Vs Client Side Encryption

> Goal: nail down exactly **where** the encryption/decryption work happens — the axis Note 15 previewed — before Notes 18-22 go deep on each individual server-side method.

---

## 1. Server-side encryption (SSE) — S3 does the work

With any **server-side encryption** method (SSE-S3, SSE-KMS, DSSE-KMS, SSE-C — Notes 18, 19, 21, 22), your application sends **plaintext data over an encrypted HTTPS connection**, and **S3 itself** encrypts it before writing to disk, then decrypts it automatically on every authorized `GetObject` call. Your application never touches the encryption/decryption logic directly.

> 🧠 **Mental model:** server-side encryption is like handing a courier company your unsealed letter (over a trusted, sealed transport truck — HTTPS) and trusting **them** to lock it away safely and unlock it again for you on request. You don't manage the lock — they do.

---

## 2. Client-side encryption — you do the work, before it ever leaves

With **client-side encryption**, your application encrypts the data **itself, locally**, before ever sending it to S3 — typically using the **AWS Encryption SDK** or the **Amazon S3 Encryption Client**, with a key you generate and manage (optionally via KMS, but the encryption *operation* happens on your side, not S3's). S3 receives and stores **already-encrypted bytes** and has no awareness that encryption happened at all — to S3, it's just an opaque blob.

> 🧠 **Mental model:** client-side encryption is sealing the letter yourself, in a locked box, **before** it ever reaches the courier — the courier (S3) never even has the ability to see inside, encrypted or not; they're just storing a sealed box.

---

## 3. Side-by-side comparison

| | Server-side encryption | Client-side encryption |
|---|---|---|
| Who performs encrypt/decrypt | S3 (or KMS, for the key operations) | Your own application code |
| Does S3 ever see plaintext? | Yes, momentarily, during the encrypt/decrypt operation on S3's side | **Never** — S3 only ever sees ciphertext |
| Implementation effort | Low — often just a request header or bucket default | Higher — requires integrating an SDK and managing key access in your application |
| Typical driver | "Encrypt data at rest, let AWS manage the mechanics" | "We need cryptographic certainty that AWS itself never has access to plaintext, or we need to encrypt before transit for reasons beyond just S3" |

> 🎯 **Exam tip:** "the data must be encrypted before it ever leaves the application, and AWS should never have access to the plaintext or the encryption keys in any form" is the signature **client-side encryption** scenario — this is a meaningfully stronger trust boundary than any server-side method, since even SSE-C (Note 22, where you supply the key) still has S3 performing the actual encrypt/decrypt operation momentarily with access to plaintext during that operation.

---

## 4. Why server-side is still the overwhelming default choice

Server-side encryption (in one of its four flavors, Notes 18-22) is sufficient for the vast majority of compliance and security requirements, and is dramatically simpler to implement and operate — no custom encryption code, no client-side key management infrastructure, and full compatibility with every S3 feature (lifecycle rules, replication, console browsing) that expects to interact with objects normally. Client-side encryption is reserved for the specific cases in Section 3's "typical driver" — often driven by a specific compliance mandate or an explicit zero-trust requirement toward the storage provider itself.

---

## 5. Recap

- **Server-side encryption**: S3 (with KMS, depending on method) performs the encrypt/decrypt work — simple, and the default choice for nearly every use case.
- **Client-side encryption**: your application encrypts data **before** it reaches S3, using the AWS Encryption SDK or S3 Encryption Client — S3 never sees plaintext or manages keys at all.
- Next: Note 18 — AWS S3 Server Side Encryption (SSE-S3), the first and simplest of the four server-side methods.

### Sources
- [Protecting data with encryption — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingEncryption.html)
- [Client-side data encryption — AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingClientSideEncryption.html)
- [AWS Encryption SDK — AWS docs](https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/introduction.html)
