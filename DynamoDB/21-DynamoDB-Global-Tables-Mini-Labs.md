# 21 - Master DynamoDB Global Tables with These Mini Labs

> Goal: a concrete, hands-on walkthrough turning an existing table into a Global Table, and directly observing cross-Region replication.

---

## 1. Prerequisites

- An existing DynamoDB table (e.g. `Orders`, from earlier notes' examples) in one Region (e.g. `us-east-1`), with **DynamoDB Streams enabled** (required — Note 20).

---

## 2. Mini Lab 1: add a Region replica

1. **DynamoDB console** → select the table → **Global tables** tab → **Create replica**.
2. Choose a second Region (e.g. `ap-south-1`).
3. DynamoDB automatically enables Streams if not already on, copies existing data, and begins bi-directional replication.
4. Wait for the new replica's status to show **Active**.

---

## 3. Mini Lab 2: observe replication

```bash
aws dynamodb put-item --table-name Orders --region us-east-1 \
  --item '{"OrderId": {"S": "500"}, "Status": {"S": "Placed"}}'

# wait a second or two, then check the other Region:
aws dynamodb get-item --table-name Orders --region ap-south-1 \
  --key '{"OrderId": {"S": "500"}}'
```

- The item written in `us-east-1` should appear in `ap-south-1` within roughly a second — direct, hands-on confirmation of Note 20's "typically sub-second" replication claim.

---

## 4. Mini Lab 3: observe multi-active writes

```bash
aws dynamodb put-item --table-name Orders --region ap-south-1 \
  --item '{"OrderId": {"S": "500"}, "Status": {"S": "Shipped"}}'

# check back in the original Region:
aws dynamodb get-item --table-name Orders --region us-east-1 \
  --key '{"OrderId": {"S": "500"}}'
```

- Writing **directly to the second Region** and seeing it propagate back to the first confirms both replicas are genuinely **multi-active** — not a primary/read-replica relationship.

---

## 5. Clean up

- Remove a Region replica from the **Global tables** tab if no longer needed (this deletes that Region's copy of the data, not the whole table, as long as at least one replica remains).

---

## 6. Recap

- Turning an existing table into a Global Table is a few console clicks; both replicas accept **writes directly**, replicating bi-directionally in roughly a second — confirmed hands-on in this lab.
- Next: Note 22 — Must-Know DynamoDB Backup, covering on-demand and continuous backup options.

### Sources
- [Global tables — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GlobalTables.html)
- [Getting started with DynamoDB global tables — AWS docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/globaltables_gettingstarted.html)
