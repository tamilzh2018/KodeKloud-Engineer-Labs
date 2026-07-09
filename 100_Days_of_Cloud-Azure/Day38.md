## Task: Running Containers on Azure Virtual Machines
The Nautilus DevOps team needs to set up an Azure Virtual Machine (VM) to interact with an Azure Blob Storage container for storing and retrieving data. The team must create a private storage account, configure Blob Storage, and test the functionality.

**Task:**

1. Azure Virtual Machine Setup:
   - The VM named `datacenter-vm` already exists in the East US region.
2. Create a Private Storage Account and Blob Container:
   - Create a storage account named `datacenterstor21516` in the East US region with Locally-redundant storage (LRS).
   - Create a private Blob container named `datacenter-container21516`.
3. Retrieve Storage Account Key:
   - Get the storage account's access key to configure access for the application.
4. Create a Test File:
   - SSH into the VM and create a file named `testfile.txt` in the `/home/azureuser` directory with content: "this is a test file".
5. Upload the File to Blob Storage:
   - Upload the `testfile.txt` file to the Blob container `datacenter-container21516` using the Azure CLI command:
```
az storage blob upload --account-name datacenterstor21516 --account-key <access-key> --container-name datacenter-container21516 --name testfile.txt --file /home/azureuser/testfile.txt
```

---

## Solution

We'll be performing this task using Azure CLI.

### **Step 1: Set Variables**
Define variables for easier management:
```bash
RESOURCE_GROUP=$(az group list --query "[0].name" -o tsv)
STORAGE_ACCOUNT="datacenterstor21516"
CONTAINER="datacenter-container21516"
FILE_NAME="testfile.txt"
VM_NAME="datacenter-vm"
```

### **Step 2: Create the Storage Account**
```bash
az storage account create \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --location "East US" \
  --sku Standard_LRS
```

### **Step 3: Create a Private Blob Container**
```bash
az storage container create \
  --account-name $STORAGE_ACCOUNT \
  --name $CONTAINER \
  --public-access off
```

### **Step 4: Retrieve the Storage Account Access Key**
```bash
az storage account keys list \
  --account-name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --query "[0].value" -o tsv
```
We'll be using this key to upload file to blob storage. 

### **Step 5: Get VM public IP**
```bash
VM_PUBLIC_IP=$(az vm list-ip-addresses \
  --name $VM_NAME \
  --resource-group $RESOURCE_GROUP \
  --query "[0].virtualMachine.network.publicIpAddresses[0].ipAddress" \
  -o tsv)
```

### **Step 6: SSH to VM**
```bash
ssh azureuser@$VM_PUBLIC_IP
```

### **Step 7: Create the test file**
```bash
echo "this is a test file" > /home/azureuser/testfile.txt
```

### **Step 8: Upload the File to Azure Blob Storage**
Replace the `<access-key>` with the key that we'd retrieved in step 5.
```bash
az storage blob upload \
  --account-name datacenterstor21516 \
  --account-key <access-key> \
  --container-name datacenter-container21516 \
  --name testfile.txt \
  --file /home/azureuser/testfile.txt
```
![upload file](assets/day38_01.png)