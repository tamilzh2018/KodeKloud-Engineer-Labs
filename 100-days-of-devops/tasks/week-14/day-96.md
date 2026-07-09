# Day 96: Create EC2 Instance Using Terraform

## Task Overview

Launch an AWS EC2 instance using Terraform with automated SSH key pair generation. This exercise demonstrates infrastructure provisioning including compute resources, security credentials, and proper resource configuration for cloud-based virtual machines.

**Technical Specifications:**
- Resource type: AWS EC2 Instance (Elastic Compute Cloud)
- Instance name: xfusion-ec2
- AMI: ami-0c101f26f147fa7fd (Amazon Linux)
- Instance type: t2.micro (1 vCPU, 1GB RAM)
- SSH key pair: xfusion-kp (RSA, generated via Terraform)
- Security group: Default VPC security group
- Region: us-east-1

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Navigate to the Terraform working directory

```sh
cd /home/bob/terraform
```

Change to the Terraform working directory where you'll create configuration files for the EC2 instance deployment. This directory will contain all Terraform files needed for this task.

**Step 2:** Create the variables.tf file

```sh
# Create variables.tf file in VS Code or text editor
# Right-click under EXPLORER section and select "New File"
# Name it: variables.tf
```

Create a variables file to define input parameters that make your infrastructure code reusable and configurable. Variables allow you to easily change values without modifying the main configuration code.

**Step 3:** Define variables in variables.tf

```hcl
variable "prefix" {
    default = "xfusion"
}

variable "ami_id" {
    default = "ami-0c101f26f147fa7fd"
}

variable "instance_type" {
    default = "t2.micro"
}
```

Define three variables for the EC2 configuration. The `prefix` variable sets a naming prefix used across all resources for consistency and easy identification. The `ami_id` specifies the Amazon Machine Image to use - in this case, an Amazon Linux image. The `instance_type` determines the compute capacity - `t2.micro` is a small, cost-effective instance suitable for testing and light workloads, providing 1 vCPU and 1GB RAM. These variables centralize configuration values and make the code more maintainable.

**Step 4:** Create the main.tf file

```sh
# Create main.tf file in VS Code or text editor
# Name it: main.tf
```

Create the main Terraform configuration file where you'll define the TLS private key, AWS key pair, and EC2 instance resources. This file contains the core infrastructure definitions.

**Step 5:** Generate RSA private key in main.tf

```hcl
resource "tls_private_key" "rsa_key" {
    algorithm = "RSA"
    rsa_bits  = 4096
}
```

Create a TLS private key resource that generates a 4096-bit RSA key pair programmatically. The `tls_private_key` resource from the TLS provider creates cryptographic keys directly within Terraform, eliminating the need to manually generate keys using `ssh-keygen`. The `algorithm = "RSA"` specifies the encryption algorithm, and `rsa_bits = 4096` sets the key length - 4096 bits provides strong security while remaining compatible with most systems. This private key will be used to create the AWS key pair and enable SSH access to the EC2 instance.

**Step 6:** Create AWS key pair in main.tf

```hcl
resource "aws_key_pair" "ec2_key_pair" {
    key_name   = "${var.prefix}-kp"
    public_key = tls_private_key.rsa_key.public_key_openssh
}
```

Define an AWS key pair resource that uploads the public key portion to AWS. The `key_name` uses string interpolation to combine the prefix variable with `-kp`, resulting in `xfusion-kp`. The `public_key` parameter references the public key from the TLS resource created in the previous step using `tls_private_key.rsa_key.public_key_openssh`. This creates an implicit dependency, ensuring Terraform generates the key before creating the key pair. AWS stores this public key and uses it to encrypt data that only your private key can decrypt, enabling secure SSH authentication.

**Step 7:** Launch EC2 instance in main.tf

```hcl
resource "aws_instance" "ec2" {
    ami           = var.ami_id
    instance_type = var.instance_type
    key_name      = aws_key_pair.ec2_key_pair.key_name

    tags = {
        Name = "${var.prefix}-ec2"
    }
}
```

Create an EC2 instance resource using the AMI and instance type from variables. The `ami` parameter specifies which operating system image to use, `instance_type` determines the virtual hardware configuration, and `key_name` associates the SSH key pair for authentication. The key pair reference (`aws_key_pair.ec2_key_pair.key_name`) creates another implicit dependency, ensuring the key pair exists before the instance launches. The `tags` block sets the instance name to `xfusion-ec2` using string interpolation. Since no security group or VPC is specified, the instance will use the default security group and default VPC.

**Step 8:** Create the outputs.tf file (optional but recommended)

```sh
# Create outputs.tf file in VS Code or text editor
# Name it: outputs.tf
```

Create an outputs file to display important information about created resources after Terraform applies the configuration. Outputs make it easy to retrieve resource attributes without manually inspecting the state file.

**Step 9:** Define outputs in outputs.tf

```hcl
output "ec2_info" {
    value = {
        public_ip  = aws_instance.ec2.public_ip
        private_ip = aws_instance.ec2.private_ip
    }
}
```

Define an output that displays both public and private IP addresses of the EC2 instance. The `ec2_info` output uses a map structure to organize multiple values. The `aws_instance.ec2.public_ip` and `aws_instance.ec2.private_ip` reference attributes from the created EC2 instance. After applying the configuration, Terraform will display these IP addresses, which you'll need for SSH access or application connectivity. The public IP allows internet access to the instance, while the private IP is used for VPC-internal communication.

**Step 10:** Initialize the Terraform project

```sh
terraform init
```

Initialize the Terraform working directory, downloading both the AWS provider and the TLS provider. Terraform automatically detects that you're using resources from both providers and fetches the necessary plugins. This command also sets up the local backend for state management and creates the provider lock file.

**Step 11:** Preview the infrastructure changes

```sh
terraform plan
```

Generate an execution plan showing the four resources that will be created: the TLS private key, the AWS key pair, and the EC2 instance. Review the plan to verify all configurations are correct, including AMI ID, instance type, key pair name, and tags. The plan will show the resource creation order based on dependencies.

**Step 12:** Apply the Terraform configuration

```sh
terraform apply -auto-approve
```

Execute the plan to create all resources in AWS. Terraform creates resources in dependency order: first the TLS private key, then the AWS key pair, and finally the EC2 instance. The output will show progress for each resource and display the `ec2_info` output with IP addresses upon successful completion. The instance will take a minute or two to fully initialize and reach the "running" state.

**Step 13:** Verify EC2 instance creation

```bash
# List all managed resources
terraform state list

# Show detailed EC2 instance information
terraform state show aws_instance.ec2

# Display outputs
terraform output

# View private key (for SSH access)
terraform output -raw tls_private_key.rsa_key.private_key_pem
```

These commands verify successful resource creation and provide access to important information. The `terraform state list` should show four resources: `tls_private_key.rsa_key`, `aws_key_pair.ec2_key_pair`, and `aws_instance.ec2`. The `terraform state show` command displays all attributes of the EC2 instance including IDs, IP addresses, and configuration settings. The `terraform output` command shows the IP addresses in a formatted way.

**Step 14:** Save private key for SSH access (if needed)

```bash
# Save private key to file
terraform output -raw tls_private_key.rsa_key.private_key_pem > xfusion-kp.pem

# Set correct permissions
chmod 400 xfusion-kp.pem

# SSH to the instance
ssh -i xfusion-kp.pem ec2-user@<public-ip>
```

Extract the private key from Terraform state and save it to a file for SSH access. The `terraform output -raw` command retrieves the private key in PEM format without quotes or formatting. The `chmod 400` command sets read-only permissions for the owner, which is required by SSH for security. Use this key with the `ssh` command to connect to your instance, replacing `<public-ip>` with the actual public IP from the outputs. For Amazon Linux AMIs, the default username is `ec2-user`.

---

## Key Concepts

**EC2 Instance Basics:**
- Virtual servers in the AWS cloud with configurable compute, memory, and storage
- Choose from various instance types optimized for different workloads
- Charged by the hour or second depending on instance type and OS
- Can be stopped (persists data) or terminated (deleted permanently)
- Instance state transitions: pending → running → stopping → stopped → terminated

**AMI (Amazon Machine Image):**
- Pre-configured template containing OS and optional software
- Includes root volume template and launch permissions
- Regional resource - must use AMI available in your deployment region
- Can create custom AMIs from configured instances
- Public AMIs available for common operating systems (Amazon Linux, Ubuntu, etc.)

**Instance Types:**
- **t2.micro:** 1 vCPU, 1GB RAM - Free tier eligible, good for testing
- **t2.small:** 1 vCPU, 2GB RAM - Light production workloads
- **t2.medium:** 2 vCPU, 4GB RAM - Small to medium applications
- T2 instances use CPU credits for burst performance
- Choose type based on CPU, memory, storage, and networking needs

**SSH Key Pair Management:**
- Asymmetric cryptography: public key encrypts, private key decrypts
- AWS stores public key, you retain private key securely
- Required for SSH access to Linux instances
- One key pair can be used for multiple instances
- Never share or commit private keys to version control

**TLS Provider in Terraform:**
- Generates cryptographic keys and certificates
- `tls_private_key` creates RSA, ECDSA, or ED25519 keys
- `public_key_openssh` attribute formats key for SSH compatibility
- Stores private key in Terraform state (sensitive data)
- Useful for automated key generation in CI/CD pipelines

**Resource Dependencies:**
- Terraform automatically orders resource creation based on references
- Implicit dependencies: `aws_key_pair.ec2_key_pair.key_name`
- Explicit dependencies: use `depends_on` when needed
- Dependency graph ensures correct creation order
- Cannot create EC2 instance before key pair exists

**Default VPC and Security Groups:**
- Default VPC created automatically in each region
- Default security group allows all outbound traffic
- Inbound traffic blocked except from same security group
- Resources without explicit VPC/SG use defaults
- Customize security groups for production workloads

**Terraform State Sensitivity:**
- State file contains private key in plaintext
- Never commit state files to public repositories
- Use remote state backends with encryption for teams
- Restrict access to state files with proper IAM policies
- Consider external key management for production

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 95](day-95.md) | [Day 97 →](day-97.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
