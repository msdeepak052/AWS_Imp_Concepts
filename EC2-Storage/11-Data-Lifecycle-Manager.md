# 11 - Data Lifecycle Manager

> Goal: stop taking EBS snapshots by hand (Note 08) and automate the whole lifecycle — creation, retention, and deletion — using **Amazon Data Lifecycle Manager (DLM)**, the managed policy engine built exactly for this.

---

## 1. The problem DLM solves

Manually snapshotting volumes (as done in Note 08) doesn't scale and doesn't stay disciplined over time:

- Someone has to remember to take the snapshot **on schedule**, every time, forever.
- Old snapshots pile up forever unless someone also remembers to **delete** them — quietly growing the storage bill.
- There's no consistent policy across a fleet of volumes — different admins might snapshot at different intervals, or forget entirely.

**Data Lifecycle Manager (DLM)** automates all three: **create** snapshots (or AMIs) on a defined schedule, **retain** a defined number/age of them, and **delete** the rest automatically — all driven by policy, not human memory.

> 🧠 **Mental model:** DLM is the same "set a rule, let AWS enforce it continuously" pattern as EC2 Auto Scaling (see `EC2/ASG/01-Introduction-to-Auto-Scaling.md`) — except instead of managing EC2 instance count, it manages the entire lifecycle of your backup snapshots.

---

## 2. What DLM can manage

- **EBS snapshot policies** — scheduled snapshots of individual volumes or **tag-based groups of volumes** (e.g. every volume tagged `Backup: daily`).
- **EBS-backed AMI policies** — scheduled AMI creation from running instances, useful for keeping a rolling set of "golden image" backups of entire instances, not just individual volumes.
- **Cross-Region and cross-account copy** — a policy can automatically copy the resulting snapshot/AMI to another Region (disaster recovery) or share it with another account, right as part of the same automated schedule.

---

## 3. Core building blocks of a DLM policy

| Building block | What it defines |
|---|---|
| **Target resource tags** | Which volumes (or instances, for AMI policies) this policy applies to — DLM finds them by tag, so adding the tag to a new volume automatically brings it under the policy with zero extra config |
| **Schedule** | How often to create a new snapshot/AMI (e.g. every 12 hours, daily, weekly) and at roughly what time |
| **Retention rule** | How many snapshots/AMIs to keep, either by **count** (e.g. keep the last 7) or by **age** (e.g. keep for 30 days) — older ones beyond the rule are deleted automatically |
| **Fast Snapshot Restore integration** | A DLM policy can also enable FSR (Note 10) automatically on the snapshots it creates, for AZs you specify |
| **Cross-Region/cross-account copy rules** | Optional additional actions run right after each scheduled snapshot/AMI is created |

---

## 4. Example policy, in plain terms

*"Every volume tagged `Backup: daily` gets snapshotted once every 24 hours. Keep the 7 most recent snapshots per volume; automatically delete anything older. Copy each new snapshot to `ap-southeast-1` for disaster recovery."*

This single policy, once created, requires no further human action — new volumes just need the `Backup: daily` tag to be included, and old snapshots never need manual cleanup.

---

## 5. Where DLM fits versus doing it yourself

| | Manual snapshots (Note 08) | DLM policy |
|---|---|---|
| Who triggers the snapshot | A human, each time | AWS, on a schedule, automatically |
| Retention/cleanup | Manual — easy to forget, snapshots accumulate | Automatic, based on the retention rule |
| Scales to many volumes | Poorly — one-by-one | Well — tag-based targeting covers new volumes automatically |
| Good for | One-off backups, or the learning exercise in Note 08 | Any real production backup strategy |

> 🎯 **Exam tip:** "automate EBS snapshot creation and retention across many volumes, with minimal ongoing administrative effort" is a near-verbatim description of DLM's purpose — if a question describes wanting a scheduled, self-cleaning snapshot policy without a custom script or Lambda function, DLM is almost always the intended answer over a hand-rolled solution.

---

## 6. Recap

- **DLM** automates the full EBS snapshot/AMI lifecycle: scheduled creation, retention-based cleanup, and optional cross-Region/cross-account copy — all driven by resource tags, not manual action.
- It replaces the "someone has to remember to snapshot and clean up" pattern from Note 08 with a policy AWS enforces continuously, the same philosophy as Auto Scaling applied to backups instead of compute.
- It can also enable Fast Snapshot Restore (Note 10) automatically as part of a policy.
- This closes out the EBS-focused portion of this folder — Note 12 onward shifts to **shared, multi-instance file storage**: EFS, then FSx.

### Sources
- [Amazon Data Lifecycle Manager — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/snapshot-lifecycle.html)
- [Create a snapshot lifecycle policy — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/snapshot-lifecycle.html#dlm-create-snapshot-policy)
- [Amazon EBS-backed AMI lifecycle policies — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ami-lifecycle.html)
