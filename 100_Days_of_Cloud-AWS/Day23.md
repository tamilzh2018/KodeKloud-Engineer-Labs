## Task: : Data Migration Between S3 Buckets Using AWS CLI
As part of a data migration project, the team lead has tasked the team with migrating data from an existing S3 bucket to a new S3 bucket. The existing bucket contains a substantial amount of data that must be accurately transferred to the new bucket. The team is responsible for creating the new S3 bucket and ensuring that all data from the existing bucket is copied or synced to the new bucket completely and accurately. It is imperative to perform thorough verification steps to confirm that all data has been successfully transferred to the new bucket without any loss or corruption.

As a member of the Nautilus DevOps Team, your task is to perform the following:

**Create a New Private S3 Bucket**: Name the bucket `devops-sync-17938`.  
**Data Migration**: Migrate the entire data from the existing `devops-s3-21287` bucket to the new `devops-sync-17938` bucket.  
**Ensure Data Consistency**: Ensure that both buckets have the same data.  
**Use AWS CLI**: Use the AWS CLI to perform the creation and data migration tasks.

---

## Solution

### Step 1: Set variables
```bash
SRC_BUCKET="devops-s3-21287"
DST_BUCKET="devops-sync-17938"
REGION="us-east-1" 
```

### Step 2: Create the new private bucket
```bash
aws s3api create-bucket --bucket "$DST_BUCKET" \
    --region "$REGION"
```

### Step 3: Sync all data from the source to the destination
```bash
aws s3 sync "s3://$SRC_BUCKET" "s3://$DST_BUCKET"
```

### Step 4: Verification — object counts and total sizes
```bash
aws s3 ls "s3://$SRC_BUCKET" --recursive --summarize > /tmp/src_summary.txt
aws s3 ls "s3://$DST_BUCKET" --recursive --summarize > /tmp/dst_summary.txt

echo "===== SOURCE SUMMARY ====="
tail -n 5 /tmp/src_summary.txt

echo "===== DEST SUMMARY ====="
tail -n 5 /tmp/dst_summary.txt
```