## Task: Configuring Secure SSH Access to an EC2 Instance
The Nautilus DevOps team needs to set up a new EC2 instance that can be accessed securely from their landing host (`aws-client`). The instance should be of type `t2.micro` and named `xfusion-ec2`. A new SSH key should be created on the `aws-client` host under the `/root/.ssh/` folder, if it doesn't already exist. This key should then be added to the `root` user's authorised keys on the EC2 instance, allowing passwordless SSH access from the `aws-client` host.

---

## Solution

We'll be performing the task using AWS CLI

### Step 1: Set variables
```bash
EC2_NAME="xfusion-ec2"
EC2_TYPE="t2.micro"
REGION="us-east-1"
```

### Step 2: Create an SSH key locally
```bash
ssh-keygen
```

### Step 3: Import SSH public key into AWS as a Key Pair
```bash
KEY_NAME="xfusion-ec2-key"

aws ec2 import-key-pair \
    --key-name "$KEY_NAME" \
    --public-key-material fileb://"/root/.ssh/id_rsa.pub"
```

### Step 4: Fetch AMI ID
Get AMI ID of `Ubuntu 22.04` image in `us-east-1` region
```bash
AMI_ID=$(aws ec2 describe-images \
  --region $REGION \
  --owners 099720109477 \
  --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*" "Name=state,Values=available" \
  --query "sort_by(Images, &CreationDate)[-1].ImageId" \
  --output text
)
```

### Step 5: Launch the EC2 Instance
```bash
INSTANCE_ID=$(aws ec2 run-instances \
  --image-id "$AMI_ID" \
  --instance-type "$EC2_TYPE" \
  --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$EC2_NAME}]" \
  --key-name "$KEY_NAME" \
  --query "Instances[0].InstanceId" \
  --output text)

echo "Instance ID: $INSTANCE_ID"
```

### Step 6: Wait for the instance to be running
```bash
aws ec2 wait instance-running --instance-ids "$INSTANCE_ID"
```

### Step 7: Get the default security group ID for your VPC
```bash
# Get the VPC ID of your EC2 instance
VPC_ID=$(aws ec2 describe-instances \
    --instance-ids "$INSTANCE_ID" \
    --query "Reservations[0].Instances[0].VpcId" \
    --output text)

# Get the default security group ID for that VPC
DEFAULT_SG_ID=$(aws ec2 describe-security-groups \
    --filters "Name=vpc-id,Values=$VPC_ID" "Name=group-name,Values=default" \
    --query "SecurityGroups[0].GroupId" \
    --output text)

echo "Default Security Group ID: $DEFAULT_SG_ID"
```

### Step 8: Add an inbound rule to allow SSH (port 22)
```bash
aws ec2 authorize-security-group-ingress \
    --group-id "$DEFAULT_SG_ID" \
    --protocol tcp \
    --port 22 \
    --cidr "0.0.0.0/0"
```

### Step 9: Fetch the public IP of the VM
```bash
PUBLIC_IP=$(aws ec2 describe-instances \
  --instance-ids "$INSTANCE_ID" \
  --query "Reservations[0].Instances[0].PublicIpAddress" \
  --output text)

echo "EC2 Public IP: $PUBLIC_IP"
```

### Step 10: Configure passwordless SSH access for root user
```bash
# SSH to VM as ubuntu user
ssh ubuntu@$PUBLIC_IP

# Copy contents of ubuntu user's authorized_keys file to that of root user
sudo cp /home/ubuntu/.ssh/authorized_keys /root/.ssh/authorized_keys

# Exit the VM
exit
```

### Step 11: Test if you are able to login to the VM as `root` user
From `aws-client` host
```bash
ssh root@$PUBLIC_IP
```
