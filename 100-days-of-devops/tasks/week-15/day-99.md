# Day 99: Attach IAM Policy for DynamoDB Access Using Terraform

## Task Overview

Create a comprehensive IAM and DynamoDB infrastructure using Terraform, including a DynamoDB table, an IAM role with trust policy, a custom IAM policy granting read-only DynamoDB access, and a policy attachment. This demonstrates fine-grained access control for AWS services using infrastructure-as-code.

**Technical Specifications:**
- DynamoDB table: devops-table (minimal configuration)
- IAM role: devops-role (assumable by AWS services)
- IAM policy: devops-readonly-policy (read-only DynamoDB access)
- Permissions: GetItem, Scan, Query on specific table
- Policy attachment: Attach policy to role
- Variable management: terraform.tfvars file

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Navigate to the Terraform working directory

```sh
cd /home/bob/terraform
```

Change to the Terraform working directory where you'll create multiple configuration files for DynamoDB, IAM role, IAM policy, and policy attachment. This comprehensive task demonstrates end-to-end IAM and database resource provisioning.

**Step 2:** Create the terraform.tfvars file

```sh
# Create terraform.tfvars file in VS Code or text editor
# Right-click under EXPLORER section and select "New File"
# Name it: terraform.tfvars
```

Create a Terraform variables values file to specify the actual values for your variables. The `.tfvars` file is the standard way to set variable values, keeping them separate from variable declarations and making configuration management easier.

**Step 3:** Define variable values in terraform.tfvars

```hcl
KKE_TABLE_NAME = "devops-table"
KKE_ROLE_NAME = "devops-role"
KKE_POLICY_NAME = "devops-readonly-policy"
```

Set the actual values for table name, role name, and policy name. Unlike variable declarations, `.tfvars` files use simple assignment syntax without the `variable` keyword. Terraform automatically loads files named `terraform.tfvars` or `*.auto.tfvars`. These values will be passed to the variables defined in `variables.tf`. Using `.tfvars` files allows you to maintain different configurations for different environments (dev, staging, production) without changing your core Terraform code.

**Step 4:** Create the variables.tf file

```sh
# Create variables.tf file in VS Code or text editor
# Name it: variables.tf
```

Create a variables declaration file to define the input variables your configuration will use. This file declares the variables without specifying their values (values come from terraform.tfvars).

**Step 5:** Declare variables in variables.tf

```hcl
variable "KKE_TABLE_NAME" {}
variable "KKE_ROLE_NAME" {}
variable "KKE_POLICY_NAME" {}
```

Declare three variables using the empty block syntax `{}`. This means the variables have no default values and must be provided via `terraform.tfvars`, command-line flags, or environment variables. The variable names use uppercase with underscores, following the task's naming convention. When Terraform runs, it will look for values for these variables in the `terraform.tfvars` file created earlier.

**Step 6:** Create the main.tf file

```sh
# Create main.tf file in VS Code or text editor
# Name it: main.tf
```

Create the main configuration file where you'll define the DynamoDB table, IAM role with trust policy, IAM policy with permissions, and policy attachment resources.

**Step 7:** Define DynamoDB table in main.tf

```hcl
resource "aws_dynamodb_table" "kk_dynamodb" {
    name           = var.KKE_TABLE_NAME
    billing_mode   = "PAY_PER_REQUEST"
    hash_key       = "id"

    attribute {
        name = "id"
        type = "S"
    }

    tags = {
        Name = var.KKE_TABLE_NAME
    }
}
```

Create a DynamoDB table with minimal configuration. The `name` uses the variable resulting in `devops-table`. The `billing_mode = "PAY_PER_REQUEST"` uses on-demand pricing (pay only for reads/writes you use) instead of provisioned capacity, making it ideal for unpredictable workloads and testing. The `hash_key = "id"` sets the partition key (primary key) for the table - every item must have this attribute. The `attribute` block defines the `id` attribute with type `S` (String). DynamoDB requires you to define only attributes used as keys; other attributes are schema-less. The tags make the table easily identifiable in the AWS console.

**Step 8:** Define IAM role in main.tf

```hcl
resource "aws_iam_role" "kk_role" {
    name = var.KKE_ROLE_NAME

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Action = "sts:AssumeRole"
                Effect = "Allow"
                Principal = {
                    Service = "ec2.amazonaws.com"
                }
            }
        ]
    })

    tags = {
        Name = var.KKE_ROLE_NAME
    }
}
```

Create an IAM role that can be assumed by EC2 instances. The `name` uses the variable resulting in `devops-role`. The `assume_role_policy` (also called trust policy) defines who can assume this role - in this case, the EC2 service. The trust policy structure includes:
- `Action = "sts:AssumeRole"`: The action that allows assuming the role
- `Effect = "Allow"`: Permits the action
- `Principal.Service = "ec2.amazonaws.com"`: Specifies that EC2 service can assume this role

This trust policy allows you to attach this role to EC2 instances, which can then use the role's permissions to access DynamoDB. The role itself has no permissions yet - those come from attached policies.

**Step 9:** Define IAM policy with DynamoDB read access in main.tf

```hcl
resource "aws_iam_policy" "kk_policy" {
    name        = var.KKE_POLICY_NAME
    description = "Read-only access to DynamoDB table"

    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Effect = "Allow"
                Action = [
                    "dynamodb:GetItem",
                    "dynamodb:BatchGetItem",
                    "dynamodb:Query",
                    "dynamodb:Scan",
                    "dynamodb:DescribeTable"
                ]
                Resource = [
                    aws_dynamodb_table.kk_dynamodb.arn,
                    "${aws_dynamodb_table.kk_dynamodb.arn}/*"
                ]
            }
        ]
    })

    tags = {
        Name = var.KKE_POLICY_NAME
    }
}
```

Create a custom IAM policy granting read-only access to the DynamoDB table. The `name` uses the variable resulting in `devops-readonly-policy`. The policy document includes:

**Allowed Actions:**
- `dynamodb:GetItem`: Retrieve a single item by primary key
- `dynamodb:BatchGetItem`: Retrieve multiple items in one request
- `dynamodb:Query`: Query items using partition key and optional sort key
- `dynamodb:Scan`: Scan entire table (read all items)
- `dynamodb:DescribeTable`: Get table metadata and schema information

**Resource Restrictions:**
- `aws_dynamodb_table.kk_dynamodb.arn`: The table's ARN (Amazon Resource Name)
- `"${aws_dynamodb_table.kk_dynamodb.arn}/*"`: Table's sub-resources (indexes, streams)

This policy grants comprehensive read-only access to the specific table only. No write operations (PutItem, UpdateItem, DeleteItem) are allowed. The resource references create implicit dependencies, ensuring the table exists before the policy is created.

**Step 10:** Attach policy to role in main.tf

```hcl
resource "aws_iam_role_policy_attachment" "kk_attachment" {
    role       = aws_iam_role.kk_role.name
    policy_arn = aws_iam_policy.kk_policy.arn
}
```

Create a policy attachment that links the IAM policy to the IAM role. The `role` parameter references the role name from the created role. The `policy_arn` references the ARN of the created policy. This attachment grants the role all permissions defined in the policy. The references create implicit dependencies, ensuring both the role and policy exist before the attachment is created. Once attached, any EC2 instance using this role can perform read-only operations on the DynamoDB table.

**Step 11:** Create the outputs.tf file

```sh
# Create outputs.tf file in VS Code or text editor
# Name it: outputs.tf
```

Create an outputs file to display resource names after deployment. The task requires specific output variable names for validation.

**Step 12:** Define outputs in outputs.tf

```hcl
output "kke_dynamodb_table" {
    value = aws_dynamodb_table.kk_dynamodb.name
}

output "kke_iam_role_name" {
    value = aws_iam_role.kk_role.name
}

output "kke_iam_policy_name" {
    value = aws_iam_policy.kk_policy.name
}
```

Define three outputs with specific names required by the task. Each output extracts the name attribute from the respective resource. The `aws_dynamodb_table.kk_dynamodb.name` returns the table name, `aws_iam_role.kk_role.name` returns the role name, and `aws_iam_policy.kk_policy.name` returns the policy name. These outputs confirm that all resources were created with the correct names from the variables.

**Step 13:** Initialize the Terraform project

```sh
terraform init
```

Initialize the Terraform working directory, downloading the AWS provider plugin that includes support for DynamoDB and IAM resources. This command prepares your environment for creating database and security resources.

**Step 14:** Preview the infrastructure changes

```sh
terraform plan
```

Generate an execution plan showing the four resources that will be created: DynamoDB table, IAM role, IAM policy, and policy attachment. Review the plan to verify table configuration, trust policy, permissions policy, and resource references are correct. Terraform will show the dependency chain ensuring resources are created in the proper order.

**Step 15:** Apply the Terraform configuration

```sh
terraform apply -auto-approve
```

Execute the plan to create all resources in AWS. Terraform creates resources in dependency order: DynamoDB table and IAM role can be created in parallel, then the IAM policy (which references the table ARN), and finally the policy attachment (which references both role and policy). Upon completion, Terraform displays the three outputs showing resource names, confirming successful deployment.

**Step 16:** Verify resource creation and relationships

```bash
# List all managed resources
terraform state list

# Show DynamoDB table details
terraform state show aws_dynamodb_table.kk_dynamodb

# Show IAM role with trust policy
terraform state show aws_iam_role.kk_role

# Show IAM policy with permissions
terraform state show aws_iam_policy.kk_policy

# Show policy attachment
terraform state show aws_iam_role_policy_attachment.kk_attachment

# Display outputs
terraform output

# Verify in AWS CLI (if configured)
aws dynamodb describe-table --table-name devops-table
aws iam get-role --role-name devops-role
aws iam get-policy --policy-arn <policy-arn>
aws iam list-attached-role-policies --role-name devops-role
```

Verify successful deployment using these commands. The `terraform state list` should show four resources: DynamoDB table, IAM role, IAM policy, and policy attachment. The individual `state show` commands display detailed configuration for each resource. The AWS CLI commands provide independent verification and show the resources as they appear in AWS.

**Step 17:** Test DynamoDB access with the role (optional)

```bash
# Attach role to EC2 instance (using instance profile)
# Then from within the EC2 instance:
aws dynamodb get-item --table-name devops-table --key '{"id":{"S":"test"}}'
aws dynamodb scan --table-name devops-table

# These should succeed (read operations)

# Try write operation (should fail)
aws dynamodb put-item --table-name devops-table --item '{"id":{"S":"test"}}'
# Error: AccessDeniedException - no PutItem permission
```

If you want to test the policy, attach the role to an EC2 instance via an instance profile, then use the AWS CLI from within the instance. Read operations (GetItem, Scan) should succeed, while write operations (PutItem) should fail with an access denied error, confirming the read-only policy works correctly.

---

## Key Concepts

**DynamoDB Table Basics:**
- NoSQL database service with single-digit millisecond latency
- Partition key (hash key) required for every item
- Optional sort key for composite primary keys
- Schema-less for non-key attributes
- Automatically scales to handle throughput and storage

**Billing Modes:**
- **PAY_PER_REQUEST:** On-demand pricing, pay per read/write
- **PROVISIONED:** Pre-allocate capacity, predictable costs
- On-demand ideal for unpredictable workloads and testing
- Provisioned cheaper for consistent, predictable traffic
- Can switch between modes once per 24 hours

**DynamoDB Attribute Types:**
- **S:** String type (text data)
- **N:** Number type (numeric data)
- **B:** Binary type (binary data)
- Must define attributes used in keys
- Other attributes defined when writing items

**IAM Roles vs Users:**
- **Roles:** Temporary credentials, assumed by services/users
- **Users:** Permanent credentials, for individuals
- Roles provide temporary security credentials
- Best practice: Use roles for applications and services
- Roles can be assumed across accounts

**Trust Policy (AssumeRole Policy):**
- Defines who/what can assume the role
- Separate from permission policies
- Principal types: Service, AWS (account), Federated
- Common services: EC2, Lambda, ECS, etc.
- Required for all IAM roles

**DynamoDB Read Operations:**
- **GetItem:** Retrieve single item by primary key (fastest, most efficient)
- **BatchGetItem:** Retrieve up to 100 items in one request
- **Query:** Retrieve items with same partition key (can filter by sort key)
- **Scan:** Read all items in table (slowest, most expensive)
- **DescribeTable:** Get table metadata (schema, status, size)

**DynamoDB Write Operations (NOT granted here):**
- **PutItem:** Create new item or replace existing item
- **UpdateItem:** Modify attributes of existing item
- **DeleteItem:** Remove item from table
- **BatchWriteItem:** Write or delete up to 25 items
- Read-only policy excludes all write operations

**Resource ARN Patterns:**
- Table ARN: `arn:aws:dynamodb:region:account:table/table-name`
- Sub-resources: `arn:aws:dynamodb:region:account:table/table-name/*`
- Includes indexes, streams, backups
- Both patterns needed for complete access
- Use `"${table_arn}/*"` for sub-resource access

**IAM Policy Attachment Types:**
- **aws_iam_role_policy_attachment:** Managed policy to role (use this)
- **aws_iam_policy_attachment:** Managed policy to multiple entities (deprecated)
- **aws_iam_role_policy:** Inline policy (embedded in role)
- Managed policies are reusable and versioned
- Prefer managed over inline for maintainability

**Terraform Variable Files:**
- **variables.tf:** Variable declarations (structure, types, defaults)
- **terraform.tfvars:** Variable values (automatically loaded)
- ***.auto.tfvars:** Auto-loaded variable files
- **Custom .tfvars:** Specify with `-var-file` flag
- Separate declarations from values for flexibility

**Least Privilege Principle:**
- Grant minimum permissions necessary for the task
- Read-only access when write isn't needed
- Limit to specific resources (not "*")
- Use conditions for additional restrictions
- Regularly audit and reduce permissions

**DynamoDB Security Best Practices:**
- Use VPC endpoints for private access
- Enable point-in-time recovery for backups
- Encrypt data at rest with KMS
- Enable CloudTrail for auditing
- Use IAM policies for fine-grained access control
- Consider DynamoDB Streams for change tracking

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 98](../week-14/day-98.md) | [Day 100 →](day-100.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
