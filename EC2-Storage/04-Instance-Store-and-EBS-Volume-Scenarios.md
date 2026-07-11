# 04 - Instance Store & EBS Volume Scenarios

> Goal: apply Notes 02-03's trade-offs to the kind of "which storage would you pick" scenario questions the exam actually asks, so the theory turns into fast, confident answers.

---

## 1. The decision test to run in your head

For any scenario, ask two questions in order:

1. **If this data disappeared right now, would it matter?**
   - No (it's a cache, a buffer, temp/scratch data, or already durably replicated elsewhere) → Instance Store is on the table.
   - Yes → EBS (or a managed data service) is required.
2. **Does more than one instance need to read/write this data at the same time?**
   - No → a single EBS volume is enough.
   - Yes → neither Instance Store nor a plain EBS volume is the right primary answer — that's EFS/FSx (or S3, or a managed database) territory, covered later in this folder.

---

## 2. Worked scenarios

### Scenario A — Temporary buffer for a video transcoding pipeline
*"Instances pull raw video segments from S3, transcode them locally, then upload results back to S3. The local working files aren't needed once the job completes."*
→ **Instance Store.** The data is disposable, already durably sourced from (and returned to) S3, and the workload benefits from Instance Store's high, consistent local IOPS/throughput during the transcode step. Losing an in-flight job on instance failure just means re-running that job from S3 — acceptable and cheap.

### Scenario B — Relational database data files on a single EC2 instance
*"A self-managed MySQL instance stores its data files on local disk. The company cannot afford to lose this data if the instance is stopped or the underlying host fails."*
→ **EBS**, ideally with an IOPS-appropriate volume type (Note 05) and a regular snapshot schedule (Notes 08, 11). This is exactly the CloudMart capstone's `cloudmart-db-1` pattern — and exactly why that pattern is named as an HA gap: even with EBS's durability, there's still only one instance/volume, so a real production system would move to RDS Multi-AZ instead.

### Scenario C — In-memory cache tier that rebuilds itself from a database
*"A fleet of cache-server instances holds frequently-read data to reduce database load. If an instance restarts, the cache simply refills from the database on the next few requests."*
→ **Instance Store** (or even no persistent disk at all beyond the root volume) is fine — the "source of truth" lives elsewhere, so losing a cache instance's local data is a performance blip, not data loss.

### Scenario D — Boot volume for a fleet that needs to stop/start on a schedule to save cost
*"Dev/test instances are stopped every night and started every morning to save money, and must come back with the exact same OS/data state."*
→ Must be **EBS-backed** — an Instance Store-backed (or instance-store-root) instance cannot be stopped and later started with data intact; it can only be rebooted or terminated. This is one of the clearest exam signals for "EBS root volume required."

### Scenario E — Shared configuration files read by 6 web servers behind a load balancer
*"All instances in the frontend Auto Scaling group need to read (and occasionally write) the same set of files at the same time."*
→ Neither Instance Store nor a single EBS volume works here (an EBS volume is normally attached to one instance at a time). This is the use case that motivates **EFS** — covered starting in Note 12.

---

## 3. Quick-reference table

| Signal in the question | Points to |
|---|---|
| "temporary", "scratch", "cache", "buffer", "can be regenerated/re-sourced" | Instance Store |
| "must survive a stop", "must survive instance/host failure", "durable", "database", "cannot lose this data" | EBS |
| "needs to be stopped and started on a schedule" | EBS-backed root volume (mandatory) |
| "shared by multiple instances simultaneously", "same files", "NFS" | EFS or FSx (not Instance Store or a single EBS volume) |
| "highest possible IOPS, data loss acceptable" | Instance Store |

> 🎯 **Exam tip:** when a question emphasizes durability requirements (or explicitly says data must survive an instance stop or a hardware failure), Instance Store is almost always a distractor answer — its entire appeal (raw speed, free) is also its entire risk (zero durability), and SAA-C03 tests whether you notice that trade-off rather than just picking "the fastest option."

---

## 4. Recap

- Two-question test: **(1)** does losing the data matter? **(2)** do multiple instances need it simultaneously? Those two answers alone resolve almost every Instance-Store-vs-EBS-vs-shared-storage scenario.
- Instance Store fits disposable, regenerable, or already-replicated-elsewhere data needing maximum local performance.
- EBS fits anything that must survive a stop, a terminate (with Delete on Termination off), or a host hardware fault, for a single instance.
- Shared, multi-instance-simultaneous access needs EFS or FSx, not either of these — previewed here, detailed starting at Note 12.
- Next: Note 05 — EBS Volume Type SSD, going deep on gp2/gp3/io1/io2.

### Sources
- [Amazon EC2 instance store — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/InstanceStorage.html)
- [Amazon EBS volumes — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volumes.html)
- [Amazon EFS use cases — AWS docs](https://docs.aws.amazon.com/efs/latest/ug/use-cases.html)
