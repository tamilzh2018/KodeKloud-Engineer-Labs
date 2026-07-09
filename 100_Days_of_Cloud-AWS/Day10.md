## Task: Attach Elastic IP to EC2 Instance
The Nautilus DevOps team has been creating a couple of services on AWS cloud. They have been breaking down the migration into smaller tasks, allowing for better control, risk mitigation, and optimization of resources throughout the migration process. Recently they came up with requirements mentioned below.

There is an instance named `nautilus-ec2` and an elastic-ip named `nautilus-ec2-eip` in `us-east-1` region. Attach the `nautilus-ec2-eip` elastic-ip to the `nautilus-ec2` instance.

---

## Solution

### **Step 1: Log in to AWS Management Console**
Sign in with the credentials provided.

### **Step 2: Navigate to Elastic IPs**
- In the left navigation panel, scroll down to the **Network & Security** section
- Click on **Elastic IPs**
- You will see a list of all Elastic IPs in the **us-east-1** region

### **Step 3: Locate the nautilus-ec2-eip Elastic IP**
- Find the Elastic IP named `nautilus-ec2-eip` in the list
- You can use the search/filter bar to quickly find it:
  - Type `nautilus-ec2-eip` in the search box
  - Or filter by the Name tag
- Click on the Elastic IP to select it (checkbox on the left)  
![Locate Elastic IP](assets/day10_01.png)

### **Step 4: Initiate Association**
With the `nautilus-ec2-eip` Elastic IP selected:
- Click the **Actions** dropdown button (top right)
- Select **Associate Elastic IP address**  
![Associate Elastic IP Menu](assets/day10_02.png)

### **Step 5: Configure Association Settings**
The **Associate Elastic IP address** dialog will appear with configuration options:
- Click on the **Instance** dropdown
- Search for or select `nautilus-ec2` from the list  
- Click **Associate**  
![Select Instance](assets/day10_03.png)

**IMPORTANT:** The instance should be in the **running** state for successful association. If stopped, start it first.  

### **Step 6: Verify Association from Instance View**
Navigate to the EC2 instance to verify from the other side:
- Click on **Instances** in the left navigation panel
- Select or click on the `nautilus-ec2` instance
- In the **Details** tab, check:
  - **Public IPv4 address:** Should now show the Elastic IP address (e.g., 23.23.148.97)
