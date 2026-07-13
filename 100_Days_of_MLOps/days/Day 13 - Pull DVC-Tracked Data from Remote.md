# Lab Information

A new xFusionCorp Industries team member has cloned the fraud-detection repository onto a fresh machine. The DVC remote is already configured to point at the team's SeaweedFS bucket, but `dvc pull`is failing. Diagnose the cause, correct the configuration, and pull the dataset.


1. A cloned project exists at `/root/code/fraud-detection/` with DVC initialised, the `data/raw/transactions.csv.dvc` pointer file present, but the dataset itself missing from disk and from the local DVC cache.
    
2. SeaweedFS is already running on the controlplane and the dataset has already been pushed to the **dvc-storage** bucket—open the **SeaweedFS Filer** button at the top of the lab and navigate to `/buckets/dvc-storage/` to confirm that the object is there.
    
    - **S3 endpoint:** `http://localhost:8333`
    - **Credentials:** `weedadmin` / `weedadmin123`
3. Review `.dvc/config` and correct everything that prevents `dvc pull` from authenticating against SeaweedFS. 
    

- After the fix, the `s3` remote must use:
    - The access key (`access_key_id`) `weedadmin`
    - The secret key (`secret_access_key`) `weedadmin123`.

1. Pull the dataset. After the pull, `data/raw/transactions.csv` must be present on disk and its content must match the hash recorded in the `.dvc` pointer.

---

# Solution
✅ Part 1: Lab Step-by-Step Guidelines
Navigate to repo

```shell
cd /root/code/fraud-detection/
```

Attempt dvc pull to view error message

```shell
dvc pull
```

Output

```shell
ERROR: failed to connect to s3 (dvc-storage/files/md5) - Unable to locate credentials
```

Add missing credentials to (/root/code/fraud-detection/.dvc/config)

```shell
[core]
    remote = s3

['remote "s3"']
    url = s3://dvc-storage
    endpointurl = http://localhost:8333
    access_key_id = weedadmin
    secret_access_key = weedadmin123
```

Try dvc pull again

```shell
dvc pull
```

Dvc pull was successful 

Output

```shell
Collecting                         |0.00 [00:00,    ?entry/s]
Fetching
Building workspace index           |2.00 [00:00,  681entry/s]
Comparing indexes                 |4.00 [00:00, 3.05kentry/s]
Applying changes                   |1.00 [00:00, 1.18kfile/s]
A       data/raw/transactions.csv
1 file fetched and 1 file added
```

Verify result

```shell
dvc status
```

Output

```shell
Data and pipelines are up to date.
```
# 🧠 Part 2: Simple Step-by-Step Explanation (Beginner Friendly)

**What happened?**

A teammate cloned the Git repository onto a new machine.

Git downloaded:

transactions.csv.dvc

but not:

transactions.csv

because DVC-managed data is stored separately from Git.

**Why is the file missing?**

Git only stores the small pointer file:

transactions.csv.dvc

The actual dataset lives in SeaweedFS:

SeaweedFS Bucket └── dvc-storage

To download it, DVC must connect to the remote storage.

**Why is dvc pull failing?**

The lab says:

Review .dvc/config and correct everything that prevents dvc pull from authenticating.

This means the most likely issue is incorrect credentials.

Required credentials:

access_key_id = weedadmin secret_access_key = weedadmin123

If either value is wrong, DVC cannot access the SeaweedFS bucket.

**What does dvc pull do?**

When you run:

dvc pull

DVC:

Reads transactions.csv.dvc Finds the file hash Connects to SeaweedFS Downloads the matching object Restores: data/raw/transactions.csv

onto your machine


