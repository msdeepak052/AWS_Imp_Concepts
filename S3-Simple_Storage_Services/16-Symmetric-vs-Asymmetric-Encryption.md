# 16 - AWS S3 Encryption Part 2 — Symmetric Vs Asymmetric Encryption

> Goal: a cryptography-fundamentals detour — understanding **symmetric vs. asymmetric encryption** in general — needed before Notes 19-21's KMS-based methods make full sense, since AWS KMS supports both key types for different purposes.

---

## 1. Symmetric encryption — one key, both directions

**Symmetric encryption** uses the **same single key** to both encrypt and decrypt data. Whoever has the key can do either operation.

- **Fast and efficient** — well suited to encrypting large volumes of data quickly, which is exactly why it's what actually encrypts your object data under the hood in S3 (via AES-256), regardless of which SSE method (S3, KMS, C) manages the key.
- **The catch**: the key must be shared between whoever encrypts and whoever decrypts, which means securely **distributing and protecting that one key** becomes the central challenge.

> 🧠 **Mental model:** symmetric encryption is like a single physical key that both locks and unlocks the same padlock — simple and fast, but you have to get a copy of that exact key to anyone who legitimately needs to open the lock, and protect it carefully so no one else does.

---

## 2. Asymmetric encryption — a key pair, different roles

**Asymmetric encryption** uses a **mathematically linked pair of keys** — a **public key** (safe to share with anyone) and a **private key** (kept secret). Data encrypted with the public key can only be decrypted with the matching private key (or vice versa, for signing use cases).

- **Slower** than symmetric encryption for large data volumes — computationally more expensive.
- **Solves the key-distribution problem** — you can freely publish the public key; only the private key holder can ever decrypt, so there's no need to secretly transmit a shared secret ahead of time.
- Commonly used for: digital signatures, TLS/HTTPS handshake setup, and — relevant to KMS — certain specialized encryption/decryption or signing operations where the *encrypting* party shouldn't need decrypt access.

> 🧠 **Mental model:** asymmetric encryption is like a public mailbox with a slot anyone can drop mail into (the public key), but only the one person with the physical key to the mailbox (the private key) can take mail back out.

---

## 3. Why this matters for AWS KMS specifically

**AWS KMS** (used by SSE-KMS, Note 19, and DSSE-KMS, Note 21) supports creating both **symmetric** and **asymmetric** KMS keys:

| | Symmetric KMS key | Asymmetric KMS key |
|---|---|---|
| Typical use in S3 context | The default and standard choice for SSE-KMS/DSSE-KMS — matches how S3 actually encrypts object data (AES-256, symmetric) | Rare for direct S3 object encryption; used for specific signing/verification workflows, or when an external party needs to encrypt using a public key without ever being granted decrypt access |
| Key material ever leaves AWS KMS? | No — even the key's owner can only ask KMS to encrypt/decrypt *using* it, never export the raw key | The private key portion also never leaves KMS; only the public key can be exported/shared |

> 🎯 **Exam tip:** "an external partner needs to encrypt data destined for us, but should never be able to decrypt anything" is the signature **asymmetric key** scenario — give them the **public key** only. For the vast majority of "encrypt this S3 bucket's contents" scenarios (Notes 19-21), a standard **symmetric** KMS key is what's actually being described, since that's what SSE-KMS defaults to and is built around.

---

## 4. Recap

- **Symmetric encryption**: one shared key for both encrypt and decrypt — fast, but requires secure key distribution. This is what actually encrypts S3 object data under the hood (AES-256), regardless of which SSE method manages the key.
- **Asymmetric encryption**: a public/private key pair — slower, but solves the distribution problem and enables use cases like signing or one-way encryption without ever granting decrypt rights.
- **AWS KMS supports both** key types; SSE-KMS/DSSE-KMS (Notes 19, 21) default to and are built around **symmetric** keys.
- Next: Note 17 — AWS S3 Server Side Vs Client Side Encryption, returning to the S3-specific question of *where* encryption actually happens.

### Sources
- [AWS KMS concepts — symmetric and asymmetric keys — AWS docs](https://docs.aws.amazon.com/kms/latest/developerguide/symm-asymm-concepts.html)
- [Using symmetric and asymmetric keys — AWS docs](https://docs.aws.amazon.com/kms/latest/developerguide/symmetric-asymmetric.html)
