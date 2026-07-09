## Task: Working with Azure Table Storage
The Nautilus DevOps team is developing a simple 'To-Do' application using Azure Table Storage to store and manage tasks efficiently. The team needs to create an Azure Table to hold tasks, each identified by a unique `taskId`. Each task will have a description and a status, which indicates the progress of the task (e.g., 'completed' or 'in-progress').

Your task is to:

1. Create an Azure Storage Account named `xfusiontablest7199` with a Table Storage table called `tasks`.
2. Insert the following tasks into the table:
   - Task 1: PartitionKey: `tasks`, RowKey: `1`, description: `Learn Table Storage`, status: `completed`
   - Task 2: PartitionKey: `tasks`, RowKey: `2`, description: `Build To-Do App`, status: `in-progress`
3. Verify that **Task 1** has a status of `completed` and **Task 2** has a status of `in-progress`.

**Note:** Use the Azure CLI to insert these tasks into the table.

---

## Solution

We'll be performing this task using Azure CLI.

### **Step 1: Set Variables**
Define variables for easier management:
```bash
RESOURCE_GROUP=$(az group list --query "[0].name" -o tsv)
STORAGE_ACCOUNT="xfusiontablest7199"
```

### **Step 2: Create the Azure Storage Account**
```bash
az storage account create \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --location "East US" \
  --sku Standard_LRS
```

### **Step 3: Create a Table Named `tasks`**
```bash
az storage table create \
  --name tasks \
  --account-name $STORAGE_ACCOUNT
```

### **Step 4: Insert Task 1**
```bash
az storage entity insert \
  --account-name $STORAGE_ACCOUNT \
  --table-name tasks \
  --entity PartitionKey=tasks RowKey=1 description="Learn Table Storage" status=completed
```

### **Step 5: Insert Task 2**
```bash
az storage entity insert \
  --account-name $STORAGE_ACCOUNT \
  --table-name tasks \
  --entity PartitionKey=tasks RowKey=2 description="Build To-Do App" status="in-progress"
```

### **Step 6: Verify Task Statuses**
Check Task 1
```bash
az storage entity show \
  --account-name $STORAGE_ACCOUNT \
  --table-name tasks \
  --partition-key tasks \
  --row-key 1
```
Check Task 2
```bash
az storage entity show \
  --account-name $STORAGE_ACCOUNT \
  --table-name tasks \
  --partition-key tasks \
  --row-key 2
```
Verify that the statuses are **"completed"** and **"in-progress"** for **Task 1** and **Task 2** respectively.
