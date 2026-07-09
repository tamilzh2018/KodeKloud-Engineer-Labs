# Day 95: Create Security Group Using Terraform

## Task Overview

Create an AWS Security Group using Terraform to control inbound and outbound network traffic for AWS resources. Security groups act as virtual firewalls, providing essential network-level security for EC2 instances and other AWS services.

**Technical Specifications:**
- Resource type: AWS Security Group with ingress rules
- VPC: Default VPC in us-east-1
- Security group name: xfusion-sg
- Description: Security group for Nautilus App Servers
- Inbound rules: HTTP (port 80) and SSH (port 22)
- Source IP range: 0.0.0.0/0 (all addresses)

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Navigate to the Terraform working directory

```sh
cd /home/bob/terraform
```

Change to the Terraform working directory where you'll create configuration files for the security group. This directory should already exist from previous Terraform exercises and will contain your infrastructure code.

**Step 2:** Create the variables.tf file

```sh
# Create variables.tf file in VS Code or text editor
# Right-click under EXPLORER section and select "New File"
# Name it: variables.tf
```

Create a variables file to define reusable input parameters for your Terraform configuration. Using variables promotes code reusability, makes configurations more maintainable, and allows easy customization without modifying the core infrastructure code.

**Step 3:** Define variables in variables.tf

```hcl
variable "sg_name" {
    default = "xfusion-sg"
}

variable "sg_description" {
    default = "Security group for Nautilus App Servers"
}
```

Define two input variables for the security group configuration. The `sg_name` variable sets the security group name to `xfusion-sg`, and `sg_description` provides a descriptive label explaining the security group's purpose. Both variables use default values, which can be overridden when needed through command-line flags, environment variables, or `.tfvars` files. This approach centralizes configuration values and makes them easy to update without touching the main resource definitions.

**Step 4:** Create the main.tf file for security group resources

```sh
# Create main.tf file in VS Code or text editor
# Name it: main.tf
```

Create the main Terraform configuration file where you'll define the security group and its associated ingress rules. If a `main.tf` file already exists from previous tasks, you may need to remove old resources or create a fresh file for this exercise.

**Step 5:** Define security group resource in main.tf

```hcl
resource "aws_security_group" "kk_sg" {
    name        = var.sg_name
    description = var.sg_description

    tags = {
        Name = var.sg_name
    }
}
```

Create an AWS security group resource with a Terraform identifier `kk_sg`. The resource uses variables for the name and description, making it flexible and reusable. The security group will be created in the default VPC since no `vpc_id` is specified. The `tags` block assigns a Name tag using the same value as the security group name, which makes the resource easily identifiable in the AWS console.

**Step 6:** Add HTTP ingress rule in main.tf

```hcl
resource "aws_vpc_security_group_ingress_rule" "allow_http" {
    security_group_id = aws_security_group.kk_sg.id
    cidr_ipv4         = "0.0.0.0/0"
    from_port         = 80
    ip_protocol       = "HTTP"
    to_port           = 80
}
```

Define an ingress rule that allows HTTP traffic on port 80 from any IP address. The `security_group_id` parameter references the security group created in the previous step using Terraform's resource reference syntax (`aws_security_group.kk_sg.id`). This creates an implicit dependency, ensuring Terraform creates the security group before the ingress rule. The `cidr_ipv4 = "0.0.0.0/0"` allows traffic from anywhere on the internet, which is common for public web servers but should be restricted in production environments. The `ip_protocol` is set to "HTTP" and ports 80-80 specify the allowed port range.

**Step 7:** Add SSH ingress rule in main.tf

```hcl
resource "aws_vpc_security_group_ingress_rule" "allow_ssh" {
    security_group_id = aws_security_group.kk_sg.id
    cidr_ipv4         = "0.0.0.0/0"
    from_port         = 22
    ip_protocol       = "SSH"
    to_port           = 22
}
```

Define a second ingress rule allowing SSH traffic on port 22 from any IP address. SSH access is essential for remote server administration and configuration management. Like the HTTP rule, this allows connections from anywhere (`0.0.0.0/0`). In production environments, you should restrict SSH access to specific IP ranges (such as your office network or VPN) for enhanced security. The rule references the same security group using `aws_security_group.kk_sg.id`.

**Step 8:** Initialize the Terraform project

```sh
terraform init
```

Initialize the Terraform working directory, downloading the AWS provider plugin and preparing the environment. This command recognizes that you're using AWS resources and automatically fetches the necessary provider binaries. It also sets up the local backend for state management.

**Step 9:** Preview the infrastructure changes

```sh
terraform plan
```

Generate an execution plan showing the three resources that will be created: one security group (`aws_security_group.kk_sg`) and two ingress rules (`aws_vpc_security_group_ingress_rule.allow_http` and `aws_vpc_security_group_ingress_rule.allow_ssh`). Review the plan to ensure all settings are correct before proceeding with the actual creation.

**Step 10:** Apply the Terraform configuration

```sh
terraform apply -auto-approve
```

Execute the plan to create the security group and ingress rules in AWS. Terraform will create resources in the correct order based on dependencies - first the security group, then the two ingress rules. The output will show successful creation of all three resources with their unique IDs.

**Step 11:** Verify resource creation

```sh
terraform state list
```

List all resources managed by Terraform. You should see three resources in the output:
- `aws_security_group.kk_sg`
- `aws_vpc_security_group_ingress_rule.allow_http`
- `aws_vpc_security_group_ingress_rule.allow_ssh`

This confirms that Terraform successfully created and is tracking all components of your security group configuration.

**Step 12:** Additional verification and inspection commands

```bash
# Show detailed security group information
terraform state show aws_security_group.kk_sg

# Show HTTP ingress rule details
terraform state show aws_vpc_security_group_ingress_rule.allow_http

# Verify in AWS CLI (if configured)
aws ec2 describe-security-groups --filters "Name=group-name,Values=xfusion-sg"

# View security group rules
aws ec2 describe-security-group-rules --filters "Name=group-id,Values=<sg-id>"
```

These commands provide detailed inspection of your created resources. The `terraform state show` commands display complete resource attributes including IDs, ARNs, and all configured parameters. The AWS CLI commands allow you to verify the resources exist in AWS and inspect their current configuration, providing an independent validation of your Terraform deployment.

---

## Key Concepts

**AWS Security Groups:**
- Virtual firewalls that control inbound and outbound traffic at instance level
- Stateful - return traffic is automatically allowed regardless of rules
- Operate at the instance level, not the subnet level (unlike Network ACLs)
- Support allow rules only (no deny rules)
- All outbound traffic is allowed by default
- Changes take effect immediately

**Security Group vs Network ACL:**
- Security groups are stateful, Network ACLs are stateless
- Security groups operate at instance level, NACLs at subnet level
- Security groups support allow rules only, NACLs support both allow and deny
- Security groups evaluate all rules, NACLs process rules in order
- One security group can be attached to multiple instances

**Ingress vs Egress Rules:**
- **Ingress:** Inbound traffic coming into the instance
- **Egress:** Outbound traffic leaving the instance
- Security groups allow all egress by default
- Use `aws_vpc_security_group_ingress_rule` for inbound rules
- Use `aws_vpc_security_group_egress_rule` for outbound rules

**CIDR Block 0.0.0.0/0:**
- Represents all possible IP addresses (the entire internet)
- Use with caution - appropriate for public web services only
- For production, restrict to specific IP ranges or security groups
- Consider using VPN or bastion hosts for SSH access
- Follows the principle of least privilege when narrowed down

**Terraform Resource Dependencies:**
- Terraform automatically detects dependencies from resource references
- `aws_security_group.kk_sg.id` creates implicit dependency
- Ensures security group is created before ingress rules
- Terraform builds dependency graph for correct creation order
- Can use `depends_on` for explicit dependencies when needed

**Variables Best Practices:**
- Centralize configuration values in variables.tf
- Use descriptive variable names that indicate purpose
- Provide default values for common use cases
- Override defaults via `.tfvars` files for different environments
- Validate variable values using validation blocks when needed

**Default VPC Behavior:**
- AWS creates a default VPC in each region automatically
- Security groups without vpc_id specification use default VPC
- Default VPC includes internet gateway and public subnets
- Good for quick testing but use custom VPCs for production
- Default VPC CIDR is typically 172.31.0.0/16

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 94](day-94.md) | [Day 96 →](day-96.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
