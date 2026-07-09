## Task: : Attach IAM Policy to IAM User
The Nautilus DevOps team has been creating a couple of services on AWS cloud. They have been breaking down the migration into smaller tasks, allowing for better control, risk mitigation, and optimization of resources throughout the migration process. Recently they came up with requirements mentioned below.

An IAM user named `iamuser_james` and a policy named `iampolicy_james` already exist. Attach the IAM policy `iampolicy_james` to the IAM user `iamuser_james`.

---

## Solution 

We'll be performing the task using AWS CLI

### **Step 1: Set variables**
```bash
USER="iamuser_james"
POLICY="iampolicy_james"
```

### **Step 2: Get policy ARN**
```bash
POLICY_ARN=$(aws iam list-policies --scope Local \
  --query "Policies[?PolicyName==\`$POLICY\`].Arn" \
  --output text)
```

### **Step 3: Attach policy to user**
```bash
aws iam attach-user-policy \
    --user-name "$USER" \
    --policy-arn "$POLICY_ARN"
```

### **Step 4: Validate policy attachment**
```bash
aws iam list-attached-user-policies \
    --user-name "$USER"
```