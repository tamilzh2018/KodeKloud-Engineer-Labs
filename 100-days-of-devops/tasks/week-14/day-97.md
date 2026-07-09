# Day 97: Create IAM Policy Using Terraform

## Task Overview

Create an AWS IAM (Identity and Access Management) policy using Terraform that grants read-only access to EC2 resources. IAM policies define permissions that control what actions users, groups, or roles can perform on AWS resources, forming the foundation of AWS security and access control.

**Technical Specifications:**
- Resource type: AWS IAM Policy
- Policy name: iampolicy_ravi
- Access level: Read-only (EC2 console)
- Permissions: View instances, AMIs, and snapshots
- Policy language: JSON with IAM syntax
- Region: us-east-1

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Navigate to the Terraform working directory

```sh
cd /home/bob/terraform
```

Change to the Terraform working directory where you'll create configuration files for the IAM policy. This directory will house all Terraform files for this security configuration task.

**Step 2:** Create the variables.tf file

```sh
# Create variables.tf file in VS Code or text editor
# Right-click under EXPLORER section and select "New File"
# Name it: variables.tf
```

Create a variables file to define the IAM policy name as a reusable parameter. Using variables makes your IAM policies easy to replicate and customize for different users or teams.

**Step 3:** Define the policy name variable in variables.tf

```hcl
variable "policy_name" {
    default = "iampolicy_ravi"
}
```

Define a variable for the IAM policy name with a default value of `iampolicy_ravi`. This variable allows you to easily change the policy name without modifying the main resource definition. You can override this default value using command-line flags (`-var`), environment variables, or `.tfvars` files when creating similar policies for different users or purposes.

**Step 4:** Create the main.tf file

```sh
# Create main.tf file in VS Code or text editor
# Name it: main.tf
```

Create the main Terraform configuration file where you'll define the IAM policy resource with its permission settings. This file contains the core security policy definition.

**Step 5:** Define IAM policy resource in main.tf

```hcl
resource "aws_iam_policy" "policy" {
    name        = var.policy_name
    path        = "/"
    description = "My test policy"

    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
        {
            Action = [
            "ec2:Describe*",
            ]
            Effect   = "Allow"
            Resource = "*"
        },
        ]
    })

    tags = {
        Name = var.policy_name
    }
}
```

Create an IAM policy resource with comprehensive read-only EC2 permissions. Let's break down each component:

- `name = var.policy_name`: Sets the policy name using the variable, resulting in `iampolicy_ravi`
- `path = "/"`: Places the policy at the root path in IAM's organizational hierarchy
- `description`: Provides a human-readable explanation of the policy's purpose
- `policy = jsonencode({...})`: Converts the HCL policy document to JSON format required by AWS

The policy document structure includes:
- `Version = "2012-10-17"`: Specifies the IAM policy language version (current standard)
- `Statement`: Array containing permission rules
- `Action = ["ec2:Describe*"]`: Grants all EC2 describe actions (read-only operations)
- `Effect = "Allow"`: Explicitly permits the specified actions
- `Resource = "*"`: Applies permissions to all EC2 resources across all regions

The `ec2:Describe*` wildcard covers all describe operations including viewing instances, AMIs, snapshots, volumes, security groups, and other EC2 resources. This provides comprehensive read-only access to the EC2 console without allowing any modifications. The `tags` block assigns a Name tag for easy identification in the IAM console.

**Step 6:** Initialize the Terraform project

```sh
terraform init
```

Initialize the Terraform working directory, downloading the AWS provider plugin that includes IAM resource support. This command prepares your environment for IAM policy creation and sets up state management.

**Step 7:** Preview the IAM policy creation

```sh
terraform plan
```

Generate an execution plan showing the IAM policy that will be created. Review the output to verify the policy name, permissions, and JSON document structure. The plan will display the complete policy document with all describe permissions that will be granted.

**Step 8:** Apply the Terraform configuration

```sh
terraform apply -auto-approve
```

Execute the plan to create the IAM policy in AWS. Terraform will create the policy with the specified permissions and display the policy ARN (Amazon Resource Name) upon successful completion. The policy will be immediately available for attachment to users, groups, or roles.

**Step 9:** Verify IAM policy creation

```bash
# List managed resources
terraform state list

# Show detailed policy information
terraform state show aws_iam_policy.policy

# Verify in AWS CLI (if configured)
aws iam get-policy --policy-arn <policy-arn>

# View policy version details
aws iam get-policy-version --policy-arn <policy-arn> --version-id v1
```

These commands verify successful policy creation and inspect its configuration. The `terraform state list` should show `aws_iam_policy.policy`. The `terraform state show` command displays all policy attributes including the ARN, ID, and JSON document. The AWS CLI commands provide independent verification and show the policy as it appears in AWS IAM.

**Step 10:** Optional - Attach policy to user, group, or role

```bash
# Attach policy to a user
resource "aws_iam_user_policy_attachment" "user_attachment" {
    user       = "username"
    policy_arn = aws_iam_policy.policy.arn
}

# Attach policy to a group
resource "aws_iam_group_policy_attachment" "group_attachment" {
    group      = "groupname"
    policy_arn = aws_iam_policy.policy.arn
}

# Attach policy to a role
resource "aws_iam_role_policy_attachment" "role_attachment" {
    role       = "rolename"
    policy_arn = aws_iam_policy.policy.arn
}
```

Creating the policy alone doesn't grant permissions - you must attach it to an IAM entity. These examples show how to attach the policy to users, groups, or roles. The `policy_arn` references the ARN from the created policy, establishing an implicit dependency. Choose the attachment type based on your access control strategy: user-level for individual permissions, group-level for team-based access, or role-level for service or federated access.

---

## Key Concepts

**IAM Policy Structure:**
- **Version:** Policy language version (always use "2012-10-17")
- **Statement:** Array of permission rules (can have multiple)
- **Effect:** Either "Allow" or "Deny" (explicit permission grant or denial)
- **Action:** AWS service actions (e.g., "ec2:Describe*", "s3:GetObject")
- **Resource:** ARNs of resources the actions apply to ("*" means all)
- **Condition:** Optional conditions for when permissions apply

**Policy Types in AWS:**
- **Managed Policies:** Standalone policies with their own ARN
  - AWS Managed: Created and maintained by AWS
  - Customer Managed: Created and maintained by you
- **Inline Policies:** Embedded directly in a single user, group, or role
- **Service Control Policies (SCPs):** AWS Organizations policies
- **Resource-based Policies:** Attached to resources (S3 buckets, etc.)

**EC2 Describe Actions:**
- `ec2:Describe*` wildcard includes all read operations
- Covers: DescribeInstances, DescribeImages, DescribeSnapshots
- Also includes: DescribeVolumes, DescribeSecurityGroups, DescribeVpcs
- Read-only - cannot modify, create, or delete resources
- No sensitive data exposure (passwords, keys, etc.)

**Least Privilege Principle:**
- Grant only the permissions necessary for the task
- Start with minimal permissions and add as needed
- Use specific actions instead of wildcards when possible
- Limit resource scope instead of using "*" in production
- Regularly audit and remove unused permissions

**Policy ARN (Amazon Resource Name):**
- Unique identifier for AWS resources
- Format: `arn:aws:iam::account-id:policy/policy-name`
- Required for attaching policies to entities
- Regional or global depending on service
- Used in resource references and access control

**IAM Best Practices:**
- Use groups to assign permissions to users
- Rotate credentials regularly
- Enable MFA (Multi-Factor Authentication) for privileged users
- Use roles for applications running on EC2 instances
- Monitor IAM activity with CloudTrail
- Review permissions regularly and remove unused policies

**Terraform jsonencode Function:**
- Converts HCL expressions to JSON format
- Required for IAM policy documents (AWS expects JSON)
- Maintains proper JSON structure and escaping
- More readable than raw JSON strings in HCL
- Supports variables and expressions within the policy

**Policy Attachment vs Inline Policies:**
- Managed policies (created here) can be reused across entities
- Inline policies are embedded and can't be shared
- Managed policies have version history (up to 5 versions)
- Inline policies are deleted when the entity is deleted
- Managed policies are recommended for maintainability

**Resource-Level Permissions:**
- `Resource = "*"` grants access to all resources (broad)
- Can specify specific resources: `arn:aws:ec2:region:account:instance/*`
- Supports wildcards for flexible matching
- More granular control improves security
- Consider resource tags for conditional access

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 96](day-96.md) | [Day 98 →](day-98.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
