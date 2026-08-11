## Task: Enabling Internet Connectivity for Virtual Machines
The Nautilus DevOps team has encountered an issue with an Azure VM named `devops-vm`. They are unable to install any packages on this VM due to connectivity issues. The team needs to identify the root cause of the problem and resolve it to restore normal operations.

1. Investigate the connectivity issue preventing package installation on the Azure VM `devops-vm`.
2. Implement a solution to resolve the connectivity issue and restore package installation capabilities on the VM.

**Note:** The SSH key required to access the Azure VM is already created and added to the VM's authorized keys. You can find the SSH key at `/root/.ssh/id_rsa` on the `azure-client` host.

---

## Solution

### **Step 1: Log in to Azure Portal**
Go to the Azure Portal:  
https://portal.azure.com  
Sign in with the credentials provided.

### **Step 2: Locate the VM**
- In the search bar, type **Virtual machines**
- Select **Virtual machines** from the list
- Find and click on **devops-vm**

### **Step 3: Get VM Public IP Address**
On the VM overview page:
- Note the **Public IP address** of the VM  
![vm ip](assets/day34_01.png)

### **Step 4: Attempt SSH Connection from azure-client**
From the `azure-client` host, try to SSH into the VM:
```bash
# Attempt SSH connection
ssh -i /root/.ssh/id_rsa azureuser@<vm_public_IP>
```

You should to able to connect to the VM via SSH.

### **Step 5: Initial Connectivity Test**
Once connected to the VM, test basic connectivity:
```bash
# Test DNS resolution
nslookup google.com

# Test internet connectivity
ping -c 4 8.8.8.8
```
![connectivity test](assets/day34_02.png)

Seems to be some issue with internet connectivity. There can many reasons for it, one of which is Security Group rules.

### **Step 6: Investigate Network Security Group (NSG)**
In Azure Portal:
- Go to **Virtual machines** → **devops-vm**
- In the left menu under **Settings**, click **Networking** or **Network settings**
- Review the **Network security group** associated with the VM

### **Step 7: Check Outbound Security Rules**
- Click on the dropdown beside **Network Security Group** name
- Review all outbound rules  
![outbound rules](assets/day34_03.png)

**Issue:** There seems to be a **Deny All** outbound rule. Delete that rule.

### **Step 8: Test Connectivity Again**
From the `azure-client` host's terminal test if connectivity is restored:
```bash
ping -c 4 8.8.8.8
```
![test connectivity restored](assets/day34_04.png)

Should be successful now.

### **Step 9: Update Package Lists**
Try updating the package lists:
```bash
sudo apt update
```

### **Step 10: Install a Test Package**
Verify package installation works:
```bash
# Install a small test package
sudo apt install -y net-tools
```

# CLI
**Get Public IP**
az group list
az vm list -g MyResourceGroup
az network public-ip list -g MyResourceGroup

**Connect the VM**
ssh -i /root/.ssh/id_rsa <username>@<VM_PUBLIC_IP>

# Basic connectivity
ip route
cat /etc/resolv.conf
getent hosts archive.ubuntu.com || getent hosts packages.microsoft.com

# Test HTTPS package-repository connectivity
curl -I --connect-timeout 5 https://archive.ubuntu.com
curl -I --connect-timeout 5 https://packages.microsoft.com

# Identify the package-manager error
sudo apt-get update

**The key things I'm looking for are: to know the VM has a public IP and its NIC is attached to datacenter-nsg**

DNS failure → incorrect DNS configuration.
No default route → routing/UDR problem.
HTTPS timeout/refusal while other connectivity works → likely an NSG outbound rule blocking TCP/443.
apt-get update reaching the repository but failing with proxy errors → proxy configuration.
NSG appears permissive but no Internet access → check whether the subnet/NIC has a public/NAT path and whether a route table is forcing traffic elsewhere.

# Check NSG's outbound rules any deny rule set and the subnet's route table
az network nsg rule list \
  -g MyResourceGroup \
  --nsg-name datacenter-nsg \
  --query "[].{name:name,direction:direction,access:access,priority:priority,protocol:protocol,src:sourceAddressPrefix,dst:destinationAddressPrefix,dstPort:destinationPortRange}" \
  -o table
**Delete deny rules**
az network nsg rule delete \
  -g MyResourceGroup  \
  --nsg-name datacenter-nsg \
  -n Block-All-Outbound
