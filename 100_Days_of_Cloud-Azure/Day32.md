## Task: Synchronizing Containers Using the CLI
As part of a data migration project, the team lead has tasked the team with migrating data from an existing Azure Blob container to a new Blob container. The existing container contains a substantial amount of data that must be accurately transferred to the new container. The team is responsible for creating the new Blob container and ensuring that all data from the existing container is copied or synced to the new container completely and accurately. It is imperative to perform thorough verification steps to confirm that all data has been successfully transferred to the new container without any loss or corruption.

As a member of the Nautilus DevOps Team, your task is to perform the following:

1. **Create a New Private Azure Blob Container:** Name the container `devops-dest-30033` under the storage account `devopsst24503`.
2. **Data Migration:** Migrate the file `devops.txt` from the existing `devops-source-14774` container to the new `devops-dest-30033` container.
3. **Ensure Data Consistency:** Ensure that both containers have the file `devops.txt` and confirm the file content is identical in both containers.
4. **Use Azure CLI:** Use the Azure CLI to perform the creation and data migration tasks.

---

## Solution

### **Step 1: Set Variables**
Define variables for easier management:
```bash
# Set variables
STORAGE_ACCOUNT="devopsst24503"
SOURCE_CONTAINER="devops-source-14774"
DEST_CONTAINER="devops-dest-30033"
FILE_NAME="devops.txt"
```

### **Step 2: Verify Storage Account Exists**
Verify that the storage account `devopsst24503` exists:
```bash
# Check specific storage account
az storage account show --name $STORAGE_ACCOUNT --output table
```

### **Step 3: Verify Source Container Exists**
Check that the source container `devops-source-14774` exists:
```bash
# List all containers in the storage account
az storage container list \
  --account-name $STORAGE_ACCOUNT \
  --output table
```

### **Step 4: Verify Source File Exists**
Confirm that `devops.txt` exists in the source container:
```bash
# List blobs in source container
az storage blob list \
  --account-name $STORAGE_ACCOUNT \
  --container-name $SOURCE_CONTAINER \
  --output table
```

### **Step 5: Download and View Source File Content**
Download the source file to verify its content:
```bash
# Download the source file
az storage blob download \
  --account-name $STORAGE_ACCOUNT \
  --container-name $SOURCE_CONTAINER \
  --name $FILE_NAME \
  --file ~/devops-source.txt

# View the content
cat ~/devops-source.txt
```

### **Step 6: Create New Destination Container**
Create the new private container `devops-dest-30033`:
```bash
# Create destination container with private access
az storage container create \
  --account-name $STORAGE_ACCOUNT \
  --name $DEST_CONTAINER \
  --public-access off

# Verify container was created
az storage container show \
  --account-name $STORAGE_ACCOUNT \
  --name $DEST_CONTAINER \
  --output table
```

### **Step 7: List All Containers to Confirm**
Verify both source and destination containers exist:
```bash
# List all containers
az storage container list \
  --account-name $STORAGE_ACCOUNT \
  --output table
```

You should see both `devops-source-14774` and `devops-dest-30033` in the list.

### **Step 8: Copy File from Source to Destination**
Copy the file from the source container to the destination container:
```bash
# Copy blob from source to destination
az storage blob copy start \
  --account-name $STORAGE_ACCOUNT \
  --destination-container $DEST_CONTAINER \
  --destination-blob $FILE_NAME \
  --source-container $SOURCE_CONTAINER \
  --source-blob $FILE_NAME
```

### **Step 9: Download Destination File**
Download the file from the destination container:
```bash
# Download the destination file
az storage blob download \
  --account-name $STORAGE_ACCOUNT \
  --container-name $DEST_CONTAINER \
  --name $FILE_NAME \
  --file ~/devops-dest.txt

# View the content
cat ~/devops-dest.txt
```

### **Step 10: Verify Data Integrity with MD5 Hash**
Compare the MD5 hashes of both files to ensure data integrity:
```bash
# Get MD5 hash of both files
echo "Source file MD5:"
md5sum ~/devops-source.txt

echo "Destination file MD5:"
md5sum ~/devops-dest.txt
```

**The MD5 hashes must be identical!**
