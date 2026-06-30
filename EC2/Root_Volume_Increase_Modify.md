# Root Volume increase/modify in EC2 instances

Here is a **complete, step-by-step guide** for increasing the root volume of an EC2 instance (Linux/Ubuntu) from start to finish, including **AWS Console, CLI, partition resize, and filesystem expansion**. This is **production-safe** and works without stopping the instance.

---

# **Increase EC2 Root Volume – Full Steps**

## **Step 0: Verify current instance and root volume**

1. Find instance ID and root volume:

   * **AWS Console → EC2 → Instances → Your Instance → Storage**
   * Note **Volume ID** (e.g., `vol-0ce3f8866f952377e`) and device name (`/dev/xvda1`)

2. **Check filesystem and partition in the instance (Linux):**

```bash
lsblk -f
df -h /
```

---

## **Step 1: Modify the EBS root volume**

### **Option A: AWS Console**

1. **EC2 → Volumes → Select root volume**
2. Click **Actions → Modify volume**
3. Enter **new size** (e.g., 20 GB)
4. Click **Modify**, then **Yes** to confirm

### **Option B: AWS CLI**

```bash
aws ec2 modify-volume --volume-id <volume-id> --size <new-size-in-GB>
```

Example:

```bash
aws ec2 modify-volume --volume-id vol-0ce3f8866f952377e --size 20
```

**Check progress:**

```bash
aws ec2 describe-volumes-modifications --volume-ids vol-0ce3f8866f952377e
```

* Wait until `"ModificationState": "completed"`

---

## **Step 2: Resize the partition**

> On Linux, the filesystem won’t see the new space until the partition is resized.

1. **Install `cloud-guest-utils` (for `growpart`):**

```bash
sudo apt update
sudo apt install cloud-guest-utils -y
```

2. **Resize the partition:**

```bash
sudo growpart /dev/xvda 1
```

* `/dev/xvda` → disk
* `1` → partition number (`xvda1`)

3. **Verify partition size:**

```bash
lsblk
```

* Partition `/dev/xvda1` should now match the EBS volume size.

---

## **Step 3: Resize the filesystem**

1. **Check filesystem type:**

```bash
lsblk -f
```

* Typically `ext4` for Ubuntu, Amazon Linux 2

2. **Resize filesystem:**

* **ext4**:

```bash
sudo resize2fs /dev/xvda1
```

* **xfs** (Amazon Linux 2 default):

```bash
sudo xfs_growfs -d /
```

3. **Verify filesystem size:**

```bash
df -h /
```

* Should show full expanded size (e.g., 20 GB)

---

## **Step 4: Verify everything**

```bash
lsblk
df -h /
```

* Root partition should match the EBS volume size
* Free space should increase according to new volume size

---

## **Optional: One-liner command sequence for Ubuntu**

```bash
sudo apt update -y && sudo apt install cloud-guest-utils -y && sudo growpart /dev/xvda 1 && sudo resize2fs /dev/xvda1 && df -h /
```

* This installs `growpart`, resizes the partition, resizes filesystem, and shows updated usage.

---

## **Notes & Best Practices**

* No need to stop the instance.
* Backup critical data before resizing (snapshot recommended).
* You **can increase** the size only; cannot shrink EBS volumes.
* This procedure works for **Ubuntu, Amazon Linux, and other Linux distros** with `ext4` or `xfs`.

---

