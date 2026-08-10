## Task: Integrating Virtual Machines with Application Load Balancer
The Nautilus DevOps team is currently working on setting up a simple application on the Azure cloud. They aim to establish an Azure Load Balancer in front of a Virtual Machine (VM) where an Nginx server is currently running. While the Nginx server currently serves a sample page, the team plans to deploy the actual application later.

1. Set up an Azure Load Balancer named `nautilus-lb`.
2. Configure the Load Balancer's frontend IP configuration with the name `nautilus-lb-ip` and assign a public IP address with the same name (`nautilus-lb-ip`).
3. Create a backend pool named `nautilus-backend-pool` and add the VM running Nginx to this pool.
4. Create a health probe named `nautilus-health-probe` on port `80` to check the VM's health.
5. Set up a load balancer rule named `nautilus-lb-rule` to route traffic on port `80` to the backend pool on port `80`.
6. Add an inbound rule to the existing NSG of the VM to allow HTTP traffic on port `80`.

---

## Solution

### **Step 1: Log in to Azure Portal**
Go to the Azure Portal:  
https://portal.azure.com  
Sign in with the credentials provided.

### **Step 2: Identify the Existing VM**
Before creating the load balancer, identify the VM running Nginx:
- In the search bar, type **Virtual machines**
- Select **Virtual machines** from the list
- Note the VM name, resource group, and region (you'll need these details)
- Click on the VM to view its details
- Note the **Virtual network** and **Subnet** the VM is in  
![identify vm](assets/day33_01.png)

### **Step 3: Create Public IP Address**
First, create the public IP address for the load balancer frontend:
- In the search bar, type **Public IP addresses**
- Select **Public IP addresses**
- Click **+ Create**

**Create public IP address:**
- **Resource group:** Select the same resource group as your VM
- **Region:** Select the same region as your VM
- **Name:** `nautilus-lb-ip`
- **IP Version:** `IPv4`
- **SKU:** `Standard` 
- **Tier:** `Regional`

Click **Review + create** → **Create**

### **Step 4: Search for Load Balancers**
- In the top search bar, type **Load balancers**
- Select **Load balancers** from the list

### **Step 5: Create New Load Balancer**
- Click **+ Create**

### **Step 6: Configure Load Balancer Basics**
**Basics Tab:**

**Project details:**
- **Resource group:** Select the same resource group as your VM

**Instance details:**
- **Name:** `nautilus-lb`
- **Region:** Select the same region as your VM 
- **SKU:** `Standard`
- **Type:** `Public`
- **Tier:** `Regional`  
![lb basics](assets/day33_02.png)

### **Step 7: Configure Frontend IP**
**Frontend IP configuration Tab:**

- Click **+ Add a frontend IP configuration**

**Add frontend IP configuration:**
- **Name:** `nautilus-lb-ip`
- **IP version:** `IPv4`
- **IP type:** `IP address`
- **Public IP address:** Select `nautilus-lb-ip` (the one created earlier)

### **Step 8: Configure Backend Pool**
**Backend pools Tab:**

- Click **+ Add a backend pool**

**Add backend pool:**
- **Name:** `nautilus-backend-pool`
- **Virtual network:** Select the virtual network where your VM is located
- **Backend Pool Configuration:** `NIC`
- **IP Version:** `IPv4`

**Virtual machines:**
- Click **+ Add** under Virtual machines
- Select your VM running Nginx by checking the checkbox
- Click **Add**

### **Step 9: Configure Load Balancing Rule**
**Inbound rules Tab:**

Under **Load balancing rules** section:
- Click **+ Add a load balancing rule**

**Add load balancing rule:**
- **Name:** `nautilus-lb-rule`
- **IP Version:** `IPv4`
- **Frontend IP address:** Select `nautilus-lb-ip`
- **Backend pool:** Select `nautilus-backend-pool`
- **Protocol:** `TCP`
- **Port:** `80`
- **Backend port:** `80`
- **Health probe:** Create new
  - **Name:** `nautilus-health-probe`
  - **Protocol:** `HTTP`
  - **Port:** `80`
  - **Path:** `/` (default)
  - **Interval:** `5` (seconds)
- **Session persistence:** `None`
- **Idle timeout (minutes):** `4` (default)

### **Step 10: Review and Create Load Balancer**
Leave other options as default and review all settings:
- **Name:** `nautilus-lb`
- **Frontend IP:** `nautilus-lb-ip`
- **Backend pool:** `nautilus-backend-pool`
- **Health probe:** `nautilus-health-probe`
- **Load balancing rule:** `nautilus-lb-rule`  
![review lb](assets/day33_03.png)

Click **Create**

### **Step 11: Add NSG Inbound Rule for HTTP Traffic**
Now, add an inbound rule to the VM's Network Security Group to allow HTTP traffic:
- Go to **Virtual machines**
- Select your VM running Nginx
- In the left menu under **Settings**, click **Networking**
- Click on **Network settings** or the NSG name

### **Step 12: Create Inbound Security Rule**
Once in the NSG:
- In the left menu under **Settings**, click **Inbound security rules**
- Click **+ Add**

**Add inbound security rule:**
- **Source:** `Any`
- **Source port ranges:** `*`
- **Destination:** `Any`
- **Service:** `HTTP`
- **Destination port ranges:** `80` 
- **Protocol:** `TCP`
- **Action:** `Allow`
- **Priority:** `100` 
- **Name:** `Allow-HTTP-80`
- **Description:** `Allow HTTP traffic on port 80`

Click **Add**

### **Step 13: Verify NSG Rule**
Verify the inbound security rule was created:
- You should see `Allow-HTTP-80` in the list of inbound security rules
- **Priority:** 100
- **Port:** 80
- **Protocol:** TCP
- **Action:** Allow  
![verify nsg rule](assets/day33_04.png)

### **Step 14: Test Load Balancer - Get Public IP**
Go back to the Load Balancer:
- Navigate to **Load balancers** → **nautilus-lb**
- In the **Overview** page, find the **Frontend IP address** 
- Note the **Public IP address** of `nautilus-lb-ip`  
![get lb ip](assets/day33_05.png)

### **Step 15: Test Load Balancer via Browser**
Open a web browser and you should see the default nginx page.

# CLI
# Get Rg
az group list
az vm list -g MyResourceGroup -d
# Set these if you know them; otherwise discover them below.
RG="<RESOURCE_GROUP>"
VM="<NGINX_VM_NAME>"

# Discover the VM's NIC
NIC_ID=$(az vm show -g "$RG" -n "$VM" \
  --query "networkProfile.networkInterfaces[0].id" -o tsv)

NIC_NAME=$(basename "$NIC_ID")

# Discover the existing NSG attached to the NIC
NSG_ID=$(az network nic show -g "$RG" -n "$NIC_NAME" \
  --query "networkSecurityGroup.id" -o tsv)

NSG_NAME=$(basename "$NSG_ID")

# Create the public IP
az network public-ip create \
  --resource-group "$RG" \
  --name devops-lb-ip \
  --sku Standard \
  --allocation-method Static

# Create the public Load Balancer, frontend configuration,
# and backend pool
az network lb create \
  --resource-group "$RG" \
  --name devops-lb \
  --sku Standard \
  --public-ip-address devops-lb-ip \
  --frontend-ip-name devops-lb-ip \
  --backend-pool-name devops-backend-pool

# Add the VM's NIC/IP configuration to the backend pool
IPCONFIG_NAME=$(az network nic show -g "$RG" -n "$NIC_NAME" \
  --query "ipConfigurations[0].name" -o tsv)

az network nic ip-config address-pool add \
  --resource-group "$RG" \
  --nic-name "$NIC_NAME" \
  --ip-config-name "$IPCONFIG_NAME" \
  --lb-name devops-lb \
  --address-pool devops-backend-pool

# Create HTTP health probe on port 80
az network lb probe create \
  --resource-group "$RG" \
  --lb-name devops-lb \
  --name devops-health-probe \
  --protocol Http \
  --port 80 \
  --path /

# Create HTTP load-balancing rule: frontend 80 -> backend 80
az network lb rule create \
  --resource-group "$RG" \
  --lb-name devops-lb \
  --name devops-lb-rule \
  --protocol Tcp \
  --frontend-port 80 \
  --backend-port 80 \
  --frontend-ip-name devops-lb-ip \
  --backend-pool-name devops-backend-pool \
  --probe-name devops-health-probe

# Allow HTTP/80 through the VM's EXISTING NSG
az network nsg rule create \
  --resource-group "$RG" \
  --nsg-name "$NSG_NAME" \
  --name Allow-HTTP-80 \
  --protocol Tcp \
  --direction Inbound \
  --source-address-prefixes Internet \
  --source-port-ranges '*' \
  --destination-address-prefixes '*' \
  --destination-port-ranges 80 \
  --access Allow \
  --priority 100

# Verify
az network lb show \
  --resource-group "$RG" \
  --name devops-lb \
  --query "{name:name,frontend:frontendIpConfigurations[0].name,backend:backendAddressPools[0].name}"

az network lb probe show \
  --resource-group "$RG" \
  --lb-name devops-lb \
  --name devops-health-probe

az network lb rule show \
  --resource-group "$RG" \
  --lb-name devops-lb \
  --name devops-lb-rule

az network lb address-pool show \
  --resource-group "$RG" \
  --lb-name devops-lb \
  --name devops-backend-pool

az network public-ip show \
  --resource-group "$RG" \
  --name devops-lb-ip \
  --query ipAddress -o tsv

Then browse to the returned public IP with http://<PUBLIC_IP>. The Nginx sample page should be served through lb.