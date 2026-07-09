# Day 98: Launch EC2 in Private VPC Subnet Using Terraform

## Task Overview

Build a complete private network infrastructure in AWS using Terraform, including a custom VPC, private subnet, security group with VPC-scoped access rules, and an EC2 instance. This architecture creates an isolated environment where resources can only communicate within the VPC, enhancing security for internal applications and services.

**Technical Specifications:**
- VPC name: datacenter-priv-vpc (CIDR: 10.0.0.0/16)
- Subnet name: datacenter-priv-subnet (CIDR: 10.0.1.0/24, private)
- EC2 instance name: datacenter-priv-ec2 (t2.micro)
- Security group: VPC-only access (no public internet ingress)
- Auto-assign public IP: Disabled
- Region: us-east-1

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Navigate to the Terraform working directory

```sh
cd /home/bob/terraform
```

Change to the Terraform working directory where you'll create a comprehensive network infrastructure configuration. This directory will contain all files for the VPC, subnet, security group, and EC2 instance.

**Step 2:** Create the variables.tf file

```sh
# Create variables.tf file in VS Code or text editor
# Right-click under EXPLORER section and select "New File"
# Name it: variables.tf
```

Create a variables file to define network CIDR blocks and naming prefix. Using variables makes the network configuration flexible and reusable for different environments.

**Step 3:** Define variables in variables.tf

```hcl
variable "KKE_VPC_CIDR" {
    default = "10.0.0.0/16"
}

variable "KKE_SUBNET_CIDR" {
    default = "10.0.1.0/24"
}

variable "prefix" {
    default = "datacenter-priv"
}
```

Define three variables for network configuration. The `KKE_VPC_CIDR` sets the VPC's IP address range - `10.0.0.0/16` provides 65,536 IP addresses (10.0.0.0 to 10.0.255.255). The `KKE_SUBNET_CIDR` defines the subnet's range - `10.0.1.0/24` provides 256 addresses (10.0.1.0 to 10.0.1.255), though AWS reserves 5 addresses leaving 251 usable. The `prefix` variable provides a consistent naming prefix across all resources, making them easily identifiable and organized.

**Step 4:** Create the main.tf file

```sh
# Create main.tf file in VS Code or text editor
# Name it: main.tf
```

Create the main configuration file where you'll define all infrastructure resources including VPC, subnet, security group, ingress/egress rules, AMI data source, and EC2 instance.

**Step 5:** Define VPC resource in main.tf

```hcl
resource "aws_vpc" "vpc" {
    cidr_block = var.KKE_VPC_CIDR

    tags = {
        Name = "${var.prefix}-vpc"
    }
}
```

Create a VPC with the specified CIDR block. The VPC serves as an isolated virtual network in AWS where you have complete control over networking configuration. The `cidr_block` parameter uses the variable to set the IP range. String interpolation (`${var.prefix}-vpc`) combines the prefix with `-vpc` to create the name `datacenter-priv-vpc`. This VPC has no internet gateway attached by default, making it truly private.

**Step 6:** Define private subnet in main.tf

```hcl
resource "aws_subnet" "subnet" {
    cidr_block = var.KKE_SUBNET_CIDR
    vpc_id = aws_vpc.vpc.id
    map_public_ip_on_launch = false

    tags = {
        Name = "${var.prefix}-subnet"
    }
}
```

Create a subnet within the VPC that functions as a private network segment. The `cidr_block` must fall within the VPC's CIDR range. The `vpc_id` references the VPC created in the previous step, establishing an implicit dependency so Terraform creates the VPC first. The critical setting `map_public_ip_on_launch = false` ensures EC2 instances launched in this subnet receive only private IP addresses, never public ones. This enforces the private nature of the subnet and prevents direct internet access.

**Step 7:** Define security group in main.tf

```hcl
resource "aws_security_group" "sg" {
    vpc_id = aws_vpc.vpc.id
    name = "${var.prefix}-sg"
    description = "Security group for EC2 instance"

    tags = {
        Name = "${var.prefix}-sg"
    }
}
```

Create a security group within the VPC to control network traffic to EC2 instances. The `vpc_id` associates this security group with the custom VPC (not the default VPC). The security group name and description provide context about its purpose. Unlike default security groups, this starts with no rules - you'll add specific rules in the following steps.

**Step 8:** Add HTTP ingress rule (VPC-only) in main.tf

```hcl
resource "aws_vpc_security_group_ingress_rule" "allow_http" {
    security_group_id = aws_security_group.sg.id
    from_port = 80
    to_port = 80
    ip_protocol = "tcp"
    cidr_ipv4 = var.KKE_VPC_CIDR
}
```

Define an ingress rule allowing HTTP traffic on port 80, but only from sources within the VPC's CIDR range. The `cidr_ipv4 = var.KKE_VPC_CIDR` restricts access to the VPC's IP range (10.0.0.0/16), meaning only resources within the same VPC can access this port. This prevents any external internet traffic from reaching the instance, even if it somehow obtained a public IP. The rule uses TCP protocol and allows port 80 for HTTP communication between VPC resources.

**Step 9:** Add SSH ingress rule (VPC-only) in main.tf

```hcl
resource "aws_vpc_security_group_ingress_rule" "allow_ssh" {
    security_group_id = aws_security_group.sg.id
    from_port = 22
    to_port = 22
    ip_protocol = "tcp"
    cidr_ipv4 = var.KKE_VPC_CIDR
}
```

Define an ingress rule allowing SSH access on port 22, restricted to the VPC's CIDR range. Like the HTTP rule, this permits SSH connections only from other resources within the VPC (10.0.0.0/16). You cannot SSH to this instance from the internet - access would require a bastion host, VPN connection, or AWS Systems Manager Session Manager. This security measure prevents unauthorized remote access while allowing internal administration.

**Step 10:** Add egress rule for outbound traffic in main.tf

```hcl
resource "aws_vpc_security_group_egress_rule" "allow_all_outbound" {
    security_group_id = aws_security_group.sg.id
    from_port = 0
    to_port = 0
    ip_protocol = "-1"
    cidr_ipv4 = "0.0.0.0/0"
}
```

Define an egress rule allowing all outbound traffic from the instance to any destination. The `ip_protocol = "-1"` means all protocols (TCP, UDP, ICMP, etc.), and `from_port = 0, to_port = 0` with protocol -1 means all ports. The `cidr_ipv4 = "0.0.0.0/0"` allows outbound connections to any IP address. This enables the instance to make outbound requests for software updates, API calls, or database connections. Note that even with this rule, the instance cannot reach the internet without a NAT Gateway or NAT instance because the subnet is private.

**Step 11:** Define AMI data source in main.tf

```hcl
data "aws_ami" "amazon_linux" {
    most_recent = true
    owners = ["amazon"]

    filter {
        name = "name"
        values = ["amzn2-ami-hvm-*-x86_64-ebs"]
    }
}
```

Create a data source to automatically find the latest Amazon Linux 2 AMI. Data sources query existing AWS resources without creating them. The `most_recent = true` parameter ensures you get the newest AMI matching the criteria. The `owners = ["amazon"]` limits results to official Amazon AMIs. The filter searches for AMI names matching the pattern `amzn2-ami-hvm-*-x86_64-ebs`, which represents Amazon Linux 2 with HVM virtualization for x86_64 architecture backed by EBS storage. This approach eliminates hardcoding AMI IDs, which vary by region and become outdated.

**Step 12:** Define EC2 instance in main.tf

```hcl
resource "aws_instance" "ec2" {
    subnet_id = aws_subnet.subnet.id
    instance_type = "t2.micro"
    vpc_security_group_ids = [aws_security_group.sg.id]
    ami = data.aws_ami.amazon_linux.id

    tags = {
        Name = "${var.prefix}-ec2"
    }
}
```

Create an EC2 instance in the private subnet with the security group and AMI from previous steps. The `subnet_id` places the instance in the private subnet, ensuring it receives only a private IP. The `instance_type = "t2.micro"` provides minimal compute resources (1 vCPU, 1GB RAM) suitable for testing. The `vpc_security_group_ids` (note the plural) takes a list of security group IDs - here just one. The `ami` references the data source to use the latest Amazon Linux 2 image. All these references create implicit dependencies, ensuring Terraform creates resources in the correct order.

**Step 13:** Create the outputs.tf file

```sh
# Create outputs.tf file in VS Code or text editor
# Name it: outputs.tf
```

Create an outputs file to display resource names after deployment. The task specifically requires certain output variable names for validation.

**Step 14:** Define outputs in outputs.tf

```hcl
output "KKE_vpc_name" {
    value = aws_vpc.vpc.tags["Name"]
}

output "KKE_subnet_name" {
    value = aws_subnet.subnet.tags["Name"]
}

output "KKE_ec2_private" {
    value = aws_instance.ec2.tags["Name"]
}
```

Define three outputs with specific names required by the task. Each output extracts the Name tag from the respective resource. The `aws_vpc.vpc.tags["Name"]` accesses the tags map and retrieves the Name value. These outputs display after `terraform apply` completes, showing: `KKE_vpc_name = "datacenter-priv-vpc"`, `KKE_subnet_name = "datacenter-priv-subnet"`, and `KKE_ec2_private = "datacenter-priv-ec2"`.

**Step 15:** Initialize the Terraform project

```sh
terraform init
```

Initialize the Terraform working directory, downloading the AWS provider plugin and preparing for resource creation. This command recognizes all resource types and data sources used in your configuration.

**Step 16:** Preview the infrastructure changes

```sh
terraform plan
```

Generate an execution plan showing all resources that will be created. You should see 8 resources: VPC, subnet, security group, 2 ingress rules, 1 egress rule, and EC2 instance. The data source (AMI lookup) won't appear in the count but will be queried. Review the plan to verify CIDR blocks, names, and security group rules are correct.

**Step 17:** Apply the Terraform configuration

```sh
terraform apply -auto-approve
```

Execute the plan to create all resources in AWS. Terraform creates resources in dependency order: VPC → subnet → security group → rules → EC2 instance. The AMI data source is queried before instance creation. The process takes 1-2 minutes for the EC2 instance to fully initialize. Upon completion, Terraform displays the three outputs showing resource names.

**Step 18:** Verify resource creation and outputs

```bash
# Verify all resources were created
terraform state list

# Show detailed EC2 instance information
terraform state show aws_instance.ec2

# Display outputs
terraform output

# Verify instance has only private IP (no public IP)
terraform output -json | grep -i ip
```

Verify successful deployment using these commands. The `terraform state list` should show 8 managed resources plus the data source. The `terraform state show aws_instance.ec2` command displays the instance's attributes - verify it has a `private_ip` but no `public_ip` attribute (or public_ip is empty). The `terraform output` displays the three required output values confirming correct resource naming.

---

## Key Concepts

**Private VPC Architecture:**
- VPC without internet gateway attachment = truly private network
- Resources cannot receive inbound connections from internet
- Outbound internet requires NAT Gateway/Instance (not included here)
- Ideal for databases, internal applications, backend services
- Enhanced security through network isolation

**Private vs Public Subnets:**
- **Private Subnet:** No route to internet gateway, instances get private IPs only
- **Public Subnet:** Has route to internet gateway, can assign public IPs
- `map_public_ip_on_launch = false` enforces private subnet behavior
- Private subnets require NAT for outbound internet access
- Use private subnets for databases, app servers, internal services

**CIDR Block Planning:**
- VPC CIDR: /16 = 65,536 addresses (recommended for flexibility)
- Subnet CIDR: /24 = 256 addresses (251 usable after AWS reservation)
- Subnet CIDR must be subset of VPC CIDR
- AWS reserves first 4 and last IP in each subnet
- Plan for growth: leave room for additional subnets

**VPC-Scoped Security Groups:**
- Security groups are VPC-specific resources
- Restricting to VPC CIDR (10.0.0.0/16) allows internal-only access
- More secure than 0.0.0.0/0 (all internet)
- Enables micro-segmentation within VPC
- Combine with security group references for tighter control

**Security Group Rules:**
- **Ingress:** Inbound traffic control (who can connect to instance)
- **Egress:** Outbound traffic control (where instance can connect)
- Stateful: Return traffic automatically allowed
- Protocol -1 = all protocols (ICMP, TCP, UDP, etc.)
- Port 0 with protocol -1 = all ports

**Data Sources in Terraform:**
- Query existing AWS resources without creating them
- `data "aws_ami"` finds AMIs matching criteria
- `most_recent = true` gets latest version
- Eliminates hardcoding region-specific AMI IDs
- Filters support wildcards for flexible matching

**Resource Dependencies:**
- VPC → Subnet (subnet needs VPC ID)
- VPC → Security Group (SG needs VPC ID)
- Security Group → Ingress/Egress Rules (rules need SG ID)
- Subnet + AMI + SG → EC2 Instance (instance needs all three)
- Terraform automatically orders creation based on references

**AWS Reserved IPs in Subnets:**
- First IP: Network address (10.0.1.0)
- Second IP: VPC router (10.0.1.1)
- Third IP: DNS server (10.0.1.2)
- Fourth IP: Future use (10.0.1.3)
- Last IP: Broadcast address (10.0.1.255)
- Usable IPs in /24: 251 (256 - 5 reserved)

**Accessing Private Instances:**
- **Bastion Host:** Jump server in public subnet
- **VPN Connection:** Site-to-site or client VPN to VPC
- **AWS Systems Manager:** Session Manager (no SSH required)
- **Direct Connect:** Dedicated network connection
- **VPC Peering:** Connect from another VPC

**NAT Gateway Considerations:**
- Required for private instances to reach internet
- Enables outbound connections for updates, API calls
- Does NOT allow inbound connections from internet
- Placed in public subnet with Elastic IP
- Costs apply based on usage and data transfer

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 97](day-97.md) | [Day 99 →](../week-15/day-99.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
