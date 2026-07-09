# Day 94: Create VPC Using Terraform

## Task Overview

Provision an AWS Virtual Private Cloud (VPC) using Terraform infrastructure-as-code. This establishes an isolated virtual network environment in AWS cloud where you can launch AWS resources with complete control over your networking configuration.

**Technical Specifications:**
- Resource type: AWS VPC (Virtual Private Cloud)
- Region: us-east-1 (US East - N. Virginia)
- VPC name: devops-vpc
- Network configuration: IPv4 CIDR block
- Infrastructure tool: Terraform (declarative IaC)

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Navigate to the Terraform working directory

```sh
cd /home/bob/terraform
```

Change to the designated Terraform working directory where all infrastructure code will be stored. This directory serves as the root location for Terraform configuration files, state files, and provider plugins. Keeping all Terraform files in a dedicated directory helps maintain organized infrastructure code and allows Terraform to properly track resource state.

**Step 2:** Create the main Terraform configuration file

```sh
# Create main.tf file using VS Code or any text editor
# Right-click under EXPLORER section in VS Code and select "New File"
# Name it: main.tf
```

Create the primary Terraform configuration file named `main.tf` in your working directory. This file will contain all resource definitions for your infrastructure. Terraform reads all `.tf` files in the directory, but using `main.tf` as the primary file is a widely adopted convention that makes your infrastructure code immediately recognizable to other engineers.

**Step 3:** Define the AWS VPC resource in main.tf

```hcl
resource "aws_vpc" "myvpc" {
    cidr_block = "10.0.0.0/16"

    tags = {
        Name = "devops-vpc"
    }
}
```

Define an AWS VPC resource using HashiCorp Configuration Language (HCL). The `resource` block specifies the resource type (`aws_vpc`) and a local identifier (`myvpc`) used within Terraform to reference this resource. The `cidr_block` parameter defines the IP address range for your VPC using CIDR notation - `10.0.0.0/16` provides 65,536 IP addresses (10.0.0.0 through 10.0.255.255). The `tags` block assigns metadata to the VPC, with the `Name` tag setting the display name in the AWS console to `devops-vpc`. This tag is crucial for identifying resources in the AWS console and cost reports.

**Step 4:** Initialize the Terraform project

```sh
terraform init
```

Initialize your Terraform working directory by downloading necessary provider plugins and preparing the backend. This command performs several critical operations: downloads the AWS provider plugin specified in your configuration, creates a `.terraform` directory to store provider binaries, initializes the backend for state management (defaults to local storage), and creates a dependency lock file (`.terraform.lock.hcl`) to ensure consistent provider versions across team members. This is always the first command you run in a new Terraform project or when adding new providers.

**Step 5:** Preview infrastructure changes

```sh
terraform plan
```

Generate and display an execution plan showing exactly what changes Terraform will make to your infrastructure. This command compares your current configuration against the existing state (if any) and shows what resources will be created, modified, or destroyed. For this task, you'll see output indicating that one VPC resource will be created, along with all its attributes. The plan command performs a dry-run without making any actual changes to your AWS account, allowing you to review and validate the proposed infrastructure changes before applying them.

**Step 6:** Apply the Terraform configuration

```sh
terraform apply -auto-approve
```

Execute the planned changes to create the VPC in AWS. Terraform will create the VPC resource with the specified CIDR block and tags. The `-auto-approve` flag skips the interactive approval prompt and immediately proceeds with resource creation. In production environments, it's recommended to review the plan manually before approving, but for lab exercises, this flag speeds up the workflow. Terraform will display progress updates and finally show a summary indicating that resources were successfully created.

**Step 7:** Verify VPC creation using Terraform state

```sh
terraform state list
```

List all resources currently managed by Terraform in the state file. This command reads the `terraform.tfstate` file and displays all tracked resources. You should see `aws_vpc.myvpc` in the output, confirming that Terraform successfully created and is now tracking the VPC. The state file is Terraform's database of record, mapping your configuration to real-world resources and storing resource metadata needed for updates and deletions.

**Step 8:** Additional verification and inspection commands

```bash
# Show detailed information about the VPC resource
terraform state show aws_vpc.myvpc

# Display all outputs (if defined in outputs.tf)
terraform output

# Verify in AWS CLI (if configured)
aws ec2 describe-vpcs --filters "Name=tag:Name,Values=devops-vpc"

# Clean up resources when no longer needed
terraform destroy -auto-approve
```

These additional commands provide comprehensive verification and management capabilities. The `terraform state show` command displays all attributes of the created VPC including ID, CIDR blocks, DNS settings, and tags. The `terraform output` command displays any defined output values (useful for sharing resource information between Terraform modules or with external systems). The `aws ec2 describe-vpcs` command verifies the VPC exists in AWS using the AWS CLI. Finally, `terraform destroy` removes all resources defined in your configuration, which is essential for cleaning up lab environments to avoid unnecessary AWS charges.

---

## Key Concepts

**Virtual Private Cloud (VPC):**
- Isolated virtual network in AWS cloud dedicated to your account
- Complete control over IP address range, subnets, route tables, and gateways
- Foundation for launching AWS resources like EC2 instances, RDS databases, etc.
- Provides network isolation and security at the infrastructure level

**CIDR Block Planning:**
- `/16` provides 65,536 IP addresses (10.0.0.0 to 10.0.255.255)
- `/24` provides 256 IP addresses (commonly used for subnets)
- `/8` provides 16,777,216 IP addresses (largest recommended VPC size)
- Private IP ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 (RFC 1918)

**Terraform Workflow:**
- **Write:** Define infrastructure as code in `.tf` files
- **Init:** Initialize working directory and download providers
- **Plan:** Preview changes before applying them
- **Apply:** Execute changes to create/update infrastructure
- **Destroy:** Remove infrastructure when no longer needed

**Terraform State Management:**
- State file (`terraform.tfstate`) tracks resource mappings and metadata
- Contains sensitive information - never commit to public repositories
- Enables Terraform to detect drift between configuration and reality
- Critical for team collaboration - use remote state backends in production

**Resource Naming Conventions:**
- Resource name in Terraform (e.g., `myvpc`) is internal identifier only
- AWS resource name comes from the `Name` tag in the `tags` block
- Use descriptive Terraform names that indicate the resource purpose
- Follow consistent naming patterns across your organization

**AWS Provider Configuration:**
- Automatically inferred from resource usage (aws_vpc implies AWS provider)
- Can be explicitly defined in a `provider` block for custom configuration
- Credentials sourced from environment variables, AWS CLI config, or IAM roles
- Region defaults to us-east-1 unless specified in provider configuration

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 93](day-93.md) | [Day 95 →](day-95.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
