# 07 - EBS (Hands-On)

> Goal: create an extra EBS volume, attach it to a running EC2 instance, format and mount it, then prove it survives a stop/start — turning Notes 02-06's theory into something you've actually clicked through.

---

## 1. Prerequisites

- One running EC2 instance (Amazon Linux 2023, any small type like `t3.micro` is fine) in any VPC/subnet you can reach via **Session Manager** (no SSH/key pair needed, matching this repo's no-SSH convention from the CloudMart capstone).
- Note which **Availability Zone** the instance is in — an EBS volume can only attach to an instance in the **same AZ**.

---

## 2. Create a new EBS volume

1. **EC2 console** → **Elastic Block Store** → **Volumes** → **Create volume**.
2. **Volume type**: `gp3` (the default/recommended General Purpose SSD from Note 05).
3. **Size**: `10` GiB.
4. **Availability Zone**: must exactly match your instance's AZ.
5. Leave IOPS/throughput at their gp3 defaults (3,000 IOPS / 125 MiB/s baseline).
6. **Create volume**.

---

## 3. Attach the volume to the instance

1. Select the new volume → **Actions** → **Attach volume**.
2. **Instance**: choose your running instance.
3. **Device name**: accept the suggested value (e.g. `/dev/sdf`) → **Attach volume**.

> 🧠 On Nitro-based instances (most current generations), the device name you specify is a hint, not a guarantee — the OS may expose it as an NVMe device (e.g. `/dev/nvme1n1`) instead. Always confirm the actual device name from inside the instance (Section 4) rather than assuming the name you typed at attach time.

---

## 4. Connect, format, and mount the volume

1. **EC2 console** → select the instance → **Connect** → **Session Manager** → **Connect**.
2. Confirm the new (unformatted) volume is visible:
   ```bash
   lsblk
   ```
   You should see the root volume (already mounted at `/`) plus a new, unmounted block device with no filesystem.
3. Create a filesystem on it (replace `nvme1n1` with whatever `lsblk` actually showed):
   ```bash
   sudo mkfs -t xfs /dev/nvme1n1
   ```
4. Mount it:
   ```bash
   sudo mkdir /data
   sudo mount /dev/nvme1n1 /data
   ```
5. Write a test file:
   ```bash
   echo "hello from the attached EBS volume" | sudo tee /data/test.txt
   ```

> ⚠️ A mount performed this way does **not** survive a reboot by itself — without an `/etc/fstab` entry, the device will still exist and still hold its data after a reboot, but it won't automatically remount at `/data`. For this hands-on exercise that's fine (you'll remount manually to verify persistence in Section 6); a production setup would add a proper `/etc/fstab` line instead.

---

## 5. Resize the volume live (no downtime)

One of EBS's most useful properties: you can grow a volume's size, IOPS, or throughput **while it's still attached and in use**, with no need to detach or stop the instance first.

1. **Volumes** → select your volume → **Actions** → **Modify volume**.
2. Change **Size** from `10` to `15` GiB → **Modify**.
3. Wait for the volume's state to show **optimizing** then **completed** (this can take anywhere from a few minutes to longer, depending on original size).
4. Back in the Session Manager terminal, the OS still sees the old size until you extend the filesystem onto the new space:
   ```bash
   sudo growpart /dev/nvme1n1 1        # only if the volume uses a partition table
   sudo xfs_growfs /data               # extends the XFS filesystem to fill the new space
   df -h /data
   ```

---

## 6. Prove persistence across stop/start (contrast with Instance Store, Note 02)

1. **Instance state** → **Stop instance**. Wait for it to fully reach **Stopped**.
2. **Instance state** → **Start instance**. Wait for **Running**, then reconnect via Session Manager.
3. Remount and check the file is still there:
   ```bash
   sudo mount /dev/nvme1n1 /data
   cat /data/test.txt
   ```
   The file survives — exactly the behavior Note 02 predicted for EBS, in contrast to Instance Store, which would have lost this data on the same stop/start cycle.

---

## 7. Detach and clean up

1. Unmount first: `sudo umount /data`.
2. **Volumes** → select the volume → **Actions** → **Detach volume**.
3. Once detached, **Actions** → **Delete volume** if you no longer need it (a detached volume keeps billing until deleted).

---

## 8. Troubleshooting

| Symptom | Likely cause |
|---|---|
| Volume attach fails / instance not selectable | Volume and instance are in **different Availability Zones** — EBS volumes can only attach within the same AZ |
| `lsblk` doesn't show the new device | Attachment is still in progress, or you're looking at the wrong device name — re-run `lsblk` after a few seconds |
| `mount` fails with "wrong fs type" | The volume was never formatted — run `mkfs` (Section 4, step 3) before mounting |
| Resized volume's filesystem doesn't reflect new size | You resized the **volume** but didn't extend the **filesystem** — always run the OS-level `growpart`/`xfs_growfs` (or `resize2fs` for ext4) step after modifying the volume |

---

## 9. Recap

- Created a `gp3` EBS volume, attached it to a running instance in the same AZ, formatted it, and mounted it — the standard extra-data-volume workflow.
- Resized the volume live (no detach/stop needed) and extended the filesystem to match.
- Proved EBS data survives a stop/start cycle, the direct hands-on confirmation of Note 02's theory.
- Next: Note 08 — EBS Snapshot Backup (Hands-On), backing this same volume up to a point-in-time snapshot.

### Sources
- [Amazon EBS volumes — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volumes.html)
- [Attach an Amazon EBS volume to an instance — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-attaching-volume.html)
- [Make an Amazon EBS volume available for use — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-using-volumes.html)
- [Modify an Amazon EBS volume — AWS docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/requesting-ebs-volume-modifications.html)
